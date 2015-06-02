# -*- coding: utf-8 -*-

__author__ = "slzhu"


from django.conf.urls import *

import mobile_views


urlpatterns = patterns('',
    (r'^$', mobile_views.index)
)
