# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^newses/$', views.list_news),
	(r'^single_news/add/$', views.add_single_news),
    (r'^multi_news/add/$', views.add_multi_news),
	(r'^news/update/(\d+)/$', views.update_news),

	(r'^news_detail/mshow/(\d+)/$', views.show_news_detail),

	(r'^api/newses/get/$', api_views.get_newses),
	(r'^api/news/delete/$', api_views.delete_news),
	(r'^api/create/$', api_views.create_material),
	(r'^api/update/$', api_views.update_material),
	(r'^api/get/$', api_views.get_material),
)