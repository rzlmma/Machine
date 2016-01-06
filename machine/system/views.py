# --*-- coding: utf-8 --*--
import datetime
import logging

from django.contrib.auth import authenticate, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from machine.base import HomePageView

from machine.deco import require_permission, require_login
from machine.system.models import User, Permission, UserRoleRelation, Role, RolePermissionRelation
from machine.system.utils import getTraceBack, get_permissions

logger = logging.getLogger('django')


class demoView(HomePageView):
    '''基本页面'''
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        return super(demoView, self).get(request, *args, **kwargs)

    def get_data(self):
        pass

# @require_login
def index(request):
    if request.session.get('_auth_user_id'):
        user_id = request.session.get('_auth_user_id')
        user = User.objects.get(pk=user_id)
    return render_to_response('base.html', locals(), context_instance=RequestContext(request))


# @csrf_exempt
def login(request):
    if request.method == "GET":
        logger.info('跳转到登陆界面')
        if request.user.id is None:
            return render_to_response("system/login.html", locals(), context_instance=RequestContext(request))
        return render_to_response('base.html', locals(), context_instance=RequestContext(request))

    else:
        logger.info('点击登陆')
        response = {"success": False, "error": ""}
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user:
                is_active = user.is_active
                if not is_active:
                    response["error"] = "用户未启用!"
                    return HttpResponse(json.dumps(response), content_type="application/json")

                login_on_server(request, user)
                response["success"] = True
                response["error"] = "执行成功!"
            else:
                response["error"] = "登陆失败!"
                return render_to_response("system/login.html", locals(), context_instance=RequestContext(request))
            return HttpResponseRedirect("/")

        except Exception as e:
            response["error"] = str(e)
            logger.error(response["error"] + getTraceBack())
            return HttpResponse(json.dumps(response), content_type="application/json")


def login_on_server(request, user):
    try:
        if user is None:
            user = request.user
        if SESSION_KEY in request.session:
            if request.session[SESSION_KEY] != user.id:
                request.session.flush()
        else:
            request.session.cycle_key()

        request.session[SESSION_KEY] = user.id
        request.session[BACKEND_SESSION_KEY] = user.backend

        user_permission_codenames = get_permissions(user.id)
        perm_all = Permission.objects.all()
        disable_list = [p.codename for p in perm_all if p.codename not in user_permission_codenames]
        request.session['PERMISSION'] = user_permission_codenames
        request.session['DISABLE'] = disable_list

        if hasattr(request, 'user'):
            request.user = user
        user.last_login = datetime.datetime.now()
        user.save()
    except Exception, e:
        logger.error(str(e) + getTraceBack())
        raise e


def logout(request):
    if request.user.is_authenticated():
        try:
            logout_on_server(request)
        except Exception as e:
            pass
    return HttpResponseRedirect("/system/login/")


def logout_on_server(request):
    user = getattr(request, 'user', None)

    from django.contrib.auth.signals import user_logged_out

    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)

    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser

        request.user = AnonymousUser()


def register(request):
    if request.method == "GET":
        return render_to_response('system/register.html', locals(), context_instance=RequestContext(request))
    else:
        resp = {"success": False, "error": ""}
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        if password != password_again:
            resp["error"] = "出错!"
            return HttpResponse(json.dumps(resp), content_type="application/json")
        try:
            User.create_user(username=username, password=make_password(password))
            resp["success"] = True
            resp["error"] = "执行成功!"
        except:
            resp["success"] = True
            resp["error"] = "出错!"
        return HttpResponseRedirect('/')


# @csrf_exempt
class AddError(object):
    pass


def user_list(request, page_num):
    user_list = User.objects.all()

    #分页
    per_page = 10
    paginator = Paginator(user_list, per_page)

    if not page_num:
        page = 1
    else:
        page = page_num

    try:
        user_list = paginator.page(page)

    except PageNotAnInteger:
        user_list = paginator.page(1)

    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)

    return render_to_response('system/user_list.html', locals(), context_instance=RequestContext(request))


def user_search(request):
    keyword = request.POST.get('keyword')
    print keyword
    user_list = User.objects.filter(username=keyword)
    print user_list
    return render_to_response('system/user_search.html', locals(), context_instance=RequestContext(request))


def user_add(request):
    if request.method == "GET":
        return render_to_response('system/user_add.html', locals(), context_instance=RequestContext(request))
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        real_name = request.POST.get('real_name')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        position = request.POST.get('position')

        # last_login = datetime.datetime.now(),
        # date_joined = datetime.datetime.now(),
        # updated_at = datetime.datetime.now(),
        # deleted_at = datetime.datetime.now(),

        User.create_user(
            username=username,
            password=make_password(password),
            real_name=real_name,
            gender=gender,
            position=position,

            email=email,
            phone=phone,
            mobile=mobile,

            # last_login=last_login,
            # date_joined=date_joined,
            # updated_at=updated_at,
            # deleted_at=deleted_at
            )
        return HttpResponseRedirect('/')


