# --*-- coding: utf-8 --*--
__author__ = 'nolan'

from django.conf.urls import url
from machine.book import views, tests

urlpatterns = [
    # 客户管理
    url(r'book_list$', views.book_list, name="book_list"),
    url(r'book_add$', views.book_add, name="book_add"),
    url(r'upload_file$', views.upload_file, name="upload_file"),
]
