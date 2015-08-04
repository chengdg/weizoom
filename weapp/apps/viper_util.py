# -*- coding: utf-8 -*-

__author__ = 'robert'


from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.contrib import auth

from termite.workbench import viper_views
from termite.workbench import viper_api_views

import pagestore as pagestore_manager
from core import model_util as mysql_model_util

FIRST_NAV_NAME = 'apps'

def __update_page_id(request):
	if not hasattr(request, 'target_resource'):
		page_id = "apps:::"
	else:
		app_name = request.GET['real_app_name']
		module = request.GET['real_module']
		resource = request.target_resource
		page_id = "apps:{}:{}:{}".format(app_name, module, resource)
		
	if request.POST:
		query_dict = request.POST
	else:
		query_dict = request.GET
	query_dict._mutable = True
	query_dict.update({"page_id": page_id, "__page_id": page_id})
	query_dict._mutable = False


##############################################################################
# create_record: 调用viper的create_record函数
##############################################################################
def create_record(request, app_settings):
	request.is_from_app = True
	__update_page_id(request)
	if getattr(app_settings, 'STORE_ENGINE', '') == 'mysql':
		mysql_model_util.create_record(request)
	else:
		viper_views.create_record(request)


##############################################################################
# update_record: 调用viper的update_record函数
##############################################################################
def update_record(request, app_settings):
	request.is_from_app = True
	__update_page_id(request)
	if getattr(app_settings, 'STORE_ENGINE', '') == 'mysql':
		mysql_model_util.update_record(request)
	else:
		viper_views.update_record(request)


##############################################################################
# delete_record: 调用viper的delete_record函数
##############################################################################
def delete_record(request, app_settings):
	request.is_from_app = True
	__update_page_id(request)
	if getattr(app_settings, 'STORE_ENGINE', '') == 'mysql':
		mysql_model_util.delete_record(request)
	else:
		viper_views.delete_record(request)


##############################################################################
# get_records_by_query: 调用viper的get_records函数，处理带参数的get records的行为
##############################################################################
def get_records_by_query(request, app_settings):
	request.is_from_app = True
	__update_page_id(request)
	pageinfo, records = viper_api_views.get_records(request)
	return pageinfo, records


##############################################################################
# get_all_records: 获得所有的record数据
##############################################################################
def get_all_records(request, app_settings):
	__update_page_id(request)
	pagestore = pagestore_manager.get_pagestore('mongo')
	page_id = request.GET['page_id']
	if hasattr(request, 'webapp_owner_id'):
		#处理从webapp来的请求
		user_id = request.webapp_owner_id
	else:
		#处理从后台系统来的请求
		user_id = request.user.id
	total_count, records = pagestore.get_records(user_id, '', page_id, {})
	result = []
	for record in records:
		data = record['model']
		data['id'] = record['id']
		result.append(data)
	return result


##############################################################################
# get_record: 调用viper的get_record函数
##############################################################################
def get_record(request, app_settings):
	__update_page_id(request)
	pagestore = pagestore_manager.get_pagestore('mongo')
	record_id = request.GET['record_id']
	page_id = request.GET['page_id']
	if getattr(app_settings, 'STORE_ENGINE', '') == 'mysql':
		record = mysql_model_util.get_record(request)
	else:
		record = pagestore.get_record(record_id, page_id)
		record['model']['id'] = record['id']
		record = record['model']

	__get_record_hook = getattr(request, '__get_record_hook', None)
	if __get_record_hook:
		__get_record_hook(request, record)

	return record
