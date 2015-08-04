# -*- coding: utf-8 -*-

__author__ = "robert"


from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.list_researches),
	(r'^research/create/$', views.create_research),
	(r'^research/update/(\d+)/$', views.update_research),
	(r'^research/delete/(\d+)/$', views.delete_research),
	(r'^research_info/view/$', views.view_research_info),
	(r'^research_members/list/$', views.list_research_members),
	(r'^research_item_value/list/$', views.list_research_item_value),

	(r'^api/', api_views.call_api),
)
