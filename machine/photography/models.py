# --*-- coding: utf-8 --*--
from machine.system.models import User, _
from django.db import models


class Photo(models.Model):
    author = models.ForeignKey(User, verbose_name=_(u"User"), blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    photo_link = models.CharField(max_length=128)
    favor_cnt = models.IntegerField(default=0, null=True)
    dislike_cnt = models.IntegerField(default=0,  null=True)
    upload_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "photography"
        db_table = "photo"
        ordering = ("-upload_time", )
        verbose_name = verbose_name_plural = '照片'

    def __unicode__(self):
        return self.name


class Remark(models.Model):
    author = models.ForeignKey(User, verbose_name=_(u"User"), blank=True, null=True)
    content = models.CharField(max_length=256, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "photography"
        db_table = "remark"
        ordering = ("create_time", )
        verbose_name = verbose_name_plural = '照片'

    def __unicode__(self):
        return self.name