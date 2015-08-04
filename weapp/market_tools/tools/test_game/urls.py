# -*- coding: utf-8 -*-

__author__ = "robert"


from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.list_test_games),
	(r'^test_game/create/$', views.create_create_game),
	(r'^test_game/update/(\d+)/$', views.update_test_game),
	(r'^test_game/join_user/(\d+)/$', views.join_user),
	(r'^test_game/delete/(\d+)/$', views.delete_test_game),
	(r'^api/', api_views.call_api),
)
