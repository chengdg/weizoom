# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf.urls import *

urlpatterns = patterns('',
	(r'^member/', include('modules.member.urls')),
)