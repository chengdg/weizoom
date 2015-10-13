# -*- coding: utf-8 -*-

import mall
import stats

import views
from django.conf.urls import *

urlpatterns = patterns('',
	(r'^(.+)/(.+)/', views.api_wrapper),
)
