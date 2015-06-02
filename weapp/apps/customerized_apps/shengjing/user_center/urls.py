# -*- coding: utf-8 -*-

from django.conf.urls import *

import mobile_views
import mobile_api_views

urlpatterns = patterns('',
	(r'^binding_page/$', mobile_views.get_binding_page),

	(r'^info/$', mobile_views.get_user_info),

	(r'^integral_log/$', mobile_views.get_integral_log),

	#################################################
		
)

