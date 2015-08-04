# -*- coding: utf-8 -*-

__author__ = "slzhu"


from django.conf.urls import *

import mobile_views
import mobile_api_views


urlpatterns = patterns('',
    (r'^$', mobile_views.index),
    (r'^api/', mobile_api_views.call_api),
)
