# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	#自定义菜单
	(r'^$', views.edit_customerized_menu),
	(r'^api/update/$', api_views.update_customer_menu),
	(r'^api/menus/get/$', api_views.get_menus),
)

