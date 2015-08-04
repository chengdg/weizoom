# -*- coding: utf-8 -*-

__author__ = "robert"


from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.list_stores),
	(r'^add/$', views.add_store),
	(r'^update/(\d+)/$', views.update_store),
	(r'^api/', api_views.call_api),
)
