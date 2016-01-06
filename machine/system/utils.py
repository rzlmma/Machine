from StringIO import StringIO
from traceback import print_exc
from machine.system.exceptions import Unauthorized
from machine.system.models import Role, User, RolePermissionRelation, UserRoleRelation, Permission


def check_permission(user, codename):
    if not has_permission(user, codename):
        raise Unauthorized("User '%s' doesn't have permission '%s'." % (user, codename))
    else:
        return True


def has_permission(user_id, codename):
    user = User.objects.get(pk=user_id)
    if user.is_superuser:
        return True

    role_ids = get_role_ids(user)
    try:
        Permission.objects.get(codename=codename)
        permission_id = Permission.objects.get(codename=codename).id
    except:
        return False

    result = False
    for role_id in role_ids:
        p = RolePermissionRelation.objects.filter(role_id=role_id, permission_id=permission_id)

        if len(p) == 1:
            result = True
    return result


def get_role_ids(user):
    if user:
        urrs = UserRoleRelation.objects.filter(user_id=user.id).values("role_id")
        role_ids = [urr["role_id"] for urr in urrs]
    return role_ids


def get_role(id_or_name):
    try:
        return Role.objects.get(pk=id_or_name)
    except (Role.DoesNotExist, ValueError):
        try:
            return Role.objects.get(name=id_or_name)
        except Role.DoesNotExist:
            return None


def get_user(id_or_username):
    try:
        return User.objects.get(pk=id_or_username)
    except (User.DoesNotExist, ValueError):
        try:
            return User.objects.get(username=id_or_username)
        except User.DoesNotExist:
            return None


def get_permission_codename(permission_id):
    return Permission.objects.get(pk=permission_id).codename


def get_permissions(id_or_name):
    user = get_user(id_or_name)
    role_ids = get_role_ids(user)
    p_ids = []
    for role_id in role_ids:
        for item in RolePermissionRelation.objects.filter(role_id=role_id):
            if item.permission_id not in p_ids:
                p_ids.append(item.permission_id)

    p_codenames = []
    for p_id in p_ids:
        p_codenames.append(get_permission_codename(p_id))

    return p_codenames


def getTraceBack():
    f = StringIO()
    print_exc(file=f)
    return f.getvalue()