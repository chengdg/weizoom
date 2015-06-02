# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
try:
	import Image
except:
	from PIL import Image

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth

from models import *
from termite.core.jsonresponse import create_response, JsonResponse
from termite.core import paginator
import pagerender
import viper_api_views
import pagestore as pagestore_manager
from webapp import views as webapp_views


FIRST_NAV_NAME = 'webapp'


#===============================================================================
# show_viper_production_page : 显示实际页面
#===============================================================================
def show_viper_production_page(request):
	pagestore = pagestore_manager.get_pagestore(request)

	project_id = request.GET['project_id']
	page_id = request.GET.get('page_id', None)
	page = pagestore.get_page(project_id, page_id)

	return HttpResponseRedirect('/workbench/viper/page/?project_id=%s&page_id=%s' % (page['project_id'], page['page_id']))


#===============================================================================
# show_viper_design_page : 显示设计页面
#===============================================================================
def show_viper_design_page(request):
	project_id = request.GET['project_id']
	page_id = request.GET.get('page_id', None)
	
	if not page_id:
		c = RequestContext(request, {
			'project_id': project_id
		})
	
		return render_to_response('workbench/wait_design_page.html', c)
	else:
		html = viper_api_views.create_page(request, return_html_snippet=True)
		c = RequestContext(request, {
			'project_id': project_id,
			'page_html_content': html
		})
		return render_to_response('workbench/viper_design_page.html', c)


#===============================================================================
# __get_webapp_navs : 生成webapp_navs
#===============================================================================
def __get_webapp_navs(request, project_id, pagestore):
	if request.user.username == 'manager':
		#manager模式
		project = Project.objects.get(id=project_id)
		pages = pagestore.get_pages(project_id=project_id)
		webapp_editor_nav = {
			'section': project.workspace.name,
			'navs': []
		}
		for page in pages:
			page_id = page['page_id']
			page_model = page['component']['model']
			if page_model['type'] == 'top_level_page':
				url = '/workbench/viper/page/?project_id=%s&page_id=%s' % (project_id, page_id)
				webapp_editor_nav['navs'].append({
					'name': page_id,
					'url': url,
					'title': page_model['navName']
				})

		second_navs = []
		second_navs.append(webapp_editor_nav)
		second_navs.append({
			'section': u'项目',
			'navs': [{
				'name': u'子项目管理',
				'url': '/webapp/projects/?workspace_id=%d' % project.workspace_id,
				'title': u'子项目管理'
			}, {
				'name': u'项目管理',
				'url': '/webapp/',
				'title': u'项目管理'
			}]
		})
	else:
		#user模式，返回user的所有webapp的navs
		second_navs = webapp_views.get_modules_page_second_navs(request)

	return second_navs


#===============================================================================
# __get_fields_to_be_save : 获得待存储的数据
#===============================================================================
def __get_fields_to_be_save(request):
	fields = request.POST.dict()
	new_fields = {}
	for field, value in fields.items():
		#处理swipeimage
		if field.startswith('swipeimage$'):
			image_urls = json.loads(value)
			images = []
			for index, image_url in enumerate(image_urls):
				images.append({'id':index+1, 'url':image_url})
			new_field = field[field.find('/')+1:]
			new_fields[new_field] = {
				'old_field': field,
				'value': json.dumps(images)
			}

		#处理plugin数据
		plugins = {}
		if field.startswith('plugin:'):
			plugin_name, plugin_field = field.split('/')
			plugins[plugin_name] = {plugin_field:value}
			del fields[field]
		fields.update(plugins)

		#处理select数据，构造raw data
		if 'json:' in value and '"type":"select"' in value:
			json_data = json.loads(value[5:])
			new_fields['raw_%s' % field] = {
				'old_field': 'no',
				'value': json_data['value']
			}

		#处理radio数据，构造raw data
		if 'json:' in value and '"type":"radio"' in value:
			json_data = json.loads(value[5:])
			new_fields['raw_%s' % field] = {
				'old_field': 'no',
				'value': json_data['value']
			}
	
	#处理component group数据
	group_name2value = {}
	for field, value in fields.items():
		if field.startswith('__viperCG:'):
			items = field.split(':')
			group_name = items[1]
			index = items[2]
			value = '{}:{}'.format(items[1], items[2])
			group_name2value.setdefault(group_name, dict()).update({value:index})
	fields.update(group_name2value)
	
	for new_field, value in new_fields.items():
		fields[new_field] = value['value']
		if value['old_field'] in fields:
			del fields[value['old_field']]

	return fields
