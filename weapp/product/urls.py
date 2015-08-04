# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^products/$', views.show_products),
	(r'^product/add/$', views.add_product),
	(r'^product/install/$', views.install_product),
	(r'^product_users/get/$', views.show_product_users),

	(r'^api/', api_views.call_api)
)