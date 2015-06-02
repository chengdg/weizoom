# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import api_views
import app_views
import statistics_views
import workspace_views
import project_views

import global_navbar_views
from core.apiurl import apiurl

urlpatterns = patterns('',
	(r'^$', workspace_views.show_webapp),
	(r'^template/$', workspace_views.edit_template),
	(r'^preview/$', workspace_views.preview_webapp),
	
	#workspace
	(r'^workspaces/$', workspace_views.show_workspaces),
	(r'^workspace/delete/(\d+)/$', workspace_views.delete_workspace),
	#(r'^workspace_data/edit/$', workspace_views.edit_workspace_data),
	(r'^workspace_template/set/$', workspace_views.set_workspace_template),
	
	#project
	(r'^projects/$', project_views.show_projects),
	(r'^project/edit/(\d+)/$', project_views.show_workbench),
	(r'^project/delete/(\d+)/$', project_views.delete_project),
	
	#modules
	#(r'^modules/$', views.list_modules),
	#(r'^module/add/$', views.add_module),
	#(r'^module/delete/(\d+)/$', views.delete_module),

	#statistics
	#(r'^visit_statistics/$', views.get_visit_statistics),

	#customized app
	(r'^api/customized_app/create/', app_views.create_customized_app),

	#statistics
	(r'^statistics/', statistics_views.call_statistics),

	#api
	(r'^api/', apiurl('webapp')),

	# modules
	url(r'^mall/', include('webapp.modules.mall.urls')),
	url(r'^user_center/', include('webapp.modules.user_center.urls')),
	url(r'^cms/', include('webapp.modules.cms.urls')),

	#webapp global navbar
	(r'^global_navbar/', global_navbar_views.edit_global_navbar),
)
