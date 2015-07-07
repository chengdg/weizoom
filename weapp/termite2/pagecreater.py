# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil
import sys

from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import Template

from termite2 import pagerender
import pagestore as pagestore_manager
from webapp import models as webapp_models
from core.jsonresponse import create_response

########################################################################
# __get_display_info: 构造request的display_info
########################################################################
def __get_display_info(request):
	pagestore = pagestore_manager.get_pagestore('mongo')

	#获取project
	project_id = int(request.REQUEST.get('project_id', 0))
	if project_id != 0:
		project = webapp_models.Project.objects.get(id=project_id)
	else:
		workspace = webapp_models.Workspace.objects.get(owner=request.webapp_owner_id, inner_name='home_page')
		project = webapp_models.Project.objects.get(workspace=workspace, type='wepage', is_active=True)
		project_id = project.id

	if request.in_design_mode and request.POST:
		page_component = json.loads(request.POST['page'])
		page = pagestore.get_page(project_id, page_component['cid'])
		page['component'] = page_component
		page_id = page_component['cid']
	else:
		page_id = request.GET.get('page_id', 1)
		page = pagestore.get_page(project_id, page_id)

	if page_id != 'preview':
		try:
			#使用project中的site_title作为真正的site_title
			#因为在page列表页面直接更新page site_title时是不会更新mongo中page数据中的site_title的
			page['component']['model']['site_title'] = project.site_title
		except:
			pass

	display_info = {
		'project': project,
		'page_id': page_id,
		'page': page
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


def create_component(request):
	page = {}
	page_component = json.loads(request.POST['component'])
	page['component'] = page_component
	project = webapp_models.Project()
	project.id = 0
	project.type = 'wepage'
	html = pagerender.create_mobile_page_html_content(request, page, page['component'], project)

	response = create_response(200)
	response.data = html
	return response.get_response()
