# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import api_views
import datasource_api_views

import viper_api_views
import viper_views
import jqm_views
import jqm_api_views

urlpatterns = patterns('',
	#workspace
	#(r'^$', views.show_workspaces),
	#(r'^workspace/create/$', views.create_workspace),
	#(r'^workspace/delete/(\d+)/$', views.delete_workspace),
	#project
	(r'^projects/$', views.show_projects),
	(r'^project/edit/(\d+)/$', views.show_workbench),
	(r'^project/copy/(\d+)/$', views.copy_project),
	(r'^project/export/$', views.export_project),
	(r'^project/import/$', views.import_project),
	(r'^project/create/$', views.create_project),
	(r'^project/delete/(\d+)/$', views.delete_project),
	#(r'^jqm/(\d+)/$', views.show_mobile_page),
	(r'^preview/(\d+)/(\d+)/$', views.preview_page),
	(r'^preview/(\d+)/$', views.preview_page, {'page_id': None}),

	(r'^jqm_design_page/get/$', jqm_views.show_design_page),
	(r'^jqm/preview/$', jqm_views.show_preview_page),
	(r'^jqm/view_production/$', jqm_views.show_production_page),
	(r'^api/jqm_design_page/create/$', jqm_api_views.create_page),

	#viper design
	(r'^viper_design_page/get/$', viper_views.show_viper_design_page),
	(r'^viper_production_page/get/$', viper_views.show_viper_production_page),
	#(r'^viper_page/get/$', views.show_viper_page),
	#(r'^viper_list_page/get/$', views.show_viper_list_page),
	(r'^viper/preview/$', viper_views.show_viper_production_page),
	(r'^viper/page/$', viper_views.show_free_page),
	# (r'^viper/records/$', viper_views.list_records),
	(r'^viper/record/create/$', viper_views.create_record),
	(r'^viper/record/update/$', viper_views.update_record),
	(r'^viper/record/delete/$', viper_views.delete_record),
	(r'^viper/api/record_display_index/update/$', viper_api_views.update_record_display_index),
	(r'^viper/api/records/get/$', viper_api_views.get_records),
	(r'^api/viper_design_page/create/$', viper_api_views.create_page),
	(r'^api/viper_design_page_by_id/create/$', viper_api_views.create_page_by_id),


	#workspace api
	(r'^api/workspace_name/update/$', api_views.update_workspace_name),
	#page template api
	(r'^api/page_template/create/$', api_views.create_page_template),
	(r'^api/page_templates/get/$', api_views.get_page_templates),
	#datasource api
	(r'^api/datasource_project_pages/get/$', datasource_api_views.get_datasource_project_pages),
	#project api
	(r'^api/project_name/update/$', api_views.update_project_name),
	(r'^api/images/get/$', api_views.get_project_images),
	(r'^api/image/delete/$', api_views.delete_project_image),
	(r'^api/nav_icons/get/$', api_views.get_project_nav_icons),
	#page api
	(r'^api/page/synchronize/$', api_views.synchronize_page),
	(r'^api/page/delete/$', api_views.delete_page),
	(r'^api/page_index/update/$', api_views.update_page_display_index),
	#(r'^api/pages/create/$', api_views.create_pages),
	#(r'^api/mobile_page/create/$', api_views.create_mobile_page),
	#(r'^api/viper_result/preview/$', api_views.preview_viper_result),
	(r'^api/pages_json/get/$', api_views.get_pages_json),
	#css api
	(r'^api/css/get/$', api_views.get_css),
	(r'^api/css/update/$', api_views.update_css),
	(r'^api/apis_content/get/$', api_views.get_apis_content),
	(r'^api/apis_content/update/$', api_views.update_apis_content),
	#records api
	#project data api's api
	#(r'^api/project_datasource_api/call/$', api_views.call_project_datasource_api),
)