# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil
import pymongo

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group
from django.contrib import auth
from termite.core import stripper
from termite.core import paginator

from models import *
from account.models import UserProfile
from termite.core.jsonresponse import create_response
import pagerender
import pagestore as pagestore_manager

from termite.workbench.templatetags import workbench_filter


########################################################################
# __preprocess_page: 对page进行预处理
#					get_record: 是否需要获取record
########################################################################
def __preprocess_page(request, get_record):
	pagestore = pagestore_manager.get_pagestore('mongo')
	if hasattr(request, 'page'):
		#生成app时，request中会携带page信息
		project_id = request.GET['project_id']
		project = Project.objects.get(id=project_id)
		page = request.page
	else:
		if request.POST:
			project_id = request.POST['project_id']
			project = Project.objects.get(id=project_id)
			page_component = json.loads(request.POST['page'])
			page_id = page_component['cid']
			if project.source_project_id == 0:
				page = pagestore.get_page(project_id, page_id)
			else:
				page = pagestore.get_page(str(project.source_project_id), page_id)
			page['component'] = page_component
		else:
			project_id = request.GET['project_id']
			project = Project.objects.get(id=project_id)
			page_id = request.GET.get('page_id', None)
			if project.source_project_id == 0:
				page = pagestore.get_page(project_id, page_id)
			else:
				page = pagestore.get_page(str(project.source_project_id), page_id)
				
			if get_record:
				record_id = request.GET['record_id']
				page['record'] = pagestore.get_record(record_id)
		
	page_component = page['component']
	
	if not 'components' in page_component:
		page_component['components'] = []
	if not 'global_content_components' in page_component:
		page_component['global_content_components'] = []

	extra_context = {}
	for component in page_component['components']:
		if component['type'] == 'viper.simulator':
			extra_context['simulator'] = pagerender.create_mobile_page_html_content(request, page, component, project)
			extra_context['simulator_component'] = component

	request.extra_page_context = extra_context
	if 'simulator' in extra_context:
		page_component['components'].remove(extra_context['simulator_component'])
		if len(page_component['components']) == 0:
			page_component['components'].append({'type': 'empty', 'model':{'index':1}})

	target_page = page

	id2page = dict([(page['page_id'], page) for page in pagestore.get_pages(project_id)])
	workbench_filter.RENDER_CONTEXT['id2page'] = id2page

	return project, target_page


########################################################################
# create_page: 创建page
########################################################################
@login_required
def create_page(request, return_html_snippet=False, get_record=False):
	project, page = __preprocess_page(request, get_record)
	request.page = page
	html = pagerender.create_mobile_page_html_content(request, page, page['component'], project)

	if return_html_snippet:
		return html
	else:
		response = create_response(200)
		response.data = html
		return response.get_response()


########################################################################
# create_page_by_id: 基于page id创建page
########################################################################
@login_required
def create_page_by_id(request, return_html_snippet=False, get_record=False):
	project_id = request.GET['project_id']
	page_id = request.GET['page_id']
	
	pagestore = pagestore_manager.get_pagestore(request)
	project = Project.objects.get(id=project_id)
	page = pagestore.get_page(project_id, page_id)

	request.page = page
	html = pagerender.create_mobile_page_html_content(request, page, page['component'], project)

	if return_html_snippet:
		return html
	else:
		response = create_response(200)
		response.data = {
			'html': html,
			'title': page['component']['model']['navName']
		}
		return response.get_response()


########################################################################
# update_record_display_index: 修改record的排列顺序
########################################################################
@login_required
def update_record_display_index(request):
	pagestore = pagestore_manager.get_pagestore('mongo')
	page_id = request.POST.get('page_id', None)
	if not page_id and ('app' in request.POST):
		app = request.POST['app']
		module = request.POST['module']
		resource = request.POST['resource']
		page_id = 'apps:{}:{}:{}'.format(app, module, resource)
		
	src_record_id = request.POST.get('src_id', None)
	dst_record_id = request.POST.get('dst_id', None)
	if dst_record_id == u'0':
		#置顶操作
		order = request.POST['sort_attr']
		if order[0] == '-':
			order = 'desc'
		else:
			order = 'asc'
		pagestore.set_record_to_top(src_record_id, order, page_id)
	else:
		src_record = pagestore.get_record(src_record_id, page_id)
		dst_record = pagestore.get_record(dst_record_id, page_id)
		pagestore.update_record_display_index(src_record_id, dst_record['display_index'], page_id)
		pagestore.update_record_display_index(dst_record_id, src_record['display_index'], page_id)

	response = create_response(200)
	return response.get_response()


