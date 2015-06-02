# -*- coding: utf-8 -*-

__author__ = 'herry'

from django.conf.urls import *

import api_views

urlpatterns = patterns('',
	(r'^api/', api_views.call_api),
)