# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	(r'^tools/$', views.list_tools),

	(r'^editor/questions/$', views.list_questions),
	(r'^editor/create/$', views.add_question),
	(r'^editor/update/(\d+)/$', views.update_question),
	(r'^editor/delete/(\d+)/$', views.delete_question),
	(r'^editor/update_status/(\d+)/$', views.update_question_status),

	(r'^api/question/create/$', api_views.create_question),
	(r'^api/problems/get/(\d+)/$', api_views.get_problems),
	(r'^api/prizes/get/(\d+)/$', api_views.get_prizes),
	(r'^api/pattern/check_duplicate/$', api_views.check_duplicate_start_patterns),

)