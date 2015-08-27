# -*- coding: utf-8 -*-
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


#===============================================================================
# get_modules : 获得webapp module集合
#===============================================================================
def get_modules(request):
	modules_dir = os.path.join(settings.PROJECT_HOME, '../webapp/modules')
	modules = []
	for file in os.listdir(modules_dir):
		if file[0] == '.':
			#skip .svn dir
			continue

		if file == 'static':
			#skip static dir
			continue

		module_dir = os.path.join(modules_dir, file)
		if not os.path.isdir(module_dir):
			#skip normal file
			continue

		modules.append({
			'name': file,
			'value': file
		})

	response = create_response(200)
	response.data = modules
	return response.get_response()


#===============================================================================
# get_installed_modules : 获得已经安装的webapp module集合
#===============================================================================
def get_installed_modules(request):
	manager = User.objects.get(username='manager')
	modules = []
	for workspace in Workspace.objects.filter(owner=manager):
		modules.append({
			'name': workspace.name,
			'value': workspace.id
		})

	response = create_response(200)
	response.data = modules
	return response.get_response()


#===============================================================================
# __delete_workspace : 删除workspace
#===============================================================================
def __delete_workspaces(workspace_ids):
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')

	project_ids = []
	for workspace_id in workspace_ids:
		for project in Project.objects.filter(workspace_id=workspace_id):
			print '>>> remove mongo page in project ', project.id
			pagestore.remove_project_pages(str(project.id))
			project_ids.append(project.id)

	Project.objects.filter(id__in=project_ids).delete()
	Workspace.objects.filter(id__in=workspace_ids).delete()


#===============================================================================
# add_user_module : 为user添加webapp module
#===============================================================================
def add_user_module(request):
	print '***************** add user module'
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')
	user = User.objects.get(id=request.POST['user_id'])

	#获得页面上选中的module
	module_id_set = set(json.loads(request.POST['modules']))

	#获得用户已经创建的workspace
	existed_workspaces = list(Workspace.objects.filter(owner=user))
	existed_source_workspace_id_set = set()
	modules_need_restore = set()
	modules_need_delete = set()
	for existed_workspace in existed_workspaces:
		existed_source_workspace_id_set.add(existed_workspace.source_workspace_id)

		if (existed_workspace.source_workspace_id in module_id_set) and existed_workspace.is_deleted:
			#已删除的workspace出现在选中的workspace集合中，需要恢复
			modules_need_restore.add(existed_workspace.id)
			continue

		if not (existed_workspace.source_workspace_id in module_id_set):
			#已有的workspace不在选中的workspace集合中，需要删除
			modules_need_delete.add(existed_workspace.id)
			continue
		
	modules_need_add = module_id_set - existed_source_workspace_id_set

	#处理需要创建的module workspace
	home_page_workspace = None
	mall_workspace = None
	user_center_workspace = None
	id2module = dict([(workspace.id, workspace) for workspace in Workspace.objects.filter(id__in=list(modules_need_add))])
	for module_workspace_id, module_workspace in id2module.items():
		new_workspace = Workspace.objects.create(
			owner = user,
			name = module_workspace.name,
			inner_name = module_workspace.inner_name,
			source_workspace_id = module_workspace.id,
			data_backend = module_workspace.data_backend,
			display_index = module_workspace.display_index
		)

		if new_workspace.inner_name == 'home_page':
			home_page_workspace = new_workspace
		elif new_workspace.inner_name == 'mall':
			mall_workspace = new_workspace
		elif new_workspace.inner_name == 'user_center':
			user_center_workspace = new_workspace

		module_projects = list(Project.objects.filter(workspace=module_workspace_id))
		#复制workspace下的jqm project，及其page
		template_project = None #template_project是inner_name为'default'的project
		new_data_backend = None
		for module_project in module_projects:
			if module_project.type == 'wepage':
				if module_project.inner_name != 'wepage_empty':
					continue
				else:
					module_project.is_active = True
					module_project.is_enable = True

			new_project = Project.objects.create(
				owner = user, 
				workspace_id = new_workspace.id,
				name = module_project.name,
				inner_name = module_project.inner_name,
				type = module_project.type,
				source_project_id = module_project.id,
				datasource_project_id = 0,
				is_active = module_project.is_active,
				is_enable = module_project.is_enable,
				site_title = module_project.site_title
			)

			if module_project.type == 'viper':
				#跳过viper project，不拷贝page
				new_data_backend = 'viper:%d' % new_project.id
				continue

			pagestore.copy_project_pages(str(module_project.id), str(new_project.id))


	#如果用户还没有global navbar，创建之
	if GlobalNavbar.objects.filter(owner=user).count() == 0:
		#准备webapp global navbar的模板
		src = open(os.path.join(settings.PROJECT_HOME, '..', 'webapp/resource/init_global_navbar.json'), 'rb')
		webapp_global_navbar_template = src.read()
		src.close()

		context = {
			"webapp_owner_id": user.id, 
			"home_page_workspace_id": home_page_workspace.id,
			"mall_workspace_id": mall_workspace.id,
			"user_center_workspace_id": user_center_workspace.id
		}
		webapp_global_navbar_content = webapp_global_navbar_template % context

		GlobalNavbar.objects.create(
			owner = user,
			content = webapp_global_navbar_content,
			is_enable = True
		)

	
	#处理需要恢复的module workspace
	#Workspace.objects.filter(id__in=list(modules_need_restore)).update(is_deleted = False)
	

	#处理需要删除的module workspace
	#Workspace.objects.filter(id__in=list(modules_need_delete)).update(is_deleted = True)
	#做物理删除
	__delete_workspaces(list(modules_need_delete))

	return create_response(200).get_response()