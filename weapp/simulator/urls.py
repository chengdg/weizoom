# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.start_simulator),
	(r'^2/$', views.start_advance_simulator),

	#TODO：将api的函数都移到api_views.py中
	(r'^api/weixin/send/', views.send_from_simulator),
	(r'^api/menu_event_response/get/', views.get_menu_event_response),
	(r'^api/mp_user/subscribe/', views.subscribe),
	(r'^api/mp_user/unsubscribe/', views.unsubscribe),
	(r'^api/mp_user/qr_subscribe/', views.qr_subscribe),
	(r'^api/', api_views.call_api),
)