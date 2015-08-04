# -*- coding: utf-8 -*-

__author__ = "guoliyan"


from django.conf.urls import *


urlpatterns = patterns('',
	url(r'^weixin/', include('pay.weixin.urls')),
)
