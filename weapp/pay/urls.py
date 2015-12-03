# -*- coding: utf-8 -*-

__author__ = "guoliyan"


from django.conf.urls import *
from pay import views

urlpatterns = patterns('',
	(r'^$', views.index),
	url(r'^weixin/', include('pay.weixin.urls')),
)
