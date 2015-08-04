# -*- coding: utf-8 -*-

__author__ = "liupeiyu"

from django.conf.urls import *
import views
import api_views
import mobile_api_views

urlpatterns = patterns('',
	(r'^$', views.list_lottery),
	(r'^list/$', views.list_lottery),
	(r'^edit/(\d+)/$', views.edit_lottery_view),
	(r'^stop/(\d+)/$', views.stop_lottery),
	(r'^start/(\d+)/$', views.start_lottery),
	(r'^delete/(\d+)/$', views.delete_lottery),
	(r'^award_prize/(\d+)/$', views.award_prize),
	(r'^api/lottery/edit/$', api_views.edit_lottery),
	(r'^api/', api_views.call_api),
)