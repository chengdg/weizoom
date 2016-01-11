# -*- coding: utf-8 -*-

__author__ = "liupeiyu"

from django.conf.urls import *
import views

urlpatterns = patterns('',
	(r'^info/$', views.get_weather_info),
)