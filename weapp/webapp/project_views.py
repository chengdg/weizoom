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
import pagestore as pagestore_manager
import modules as raw_webapp_modules
from account.social_account.models import SocialAccount
from views import FIRST_NAV_NAME

#===============================================================================
# show_projects : 显示项目列表
#===============================================================================
@login_required
def show_projects(request):
	workspace_id = request.GET.get('workspace_id', 0)
	workspace = Workspace.objects.get(id=workspace_id)
	projects = Project.objects.filter(owner=request.user, workspace_id=workspace_id)

	#获得项目模块
	system_manager = User.objects.get(username='manager')
	modules = Workspace.objects.filter(owner=system_manager)

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': None,
		'workspace_id': workspace_id,
		'workspace': workspace,
		'projects': projects
	})
	return render_to_response('webapp/projects.html', c)


#===============================================================================
# copy_project : 复制项目
#===============================================================================
@login_required
def copy_project(request, project_id):
	source_project = Project.objects.get(id=project_id)

	#copy project
	project = Project.objects.create(
		owner=request.user, 
		name=source_project.name + ' COPY',
		type=source_project.type,
		workspace_id=source_project.workspace_id,
		datasource_project_id=source_project.datasource_project_id
	)
	__create_project_css(project)

	#copy pages
	source_pages = Page.objects.filter(project=source_project)
	for source_page in source_pages:
		page = Page.objects.create(
			owner = request.user,
			project = project,
			display_index = source_page.display_index,
			page_id = source_page.page_id,
			json_content = source_page.json_content
		)

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#===============================================================================
# delete_project : 删除项目
#===============================================================================
@login_required
def delete_project(request, project_id):
	#删除mongo中project所有的page
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')
	pagestore.remove_project_pages(str(project_id))

	#删除project本身
	Project.objects.filter(id=project_id).delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#===============================================================================
# show_workbench : 显示工作台
#===============================================================================
@login_required
def show_workbench(request, project_id):
	return HttpResponseRedirect('/termite/workbench/project/edit/%s/' % project_id)