_get_fields_to_be_save = __get_fields_to_be_save


#===============================================================================
# create_record : 创建记录
#===============================================================================
def create_record(request):
	#获取project
	project_id = request.GET['project_id']

	page_id = request.GET.get('page_id', None)
	
	pagestore = pagestore_manager.get_pagestore('mongo')
	if request.POST:
		page_id = request.POST.get('__page_id')
		record = __get_fields_to_be_save(request)
		__save_record_hook = getattr(request, '__save_record_hook', None)
		if __save_record_hook:
			__save_record_hook(request, record)
		pagestore.save_record(request.user.id, project_id, page_id, record)

		redirect_to_page_id = request.GET.get('submit_redirect_to', page_id)
		if not hasattr(request, 'is_from_app'):
			return HttpResponseRedirect('/workbench/viper/page/?project_id=%s&page_id=%s' % (project_id, redirect_to_page_id))
	else:
		if not hasattr(request, 'is_from_app'):
			return show_free_page(request)


#===============================================================================
# update_record : 更新记录
#===============================================================================
def update_record(request):
	project_id = request.GET['project_id']
	record_id = request.GET['record_id']
	
	pagestore = pagestore_manager.get_pagestore('mongo')
	if request.POST:
		page_id = request.POST.get('__page_id')
		record_id = request.POST.get('__record_id')

		record = __get_fields_to_be_save(request)
		__save_record_hook = getattr(request, '__save_record_hook', None)
		if __save_record_hook:
			__save_record_hook(request, record)
		pagestore.update_record(record_id, record, page_id)

		redirect_to_page_id = request.GET.get('submit_redirect_to', page_id)
		if not hasattr(request, 'is_from_app'):
			return HttpResponseRedirect('/workbench/viper/page/?project_id=%s&page_id=%s' % (project_id, redirect_to_page_id))
	else:
		request.should_get_record = True
		if not hasattr(request, 'is_from_app'):
			return show_free_page(request)


#===============================================================================
# delete_record : 删除记录
#===============================================================================
def delete_record(request):
	page_id = request.GET['page_id']
	record_id = request.GET['record_id']
	pagestore = pagestore_manager.get_pagestore('mongo')
	pagestore.remove_record(record_id, page_id)
	if not hasattr(request, 'is_from_app'):
		return HttpResponseRedirect(request.META['HTTP_REFERER'])


