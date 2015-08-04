# -*- coding: utf-8 -*-

__author__ = "chuter"

from django.conf.urls import *
import mobile_views

urlpatterns = patterns('',
    (r'^(\d+)/$', mobile_views.map),
)