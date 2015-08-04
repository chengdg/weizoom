# -*- coding: utf-8 -*-

__author__ = "robert"


from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.list_delivery_plan),
	(r'^deliver_plan/create/$', views.create_deliver_plan),
	(r'^delivery_plan/update/(\d+)/$', views.edit_delivery_plan),
	(r'^delete/(\d+)/$', views.delete_delivery_plan),
	
	(r'^api/', api_views.call_api),
)
