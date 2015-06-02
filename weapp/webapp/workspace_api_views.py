# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil
import base64
import random

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group
from django.contrib import auth

from models import *
from account.models import UserProfile
from product.models import Product
from product.models import UserHasProduct
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from core import apiview_util
import pagestore as pagestore_manager

import apps

def __get_workspace_data_backend(workspace):
	if not workspace.data_backend:
		return None, None
	else:
		return workspace.data_backend.split(':')


#######################################################################
# get_workspaces: 获得属于一个用户的所有workspace
#######################################################################
@login_required
def get_tools(request):
	tools = dict()
	
	market_tools_dir = os.path.join(settings.PROJECT_HOME, '../market_tools/tools/')
	existed_market_tools = set(UserHasProduct.objects.get(owner=request.user).product.market_tool_modules.split(','))
		
	for market_tool in os.listdir(market_tools_dir):
		market_tool_dir = os.path.join(market_tools_dir, market_tool)
		if not os.path.isdir(market_tool_dir):
			continue

		export_file = os.path.join(market_tool_dir, 'export.py')
		if not os.path.exists(export_file):
			continue
		if not market_tool in existed_market_tools:
			continue

		export_module_name = 'market_tools.tools.%s.export' % market_tool
		export_module = __import__(export_module_name, {}, {}, ['*',])
		
 		if not hasattr(export_module, 'get_link_targets'):
 			continue

		tools[market_tool] = 1

	for app in apps.get_apps(request):
		tools[app['value'].replace('app:', '')] = 1

	response = create_response(200)
	response.data = tools
	return response.get_response()

#######################################################################
# get_workspaces: 获得属于一个用户的所有workspace
#######################################################################
@login_required
def get_workspaces(request):
	workspaces = [{'text': u'选择项目...', 'value':0}]
	workspace_filter_set = None
	if 'workspace_filter' in request.GET:
		#workspace_filter参数是"cms:mall"这样的格式
		workspace_filter_set = set(request.GET.get('workspace_filter', '').split(':'))
	#选择webapp中的module对应的workspace
	for workspace in Workspace.objects.filter(owner=request.user):
		if workspace_filter_set:
			if not workspace.inner_name in workspace_filter_set:
				#workspace不在workspace_filter_set中，跳过
				continue

		workspaces.append({
			'text': workspace.name,
			'innerName': workspace.inner_name,
			'value': str(workspace.id)
		})

	if not workspace_filter_set:
		#选择market_tool
		market_tools_dir = os.path.join(settings.PROJECT_HOME, '../market_tools/tools/')
		existed_market_tools = set()
		if request.user.username != 'manager':
			existed_market_tools = set(UserHasProduct.objects.get(owner=request.user).product.market_tool_modules.split(','))
			
		for market_tool in os.listdir(market_tools_dir):
			market_tool_dir = os.path.join(market_tools_dir, market_tool)
			if not os.path.isdir(market_tool_dir):
				continue

			export_file = os.path.join(market_tool_dir, 'export.py')
			if not os.path.exists(export_file):
				continue
			if request.user.username != 'manager' and (not market_tool in existed_market_tools):
				continue

			export_module_name = 'market_tools.tools.%s.export' % market_tool
			export_module = __import__(export_module_name, {}, {}, ['*',])
			
	 		if not hasattr(export_module, 'get_link_targets'):
	 			continue

			workspaces.append({
					'text': export_module.TOOL_NAME,
					'value': 'market_tool:%s' % market_tool
				})
		workspaces.extend(apps.get_apps(request))
		workspaces.append({
			'text': u'外部链接',
			'value': u'custom'
		})
	
	response = create_response(200)
	response.data = workspaces
	return response.get_response()


#######################################################################
# create_workspace: 创建workspace
#######################################################################
def create_workspace(request):
	inner_name = request.POST['inner_name']

	#检查是否有相同inner_name的workspace
	if Workspace.objects.filter(owner=request.user, inner_name=inner_name).count() > 0:
		response = create_response(500)
		response.data = u'已存在相同inner_name的项目'
		return response.get_response()
	
	workspace = Workspace.objects.create(
		owner = request.user, 
		name = request.POST['name'],
		inner_name = request.POST['inner_name']
	)
	Workspace.objects.filter(id=workspace.id).update(display_index=workspace.id)
	
	response = create_response(200)
	return response.get_response()


#######################################################################
# update_workspace_name: 更新workspace名
#######################################################################
def update_workspace_name(request):
	workspace_id = request.POST['workspace_id']
	Workspace.objects.filter(id=workspace_id).update(name=request.POST['name'])

	response = create_response(200)
	return response.get_response()


