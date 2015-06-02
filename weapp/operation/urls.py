# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import api_views
urlpatterns = patterns('',
	(r'^editor/problem_titles/$', views.list_problem_titles),
	(r'^editor/problem_title/delete/(\d+)/$', views.delete_problem_title),
	(r'^editor/problem_title/get/(\d+)/$', views.get_problem_title),
	(r'^editor/problem/delete/(\d+)/$', views.delete_problem),


	(r'^api/problem_title/add/$', api_views.add_problem_title),
	(r'^editor/problem_title/add/$', views.add_problem,{'title_id': 0}),
	(r'^api/problem_titles/get/$', api_views.get_problem_title_list),
	(r'^api/problem_titles/display_index/update/$', api_views.update_problem_title_display_index),
	(r'^api/problem/add/$', api_views.add_problem),

	(r'^api/problems/display_index/update/$', api_views.update_problems_display_index),

	(r'^api/problems/get/(\d+)/$', api_views.list_problems),

	(r'^editor/versions/$', views.list_versions),
	(r'^editor/version/delete/(\d+)/$', views.delete_version),
	(r'^editor/version/update/(\d+)/$', views.update_version),
	(r'^editor/version/add/$', views.add_version),

	(r'^editor/feedbacks/$', views.list_feedbacks),
	(r'^api/feedback/add/$', api_views.add_feedback),
	
	#(r'^editor/use_help/$', views.use_help),


)