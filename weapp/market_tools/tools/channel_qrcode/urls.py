# -*- coding: utf-8 -*-

__author__ = "robert"


from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.list_channel_qrcode_settings),
 	(r'^edit_setting/$', views.edit_channel_qrcode_setting),
 	(r'^view_setting/(\d+)/$', views.view_channel_qrcode_setting),
 	(r'^channel_qrcode_pay_orders/get/(\d+)/$', views.get_channel_qrcode_pay_orders),

	(r'^api/', api_views.call_api),
)
