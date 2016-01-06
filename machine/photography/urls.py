# --*-- coding: utf-8 --*--
__author__ = 'nolan'

from django.conf.urls import url
from machine.photography import views, tests

urlpatterns = [
    url(r'^photo_list$', views.photo_list, name="photo_list"),
    url(r'^photo_add$', views.photo_add, name="photo_add"),
    url(r'^photo_vote$', views.photo_vote, name="photo_vote"),
]

