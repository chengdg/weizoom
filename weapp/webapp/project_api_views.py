# -*- coding: utf-8 -*-
"""@package webapp.project_api_views
Webapp Project API

"""

#import logging
#import time
#from datetime import timedelta, datetime, date
#import urllib, urllib2
import os
import json
#import subprocess
import shutil
#import base64
#import random

#from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
#from django.template import Context, RequestContext
#from django.template.loader import get_template
#from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
#from django.shortcuts import render_to_response
#from django.contrib.auth.models import User, Group
#from django.contrib import auth

from models import *
#from account.models import UserProfile
#from product.models import Product
#from product.models import UserHasProduct
from core.jsonresponse import create_response
#from core.exceptionutil import unicode_full_stack
#from core import apiview_util
from termite import pagestore as pagestore_manager
import apps


def sync_to_user_template_project(request):
	"""
	将template project同步到所有用户
	"""
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')

	project_id = request.POST['project_id']
	page = pagestore.get_first_page(project_id)
	project = Project.objects.get(id=project_id)
	inner_name = project.inner_name

	manager = User.objects.get(username='manager')

	#workspace_ids = Project.objects.values_list('workspace_id', flat=True).filter(inner_name=inner_name, owner=manager)
	#workspace2project = dict([(p.workspace_id, p) for p in Project.objects.filter(workspace_id__in=workspace_ids, inner_name=inner_name)])

	#为所有拥有该workspace的用户添加project
	source_workspace = Workspace.objects.get(owner=manager, inner_name="home_page")
	project = Project.objects.get(owner=manager, workspace=source_workspace, inner_name=inner_name)
	for workspace in Workspace.objects.filter(source_workspace_id=source_workspace.id):
		is_new_created_page = True
		if Project.objects.filter(workspace=workspace, inner_name=inner_name).count() > 0:
			#更新
			is_new_created_page = False
			new_project = Project.objects.get(workspace=workspace, inner_name=inner_name)
			new_project_id = str(new_project.id)
		else:
			#创建
			new_project = Project.objects.create(
				owner_id = workspace.owner_id,
				workspace = workspace,
				name = project.name,
				inner_name = project.inner_name,
				type = project.type,
				css = project.css,
				pagestore = project.pagestore,
				source_project_id = project.id,
				datasource_project_id = 0,
				template_project_id = 0
			)
			new_project_id = str(new_project.id)

		if project.type == 'jqm':
			page_id = page['page_id']
			page_component = page['component']
			page_component['is_new_created'] = is_new_created_page
			pagestore.save_page(new_project_id, page_id, page_component)

	response = create_response(200)
	return response.get_response()


def update_template_project(request):
	"""
	从硬盘上更新数据库中的模板project和page信息
	"""
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')

	project_id = request.POST['project_id']
	project = Project.objects.get(id=project_id)

	#删除已有的page
	pagestore.remove_project_pages(project_id)

	#更新page
	project_dir = '%s/../webapp/modules/viper_workspace_home_page/project_jqm_%s' % (settings.PROJECT_HOME, project.inner_name)
	pages_data_file_path = os.path.join(project_dir, 'pages.json')
	pages_data_file = open(pages_data_file_path, 'rb')
	content = pages_data_file.read()
	pages_data_file.close()
	has_page = False
	for page in json.loads(content):
		has_page = True
		page_id = page['page_id']
		page_component = page['component']
		page_component['is_new_created'] = True
		pagestore.save_page(str(project.id), page_id, page_component)
	if settings.MODE == 'develop' and has_page:
		print 'create project\'s pages: %s' % pages_data_file_path

	#更新css
	# css_dir = os.path.join(settings.TERMITE_HOME, '../static/project_css')
	# src_file = os.path.join(project_dir, 'project.css')
	# dst_file = os.path.join(css_dir, 'project_%s.css' % project.id)
	# shutil.copyfile(src_file, dst_file)
	# if settings.MODE == 'develop':
	# 	print 'update css file: %s' % dst_file

	response = create_response(200)
	return response.get_response()


def __create_project_css(project):
	"""
	创建project的css文件
	"""
	css_dir = os.path.join(settings.TERMITE_HOME, '..', 'static', 'project_css')
	if not os.path.exists(css_dir):
		os.makedirs(css_dir)

	project_id = project.id
	css_file = os.path.join(css_dir, 'project_%s.css' % project_id)
	if not os.path.exists(css_file):
		f = open(css_file, 'wb')
		print >> f, '/* css conentet for project %s */' % project_id
		f.close()


def __create_project_apis_file(project):
	"""
	创建project的apis.py文件
	"""
	apis_dir = os.path.join(settings.PROJECT_HOME, '..', 'webapp')

	project_id = project.id
	src_file = os.path.join(apis_dir, 'apis_template.py')
	dst_file = os.path.join(apis_dir, 'apis_%s.py' % project_id)
	shutil.copyfile(src_file, dst_file)


