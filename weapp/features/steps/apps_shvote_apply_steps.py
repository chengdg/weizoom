#!/usr/bin/env python
# -*- coding: utf-8 -*-
from features.steps.apps_shvote_index_steps import get_dynamic_data

__author__ = 'mark24'

from behave import *
from test import bdd_util
from collections import OrderedDict

from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
import termite.pagestore as pagestore_manager
from apps.customerized_apps.shvote.models import Shvote, ShvoteParticipance, ShvoteControl
from weixin.message.material import models as material_models
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json
import re

import time
from django.core.management.base import BaseCommand, CommandError
from utils.cache_util import SET_CACHE
from modules.member.models import Member
import apps_step_utils as apps_util


def __date2time(date_str):
	"""
	字符串 今天/明天……
	转化为字符串 "%Y-%m-%d %H:%M"
	"""
	cr_date = date_str
	p_date = bdd_util.get_date_str(cr_date)
	p_time = "{} 00:00".format(bdd_util.get_date_str(cr_date))
	return p_time

def __status2name(status_num):
	"""
	微助力：状态值 转 文字
	"""
	status2name_dic = {-1:u"全部",0:u"待审核",1:u"审核通过"}
	return status2name_dic[status_num]

def __name2status(name):
	"""
	微助力： 文字 转 状态值
	"""
	if name:
		name2status_dic = {u"全部":-1,u"待审核":0,u"审核通过":1}
		return name2status_dic[name]
	else:
		return -1

def __get_actions(status):
	"""
	根据输入微助力状态
	返回对于操作列表
	"""
	actions_list = [u"查看","删除"]
	if status == u"待审核":
		actions_list = ["审核通过"]+actions_list
	elif status=="审核通过":
		pass
	return actions_list


def __get_into_shvote_pages(context,webapp_owner_id,shvote_id,openid):
	#进入高级微信投票活动页面
	url = '/m/apps/shvote/m_shvote/?webapp_owner_id=%s&id=%s&opid=%s' % (webapp_owner_id, shvote_id,openid)
	url = bdd_util.nginx(url)
	context.link_url = url
	response = context.client.get(url)
	if response.status_code == 302:
		print('[info] redirect by change fmt in shared_url')
		redirect_url = bdd_util.nginx(response['Location'])
		context.last_url = redirect_url
		response = context.client.get(bdd_util.nginx(redirect_url))
		if response.status_code == 302:
			print('[info] redirect by change fmt in shared_url')
			redirect_url = bdd_util.nginx(response['Location'])
			context.last_url = redirect_url
			response = context.client.get(bdd_util.nginx(redirect_url))
		else:
			print('[info] not redirect')
	else:
		print('[info] not redirect')
	return response


def __get_into_shvote_signup_pages(context):
	#进入高级微信投票-- 报名，填写个人资料页面
	webapp_owner_id = context.webapp_owner_id
	shvote_id = context.shvote_id
	url = '/m/apps/shvote/shvote_participance/?webapp_owner_id=%s&id=%s&opid=%s' % (webapp_owner_id, shvote_id,context.openid)
	#模拟获取填写资料页面
	apps_util.get_response(context, url)

	text = json.loads(context.text)

	termite_post_args = {
		'webapp_owner_id':webapp_owner_id,
		'belong_to':shvote_id,
		'icon': text.get('icon'),
		'name': text.get('name',''),
		'group':text.get('group',""),
		'serial_number': text.get('serial_number'),
		'details': text.get('details',''),
		'pics': json.dumps(text.get('pics'))
	}
	return apps_util.get_response(context, {
		"app": "m/apps/shvote",
		"resource": "shvote_participance",
		"type": "api",
		"method": "put",
		"args": termite_post_args
	})

def __Search_ShVoteParticipance(context,search_dic):
	"""
	搜索高级投票报名详情
	输入搜索字典
	返回数据列表
	"""
	design_mode = 0
	count_per_page = 10
	version = 1
	page = 1
	enable_paginate = 1
	openid = context.openid

	participant_name = unicode(search_dic["name"])
	serial_number = search_dic["serial_number"]
	participant_status = __name2status(search_dic["status"])
	shvote_id = str(context.shvote_id)
	search_url = "/apps/shvote/api/shvote_registrators/?&id={}&design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}&fmd={}&participant_name={}&serial_number={}&participant_status={}".format(
			shvote_id,
			design_mode,
			version,
			count_per_page,
			page,
			enable_paginate,
			openid,
			participant_name,
			serial_number,
			participant_status)

	search_response = context.client.get(search_url)
	bdd_util.assert_api_call_success(search_response)
	return search_response

