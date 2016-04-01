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
	print "zl------------------------------------------------------"

@then(u'{user}获得会员购买占比统计数据')
def step_impl(context, user):
	client = context.client
	url = '/stats/api/buy_percent/?is_subscribed=all'
	print "zl--------------------------------------------------------"
	response = client.get(url)
	content = json.loads(response.content)
	print "zl---------------------------",content
	print "zl---------------------------",content['data'][u'series'][0]['data']
	actual_real_list =content['data'][u'series'][0]['data']
	actual_list = []
	for actual_dict in actual_real_list:
		actual_list.append(actual_dict['name'])
	expected_data = json.loads(context.text)
	print "zl-----------------",expected_data
	print "zl-----------------",actual_list
	print bdd_util.assert_list(expected_data, actual_list)


@then(u'{user}获得复购会员分析统计数据')
def step_impl(context, user):

	 # coupon_info = json.loads(context.text)
	# bdd_util.assert_list(expected_data, actual_data)
	pass

@when(u'{user}设置筛选条件')
def step_impl(context, member_a, user):

	is_subscribed = json.loads(context.text)
	if is_subscribed == u'已关注':
		context.is_subscribed ='1'
	elif is_subscribed == u'取消关注':
		context.is_subscribed ='0'

@when(u'{user}设置消费总额')
def step_impl(context, member_a, user):
	# if hasattr(context, 'client'):
	# 	context.client.logout()
	# context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	# user = context.client.user
	user_profile = user.get_profile()
	openid = '%s_%s' % (member_a, user)
	url = '/simulator/api/mp_user/unsubscribe/?version=2'
	data = {
		"timestamp": "1402211023857",
		"webapp_id": user_profile.webapp_id,
		"from_user": openid
	}
	response = client.post(url, data)
