# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.show_db_window),
	(r'^db/$', views.show_db_window),

	(r'^api/', api_views.call_api),
)