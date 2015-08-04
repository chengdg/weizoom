# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf.urls import *

import mobile_views
import api_views

urlpatterns = patterns('',
	(r'^$', mobile_views.wxpay_index),

	(r'feedback/$', api_views.create_pay_feedback),
	(r'warning/$', api_views.create_pay_warning_notify),
	# (r'^$', mobile_views.wxpay_index),
)