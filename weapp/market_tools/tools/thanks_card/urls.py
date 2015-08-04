# -*- coding: utf-8 -*-

__author__ = "sunny"


from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.get_thanks_cards),
	(r'^thanks_card/edit/$', views.edit_thanks_card),
)
