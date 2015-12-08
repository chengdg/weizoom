# -*- coding: utf-8 -*-

import mall
import stats
import auth
import sample

import views
from django.conf.urls import *

urlpatterns = patterns('',
	(r'^(.+)/(.+)/', views.api_wrapper),
)
