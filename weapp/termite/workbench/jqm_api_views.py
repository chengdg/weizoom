# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group
from django.contrib import auth
# from termite.core import stripper

from models import *
from account.models import UserProfile
from termite.core.jsonresponse import create_response
import pagerender
from termite import pagestore as pagestore_manager
from webapp.models import Workspace


########################################################################
# __get_display_info: 构造request的display_info
########################################################################
def __get_display_info(request):
	pagestore = pagestore_manager.get_pagestore('mongo')

	#获取project
	project_id = int(request.REQUEST.get('project_id', 0))
	if project_id == 0:
		#project信息缺失，使用当前选中的模板project
		workspace = Workspace.objects.get(owner_id=request.webapp_owner_id, inner_name='home_page')
		project = Project.objects.get(workspace=workspace, inner_name=workspace.template_name)
		project_id = str(project.id)
	else:
		project = Project.objects.get(id=project_id)

	if request.in_design_mode:
		#design模式下的逻辑
		if request.POST:
			page_component = json.loads(request.POST['page'])
			page = pagestore.get_page(project_id, page_component['cid'])
			page['component'] = page_component
			page_id = page_component['cid']
		else:
			page_id = request.GET.get('page_id', None)
			page = pagestore.get_page(project_id, page_id)

		display_info = {
			#'project_id': project_id,
			'project': project,
			'page_id': page_id,
			'page': page,
			'datasource_project_id': 0,
			'datasource_record_id': 0,
			'datasource_record': None
		}
	else:
		#非design模式，寻找datasource
		workspace = Workspace.objects.get(id=project.workspace_id)
		data_type, name_or_id = workspace.data_backend.split(':')

		if data_type == 'viper':
			#数据来自动态创建的viper工程，页面 = page + record
			#获得record
			datasource_record_id = request.GET.get('rid', None)
			if datasource_record_id:
				datasource_record = pagestore.get_record(datasource_record_id)
				datasource_project_id = datasource_record['project_id']
				datasource_page_id = datasource_record['page_id']
			else:
				datasource_record = None
				datasource_project_id = name_or_id
				datasource_page_id = 0
			
			#获得page
			if datasource_page_id == 0:
				page_id = request.GET.get('page_id', 1)
				page = pagestore.get_page(project_id, page_id)
			else:
				#url中没有提供page_id，根据datasource_page寻找渲染它的jqm page
				page = pagestore.find_page_by_datasource_page_id(project_id, datasource_page_id)
		elif data_type == 'module':
			#数据来自weapp提供的标准module，url形式为：./?module=shop&model=category&rid=3
			#获得record信息
			datasource_record_id = request.GET.get('rid', None)
			datasource_project_id = request.GET.get('module', None)
			datasource_page_id = request.GET.get('model', None)
			datasource_record = None

			#获得page
			if datasource_page_id:
				#根据datasource_page寻找渲染它的jqm page
				page = pagestore.find_page_by_datasource_page_id(project_id, datasource_page_id)				
			else:
				page_id = request.GET.get('page_id', 1)
				page = pagestore.get_page(project_id, page_id)
			

		display_info = {
			#'project_id': project_id,
			'project': project,
			'page_id': page['page_id'],
			'page': page,
			'datasource_project_id': datasource_project_id,
			'datasource_record_id': datasource_record_id,
			'datasource_record': datasource_record
		}

	request.display_info = display_info


########################################################################
# create_page: 创建design page
########################################################################
def __preprocess_page(request):
	__get_display_info(request)
	project = request.display_info['project']
	page = request.display_info['page']

	#填充page.component
	page_component = page['component']
	if not 'components' in page_component:
		page_component['components'] = []
	if not 'global_content_components' in page_component:
		page_component['global_content_components'] = []		
	#识别header, content components, footer
	page_component['headers'] = []
	page_component['footers'] = []
	if 'wepage' in page_component['type']:
		page_component['content'] = {'type': 'wepage.inner_content', 'uid':'', 'components':[], 'model': {'index': 1}}
	else:
		page_component['content'] = {'type': 'content', 'uid':'', 'components':[], 'model': {'index': 1}}
	for component in page_component['components']:
		if component['type'] == 'jqm.page_header':
			component['model']['index'] = 0
			page_component['headers'].append(component)
		elif component['type'] == 'jqm.page_footer':
			component['model']['index'] = 999999999
			page_component['footers'].append(component)
		else:
			page_component['content']['components'].append(component)

		if 'yes' == component['has_global_content']:
			page_component['global_content_components'].append(component)

	page_component['original_components'] = page_component['components']
	page_component['components'] = []
	page_component['components'].extend(page_component['headers'])
	page_component['components'].append(page_component['content'])
	page_component['components'].extend(page_component['footers'])

	return project, page


def create_page(request, return_html_snippet=False):
	project, page = __preprocess_page(request)
	#将page的class放入request，解决design page下无法为data-role=page设置class的问题
	#TODO: 优化解决方案
	request.page_model = page['component']['model']
	html = pagerender.create_mobile_page_html_content(request, page, page['component'], project)

	if return_html_snippet:
		return html
	else:
		response = create_response(200)
		response.data = html
		return response.get_response()
