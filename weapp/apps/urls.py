# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf.urls import *

import views
import api_views
import apps_router

urlpatterns = patterns('',
	#定制化app管理相关
	(r'^$', views.list_apps),
	(r'^app/add', views.add_app),
	(r'^app/update/(\d+)', views.update_app),

	(r'^api/', api_views.call_api),

	#定制app访问相关
	(r'^(\w+)/home', views.show_app),
	(r'^(\w+)/api/(\w+)/(\w+)/(\w+)', apps_router.call_resource_process_api),
	(r'^(\w+)/', apps_router.process_resource),
)