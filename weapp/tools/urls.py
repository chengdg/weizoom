# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import map

urlpatterns = patterns('',
	# 天气api
	url(r'^api/weather/', include('tools.weather.urls')),

	#自定义菜单api
	url(r'^api/customerized_menu/', include('tools.customerized_menu.urls')),

	#地域信息api
	url(r'^api/regional/', include('tools.regional.urls')),

	#排行榜翻页api
	#url(r'^api/top/', include('tools.top.mobile_urls')),

	#地域信息api
	url(r'^api/express/', include('tools.express.urls')),
)
