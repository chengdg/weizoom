# -*- coding: utf-8 -*-
import os
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from tools.express import util as express_util
from core import dateutil
from termite2.models import TemplateCustomModule

@given(u"{user}未添加模块")
def step_impl(context, user):
	user = context.client.user
	_delete_all_custom_module(user)

@given(u"{user}已添加模块")
def step_impl(context, user):
	user = context.client.user

	context.custom_modules = json.loads(context.text)
	for custom_module in context.custom_modules:
		_save_custom_module(user, custom_module)

@when(u"{user}添加模块")
def step_impl(context, user):
	user = context.client.user

	custom_module = json.loads(context.text)
	_save_custom_module(user, custom_module)

def _delete_all_custom_module(user):
	TemplateCustomModule.objects.filter(owner=user).delete()

def _save_custom_module(user, custom_module):
	import time
	time.sleep(1)
	name = custom_module.get('name')
	TemplateCustomModule.objects.create(
		owner=user, 
		name=name
	)

def _get_custom_module_id_by_name(user, name):
	try:
		return TemplateCustomModule.objects.filter(owner=user, name=name)[0].id
	except:
		return 0

@then(u"{user}获取模块列表")
def step_impl(context, user):
	client = context.client
	count_per_page = client.object_count if hasattr(client, 'object_count') else 20
	cur_page =  client.cur_page if hasattr(client, 'cur_page') else 1
	search = client.search if hasattr(client, 'search') else ''

	url = u'/termite2/api/custom_modules/?design_mode=0&version=1&sort_attr=-updated_at&count_per_page={}&page={}&query={}'.format(count_per_page, cur_page, search)
	# print url
	response = client.get(url)
	custom_modules = json.loads(response.content)['data']['items']
	actual_data = []
	for custom_module in custom_modules:
		actual_data.append({
			"name": custom_module['name']
		})

	expected = json.loads(context.text)

	bdd_util.assert_list(expected, actual_data)


@when(u"{user}删除模块")
def step_impl(context, user):
	user = context.client.user
	client = context.client

	custom_module = json.loads(context.text)
	module_id = _get_custom_module_id_by_name(user, custom_module.get('name'))
	response = client.post('/termite2/api/custom_module/',{'id': module_id, '_method': 'delete'})


@when(u"{user}修改'{module_name}'的名称")
def step_impl(context, user, module_name):
	user = context.client.user
	client = context.client

	custom_module = json.loads(context.text)
	module_id = _get_custom_module_id_by_name(user, module_name)
	response = client.post('/termite2/api/custom_module_name/',{'id': module_id, 'name': custom_module.get('name')})


@when(u"{user}已设置分页条件")
def step_impl(context, user):
	user = context.client.user
	client = context.client

	page_count = json.loads(context.text).get("page_count")
	client.object_count = page_count


@then(u"{user}获取模块列表显示共'{page_count}'页")
def step_impl(context, user, page_count):
	user = context.client.user
	client = context.client
	# 每页显示多少条
	count_per_page = client.object_count
	response = client.get(u'/termite2/api/custom_modules/?design_mode=0&version=1&sort_attr=-updated_at&count_per_page={}&page=1'.format(count_per_page))
	count = json.loads(response.content).get('data')['pageinfo']['max_page']
	actual = {'page_count': count}
	expected = {'page_count': page_count}

	bdd_util.assert_dict(expected, actual)


@when(u"{user}浏览'第{page_info}页'")
def step_impl(context, user, page_info):
	user = context.client.user
	client = context.client

	client.cur_page = page_info
	# print u'第{}页，每页{}条'.format(client.cur_page, client.object_count)


@when(u"{user}浏览'{page_info}'")
def step_impl(context, user, page_info):
	user = context.client.user
	client = context.client

	if page_info == '上一页':
		client.cur_page = int(client.cur_page) - 1
	else:
		client.cur_page = int(client.cur_page) + 1

	# print u'第{}页，每页{}条'.format(client.cur_page, client.object_count)


@when(u"{user}按照模块名称搜索")
def step_impl(context, user):
	client = context.client

	client.search = json.loads(context.text).get("search")
	
