# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf.urls import *

urlpatterns = patterns('',
	#自定义菜单
	(r'^customized_menu/', include('weixin.manage.customerized_menu.urls')),
)