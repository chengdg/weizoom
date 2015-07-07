# -*- coding: utf-8 -*-

import logging
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
import project_views
from views import WEBAPP_TEMPLATE_FIRST_NAV_NAME, FIRST_NAV_NAME, WEBAPP_TEMPLATE_SECOND_NAVS


#===============================================================================
# show_webapp : 显示“微站”页面，根据用户不同显示不同页面
#===============================================================================
@login_required
def show_webapp(request):
	if request.user.username == 'manager':
		return show_workspaces(request)
	else:
		return HttpResponseRedirect('/webapp/mall/')


#===============================================================================
# preview_webapp : 预览一个微站
#===============================================================================
def preview_webapp(request):
	project_id = int(request.GET.get('project_id', '0'))
	workspace_id = int(request.GET.get('workspace_id', '0'))

	if workspace_id == 0 and project_id == 0:
		raise Http404('project_id and workspace_id are all 0')

	webapp_id = '';
	if project_id == 0:
		workspace = Workspace.objects.get(id=workspace_id)
		webapp_id = workspace.owner.get_profile().webapp_id
		project_id = workspace.template_project_id
	else:
		project = Project.objects.get(id=project_id)
		webapp_id = project.owner.get_profile().webapp_id

	if request.user.is_authenticated():
		sessionid = request.COOKIES['sessionid']
		openid = 'pc-weixin-user-%s' % sessionid
		is_subscribed = (SocialAccount.objects.filter(openid=openid).count() > 0)
		
		c = RequestContext(request, {
			'is_under_deploy': (settings.MODE == 'deploy'),
			'is_subscribed': is_subscribed,
			'webapp_id': webapp_id,
			'project_id': project_id,
			'workspace_id': workspace_id
		})
		return render_to_response('webapp/preview.html', c)
	else:
		return HttpResponseRedirect('/workbench/jqm/preview/?project_id=%s' % project_id)


#===============================================================================
# show_workspaces : 为manager用户显示workspace列表
#===============================================================================
@login_required
def show_workspaces(request):
	workspaces = Workspace.objects.filter(owner=request.user).order_by('display_index')

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': None,
		'workspaces': workspaces
	})
	return render_to_response('webapp/workspaces.html', c)


#===============================================================================
# delete_workspace : 删除workspace
#===============================================================================
@login_required
def delete_workspace(request, workspace_id):
	#删除workspace所有的project
	for project in Project.objects.filter(workspace_id=workspace_id):
		project_views.delete_project(request, project.id)

	#删除workspace本身
	Workspace.objects.filter(id=workspace_id).delete()
	return HttpResponseRedirect('/webapp/');


#===============================================================================
# edit_workspace_data : 编辑workspace数据(DO NOT DELETE)
#===============================================================================
# @login_required
# def edit_workspace_data(request):
# 	if 'workspace_id' in request.GET:
# 		workspace = Workspace.objects.get(id=request.GET['workspace_id'])
		
# 		type, name_or_id = workspace.data_backend.split(':')
# 		if type == 'viper':
# 			data_backend_project_id = name_or_id
# 			return HttpResponseRedirect('/workbench/viper/records/?project_id=%s' % data_backend_project_id)
# 		elif type == 'module':
# 			module_name = name_or_id
# 			return HttpResponseRedirect('/webapp/%s/' % module_name)
# 	else:
# 		workspaces = Workspace.objects.filter(owner=request.user)
# 		for workspace in workspaces:
# 			type, name_or_id = workspace.data_backend.split(':')
# 			if type == 'viper':
# 				data_backend_project_id = name_or_id
# 				return HttpResponseRedirect('/workbench/viper/records/?project_id=%s' % data_backend_project_id)
# 			elif type == 'module':
# 				module_name = name_or_id
# 				return HttpResponseRedirect('/webapp/%s/' % module_name)


#===============================================================================
# set_workspace_template : 在manager的系统中设置workspace默认模板
#===============================================================================
@login_required
def set_workspace_template(request):
	workspace_id = request.GET['workspace_id']
	project_id = request.GET['project_id']
	Workspace.objects.filter(id=workspace_id).update(template_project_id=project_id)

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#===============================================================================
# edit_template : 显示模板列表页面
#===============================================================================
@login_required
def edit_template(request):
	workspace = Workspace.objects.get(owner=request.user, inner_name='home_page')

	template_type = request.GET.get('type', 'common')
	project_type = None
	enable_add_action = False
	if 'common' == template_type:
		project_type = 'jqm'
		enable_add_action = False
	elif 'custom' == template_type:
		project_type = 'weapp'
		enable_add_action = True

	projects = []
	for project in Project.objects.filter(workspace=workspace, type=project_type):
		if project_type == 'jqm':
			project.template_pic_url = ('/webapp_static/%s/template.jpg' % project.inner_name)
		else:
			project.template_pic_url = '/standard_static/upload/custom_template/%d_%d.png' % (request.user.id, project.id)

		projects.append(project)

	c = RequestContext(request, {
		'first_nav_name': WEBAPP_TEMPLATE_FIRST_NAV_NAME,
		'second_navs': WEBAPP_TEMPLATE_SECOND_NAVS,
		'second_nav_name': '%s_template' % template_type,
		'enable_add_action': enable_add_action,
		'workspace': workspace,
		'projects': projects
	})
	return render_to_response('webapp/templates.html', c)