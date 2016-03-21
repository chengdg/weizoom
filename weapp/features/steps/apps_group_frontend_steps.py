#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'kuki'

from behave import *
from test import bdd_util
from collections import OrderedDict

from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
import termite.pagestore as pagestore_manager
from apps.customerized_apps.group.models import Group, GroupRelations, GroupDetail
from mall.models import *
from utils.string_util import byte_to_hex
import json
import re

import time
from django.core.management.base import BaseCommand, CommandError
from utils.cache_util import SET_CACHE
from modules.member.models import Member


def __get_group_rule_id(group_rule_name):
	return Group.objects.get(name=group_rule_name).id

def __get_product_idByname(product_name):
	return Product.objects.get(name=product_name).id

def __get_group_relation_id(activity_id,page_owner_member_id):
	try:
		return str(GroupRelations.objects.get(belong_to=str(activity_id), member_id=str(page_owner_member_id)).id)
	except:
		return None
"""
m_group.html页面的请求
"""
def __get_into_group_pages(context,webapp_owner_id,activity_id,openid,fid):
	#进入团购活动页面
	url = '/m/apps/group/m_group/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s&fid=%s' % (webapp_owner_id, activity_id, context.member.token, openid,fid)
	url = bdd_util.nginx(url)
	context.link_url = url
	response = context.client.get(url)
	while response.status_code == 302:
		print('[info] redirect by change fmt in shared_url')
		redirect_url = bdd_util.nginx(response['Location'])
		context.last_url = redirect_url
		response = context.client.get(bdd_util.nginx(redirect_url))
	return response

def __get_group_informations(context,webapp_owner_id,activity_id,openid,fid):
	group_relation_id = __get_group_relation_id(activity_id,fid)
	if group_relation_id:
		url = '/m/apps/group/api/m_group/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s&fid=%s&group_relation_id=%s' % (webapp_owner_id, activity_id, context.member.token, openid, fid,group_relation_id)
	else:
		url = '/m/apps/group/api/m_group/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s&fid=%s' % (webapp_owner_id, activity_id, context.member.token, openid, fid)
	url = bdd_util.nginx(url)
	response = context.client.get(url)
	while response.status_code == 302:
		print('[info] redirect by change fmt in shared_url')
		redirect_url = bdd_util.nginx(response['Location'])
		context.last_url = redirect_url
		response = context.client.get(bdd_util.nginx(redirect_url))
	if response.status_code == 200:
		return response
	else:
		print('[info] redirect error,response.status_code :')
		print(response.status_code)

def __open_group(context,activity_id,fid,group_type,group_days,group_price,product_id,openid):
	# 开团操作
	webapp_owner_id = context.webapp_owner_id
	params = {
		'webapp_owner_id': webapp_owner_id,
		'group_record_id': activity_id,
		'fid': fid,
		'group_type': group_type,
		'group_days': group_days,
		'group_price': group_price,
		'product_id': product_id
	}
	response = context.client.post('/m/apps/group/api/group_participance/?_method=post', params)
	while response.status_code == 302:
		print('[info] redirect by change fmt in shared_url')
		redirect_url = bdd_util.nginx(response['Location'])
		context.last_url = redirect_url
		response = context.client.get(bdd_util.nginx(redirect_url))

	if json.loads(response.content)['code'] == 500:
		context.err_msg = json.loads(response.content)['errMsg']
		return response
	else:
		group_id = json.loads(response.content)['data']['relation_belong_to']
		context.put_order_info = {
			'woid': webapp_owner_id,
			'group_id': group_id,
			'product_ids': product_id,
			'activity_id': str(activity_id)
		}
		return response

def __join_group(context,activity_id,fid,product_id,group_relation_id,openid):
	# 参团操作
	webapp_owner_id = context.webapp_owner_id
	params = {
		'webapp_owner_id': webapp_owner_id,
		'group_relation_id': group_relation_id,
		'fid': fid
	}
	response = context.client.post('/m/apps/group/api/group_participance/?_method=put', params)
	while response.status_code == 302:
		print('[info] redirect by change fmt in shared_url')
		redirect_url = bdd_util.nginx(response['Location'])
		context.last_url = redirect_url
		response = context.client.get(bdd_util.nginx(redirect_url))

	if json.loads(response.content)['code'] == 500:
		context.err_msg = json.loads(response.content)['errMsg']
		return response
	else:
		context.put_order_info = {
			'woid': webapp_owner_id,
			'group_id': group_relation_id,
			'product_ids': product_id,
			'activity_id': activity_id
		}
		return response

"""
m_group_list.html页面的请求
"""
def __get_into_group_list_pages(context,webapp_owner_id,openid):
	#进入全部团购活动列表页面
	url = '/m/apps/group/m_group_list/?webapp_owner_id=%s&fmt=%s&opid=%s' % (webapp_owner_id, context.member.token, openid)
	url = bdd_util.nginx(url)
	response = context.client.get(url)
	while response.status_code == 302:
		print('[info] redirect by change fmt in shared_url')
		redirect_url = bdd_util.nginx(response['Location'])
		context.last_url = redirect_url
		response = context.client.get(bdd_util.nginx(redirect_url))
	return response

def __api_get_group_list(context,webapp_owner_id,belong_to):
	#所有已开团购
	url = '/m/apps/group/api/m_group_list/?webapp_owner_id=%s&belong_to=%s' % (webapp_owner_id, belong_to)
	response = context.client.get(url)
	while response.status_code == 302:
		print('[info] redirect by change fmt in shared_url')
		redirect_url = bdd_util.nginx(response['Location'])
		context.last_url = redirect_url
		response = context.client.get(bdd_util.nginx(redirect_url))
	return response.content

