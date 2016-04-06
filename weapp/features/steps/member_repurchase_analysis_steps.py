# -*- coding: utf-8 -*-
# __editor__='zhaolei'
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from django.contrib.auth.models import User

from mall.models import *
# from modules.member.models import *
from modules.member.models import MemberGrade, Member
from weixin.user import models as weixn_models
from account import models as account_models
from utils.string_util import byte_to_hex

@then(u'{user}获得默认筛选条件')
def step_impl(context, user):

	is_subscribed = json.loads(context.text)
	if is_subscribed == u'全部':
		context.is_subscribed ='all'

@then(u'{user}获得会员购买占比统计数据')
def step_impl(context, user):
	client = context.client
	if hasattr(context,'is_subscribed'):
		url = '/stats/api/buy_percent/?is_subscribed='+context.is_subscribed
	else:
		url = '/stats/api/buy_percent/?is_subscribed=all'
	response = client.get(url)
	content = json.loads(response.content)
	actual_real_list =content['data'][u'series'][0]['data']
	actual_list = []
	for actual_dict in actual_real_list:
		actual_list.append(actual_dict['name'])
	expected_data = json.loads(context.text)
	print bdd_util.assert_list(expected_data, actual_list)


@then(u'{user}获得复购会员分析统计数据')
def step_impl(context, user):

	client = context.client


	url = '/stats/api/repeat_buy_analysis/?is_subscribed='
	if hasattr(context,'is_subscribed'):
		url+= context.is_subscribed
	else:
		url+='all'
	if hasattr(context,'search_pay_list'):
		url += '&search_pay_list='+context.search_pay_list
	print "zl--------------------------------------------------------"
	response = client.get(url)
	content = json.loads(response.content)
	actual_real_list =content['data']['series'][0]['data']
	actual_list = []
	for actual_dict in actual_real_list:
		actual_list.append(actual_dict['name'])
	expected_data = json.loads(context.text)

	print bdd_util.assert_list(expected_data, actual_list)


@when(u'{user}设置筛选条件')
def step_impl(context, user):

	is_subscribed = json.loads(context.text)['member_status']
	if is_subscribed == u'已关注':
		context.is_subscribed ='1'
	elif is_subscribed == u'取消关注':
		context.is_subscribed ='0'

@when(u'{user}设置消费总额')
def step_impl(context, user):
	"""
		{
			"one_interval_mini":0,
			"one_interval_max":180,
			"two_interval_mini":190,
			"two_interval_max":700,
			"three_interval_mini":701,
			"three_interval_max":900
		}

	"""
	val = []
	for itemx,itemy in json.loads(context.text).items():
		val.append(itemy)
	val = sorted(val)
	val = [str(v) for v in val]
	context.search_pay_list =",".join(val)


@then(u'{user}获得用户分析统计数据')
def step_impl(context, user):
	client = context.client
	url = '/stats/api/user_analysis/?is_subscribed='
	if hasattr(context,'is_subscribed'):
		url+= context.is_subscribed
	else:
		url+='all'
	if hasattr(context,'pay_times'):
		url += '&pay_times='+context.pay_times
	if hasattr(context,'pay_money'):
		url += '&pay_money='+context.pay_money
	response = client.get(url)
	content = json.loads(response.content)

	expected_data = json.loads(context.text)['member_counts']
	bdd_util.assert_list([expected_data], [content['data']['fans_num']])

@when(u'{user}设置条件设置')
def step_impl(context, user):
	text = json.loads(context.text)
	context.pay_times = "{},{}".format(text['pay_times_start'],text['pay_times_end'])
	context.pay_money = "{},{}".format(text['pay_money_start'],text['pay_money_end'])