#######################################################################
# update_workspace_data_backend: 更新workspace的data backend
#######################################################################
def update_workspace_data_backend(request):
	workspace_id = request.POST['workspace_id']
	Workspace.objects.filter(id=workspace_id).update(data_backend=request.POST['data_backend'])

	response = create_response(200)
	return response.get_response()


#######################################################################
# get_data_backends: 获得后台数据源
#######################################################################
def get_data_backends(request):
	backends = []

	#获得viper project
	workspace_id = request.GET['workspace_id']
	for project in Project.objects.filter(workspace_id=workspace_id):
		if project.type == 'viper':
			backends.append({
				'name': u'Viper项目-%s' % project.name,
				'value': 'viper:%d' % project.id
			})


	#获得webapp modules
	import models
	modules_dir = os.path.join(os.path.dirname(models.__file__), 'modules')
	for file in os.listdir(modules_dir):
		if file[0] == '.':
			#skip .svn
			continue

		if os.path.isdir(os.path.join(modules_dir, file)):
			backends.append({
				'name': u'通用模块-%s' % file,
				'value': 'module:%s' % file
			})

	response = create_response(200)
	response.data = backends
	return response.get_response()


#######################################################################
# update_workspace_display_index: 更新workspace的显示顺序
#######################################################################
def update_workspace_display_index(request):
	ids = request.GET['ids'].split(',')
	for index, id in enumerate(ids):
		Workspace.objects.filter(id=int(id)).update(display_index=index+1)

	response = create_response(200)
	return response.get_response()


#######################################################################
# export_workspace: 导出workspace
#######################################################################
def export_workspace(request):
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')
	workspace_id = request.GET['workspace_id']
	workspace = Workspace.objects.get(id=workspace_id)

	if not workspace.data_backend:
		response = create_response(500)
		response.data = u'没有配置数据源，请先配置'
		return response.get_response()

	#
	#获得workspace_dir
	#
	data_type, name_or_id = workspace.data_backend.split(':')
	webapp_modules_dir = os.path.join(settings.PROJECT_HOME, '../webapp/modules')
	workspace_dir = None
	if data_type == 'viper':
		workspace_name = 'viper_workspace_%s' % workspace.inner_name
		workspace_dir = os.path.join(webapp_modules_dir, workspace_name)
		'''
		if os.path.isdir(workspace_dir):
			#删除已存在的workspace
			shutil.rmtree(workspace_dir)

		#重建workspace目录
		os.makedirs(workspace_dir)
		'''
	elif data_type == 'module':
		workspace_name = name_or_id
		workspace_dir = os.path.join(webapp_modules_dir, workspace_name)

	#
	#导出workspace数据表的内容到${workspace_dir}/workspace目录下
	#
	workspace_data_dir = os.path.join(workspace_dir, 'workspace')
	table_data = {
		'id': workspace.id,
		'name': workspace.name,
		'inner_name': workspace.inner_name,
		'data_backend': workspace.data_backend,
		'source_workspace_id': workspace.source_workspace_id,
		'template_project_id': workspace.template_project_id
	}

	workspace_data_file_path = os.path.join(workspace_dir, 'workspace_table.json')
	workspace_data_file = open(workspace_data_file_path, 'wb')
	print >> workspace_data_file, json.dumps(table_data, indent=True)
	workspace_data_file.close()

	#
	#删除已存在的project
	#
	'''
	for file in os.listdir(workspace_dir):
		if not file.startswith('project_'):
			continue

		project_dir = os.path.join(workspace_dir, file)
		if os.path.isdir(project_dir):
			project_info_file_path = os.path.join(project_dir, 'project_info.json')
			if os.path.exists(project_info_file_path):
				f = open(project_info_file_path, 'rb')
				content = f.read()
				f.close()
				print content

				project_info = json.loads(content)
				if project_info['type'] == 'raw':
					#跳过raw 类型的project
					continue
				else:
					shutil.rmtree(project_dir)
	'''

	#
	#导出project
	#
	apis_dir = os.path.join(settings.PROJECT_HOME, '../webapp')
	css_dir = os.path.join(settings.TERMITE_HOME, '../static/project_css')
	for project in Project.objects.filter(workspace_id=workspace.id):
		project_name = 'project_%s_%s' % (project.type, project.inner_name)
		project_dir = os.path.join(workspace_dir, project_name)
		if not os.path.isdir(project_dir):
			os.makedirs(project_dir)

		#写数据库数据文件
		table_data = {
			'id': project.id,
			'name': project.name,
			'inner_name': project.inner_name,
			'type': project.type,
			'css': project.css,
			'pagestore': project.pagestore,
			'source_project_id': project.source_project_id,
			'datasource_project_id': project.datasource_project_id,
			'template_project_id': project.template_project_id
		}

		data_file_path = os.path.join(project_dir, 'project_table.json')
		data_file = open(data_file_path, 'wb')
		print >> data_file, json.dumps(table_data, indent=True)
		data_file.close()

		#拷贝apis.py
		src_file = os.path.join(apis_dir, 'apis_%s.py' % project.id)
		if os.path.exists(src_file):
			dst_file = os.path.join(project_dir, 'apis.py')
			shutil.copyfile(src_file, dst_file)

		#export project.css
		src_file = os.path.join(css_dir, 'project_%s.css' % project.id)
		if os.path.exists(src_file):
			dst_file = os.path.join(project_dir, 'project.css')
			shutil.copyfile(src_file, dst_file)	

		#导出project中的page
		pages = []
		for page in pagestore.get_pages(str(project.id)):
			del page['_id']
			pages.append(page)
		data_file_path = os.path.join(project_dir, 'pages.json')
		data_file = open(data_file_path, 'wb')
		print >> data_file, json.dumps(pages, indent=True)
		data_file.close()		

	response = create_response(200)
	return response.get_response()


