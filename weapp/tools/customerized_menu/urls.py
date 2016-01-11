# -*- coding: utf-8 -*-

__author__ = "chuter"

from django.conf.urls import *
import views

urlpatterns = patterns('',
	(r'^create/$', views.create_customerized_menu),
#	(r'^get/$', views.get_customerized_menu),
	(r'^update/$', views.update_customerized_menu),
)