def user_edit(request, id):
    if request.method == "GET":
        user = User.objects.get(pk=id)
        return render_to_response('system/user_edit.html', locals(), context_instance=RequestContext(request))
    else:
        user = User.objects.filter(pk=id)
        if request.POST.get('username') != '':
            user.update(username=request.POST.get('username'))
        if request.POST.get('real_name') != '':
            user.update(real_name=request.POST.get('real_name'))
        if request.POST.get('gender') != '':
            user.update(gender=request.POST.get('gender'))
        if request.POST.get('mobile') != '':
            user.update(mobile=request.POST.get('mobile'))
        if request.POST.get('phone') != '':
            user.update(phone=request.POST.get('phone'))
        if request.POST.get('email') != '':
            user.update(email=request.POST.get('email'))
        if request.POST.get('position') != '':
            user.update(position=request.POST.get('position'))

        return render_to_response('system/user_edit.html', locals(), context_instance=RequestContext(request))


def change_password(request, user_id):
    if request.method == 'GET':
        user_id = user_id
        return render_to_response('system/change_password.html', locals(), context_instance=RequestContext(request))
    else:
        resp = {"success": False, "error": ""}
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        try:
            username = User.objects.get(pk=user_id).username
            user = authenticate(username=username, password=old_password)
            if user is not None and user.is_active:
                user.set_password(new_password)
                user.save()
                resp["success"] = True
                resp["msg"] = "修改成功!"
            else:
                resp["success"] = False
                resp["msg"] = "验证出错!"
        except:
            resp["success"] = False
            resp["msg"] = "出错!"
        return HttpResponse(json.dumps(resp), content_type="application/json")


def reset_password(request, user_id):
    if request.method == 'GET':
        user_id = user_id
        return render_to_response('system/reset_password.html', locals(), context_instance=RequestContext(request))
    else:
        resp = {"success": False, "msg": ""}
        password = request.POST.get('password')
        try:
            user = User.objects.get(pk=user_id)
            if user is not None:
                user.set_password(password)
                user.save()
                resp["success"] = True
                resp["msg"] = "重置成功!"
        except:
            resp["success"] = False
            resp["msg"] = "出错!"
        return HttpResponse(json.dumps(resp), content_type="application/json")


def user_delete(request):
    resp = {"success": False, "error": ""}
    if request.POST.get('id'):
        id = request.POST.get('id')
        try:
            user = User.objects.get(pk=id)
            user.delete()
            resp["success"] = True
            resp["error"] = "执行成功!"
        except:
            resp["success"] = False
            resp["error"] = "出错!"
        return HttpResponse(json.dumps(resp), content_type="application/json")

    elif request.POST.get('user_ids'):
        user_ids = request.POST.get('user_ids')
        try:
            user_ids_list = user_ids.split(',')
            for u_id in user_ids_list:
                if u_id:
                    user = User.objects.get(pk=u_id)
                    user.delete()
        except:
            resp["success"] = False
            resp["error"] = "出错!"
        return HttpResponse(json.dumps(resp), content_type="application/json")


def user_profile(request, id):
    user = User.objects.get(pk=id)
    return render_to_response('system/user_profile.html', locals(), context_instance=RequestContext(request))


@require_login
def current_user_profile(request):
    user_id = request.session.get('_auth_user_id')
    user = User.objects.get(pk=user_id)
    CURRENT_USER = True
    return render_to_response('system/user_profile.html', locals(), context_instance=RequestContext(request))


def user_role_management(request, user_id):
    if request.method == 'GET':
        user = User.objects.get(pk=user_id)
        urrs_selected = UserRoleRelation.objects.filter(user_id=user_id)
        roles_all = Role.objects.all()

        role_selected_list = []
        role_unselected_list = []

        for urrs in urrs_selected:
            role = Role.objects.get(pk=urrs.role_id)
            role_selected_list.append(role)

        role_unselected_list = [role for role in roles_all if role not in role_selected_list]
        return render_to_response('system/user_role_management.html', locals(), context_instance=RequestContext(request))

    else:
        resp = {"success": False, "error": ""}
        role_ids = request.POST.get('role_ids')
        user_roles = UserRoleRelation.objects.filter(user_id=user_id)

        for ur in user_roles:
            if ur:
                ur.delete()
        try:
            role_ids_list = role_ids.split(',')
            for r_id in role_ids_list:
                if r_id:
                    UserRoleRelation.objects.create(user_id=user_id, role_id=r_id)

            resp["success"] = True
            resp["error"] = "执行成功!"
        except:
            resp["success"] = False
            resp["error"] = "出错!"
        return HttpResponse(json.dumps(resp), content_type="application/json")


