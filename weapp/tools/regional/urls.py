# -*- coding: utf-8 -*-

from django.conf.urls import *

import views as apiviews

urlpatterns = patterns('',
	(r'^provinces/$', apiviews.get_provinces),
	(r'^cities/(\d+)/$', apiviews.get_cities),
	(r'^districts/(\d+)/$', apiviews.get_districts),
)