# -*- coding: utf-8 -*-

__author__ = "robert"


from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.list_activities),
	(r'^activity/create/$', views.create_activity),
	(r'^activity/update/(\d+)/$', views.update_activity),
	(r'^activity/export/(\d+)/$', views.export_activity_members),
	(r'^activity/delete/(\d+)/$', views.delete_activity),
	(r'^activity_status/update/(\d+)/$', views.update_activity_status),
	(r'^activity_member/list/$', views.list_activity_members),
	(r'^activity_sign_status/update/(\d+)/$', views.update_activity_sign_status),
	(r'^api/', api_views.call_api),
)
