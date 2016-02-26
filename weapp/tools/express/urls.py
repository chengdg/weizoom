# -*- coding: utf-8 -*-

__author__ = "liupeiyu"

from django.conf.urls import *
import views

urlpatterns = patterns('',
	(r'^test/$', views.get_test),
	(r'^test_kuaidi_poll/$', views.test_kuaidi_poll),
	(r'^test_kdniao_push_data/$', views.test_kdniao_push_data),
	(r'^test_analog_push_data/$', views.test_analog_push_data),

	(r'^order_info/get/$', views.get_order_info),

	(r'^companies/get/$', views.get_companies),

	(r'^kuaidi/callback/$', views.kuaidi_callback),
	(r'^kdniao/callback/$', views.kdniao_callback),
)