#===============================================================================
# list_records : 显示记录的列表页面
#===============================================================================
def list_records_bak(request):
	from workbench.templatetags import workbench_filter

	pagestore = pagestore_manager.get_pagestore(request)
	#获得project
	project_id = request.GET['project_id']
	project = Project.objects.get(id=project_id)
	#获得左侧导航
	webapp_editor_nav = __get_webapp_navs(request, project_id, pagestore)
	#获得page
	page_id = request.GET.get('page_id', None)
	if project.source_project_id == 0:
		page = pagestore.get_page(project_id, page_id)
	else:
		page = pagestore.get_page(str(project.source_project_id), page_id)
	
	page_model = page['component']['model']
	is_enable_paginate = (page_model['is_enable_paginate'] == 'yes')

	#获取page list页面的columns
	#TODO: 将columns的存储从json str变为json obj
	page['columns'] = []
	for column in json.loads(page_model['columns']):
		if column['is_checked']:
			if not column['name']:
				column['name'] = 'component_%d' % column['id']
			page['columns'].append(column)
	page['columns'].sort(lambda x,y: cmp(x['index'], y['index']))
	
	#填充filter
	'''
	page.filter_component = None
	cid2component = {}
	for sub_component in page.component['components']:
		cid2component[sub_component['cid']] = sub_component
	for column in page.columns:
		if 'checkbox_group' in column['type']:
			cid = column['id']
			sub_component = cid2component[cid]
			if sub_component['model']['is_filter_in_list_page'] == 'yes':
				page.filter_component = sub_component
	filters = None
	current_filter_name = request.GET.get('filter', 'all')
	if page.filter_component:
		filter_component = page.filter_component
		filter_page_id = filter_component['model']['datasource_page'].split('-')[1]
		filter_page_field = filter_component['model']['datasource_field']

		filters = [{'name':'all', 'text':u'全部'}]
		if current_filter_name == 'all':
			page.current_filter = filters[0]

		for filter_record in Record.objects.filter(page_id=filter_page_id):
			filter_record_model = json.loads(filter_record.json_content)
			filter_name = '%s$%s_%d' % (filter_page_field, filter_page_id, filter_record.id)
			filter = {
				'name': filter_name,
				'text': filter_record_model[filter_page_field]
			}
			filters.append(filter)
			if filter_name == current_filter_name:
				page.current_filter = filter
	'''
	current_filter_name = 'all'
	page['filters'] = []

	#获取record集合
	records = pagestore.get_records(project_id, page['page_id'])
	if not current_filter_name == 'all':
		filtered_records = []
		for record in records:
			if current_filter_name in record.json_content:
				filtered_records.append(record)
		records = filtered_records

	#分页
	pageinfo_json_str = None
	if is_enable_paginate:
		count_per_page = int(page_model['count_per_page'])
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, records = paginator.paginate(records, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		pageinfo_json_str = json.dumps(paginator.to_dict(pageinfo))
	
	#渲染页面
	c = RequestContext(request, {
		'project_id': project_id,
		'project': project,
		'page': page,
		'records': records,
		'second_navs': webapp_editor_nav,
		'first_nav_name': FIRST_NAV_NAME,
		'second_nav_name': page['page_id'],
		'pageinfo': pageinfo_json_str
	})
	return render_to_response('workbench/viper_records_page.html', c)


#===============================================================================
# show_free_page : 显示自由页面
#===============================================================================
def show_free_page(request):
	project_id = request.GET['project_id']
	page_id = request.GET['page_id']
	
	pagestore = pagestore_manager.get_pagestore(request)

	#获取左侧导航信息
	webapp_editor_nav = __get_webapp_navs(request, project_id, pagestore)

	#获取page对象
	project = Project.objects.get(id=project_id)
	if project.source_project_id == 0:
		page = pagestore.get_page(project_id, page_id)
	else:
		page = pagestore.get_page(str(project.source_project_id), page_id)
	#获取二级导航信息
	page_model = page['component']['model']
	page_type = page_model['type']
	if page_type == 'top_level_page':
		second_nav_name = page['page_id']
	else:
		second_nav_name = request.COOKIES.get('top_level_page_id', '')

	#获取html页面
	if hasattr(request, 'should_get_record') and request.should_get_record:
		html = viper_api_views.create_page(request, return_html_snippet=True, get_record=True)
	else:
		html = viper_api_views.create_page(request, return_html_snippet=True)

	jsons = []
	if 'record' in request.page:
		jsons.append({
			"name": "record",
			"content": json.dumps(request.page['record']['model'])
		})

	#渲染最终页面
	c = RequestContext(request, {
		'project_id': project_id,
		'jsons': jsons,
		'page_html_content': html,
		'second_navs': webapp_editor_nav,
		'first_nav_name': FIRST_NAV_NAME,
		'second_nav_name': second_nav_name
	})
	response = render_to_response('workbench/viper_record_page.html', c)

	#设置cookie，保持导航信息跟踪
	if page_type == 'top_level_page':
		response.set_cookie('top_level_page_id', page['page_id'], max_age=3600*24)
		response.set_cookie('top_level_page_nav_name', page_model['navName'].encode('utf8'), max_age=3600*24)
	else:
		pass

	return response