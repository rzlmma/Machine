# --*--coding: utf-8 --*--

import time
from machine.settings import register
from machine.system.models import User, Role
from django import template

@register.filter(name='stamp2str')
def stamp2str(value):
    try:
        return time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(value))
    except AttributeError:
        return '0000/00/00 00:00:00'


@register.filter(name='int2str')
def int2str(value):
    return str(value)


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='bool2str')
def bool2str(value):
    if value:
        return u'是'
    else:
        return u'否'


@register.filter(name='member_count')
def member_count(user_id):
    user = User.objects.get(pk=user_id)
    return user.user_set.count()


@register.filter(name='to_avatar')
def to_avatar(role_id='0'):
    role_dict = {'0': 'user', '1': 'admin', '2': 'root'}
    return role_dict.get(str(role_id), 'user')


@register.filter(name='to_rolename')
def to_rolename(role_id='0'):
    role_name = Role.objects.get(pk=role_id).name
    return role_name
