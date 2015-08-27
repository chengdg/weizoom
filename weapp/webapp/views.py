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
import module_views


FIRST_NAV_NAME = 'webapp'
WEBAPP_TEMPLATE_FIRST_NAV_NAME = 'template'
CUSTOM_TEMPLATE_FIRST_NAV_NAME = 'custom_template'
SECOND_NAV_NAME = 'webapp'
MODULE_NAV_NAME = 'module'
STATISTICS_NAV_NAME = 'statistics'


WEBAPP_TEMPLATE_SECOND_NAVS = [{
	'section': u'行业模板',
	'navs': [{
		'name': 'common_template',
		'title': u'通用模板',
		'url': '/webapp/template/?type=common',
	}, {
		'name': 'custom_template',
		'title': u'定制模板',
		'url': '/webapp/template/?type=custom',
	}]	
}, {
	'section': u'全局导航',
	'navs': [{
		'name': 'webapp_global_navbar',
		'title': u'导航设置',
		'url': '/webapp/global_navbar/',
	}]	
}]


#===============================================================================
# show_statistics: 显示统计信息
#===============================================================================
@login_required
def show_statistics(request):
	return get_visit_statistics(request)


#===============================================================================
# get_visit_statistics : 获取访问统计
#===============================================================================
@login_required
def get_visit_statistics(request):
	#获得系统中的webapp module
	home_page_workspace = Workspace.objects.get(owner=request.user, inner_name='home_page')
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_nav_name': STATISTICS_NAV_NAME,
		'second_navs': get_modules_page_second_navs(request),
		'home_page_workspace': home_page_workspace
	})
	return render_to_response('webapp/visit_statistics.html', c)




get_modules_page_second_navs = module_views.get_modules_page_second_navs #向后兼容





PROJECT2APIS = {
	
}


#===============================================================================
# call_api : 调用api
#===============================================================================
def call_api(request):
	if request.in_design_mode:
		return {}
		
	#获得api name
	api_name = getattr(request, 't__api_name', None)
	if not api_name:
		path = request.path
		_, api_name = path.split('/api/')
		api_name = api_name[:-1]
	
	#获得apis_{project_id}.py
	project_id = request.GET.get('project_id', None)
	if not project_id:
		project_id = request.POST.get('project_id', None)

	if project_id and int(project_id) != 0:
		project = Project.objects.get(id=project_id)
	elif request.project:
		project = request.project
		project_id = project.id
	else:
		pass

	if project.source_project_id != 0:
		project_id = project.source_project_id
	apis = PROJECT2APIS.get(project_id, None)
	if not apis:
		apis = __import__('webapp.apis_%s' % project_id, {}, {}, ['*',])
		PROJECT2APIS[project_id] = apis

	#调用api函数
	items = api_name.split('/')
	items.reverse()
	api_function_name = '_'.join(items)
	print 'call api "%s" in %s' % (api_function_name, apis.__file__)
	return getattr(apis, api_function_name)(request)