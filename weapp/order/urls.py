# -*- coding: utf-8 -*-

from django.conf.urls import *

import views

urlpatterns = patterns('',
	(r'^$', views.show_index),

	url(r'^account/', include('order.account.urls')),

	url(r'^waybill/', include('order.delivery.urls')),
)