# --*-- coding: utf-8 --*--
__author__ = 'nolan'


from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    class Meta:
        app_label = 'system'
        db_table = "department"
        verbose_name = verbose_name_plural = '部门'
    name = models.CharField(max_length=128)
    parent_id = models.IntegerField(blank=True, null=True)
    manager = models.CharField(max_length=128, blank=True, null=True)
    comment = models.CharField(max_length=128, blank=True, null=True)
    created_time = models.TimeField(blank=True, null=True)
    updated_time = models.TimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    @staticmethod
    def create(**kwargs):
        dept = Department(**kwargs)
        dept.save()
        return dept


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = verbose_name_plural = '用户'
        app_label = 'system'
        db_table = "user"

    USER_GENDER_CHOICES = (
        ('男', 'male'),
        ('女', 'female'),
        ('保密', 'secrecy'),
    )
    user_id = models.CharField(max_length=128, blank=True, null=True)
    real_name = models.CharField(max_length=128, blank=True, null=True)
    position = models.CharField(max_length=128, blank=True, null=True)
    gender = models.CharField(choices=USER_GENDER_CHOICES, max_length=16, default='SECRECY', blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    mobile = models.CharField(max_length=64, blank=True, null=True)
    status = models.BooleanField(default=True)
    leader_id = models.CharField(max_length=64, blank=True, null=True)
    dept_id = models.CharField(max_length=64, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.username

    @staticmethod
    def create_user(**kwargs):
        user = User(**kwargs)
        user.save()
        return user


class Role(models.Model):
    name = models.CharField(max_length=128, unique=True)
    codename = models.CharField(max_length=128, unique=True)

    class Meta:
        app_label = "system"
        db_table = "role"
        ordering = ("name", )
        verbose_name = verbose_name_plural = '角色'

    def __unicode__(self):
        return self.name

    def get_users(self):
        prrs = UserRoleRelation.objects.filter(role=self).exclude(user=None)
        return [prr.user for prr in prrs]


class Permission(models.Model):
    name = models.CharField(_(u"Name"), max_length=100, unique=True)
    codename = models.CharField(_(u"Codename"), max_length=100, unique=True)

    class Meta:
        app_label = "system"
        db_table = "permission"
        verbose_name = verbose_name_plural = '权限'

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.codename)


class UserRoleRelation(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u"User"), blank=True, null=True)
    role = models.ForeignKey(Role, verbose_name=_(u"Role"))

    class Meta:
        app_label = "system"
        db_table = "user_role_relation"
        ordering = ("user", )
        verbose_name = verbose_name_plural = '用户-角色'

    def __unicode__(self):
        return "%s / %s" % (self.user.username, self.role.name)


class RolePermissionRelation(models.Model):
    role = models.ForeignKey(Role, verbose_name=_(u"Role"), blank=True, null=True)
    permission = models.ForeignKey(Permission, verbose_name=_(u"Permission"))

    class Meta:
        app_label = "system"
        db_table = "role_permission_relation"
        ordering = ("role", )
        verbose_name = verbose_name_plural = '角色-权限'

    def __unicode__(self):
        return "%s / %s" % (self.permission.name, self.role)
