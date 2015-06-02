# -*- coding: utf-8 -*-

from django.conf.urls import *

import views

urlpatterns = patterns('',

	(r'^login/$', views.login),

	(r'^logout/$', views.logout),
)