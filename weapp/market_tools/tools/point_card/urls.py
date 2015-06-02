# -*- coding: utf-8 -*-

__author__ = "robert"


from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.list_point_card),
	(r'^point_card_rule/create/$', views.create_point_card_rule),
	(r'^point_card_rule/update/(\d+)/$', views.edit_point_card_rule),
	(r'^point_card_rule/export/$', views.export_point_card_rule),
	
	(r'^api/', api_views.call_api),
)
