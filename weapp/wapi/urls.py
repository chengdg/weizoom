# -*- coding: utf-8 -*-

import mall

import views
from django.conf.urls import *

urlpatterns = patterns('',
	(r'^(.+)/(.+)/', views.api_wrapper),
)