# @When(u'{webapp_user_name}点击图文"{title}"进入高级微信投票活动页面')
# def step_impl(context, webapp_user_name, title):
# 	webapp_owner_id = str(context.webapp_owner_id)
# 	user = User.objects.get(id=webapp_owner_id)
# 	openid = "%s_%s" % (webapp_user_name, user.username)
#
# 	shvote = Shvote.objects.get(owner_id=context.webapp_owner_id)
# 	shvote_id = str(shvote.id)
# 	response = __get_into_shvote_pages(context,webapp_owner_id,shvote_id,openid)#resp.context=> data ; resp.content => Http Text
# 	print ">>>> Get Into Shvote Mobile Page [start]>>>>"
# 	print "webapp_owner_id:"+webapp_owner_id
# 	print "shvote_id:"+shvote_id
# 	print "Response[record_id]:"+response.context['record_id']
# 	print "<<<< Get Into Shvote Mobile Page [ end ] <<<<"
# 	record_id = str(response.context['record_id'])
# 	context.record_id = record_id
# 	context.webapp_owner_id = webapp_owner_id
# 	context.shvote_id = shvote_id
# 	context.openid = openid

@When(u'{webapp_user_name}参加高级投票报名活动')
def step_impl(context, webapp_user_name):
	webapp_owner_id = str(context.webapp_owner_id)
	shvote_id = context.shvote_id
	print (">>>> Shvote Mobile Page --- Sign Up ----[start]>>>>")
	print ("webapp_owner_id:"+webapp_owner_id)
	print ("shvote_id:"+shvote_id)
	print ("<<<< Shvote Mobile Page --- Sign Up ----[ end ] <<<<")

	response = __get_into_shvote_signup_pages(context)#resp.context=> data ; resp.content => Http Text
	# apps_util.debug_print(response.content)

#后端的
@Then(u'{webapp_user_name}能获得报名详情列表')
def step_impl(context,webapp_user_name):
	design_mode = 0
	count_per_page = 10
	version = 1
	page = 1
	enable_paginate = 1
	openid = context.openid
	webapp_owner_id = context.webapp_owner_id
	shvote_id = str(context.shvote_id)

	actual_list = []
	raw_expected = json.loads(context.text)
	expected = []
	for expect in raw_expected:
		icon = expect['headImg']
		name = expect['player']
		count = expect['votes']
		serial_number = expect['number']
		status = expect['status']
		actions = expect['actions']
		created_at = __date2time(expect['start_date'])
		tmp = {
			"icon":icon,
			"name":name,
			"count":count,
			"created_at":created_at,
			"serial_number":serial_number,
			"status":status,
			"actions":actions
		}
		expected.append(tmp)

	#搜索查看结果
	if hasattr(context,"search_array"):
		pass
		rec_search_list = context.search_array
		for item in rec_search_list:
			tmp = {
				"id":item['id'],
				"icon":item['icon'],
				"name":item['name'],
				"count":item['count'],
				"serial_number":item['serial_number'],
				"status":__status2name(item['status']),
				"created_at":"%s 00:00"%(item['created_at'].replace('/','-').split(' ')[0]),
			}
			tmp["actions"] = __get_actions(__status2name(item['status']))
			actual_list.append(tmp)
		print("expected: {}".format(expected))
		print("actual_data: {}".format(actual_list))
		bdd_util.assert_list(expected,actual_list)#assert_list(小集合，大集合)
	#其他查看结果
	else:
		# #分页情况，更新分页参数
		# if hasattr(context,"paging"):
		#	 pass
		#	 paging_dic = context.paging
		#	 count_per_page = paging_dic['count_per_page']
		#	 page = paging_dic['page_num']

		#针对后端的 request.GET['id']在url里把id当做参数传过去，id为活动id
		url ="/apps/shvote/api/shvote_registrators/?&id={}&design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}&fmd={}".format(shvote_id,design_mode,version,count_per_page,page,enable_paginate,openid)
		response = context.client.get(url)
		items = json.loads(response.content)['data']['items']#[::-1]

		for item in items:
			tmp = {
				"icon":item['icon'],
				"name":item['name'],
				"count":item['count'],
				"serial_number":item['serial_number'],
				"status":__status2name(item['status']),
				"created_at":"%s 00:00"%(item['created_at'].replace('/','-').split(' ')[0]),
			}
			tmp["actions"] = __get_actions(__status2name(item['status']))
			actual_list.append(tmp)
		print("expected: {}".format(expected))
		print("actual_data: {}".format(actual_list))
		bdd_util.assert_list(expected,actual_list)

@when(u"{user}设置高级投票报名详情查询条件")
def step_impl(context,user):
	expect = json.loads(context.text)
	search_dic = {
		"name": expect.get("name",""),
		"serial_number": expect.get("serial_number",""),
		"status": expect.get("status",u"全部")
	}
	search_response = __Search_ShVoteParticipance(context,search_dic)
	search_array = json.loads(search_response.content)['data']['items']
	context.search_array = search_array