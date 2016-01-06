# --*-- coding: utf-8 --*--
__author__ = 'nolan'

from django.conf.urls import url
from machine.system import views, tests

urlpatterns = [

    url(r'^$', views.index, name="index"),

    # 用户登录注销
    url(r'login/$', views.login, name="login"),
    url(r'logout/$', views.logout, name="logout"),
    url(r'register/$', views.register, name="register"),

    # 操作日志
    # url(r'^operate_log$', views.operate_log, name="operate_log"),

    # 用户
    url(r'^user_list/(.+)$', views.user_list, name="user_list"),
    url(r'^user_search/$', views.user_search, name="user_search"),
    url(r'^user_role_management/(.+)$', views.user_role_management, name="user_role_management"),
    url(r'^user_profile/(.+)$', views.user_profile, name="user_profile"),
    url(r'^user_edit/(.+)$', views.user_edit, name="user_edit"),
    url(r'^change_password/(.+)$', views.change_password, name="change_password"),
    url(r'^reset_password/(.+)$', views.reset_password, name="reset_password"),
    url(r'^user_add$', views.user_add, name="user_add"),
    url(r'^user_delete', views.user_delete, name="user_delete"),
    url(r'^current_user_profile', views.current_user_profile, name="current_user_profile"),

    # # 添加部门
    # url(r'^dept_add$', views.dept_add, name="dept_add"),

    # 角色
    url(r'^role_list/(.+)$', views.role_list, name="role_list"),
    url(r'^role_permission_management/(.+)$', views.role_permission_management, name="role_permission_management"),
    url(r'^role_edit/(.+)$', views.role_edit, name="role_edit"),
    url(r'^role_add$', views.role_add, name="role_add"),
    url(r'^role_delete$', views.role_delete, name="role_delete"),
    url(r'^user_profile', views.user_profile, name="user_profile"),

    # 权限
    url(r'^permission_list/(.+)$', views.permission_list, name="permission_list"),
    url(r'^permission_edit/(.+)$', views.permission_edit, name="permission_edit"),
    url(r'^permission_add$', views.permission_add, name="permission_add"),
    url(r'^permission_delete$', views.permission_delete, name="permission_delete"),

    # 用户-角色
    url(r'^user_role_list$', views.user_role_list, name="user_role_list"),
    url(r'^user_role_add$', views.user_role_add, name="user_role_add"),
    url(r'^user_role_delete$', views.user_role_delete, name="user_role_delete"),

    # 角色-权限
    url(r'^role_permission_list$', views.role_permission_list, name="role_permission_list"),
    url(r'^role_permission_add$', views.role_permission_add, name="role_permission_add"),
    url(r'^role_permission_delete$', views.role_permission_delete, name="role_permission_delete"),

    # 页面获取session
    url(r'^get_session_permit$', views.get_session_permit, name="get_session_permit"),
    url(r'^get_session_disable$', views.get_session_disable, name="get_session_disable"),

    # 权限认证未通过跳转
    url(r'^auth_fail/$', views.auth_fail, name="auth_fail"),

    url(r'^test$', tests.test_case, name="test_case"),
]

