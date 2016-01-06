# # --*-- coding: utf-8 --*--
__author__ = 'nolan'


# import hashlib
from django.http import HttpResponseRedirect
from machine.system.utils import has_permission


# def md5_crypt(string):
#     return hashlib.new("md5", string).hexdigest()


def require_login(func):
    """要求登录的装饰器"""
    def _deco(request, *args, **kwargs):
        if not request.session.get('_auth_user_id'):
            return HttpResponseRedirect('/system/login/')
        return func(request, *args, **kwargs)
    return _deco


def require_permission(permission_codename):
    """检验登录用户的权限的装饰器"""
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            auth_user_id = request.session.get('_auth_user_id')
            check_result = has_permission(auth_user_id, permission_codename)
            if not check_result:
                return HttpResponseRedirect('/system/auth_fail/')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator