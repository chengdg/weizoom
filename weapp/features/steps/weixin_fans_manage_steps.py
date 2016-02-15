#coding:utf8
# weixin2粉丝管理相关的steps

import json
import time
from datetime import datetime, timedelta

from behave import *
from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client

from weixin2.models import FanCategory


@given(u'{user}添加粉丝')
def step_impl(context):
	assert False

@when(u'{user}创建分组')
def step_impl(context, user):
	"""
	创建分组

	response_json示例：
	~~~~~~~~~~~~{.c}
	{"errMsg": "", "code": 200, "data": {"category_id": 8}, "success": true, "innerErrMsg": ""}
	~~~~~~~~~~~~
	"""
	# 清除现有的粉丝分类
	FanCategory.objects.all().delete()
	client = context.client
	context.fan_categories = json.loads(context.text)
	for category in context.fan_categories:
		#print("category: {}".format(category))
		context.response = client.post('/new_weixin/api/fans_category/?_method=PUT', category)
		response_json = json.loads(context.response.content)
		response_data = response_json['data']
		if response_data.has_key('category_id'):
			context.category_id = response_data['category_id']

@when(u"{user}添加一个分组")
def step_impl(context, user):
	"""
	添加一个分组(与"创建分组"不同，此操作不清空数据库)

	response_json示例：
	~~~~~~~~~~~~{.c}
	{"errMsg": "", "code": 200, "data": {"category_id": 8}, "success": true, "innerErrMsg": ""}
	~~~~~~~~~~~~
	"""
	client = context.client
	category = json.loads(context.text)
	#print("category: {}".format(category))
	context.response = client.post('/new_weixin/api/fans_category/?_method=PUT', category)
	response_json = json.loads(context.response.content)
	response_data = response_json['data']
	if response_data.has_key('category_id'):
		context.category_id = response_data['category_id']


@then(u"{user}看到分组列表中有'{category_name}'")
def step_impl(context, user, category_name):
	"""
	category的数据格式：
	~~~~~~~~~~~~{.c}
		{
			"id": 0,
			"name": u"全部分组",
			"count": 100,
		}
	~~~~~~~~~~~~
	"""
	client = context.client
	response = client.get('/new_weixin/fanses/')
	categories = response.context['categories']
	names = dict()
	for category in categories:
		names[category.get('name')] = category
	context.tc.assertTrue(names.has_key(category_name))

@then(u"{user}能看到的分组名列表")
def step_impl(context, user):
	client = context.client
	# 期待的列表
	expected_list = json.loads(context.text)

	response = client.get('/new_weixin/fanses/')
	# 获取页面返回的分组列表
	categories = response.context['categories']
	real_list = []
	for category in categories:
		real_list.append({
			'category_name': category.get('name')
		})
	bdd_util.assert_list(expected_list, real_list)


@when(u"{user}修改刚添加的分组名为'{category_name}'")
def step_impl(context, user, category_name):
	client = context.client
	category_id = context.category_id
	param = {
		'category_id': category_id,
		'category_name': category_name
	}
	response = client.post('/new_weixin/api/fans_category/', param)