#######################################################################
# sync_workspace: 同步workspace
#######################################################################
def sync_workspace(request):
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')
	modules_info = json.loads(request.POST['modules_info'])
	modules = modules_info['modules']
	allow_update = modules_info['allow_update']
	modules_dir = os.path.join(settings.PROJECT_HOME, '../webapp/modules')

	for module in modules:
		module_dir = os.path.join(modules_dir, module)
		print 'process module: ', module_dir

		#加载workspace的table data json文件
		workspace_table_data_file_path = os.path.join(module_dir, 'workspace_table.json')
		if os.path.exists(workspace_table_data_file_path):
			workspace_table_data_file = open(workspace_table_data_file_path, 'rb')
			content = workspace_table_data_file.read()
			workspace_table_data_file.close()

			data = json.loads(content)
			data['owner'] = request.user
			del data['id']

			try:
				workspace = Workspace.objects.get(owner=request.user, inner_name=data['inner_name'])
			except:
				workspace = None
			if workspace:
				if allow_update:
					#workspace已经存在，更新之
					print 'update workspace: ', workspace.inner_name
					Workspace.objects.filter(owner=request.user, inner_name=data['inner_name']).update(**data)
				else:
					print 'not allowed to update workspace'
			else:
				#workspace不存在，创建之
				print 'create workspace: ', data['inner_name']
				workspace = Workspace.objects.create(**data)
				#TODO: 是否为所有用户创建workspace?

		#同步project
		apis_dir = os.path.join(settings.PROJECT_HOME, '../webapp')
		css_dir = os.path.join(settings.TERMITE_HOME, '../static/project_css')
		template_project = None
		for file in os.listdir(module_dir):
			if not file.startswith('project_'):
				continue

			project_dir = os.path.join(module_dir, file)
			print 'process project: ', project_dir
			#加载project的table data json文件
			project_table_data_file_path = os.path.join(project_dir, 'project_table.json')
			if not os.path.exists(project_table_data_file_path):
				continue
				
			project_table_data_file = open(project_table_data_file_path, 'rb')
			content = project_table_data_file.read()
			project_table_data_file.close()

			data = json.loads(content)
			data['owner'] = request.user
			data['workspace'] = workspace
			del data['id']

			allow_update_pages = False #是否允许更新mongo中的pages
			try:
				project = Project.objects.get(workspace=workspace, inner_name=data['inner_name'])
				if allow_update:
					#如果project存在，删除pages
					print 'delete pages for project: ', project.inner_name, ' ', project.id
					pagestore.remove_project_pages(str(project.id))
					allow_update_pages = True
				else:
					print 'not allowed to remove project\'s pages'
			except:
				project = None
			if project:
				if allow_update:
					#project已经存在，更新之
					print 'update project: %s(%d)-%s' % (workspace.inner_name, workspace.id, data['inner_name'])
					Project.objects.filter(workspace=workspace, inner_name=data['inner_name']).update(**data)
				else:
					print 'not allowed to update project'
			else:
				#project不存在，创建之
				print 'create project: %s-%s' % (workspace.inner_name, data['inner_name'])
				project = Project.objects.create(**data)
				allow_update_pages = True

			if project.inner_name == 'default':
				template_project = project

			#拷贝apis.py
			# src_file = os.path.join(project_dir, 'apis.py')
			# dst_file = os.path.join(apis_dir, 'apis_%s.py' % project.id)
			# shutil.copyfile(src_file, dst_file)

			#拷贝project.css
			# src_file = os.path.join(project_dir, 'project.css')
			# dst_file = os.path.join(css_dir, 'project_%s.css' % project.id)
			# shutil.copyfile(src_file, dst_file)		

			#拷贝pages
			if allow_update_pages:
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
				if has_page:
					print 'create project\'s pages: %s' % pages_data_file_path
			else:
				print 'not allowed to re-create pages'

		if template_project:
			print 'set template project to: ', template_project.id
			Workspace.objects.filter(id=workspace.id).update(template_project_id=template_project.id)

	response = create_response(200)
	return response.get_response()