def role_list(request, page_num):
    role_list = Role.objects.all()

    # 分页
    per_page = 10
    paginator = Paginator(role_list, per_page)

    if not page_num:
        page = 1
    else:
        page = page_num

    try:
        role_list = paginator.page(page)

    except PageNotAnInteger:
        role_list = paginator.page(1)

    except EmptyPage:
        role_list = paginator.page(paginator.num_pages)

    return render_to_response('system/role_list.html', locals(), context_instance=RequestContext(request))


def role_permission_management(request, role_id):
    if request.method == 'GET':
        role = Role.objects.get(pk=role_id)
        rprs_selected = RolePermissionRelation.objects.filter(role_id=role_id)
        permissions_all = Permission.objects.all()

        permission_selected_list = []
        permission_unselected_list = []

        for rprs in rprs_selected:
            p_obj = Permission.objects.get(pk=rprs.permission_id)
            permission_selected_list.append(p_obj)

        permission_unselected_list = [p for p in permissions_all if p not in permission_selected_list]
        return render_to_response('system/role_permission_management.html', locals(), context_instance=RequestContext(request))

    else:
        resp = {"success": False, "error": ""}
        permission_ids = request.POST.get('permission_ids')
        role_permissions = RolePermissionRelation.objects.filter(role_id=role_id)

        for rp in role_permissions:
            if rp:
                rp.delete()
        try:
            permission_ids_list = permission_ids.split(',')
            for p_id in permission_ids_list:
                if p_id:
                    RolePermissionRelation.objects.create(role_id=role_id, permission_id=p_id)

            resp["success"] = True
            resp["error"] = "执行成功!"
        except:
            resp["success"] = False
            resp["error"] = "出错!"
        return HttpResponse(json.dumps(resp), content_type="application/json")


def role_add(request):
    if request.method == "GET":
        return render_to_response('system/role_add.html', locals(), context_instance=RequestContext(request))
    else:
        if request.POST.get('role_name') != '':
            role_name = request.POST.get('role_name')
        if request.POST.get('role_codename') != '':
            role_codename = request.POST.get('role_codename')

        Role.objects.create(name=role_name, codename=role_codename)
        return HttpResponseRedirect('/')


def role_edit(request, id):
    if request.method == "GET":
        role = Role.objects.filter(pk=id)[0]
        return render_to_response('system/role_edit.html', locals(), context_instance=RequestContext(request))
    else:
        role = Role.objects.filter(pk=id)[0]
        if request.POST.get('role_name') != '':
            role_name = request.POST.get('role_name')
        else:
            role_name = role.name

        if request.POST.get('role_codename') != '':
            role_codename = request.POST.get('role_codename')
        else:
            role_codename = role.codename

        role.name = role_name
        role.codename = role_codename
        role.save()
        return HttpResponseRedirect('/')


def role_delete(request):
    resp = {"success": False, "error": ""}
    if request.POST.get('role_name'):
        role_name = request.POST.get('role_name')
        try:
            role = Role.objects.filter(name=role_name)
            role.delete()
            resp["success"] = True
            resp["error"] = "执行成功!"
        except Exception as e:
            resp["error"] = "出错！"

    elif request.POST.get('role_ids'):
        role_ids = request.POST.get('role_ids')
        try:
            role_ids_list = role_ids.split(',')
            for r_id in role_ids_list:
                if r_id:
                    role = Role.objects.filter(pk=r_id)
                    role.delete()

            resp["success"] = True
            resp["error"] = "执行成功!"

        except:
            resp["error"] = "出错！"

    return HttpResponse(json.dumps(resp), content_type="application/json")


def permission_list(request, page_num=None):
    permission_list = Permission.objects.all()

    # 分页
    per_page = 10
    paginator = Paginator(permission_list, per_page)

    if not page_num:
        page = 1
    else:
        page = page_num

    try:
        permission_list = paginator.page(page)

    except PageNotAnInteger:
        permission_list = paginator.page(1)

    except EmptyPage:
        permission_list = paginator.page(paginator.num_pages)
    return render_to_response('system/permission_list.html', locals(), context_instance=RequestContext(request))


