# -*- coding: utf-8 -*-

__author__ = "bert"

from django.conf.urls import *
import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.list_shake),
	# (r'^list/$', views.list_red_envelope),
	(r'^edit/(\d+)/$', views.edit_shake),
	(r'^delete/(\d+)/$', views.delete_shake),
	(r'^api/shakes/get/$', api_views.get_shakes),
	(r'^api/shake/edit/$', api_views.edit_shake),
	(r'^api/records/get/$', api_views.get_records),
	# (r'^api/', api_views.call_api),
)