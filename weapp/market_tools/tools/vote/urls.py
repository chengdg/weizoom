# -*- coding: utf-8 -*-

__author__ = "chuter"

from django.conf.urls import *
import views
import api_views

import mobile_views

urlpatterns = patterns('',
	(r'^$', views.list_votes),
	(r'^add/$', views.add_vote),
	(r'^update/(\d+)/$', views.update_vote),
	(r'^delete/(\d+)/$', views.delete_vote),
	(r'^vote_statistics/(\d+)/$', views.show_vote_statistics),
	
	(r'^export/(\d+)/$', views.export_vote_statistics),

	(r'^api/', api_views.call_api),
)