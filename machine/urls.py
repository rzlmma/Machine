# --*-- coding: utf-8 --*--
"""machine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from machine.book import urls as book_url
from machine.photography import urls as photography_url
from machine.video import urls as video_url
from machine.system import urls as system_url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    # 读书
    url(r'^book/', include(book_url)),
    # 摄影
    url(r'^photography/', include(photography_url)),
    # 摄影
    url(r'^video/', include(video_url)),

    # 系统设置
    url(r'^system/', include(system_url)),
    # 首页
    url(r'^$', include(system_url)),
]
