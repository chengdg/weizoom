# -*- coding: utf-8 -*-

__author__ = "chuter"

from django.conf.urls import *
import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.list_red_envelope),
	(r'^list/$', views.list_red_envelope),
	(r'^edit/(\d+)/$', views.edit_red_envelope_view),
	(r'^api/red_envelope/edit/$', api_views.edit_red_envelope),
	(r'^api/', api_views.call_api),
)