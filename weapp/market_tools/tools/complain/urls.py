# -*- coding: utf-8 -*-

__author__ = "paco bert"

from django.conf.urls import *
import views
import api_views
import mobile_views

urlpatterns = patterns('',
	(r'^$', views.get_complain),
	#(r'^feedback/settings$', views.member_feedback_settings),
	(r'^settings', views.member_complain_settings),
	#(r'^feedback/get$', views.get_feedback),
	# (r'^update/(\d+)/$', views.update_vote),
	# (r'^delete/(\d+)/$', views.delete_vote),
	# (r'^vote_statistics/(\d+)/$', views.show_vote_statistics),
	
	#(r'^api/', api_views.call_api),
)