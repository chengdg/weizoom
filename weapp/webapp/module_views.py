# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
import shutil
try:
    import Image
except:
    from PIL import Image
import copy

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth

from models import *
from core.jsonresponse import create_response, JsonResponse
from termite import pagestore as pagestore_manager
import modules as raw_webapp_modules
from account.social_account.models import SocialAccount

from webapp import FIRST_NAV_NAME, MODULE_NAV_NAME

#===============================================================================
# show_modules : 显示module列表
#===============================================================================
def __get_modules_page_second_navs(workspaces):
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')
	second_navs = []

	for workspace in workspaces:
		if workspace.is_deleted:
			continue

		if 'viper:' in workspace.data_backend:
			project_id = workspace.data_backend.split(':')[-1]
			project = Project.objects.get(id=project_id)
			#取viper project的source project的page集合
			pages = list(pagestore.get_pages(str(project.source_project_id)))
			webapp_editor_nav = {
				'section': workspace.name,
				'navs': []
			}
			for page in pages:
				page_id = page['page_id']
				page_model = page['component']['model']
				print page_model
				if page_model.get('is_free_page', 'no') == 'yes':
					url = '/workbench/viper/page/?project_id=%s&page_id=%s' % (project_id, page_id)
				else:
					url = '/workbench/viper/records/?project_id=%s&page_id=%s' % (project_id, page_id)
				webapp_editor_nav['navs'].append({
					'name': page_id,
					'url': url,
					'title': page['component']['model']['navName']
				})

			#插入“管理模板”
			'''
			webapp_editor_nav['navs'].append({
				'name': 'template',
				'url': '/termite/workbench/project/edit/%d/' % workspace.template_project_id,
				'title': u'模板管理'
			})
			'''

			second_navs.append(webapp_editor_nav)
		elif 'module:' in workspace.data_backend:
			export_module_name = 'webapp.modules.%s.export' % workspace.data_backend.split(':')[-1]
			module = __import__(export_module_name, {}, {}, ['*',])
			#second_navs.append({'section': workspace.name, 'navs':module.NAV['navs']})
			nav = copy.deepcopy(module.NAV)
			#插入“管理模板”
			'''
			nav['navs'].append({
				'name': 'template',
				'url': '/termite/workbench/project/edit/%d/' % workspace.template_project_id,
				'title': u'模板管理'
			})
			'''
			second_navs.append(nav)
		else:
			pass

	'''
	second_navs.append(
		{
			'section': u'微站模块',
			'navs': [{
				'name': 'module',
				'title': u'模块管理',
				'url': '/webapp/modules/',
			}]
		}
	)
	second_navs.append(
		{
			'section': u'微站统计',
			'navs': [{
				'name': 'statistics',
				'title': u'流量统计',
				'url': '/webapp/visit_statistics/',
			}]
		}
	)
	'''

	return second_navs


#===============================================================================
# get_modules_page_second_navs: 供外部调用，获得当前user的左侧导航
#===============================================================================
def get_modules_page_second_navs(request):
	workspaces = [workspace for workspace in Workspace.objects.filter(owner=request.user) if workspace.inner_name != 'home_page']
	workspaces.sort(lambda x,y: cmp(x.display_index, y.display_index))
	return __get_modules_page_second_navs(workspaces)


#===============================================================================
# show_modules: 显示module列表
#===============================================================================
@login_required
def show_modules(request):
	return list_modules(request)


#===============================================================================
# list_modules : 显示module列表
#===============================================================================
@login_required
def list_modules(request):
	#获得系统中的webapp module
	system_manager = User.objects.get(username='manager')
	module_workspaces = list(Workspace.objects.filter(owner=system_manager))
	module_workspaces.sort(lambda x,y: cmp(x.id, y.id))
	id2module = dict([(module_workspace.id, module_workspace) for module_workspace in module_workspaces])

	#识别当前已选中的webapp module
	user_workspaces = list(Workspace.objects.filter(owner=request.user))
	for workspace in user_workspaces:
		module = id2module.get(workspace.source_workspace_id, None)
		module.is_selected = (not workspace.is_deleted)
	user_workspaces.sort(lambda x,y: cmp(x.display_index, y.display_index))

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_nav_name': MODULE_NAV_NAME,
		'second_navs': __get_modules_page_second_navs(user_workspaces),
		'module_workspaces': module_workspaces
	})
	return render_to_response('webapp/modules.html', c)


#===============================================================================
# __delete_project : 删除project
#===============================================================================
def __delete_project(project):
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')

	#module_project = Project.objects.get(id=project_id)

	'''	
	for jqm_project in Project.objects.filter(datasource_project_id=module_project.id):
		pagestore.remove_project_pages(str(jqm_project.id))
	Project.objects.filter(datasource_project_id=module_project.id).delete()
	'''

	pagestore.remove_project_pages(str(project.id))
	Project.objects.filter(id=project.id).delete()


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
# add_module : 添加module
#===============================================================================
@login_required
def add_module(request):
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')

	#获得页面上选中的module
	module_ids = []
	for key, value in request.POST.items():
		if key.startswith('module_'):
			module_ids.append(int(value))
	module_id_set = set(module_ids)

	#获得用户已经创建的workspace
	existed_workspaces = list(Workspace.objects.filter(owner=request.user))
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
	id2module = dict([(workspace.id, workspace) for workspace in Workspace.objects.filter(id__in=list(modules_need_add))])
	for module_workspace_id, module_workspace in id2module.items():
		new_workspace = Workspace.objects.create(
			owner = request.user,
			name = module_workspace.name,
			source_workspace_id = module_workspace.id,
			data_backend = module_workspace.data_backend
		)

		module_projects = list(Project.objects.filter(workspace=module_workspace_id))
		#复制workspace下的jqm project，及其page
		template_project = None #template_project默认为遇到的第一个jqm project
		new_data_backend = None
		for module_project in module_projects:
			new_project = Project.objects.create(
				owner = request.user, 
				workspace_id = new_workspace.id,
				name = module_project.name,
				type = module_project.type,
				source_project_id = module_project.id,
				datasource_project_id = 0
			)

			if module_project.type == 'viper':
				#跳过viper project，不拷贝page
				new_data_backend = 'viper:%d' % new_project.id
				continue

			pagestore.copy_project_pages(str(module_project.id), str(new_project.id))

			if not template_project:
				template_project = new_project

		if new_data_backend:
			Workspace.objects.filter(id=new_workspace.id).update(
				template_project_id = template_project.id, 
				data_backend = new_data_backend
			)
		else:
			Workspace.objects.filter(id=new_workspace.id).update(
				template_project_id = template_project.id
			)
	
	#处理需要恢复的module workspace
	#Workspace.objects.filter(id__in=list(modules_need_restore)).update(is_deleted = False)

	#处理需要删除的module workspace
	#Workspace.objects.filter(id__in=list(modules_need_delete)).update(is_deleted = True)
	#做物理删除
	__delete_workspaces(list(modules_need_delete))

	return HttpResponseRedirect('/webapp/modules/')
