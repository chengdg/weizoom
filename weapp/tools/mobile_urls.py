# -*- coding: utf-8 -*-

__author__ = "chuter"

from django.conf.urls import *
from map import mobile_views as map_mobile_views

urlpatterns = patterns('',
    #地图
    url(r'^map/', include('tools.map.mobile_urls')),
)