def permission_add(request):
    if request.method == "GET":
        return render_to_response('system/permission_add.html', locals(), context_instance=RequestContext(request))
    else:
        permission_name = request.POST.get('permission_name')
        permission_codename = request.POST.get('permission_codename')
        Permission.objects.create(name=permission_name, codename=permission_codename)
        return HttpResponseRedirect('/')


def permission_edit(request, id):
    if request.method == "GET":
        permission = Permission.objects.filter(pk=id)[0]
        return render_to_response('system/permission_edit.html', locals(), context_instance=RequestContext(request))
    else:
        resp = {"success": False, "error": ""}
    try:
        permission = Permission.objects.filter(pk=id)[0]
        if request.POST.get('permission_name') != '':
            permission_name = request.POST.get('permission_name')
        else:
            permission_name = permission.name
        if request.POST.get('permission_codename'):
            permission_codename = request.POST.get('permission_codename')
        else:
            permission_codename = permission.codename

        permission.name = permission_name
        permission.codename = permission_codename
        permission.save()
        resp["success"] = True
        resp["error"] = "执行成功!"
    except:
        resp["error"] = "出错！"
    return HttpResponseRedirect('/')


def permission_delete(request):
    resp = {"success": False, "error": ""}
    if request.POST.get('permission_id'):
        permission_id = request.POST.get('permission_id')
        try:
            permission = Permission.objects.filter(pk=permission_id)
            permission.delete()
            resp["success"] = True
            resp["error"] = "执行成功!"
        except:
            resp["error"] = "出错！"
        return HttpResponse(json.dumps(resp), content_type="application/json")

    elif request.POST.get('permission_ids'):
        permission_ids = request.POST.get('permission_ids')
        try:
            permission_ids_list = permission_ids.split(',')
            for p_id in permission_ids_list:
                if p_id:
                    permission = Permission.objects.filter(pk=p_id)
                    permission.delete()
            resp["success"] = True
            resp["error"] = "执行成功!"

        except:
            resp["error"] = "出错！"

    return HttpResponse(json.dumps(resp), content_type="application/json")


def user_role_list(request):
    user_role_list = UserRoleRelation.objects.all()
    return render_to_response('system/user_role_list.html', locals(), content_type=RequestContext(request))


def user_role_add(request):
    if request.method == "GET":
        user_list = User.objects.all()
        role_list = Role.objects.all()
        return render_to_response('system/user_role_add.html', locals(), context_instance=RequestContext(request))
    else:
        user_id = request.POST.get('user')
        role_id = request.POST.get('role')

        UserRoleRelation.objects.create(user_id=user_id, role_id=role_id)
        return HttpResponseRedirect('/')


def user_role_delete(request):
    resp = {"success": False, "error": ""}
    user_role_id = request.POST.get('user_role_id')
    try:
        user_role = UserRoleRelation.objects.filter(pk=user_role_id)
        user_role.delete()
        resp["success"] = True
        resp["error"] = "执行成功!"
    except:
        resp["success"] = False
        resp["error"] = "出错！"
    return HttpResponse(json.dumps(resp), content_type="application/json")


def role_permission_list(request):
    role_permisison_list = RolePermissionRelation.objects.all()
    return render_to_response('system/role_permission_list.html', locals(), content_type=RequestContext(request))


def role_permission_add(request):
    if request.method == "GET":
        role_list = Role.objects.all()
        permission_list = Permission.objects.all()
        return render_to_response('system/role_permission_add.html', locals(), context_instance=RequestContext(request))
    else:
        role_id = request.POST.get('role')
        permission_id = request.POST.get('permission')
        RolePermissionRelation.objects.create(role_id=role_id, permission_id=permission_id)
        return HttpResponseRedirect('/')
        UserRoleRelation.objects.create(user_id=user_id, role_id=role_id)
        return HttpResponseRedirect('/')


def role_permission_delete(request):
    resp = {"success": False, "error": ""}
    role_permission_id = request.POST.get('role_permission_id')
    try:
        role_permission = RolePermissionRelation.objects.filter(pk=role_permission_id)
        role_permission.delete()
        resp["success"] = True
        resp["error"] = "执行成功!"
    except:
        resp["success"] = False
        resp["error"] = "出错！"
    return HttpResponse(json.dumps(resp), content_type="application/json")


def get_session_disable(request):
    """
    获取session中用户的禁用权限列表
    """
    resp = request.session['DISABLE']
    return HttpResponse(json.dumps(resp), content_type="application/json")


def get_session_permit(request):
    """
    获取session中用户的许可权限列表
    """
    resp = request.session['PERMISSION']
    return HttpResponse(json.dumps(resp), content_type="application/json")


def auth_fail(request):
    return render_to_response('system/auth_fail.html', locals(), content_type=RequestContext(request))