#######################################################################
# call_data_backend_project_api: 调用workspace内指定的data backend project中的api
#######################################################################
@login_required
def call_data_backend_project_api(request):
	workspace_id = request.REQUEST.get('workspace_id', '')
	workspace = None
	if workspace_id:
		if 'market_tool' in workspace_id:
			workspace = Workspace.get_market_tool_workspace(request.user, workspace_id)
		elif 'app:' in workspace_id:
			workspace = Workspace.get_app_workspace(request.user, workspace_id)
		else:
			workspace = Workspace.objects.get(id=workspace_id)
	else:
		project_id = request.GET.get('project_id', None)
		if not project_id:
			project_id = request.POST.get('project_id', None)
		project = Project.objects.get(id=project_id)
		workspace = Workspace.objects.get(id=project.workspace_id)

	#获得api name
	target_api = request.GET.get('target_api', None)
	if not target_api:
		target_api = request.POST['target_api']
	items = target_api.split('/')
	if not items[-1]:
		resource = items[-3]
		action = items[-2]
	else:
		resource = items[-2]
		action = items[-1]
	api_function_name = '%s_%s' % (action, resource)

	type, name_or_id = workspace.data_backend.split(':')
	if type == 'module' or type == 'viper':
		if type == 'viper':
			webapp_module_name = 'viper_workspace_home_page'
		else:
			webapp_module_name = name_or_id
		api_module_name = 'webapp.modules.%s.export' % webapp_module_name
		
		api_module = __import__(api_module_name, {}, {}, ['*',])
		
		request.workspace = workspace
		return getattr(api_module, api_function_name)(request)
	elif type == 'market_tool':
		market_tool_name = name_or_id
		api_module_name = 'market_tools.tools.%s.export' % market_tool_name

		api_module = __import__(api_module_name, {}, {}, ['*',])
		
		request.workspace = workspace
		return getattr(api_module, api_function_name)(request)
	elif type == 'app':
		api_module_name = 'apps.export'

		api_module = __import__(api_module_name, {}, {}, ['*',])

		if settings.IN_DEVELOP_MODE:
			print 'call apps api "%s" in %s' % (api_function_name, api_module.__file__)
		request.workspace = workspace
		return getattr(api_module, api_function_name)(request)


#######################################################################
# update_workspace_template: user更新workspace的template
#######################################################################
def update_workspace_template(request):
	template_name = request.POST['target_project_inner_name']
	Workspace.objects.filter(owner=request.user, inner_name='home_page').update(template_name=template_name)
	UserProfile.objects.filter(user=request.user).update(homepage_template_name=template_name)
		
	response = create_response(200)
	return response.get_response()


#######################################################################
# create_template_project: 为workspace创建template project
#######################################################################
def create_template_project(request):
	workspace = Workspace.objects.get(owner=request.user, inner_name='home_page')

	count = Project.objects.filter(owner=request.user, inner_name__startswith='custom_template').count()

	project = Project.objects.create(
		owner=request.user, 
		inner_name = 'custom_template',
		workspace_id=workspace.id,
		name=u'定制模板{}'.format(count+1),
		type='weapp'
	)
	Project.objects.filter(id=project.id).update(inner_name = project.inner_name + str(project.id))
	
	#导入page
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')
	custom_template_source_dir = os.path.join(settings.PROJECT_HOME, '../webapp/modules/viper_workspace_home_page/project_weapp_custom_template_base/')
	pages_data_file_path = os.path.join(custom_template_source_dir, 'pages.json')
	pages_data_file = open(pages_data_file_path, 'rb')
	content = pages_data_file.read()
	pages_data_file.close()
	for page in json.loads(content):
		page_id = page['page_id']
		page_component = page['component']
		page_component['is_new_created'] = True
		pagestore.save_page(str(project.id), page_id, page_component)

	response = create_response(200)
	response.data = {
		'project_id': project.id
	}
	return response.get_response()