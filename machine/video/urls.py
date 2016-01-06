# --*-- coding: utf-8 --*--
__author__ = 'nolan'

from django.conf.urls import url
from machine.video import views

urlpatterns = [
    url(r'^video_list$', views.video_list, name="video_list"),
]
