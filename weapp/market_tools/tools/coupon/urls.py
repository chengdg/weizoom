# -*- coding: utf-8 -*-

__author__ = "robert"


from django.conf.urls import *

import views

urlpatterns = patterns('',
	(r'^$', views.list_coupons),
	(r'^coupon_rule/create/$', views.create_coupon_rule),
	(r'^coupon_rule/update/$', views.update_coupon_rule),
	(r'^coupon_rule/export/$', views.export_coupon_rule),
	(r'^coupon_rule/delete/$', views.delete_coupon_rule),
	(r'^expired_coupon/delete/$', views.delete_expired_coupon),
)
