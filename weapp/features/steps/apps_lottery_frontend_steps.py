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
from apps.customerized_apps.lottery.models import lottery, lotteryParticipance
from weixin.message.material import models as material_models
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json
import re

# def __get_power_me_rule_name(title):
# 	material_url = material_models.News.objects.get(title=title).url
# 	power_me_rule_name = material_url.split('-')[1]
# 	return power_me_rule_name

def __get_lottery_id(lottery_name):
	return lottery.objects.get(name=lottery_name).id

def __get_into_lottery_pages(context,webapp_owner_id,lottery_id,openid):
	#进入微助力活动页面
	url = '/m/apps/lottery/m_lottery/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s' % (webapp_owner_id, lottery_id, context.member.token, openid)
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

@when(u"{webapp_user_name}参加微信抽奖活动'{lottery_name}'")
def step_impl(context,webapp_user_name,lottery_name):
	lottery_id = __get_lottery_id(lottery_name)
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	# response = __get_into_lottery_pages(context,webapp_owner_id,lottery_id,openid)
	params = {
		'webapp_owner_id': webapp_owner_id,
		'id': lottery_id,
		'fmt':context.member.token,
		'opid':openid
	}
	response = context.client.post('/m/apps/lottery/api/lottery_prize/?_method=put', params)
	print('response!!!!!!')
	print(response)
	context.lottery_result = json.loads(response.content)

@then(u"{webapp_user_name}获得抽奖结果")
def step_impl(context,webapp_user_name):
	lottery_result = context.lottery_result['data']
	type2name = {
		'integral': u'积分',
		'coupon': u'优惠券',
		'entity': u'实物'
	}
	# 构造实际数据
	actual = []
	actual.append({
		"prize_grade": lottery_result['result'],
		"prize_type": type2name[lottery_result['prize_type']],
		"coupon": lottery_result['prize_name']
	})
	print("actual_data: {}".format(actual))
	expected = json.loads(context.text)
	print("expected: {}".format(expected))
	bdd_util.assert_list(expected, actual)

@then(u"{webapp_user_name}获得抽奖错误提示'{message}'")
def step_impl(context,webapp_user_name,message):
	actual = context.lottery_result['errMsg']
	context.tc.assertEquals(message, actual)