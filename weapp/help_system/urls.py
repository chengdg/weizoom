# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.list_documents),
	(r'^document/create/$', views.add_document),
	(r'^document/update/$', views.update_document),

	#api调用
	(r'^api/', api_views.call_api),
)