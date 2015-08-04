# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.list_rules),

	(r'^rule/add/$', views.add_rule),
	(r'^rule/update/(\d+)/$', views.update_rule),
	(r'^rule/delete/(\d+)/$', views.delete_rule),
	(r'^api/rule/update/$', api_views.update_rule),
	(r'^api/rule/add/$', api_views.add_rule),
	
	(r'^api/pattern/check_duplicate/$', api_views.check_duplicate_patterns),

	(r'^follow_rule/$', views.edit_follow_rule),
	(r'^api/follow_rule/add/$', api_views.add_follow_rule),
	(r'^api/follow_rule/update/$', api_views.update_follow_rule),

	(r'^unmatch_rule/$', views.edit_unmatch_rule),
	(r'^api/unmatch_rule/add/$', api_views.add_unmatch_rule),
	(r'^api/unmatch_rule/update/$', api_views.update_unmatch_rule),

	#(r'^api/keywords/get/$', api_views.get_keywords),
	#(r'^api/newses/get/$', api_views.get_newses),
)