########################################################################
# get_records: 获得page对应的record集合
########################################################################
def __get_records_from_pagestore(request):
	from workbench.templatetags import workbench_filter

	pagestore = pagestore_manager.get_pagestore('mongo')
	#获得project
	project_id = request.GET['project_id']

	'''
	处理page_id
	'''
	is_query_from_app = False
	if (not 'page_id' in request.GET) and ('app' in request.GET):
		is_query_from_app = True
		app = request.GET['app']
		module = request.GET['module']
		resource = request.GET['resource']
		page_id = 'apps:{}:{}:{}'.format(app, module, resource)
	else:
		page_id = request.GET.get('page_id', None)
		if page_id and page_id[0] == 'p':
		 	page_id = page_id.split('-')[1]

	is_enable_paginate = (request.GET.get('enable_paginate', '0') == '1')

	'''
	获取record集合
	'''
	options = {}
	#处理sort_attr参数
	sort_attr = request.GET.get('sort_attr', 'display_index')
	if sort_attr[0] == '-':
		sort_attr = sort_attr[1:]
		direction = pymongo.DESCENDING
	else:
		direction = pymongo.ASCENDING		
	if sort_attr != 'display_index':
		sort_attr = 'model.{}'.format(sort_attr)
	options['sort'] = [(sort_attr, direction)]
	#获取filter参数
	filter_attr = request.GET.get('filter_attr', None)
	filter_value = request.GET.get('filter_value', None)
	if filter_value != u'-1' and filter_value != None:
		filter_attr = 'model.raw_{}'.format(filter_attr)
		options['filter'] = {filter_attr: filter_value}
	#获取search参数
	search = request.GET.get('query', None)
	if search:
		search_attr = 'model.{}'.format(request.GET.get('query_attr', ''))
		options['search'] = {search_attr: search}
	#获取pagination参数
	if is_enable_paginate:
		cur_page = int(request.GET.get('page', 1))
		count_per_page = int(request.GET.get('count_per_page', 20))
		options['pagination'] = {
			'cur_page': cur_page-1, 
			'count_per_page': count_per_page
		}

	if hasattr(request, 'webapp_owner_id'):
		#处理从webapp来的请求
		user_id = request.webapp_owner_id
	else:
		#处理从后台系统来的请求
		user_id = request.user.id
	total_count, records = pagestore.get_records(user_id, project_id, page_id, options)

	#分页
	pageinfo = None
	if is_enable_paginate:
		count_per_page = int(request.GET.get('count_per_page', '15'))
		cur_page = int(request.GET.get('page', '1'))
		#TODO: 当total_count很大时，temp_records的构造会带来性能问题
		temp_records = [1] * total_count #构造临时的数据，获取pageinfo信息
		pageinfo, _ = paginator.paginate(temp_records, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		
	items = []

	#解析target_fields
	target_fields = request.GET.get('target_fields', '')
	if len(target_fields) > 0:
		target_fields = target_fields.split(',')
	else:
		target_fields = ()
	buf = []
	for target_field in target_fields:
		field, field_type = target_field.split(':')
		buf.append({
			'field': field,
			'type': field_type
		})
	target_fields = buf
	
	#从records中抽取item
	submit_redirect_to_page_id = request.GET.get('submit_redirect_to', '')
	for record in records:
		model = record['model']
		meta_data = {"id": record['id']}
		result = []
		for target_field in target_fields:
			if target_field['type'] == 'link':
				if hasattr(request, 'is_from_app'):
					link = '#haha'
				elif is_query_from_app:
					_, app_name, page_module, page_name = page_id.split(':')
					link = '<a class="btn btn-mini" href="/apps/%s/?module=%s&resource=%s&action=update&project_id=%s&record_id=%s&submit_redirect_to=%s"><i class="icon icon-pencil"></i></a>' % (app_name, page_module, page_name, project_id, record['id'], submit_redirect_to_page_id)
				else:
					link = '<a class="btn btn-mini" href="/workbench/viper/record/update/?project_id=%s&page_id=%s&record_id=%s&submit_redirect_to=%s"><i class="icon icon-pencil"></i></a>' % (project_id, page_id, record['id'], submit_redirect_to_page_id)
				result.append(link)
				meta_data["has_operation_link"] = True
			else:
				field_data = model.get(target_field['field'], '')
				if 'json:' in field_data:
					#json格式存储的数据，比如select component存储的数据为
					#json:{"type":"select","text":"刮刮卡","value":"guaguaka"}这样的格式
					#需要解析出其中的value
					field_data = json.loads(field_data.split('json:')[1])['text']
				result.append(field_data)
		items.append({"meta_data":meta_data, "data":result})

	return pageinfo, items


########################################################################
# __get_records_from_mysql: 从msyql中获得page对应的record集合
########################################################################
def __get_records_from_mysql(request):
	from workbench.templatetags import workbench_filter

	models_path = 'apps.customerized_apps.'

	pagestore = pagestore_manager.get_pagestore('mongo')
	#获得project
	project_id = request.GET['project_id']

	'''
	处理page_id
	'''
	is_query_from_app = False
	if (not 'page_id' in request.GET) and ('app' in request.GET):
		is_query_from_app = True
		app = request.GET['app']
		module = request.GET['module']
		resource = request.GET['resource']
		page_id = 'apps:{}:{}:{}'.format(app, module, resource)
	else:
		page_id = request.GET.get('page_id', None)
		if page_id and page_id[0] == 'p':
		 	page_id = page_id.split('-')[1]

	is_enable_paginate = (request.GET.get('enable_paginate', '0') == '1')

	#TODO: 进行缓存
	mysql_models_module_path = 'apps.customerized_apps.{}.mysql_models'.format(request.GET['app'])
	mysql_models_module = __import__(mysql_models_module_path, {}, {}, ['*',])
	model_class_name = request.GET['model_class']
	model_class = getattr(mysql_models_module, model_class_name)

	'''
	获取record集合
	'''
	params = {"owner": request.user}
	#处理sort_attr参数
	sort_attr = request.GET.get('sort_attr', 'display_index')
	sort_attr = sort_attr.replace('display_index', 'id')
	#获取filter参数
	filter_attr = request.GET.get('filter_attr', None)
	filter_value = request.GET.get('filter_value', None)
	if filter_attr:
		params[filter_attr] = filter_value
	#获取search参数
	search = request.GET.get('query', None)
	if search:
		search_attr = 'model.{}'.format(request.GET.get('query_attr', ''))
		params['%s_contains' % search_attr] = search

	records = model_class.objects.filter(**params).order_by(sort_attr)

	#分页
	pageinfo = None
	if is_enable_paginate:
		count_per_page = int(request.GET.get('count_per_page', '15'))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, records = paginator.paginate(records, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		
	items = []

	#解析target_fields
	target_fields = request.GET.get('target_fields', '')
	if len(target_fields) > 0:
		target_fields = target_fields.split(',')
	else:
		target_fields = ()
	buf = []
	for target_field in target_fields:
		field, field_type = target_field.split(':')
		buf.append({
			'field': field,
			'type': field_type
		})
	target_fields = buf
	
	#从records中抽取item
	submit_redirect_to_page_id = request.GET.get('submit_redirect_to', '')
	for record in records:
		meta_data = {"id": record.id}
		result = []
		for target_field in target_fields:
			if target_field['type'] == 'link':
				if hasattr(request, 'is_from_app'):
					link = '#haha'
				elif is_query_from_app:
					_, app_name, page_module, page_name = page_id.split(':')
					link = '<a class="btn btn-mini" href="/apps/%s/?module=%s&resource=%s&action=update&project_id=%s&record_id=%s&submit_redirect_to=%s"><i class="icon icon-pencil"></i></a>' % (app_name, page_module, page_name, project_id, record.id, submit_redirect_to_page_id)
				else:
					link = '<a class="btn btn-mini" href="/workbench/viper/record/update/?project_id=%s&page_id=%s&record_id=%s&submit_redirect_to=%s"><i class="icon icon-pencil"></i></a>' % (project_id, page_id, record.id, submit_redirect_to_page_id)
				result.append(link)
				meta_data["has_operation_link"] = True
			else:
				field_data = getattr(record, target_field['field'], '')
				if type(field_data) == datetime:
					field_data = str(field_data)
				elif 'json:' in field_data:
					#json格式存储的数据，比如select component存储的数据为
					#json:{"type":"select","text":"刮刮卡","value":"guaguaka"}这样的格式
					#需要解析出其中的value
					field_data = json.loads(field_data.split('json:')[1])['text']
				result.append(field_data)
		items.append({"meta_data":meta_data, "data":result})

	return pageinfo, items


@login_required
def get_records(request):
	page = request.GET.get('page', '1')
	fields = request.GET.get('target_fields', '').split(',')
	store_engine = request.GET.get('store_engine', 'mongo')

	items = []
	pageinfo = None
	sort_attr = request.GET.get('sort_attr', '')
	if request.in_design_mode:
		for i in range(3):
			row = []
			for j in range(len(fields)):
				
				row.append(u'数据%d%d' % (i+1, j+1))
			items.append({'meta_data':{'id':1}, 'data':row})
	else:
		if store_engine == 'mysql':
			pageinfo, items = __get_records_from_mysql(request)
		else:
			pageinfo, items = __get_records_from_pagestore(request)

	if getattr(request, 'is_from_app', False):
		return pageinfo, items
	else:
		response = create_response(200)
		response.data = {
			'items': items,
			'sortAttr': sort_attr,
			'pageinfo': pageinfo.to_dict() if pageinfo else pageinfo
		}

		return response.get_response()