def create_project(request):
	"""
	创建project
	"""
	workspace_id = request.POST['workspace_id']
	type = request.POST['type']
	inner_name = request.POST['inner_name']

	#检查是否有相同inner_name的project
	if Project.objects.filter(workspace_id=workspace_id, inner_name=inner_name).count() > 0:
		response = create_response(500)
		response.data = u'已存在相同inner_name的子项目'
		return response.get_response()

	#无同inner_name的project，创建project
	project = Project.objects.create(
		owner=request.user, 
		workspace_id=workspace_id,
		name=request.POST['name'],
		inner_name=request.POST['inner_name'],
		type=type,
		datasource_project_id=0
	)
	#__create_project_css(project)
	#__create_project_apis_file(project)

	response = create_response(200)
	return response.get_response()


def update_project_name(request):
	"""
	更新project名
	"""
	project_id = request.POST['project_id']
	new_name = request.POST['name'].strip()
	print request.POST['name']
	print new_name
	Project.objects.filter(id=project_id).update(name=new_name)

	response = create_response(200)
	return response.get_response()


def get_project_templates(request):
	"""
	获得project的template集合
	"""
	#获取相同datasource_project_id的jqm project，作为模板
	templates = []
	for project in Project.objects.filter(workspace_id=request.project.workspace_id):
		if project.type != 'viper':
			templates.append({
				'id': project.id,
				'name': project.name,
				'innerName': project.inner_name
			})

	response = create_response(200)
	response.data = {
		'currentTemplateProjectId': request.project.workspace.template_project_id,
		'templates': templates
	}
	return response.get_response()


def __get_workspace_data_backend(workspace):
	"""
	处理workspace data backend
	"""
	if not workspace.data_backend:
		return None, None
	else:
		return workspace.data_backend.split(':')


def get_raw_mobile_projects(request):
	"""
	获得raw mobile project集合
	"""
	workspace = Workspace.objects.get(id=request.GET['workspace_id'])
	data_type, name_or_id = __get_workspace_data_backend(workspace)
	print data_type, name_or_id, workspace.data_backend

	projects = []
	if data_type == 'module':
		module_name = name_or_id
	elif data_type == 'viper':
		data_backend_project_id = name_or_id
		try:
			data_backend_project = Project.objects.get(id=data_backend_project_id)
		except:
			response = create_response(200)
			response.data = []
			return response.get_response()
		module_name = 'viper_workspace_%s' % workspace.inner_name
	else:
		module_name = None

	if module_name:
		modules_dir = os.path.join(settings.PROJECT_HOME, '../webapp/modules', module_name)
		print modules_dir
		for file in os.listdir(modules_dir):
			if not file.startswith('project_'):
				continue

			project_info_json_path = os.path.join(modules_dir, file, 'project_info.json')
			print 'check ', project_info_json_path
			if not os.path.exists(project_info_json_path):
				continue

			info_file = open(project_info_json_path, 'rb')
			content = info_file.read()
			info_file.close()

			info = json.loads(content)
			print info
			if info['type'] == 'raw':
				projects.append({
					'text': file,
					'value': file
				})

	response = create_response(200)
	response.data = projects
	return response.get_response()


def call_project_api(request):
	"""
	调用project中的api
	"""
	target_api = request.REQUEST.get('target_api', None)

	path_info = request.META['PATH_INFO']
	is_call_webapp_api = '/webapp/api' in path_info
	is_call_market_tool_api = False
	if hasattr(request, 'market_tool_name'):
		is_call_webapp_api = False
		is_call_market_tool_api = True
	is_call_app_api = False
	if hasattr(request, 'app_name'):
		is_call_webapp_api = False
		is_call_market_tool_api = False
		is_call_app_api = True
		
	if target_api and target_api == 'shared_url/record':
		is_call_app_api = True

	if is_call_webapp_api:
		module_name = request.REQUEST.get('module', None)

		api_module_path = 'webapp.modules.%s.mobile_api_views' % module_name
		api_module = __import__(api_module_path, {}, {}, ['*',])
		resource, action = target_api.split('/')
		api_function_name = '%s_%s' % (action, resource)
		function = getattr(api_module, api_function_name)
		if settings.IN_DEVELOP_MODE:
			print 'call api "%s" in %s' % (api_function_name, api_module.__file__)
		return function(request)
	elif is_call_market_tool_api:
		module_name = request.market_tool_name

		api_module_path = 'market_tools.tools.%s.mobile_api_views' % module_name
		api_module = __import__(api_module_path, {}, {}, ['*',])
		resource, action = target_api.split('/')
		api_function_name = '%s_%s' % (action, resource)
		function = getattr(api_module, api_function_name)
		if settings.IN_DEVELOP_MODE:
			print 'call api "%s" in %s' % (api_function_name, api_module.__file__)
		return function(request)
	elif is_call_app_api:
		return apps.get_mobile_api_response(request)
	else:
		pass