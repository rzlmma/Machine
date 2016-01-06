# --*--coding: utf-8 --*--
from machine.system.utils import get_role_ids
from machine.system.models import User

__author__ = 'nolan'


def name_proc(request):
    is_superuser = False
    session_username = "未登录"
    session_user_id = -1
    session_role_id = -1

    if request.session.get('_auth_user_id'):
        session_user_id = request.session.get('_auth_user_id')
        user = User.objects.get(pk=session_user_id)
        session_username = user.username

        if user.is_superuser:
            is_superuser = True

        role_ids = get_role_ids(user)

        if len(role_ids) != 0:
            session_role_id = role_ids[0]

    info_dic = {
        "is_superuser": is_superuser,
        "session_username": session_username,
        "session_user_id": session_user_id,
        "session_role_id": session_role_id,

    }

    return info_dic