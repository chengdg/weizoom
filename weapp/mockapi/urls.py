# -*- coding: utf-8 -*-

from django.conf.urls import *

import views

urlpatterns = patterns('',
	(r'^call_back_url/request/$', views.request_call_back_url),
	(r'^alipay/do_pay/$', views.show_alipay_page),
	(r'^weixin_pay/async_pay/$', views.do_async_weixin_pay),
	(r'^tenpay/pay/$', views.show_tenpay_page),
)