@then(u'{webapp_user_name}能获得{webapp_owner_name}在"{group_record_name}"下的团购活动页面')
def step_tmpl(context, webapp_user_name, webapp_owner_name, group_record_name):
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	activity_id = __get_group_rule_id(group_record_name)
	webapp_owner_id = context.webapp_owner_id
	fid = context.page_owner_member_id
	response = __get_into_group_pages(context,webapp_owner_id,activity_id,openid,fid)
	group_name = response.context['page_title']
	context.data_response = __get_group_informations(context,webapp_owner_id,activity_id,openid,fid).content
	member_info = json.loads(context.data_response)['data']['member_info']
	helpers_info = json.loads(context.data_response)['data']['helpers_info']
	#构造实际数据
	actual = []
	actual.append({
		"group_name": group_name,
		"group_leader": member_info['page_owner_name'],
		"group_dict":[{
			"group_type": member_info['group_type'],
			"group_price": member_info['product_group_price'],
			"offered":[{
				"number": member_info['grouped_number'],
				"member":[h['username'] for h in helpers_info]
				}]
		}]
	})
	print("actual_data: {}".format(actual))
	expected = json.loads(context.text)
	print("expected: {}".format(expected))
	bdd_util.assert_list(expected, actual)

@When(u'{webapp_user_name}参加{webapp_owner_name}的团购活动"{group_record_name}"进行开团')
def step_tmpl(context, webapp_user_name, webapp_owner_name,group_record_name):
	webapp_owner_id = context.webapp_owner_id
	activity_id = __get_group_rule_id(group_record_name)
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	fid = Member.objects.get(username_hexstr=byte_to_hex(webapp_user_name)).id
	response = __get_into_group_pages(context,webapp_owner_id,activity_id,openid,fid)
	context.data_response = __get_group_informations(context,webapp_owner_id,activity_id,openid,fid).content
	context.page_owner_member_id = json.loads(context.data_response)['data']['member_info']['page_owner_member_id']
	fid = context.page_owner_member_id
	data = json.loads(context.text)
	group_type= data['group_dict']['group_type']
	group_days= data['group_dict']['group_days']
	group_price= data['group_dict']['group_price']
	product_id = __get_product_idByname(data['products']['name'])
	__open_group(context,activity_id,fid,group_type,group_days,group_price,product_id,openid)

@When(u'{webapp_user_name}参加{group_owner_name}的团购活动"{group_record_name}"')
def step_tmpl(context, webapp_user_name,group_owner_name, group_record_name):
	webapp_owner_id = context.webapp_owner_id
	activity_id = __get_group_rule_id(group_record_name)
	user = User.objects.get(id=webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	fid = context.page_owner_member_id
	response = __get_into_group_pages(context,webapp_owner_id,activity_id,openid,fid)
	product_id = response.context['product_id']
	page_owner_member_id = context.page_owner_member_id
	group_relation_id = __get_group_relation_id(activity_id,page_owner_member_id)
	__join_group(context,activity_id,fid,product_id,group_relation_id,openid)

@When(u'{webapp_user_name}把{webapp_owner_name}的团购活动"{group_record_name}"的链接分享到朋友圈')
def step_impl(context, webapp_user_name, webapp_owner_name,group_record_name):
	context.shared_url = context.link_url
	print('context.shared_url:',context.shared_url)

@then(u"{webapp_user_name}能获得{webapp_owner_name}的团购活动列表")
def step_tmpl(context, webapp_user_name, webapp_owner_name):
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	webapp_owner_id = context.webapp_owner_id
	response = __get_into_group_list_pages(context,webapp_owner_id,openid)
	all_groups_can_open = response.context['all_groups_can_open']
	print('all_groups_can_open')
	print(all_groups_can_open)
	# 构造实际数据
	actual = []
	for group in all_groups_can_open:
		actual.append({
			"group_name": group['name'],
			"group_dict": group['all_group_dict']
		})
	print("actual_data: {}".format(actual))
	expected = json.loads(context.text)
	print("expected: {}".format(expected))
	bdd_util.assert_list(expected, actual)

@then(u'{webapp_user_name}能获得"{group_record_name}"的已开团活动列表')
def step_tmpl(context, webapp_user_name,group_record_name):
	webapp_owner_id = context.webapp_owner_id
	belong_to = __get_group_rule_id(group_record_name)
	response = json.loads(__api_get_group_list(context,webapp_owner_id,belong_to))
	all_groups_can_join = []
	if response['code'] == 200:
		all_groups_can_join = response['data']['all_groups_can_join']
	elif response['code'] == 500:
		all_groups_can_join = []
	#构造实际数据
	actual = []
	for group in all_groups_can_join:
		actual.append({
			"group_name": group['group_name'],
			"group_leader": group['group_owner_name'],
			"product_name": group['product_name'],
			"participant_count": group['participant_count']
		})
	print("actual_data: {}".format(actual))
	expected = json.loads(context.text)
	print("expected: {}".format(expected))
	bdd_util.assert_list(expected, actual)

@then(u'{webapp_user_name}得到团购活动提示"{err_msg}"')
def step_tmpl(context, webapp_user_name, err_msg):
	expected = err_msg
	actual = context.err_msg
	context.tc.assertEquals(expected, actual)