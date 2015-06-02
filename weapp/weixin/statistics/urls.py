# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf.urls import *

import api_views

urlpatterns = patterns('',
	(r'^api/daily_message_trend/get/$', api_views.get_message_daily_trend),
)