#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behave import *
from test import bdd_util
from collections import OrderedDict

from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
import termite.pagestore as pagestore_manager
from apps.customerized_apps.exlottery.models import Exlottery, ExlotteryParticipance, ExlotteryControl ,ExlottoryRecord
from utils.string_util import byte_to_hex
import json
import re
import time

def __get_exlottery_id(lottery_name):
	return Exlottery.objects.get(name=lottery_name).id

def __get_into_lottery_pages(context,webapp_owner_id,lottery_id,lottery_code):
	#进入专项抽奖活动页面
	response = app_utils.get_response(context, {
		"app": "m/apps/exlottery",
		"resource": "m_exlottery",
		"method": "get",
		"args": {
			"webapp_owner_id": webapp_owner_id,
			"code": lottery_code,
			"id": lottery_id
		}
	})
	return response

@then(u"{user}获得'{exlottery_name}'系统回复的消息")
def step_impl(context, user, exlottery_name):
	answer = context.text.strip()
	answer_list =  answer.split('<br />')
	result = context.qa_result["data"]

	if result.find(answer_list[0]) != -1 and result.find(answer_list[1]) != -1:
		pass
	else:
		context.tc.assertEquals(True, False)

import apps_step_utils as app_utils
@when(u"{webapp_user_name}用抽奖码{lottery_code}参加专项抽奖活动'{lottery_name}'")
def step_impl(context,webapp_user_name,lottery_code,lottery_name):
	lottery_id = __get_exlottery_id(lottery_name)
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	context.openid = openid
	__get_into_lottery_pages(context,webapp_owner_id,lottery_id,lottery_code)
	params = {
		'webapp_owner_id': webapp_owner_id,
		'id': str(lottery_id),
        'code': lottery_code
	}
	print "=============111================="
	print context.member.id
	print "=============111================="
	response = app_utils.get_response(context, {
        "app": "m/apps/exlottery",
        "resource": "exlottery_prize",
        "method": "put",
        "type": "api",
        "args": params
    })
	context.lottery_result = json.loads(response.content)

@then(u"{webapp_user_name}获得专项抽奖结果")
def step_impl(context, webapp_user_name):
	app_utils.debug_print(context.lottery_result)
	lottery_result = context.lottery_result['data']
	type2name = {
		'integral': u'积分',
		'coupon': u'优惠券',
		'entity': u'实物',
		'no_prize': u'谢谢参与'
	}
	# 构造实际数据
	actual = []
	actual.append({
		"prize_grade": lottery_result['result'],
		"prize_type": type2name[lottery_result['prize_type']],
		"prize_name": lottery_result['prize_name']
	})
	print("actual_data: {}".format(actual))
	expected = json.loads(context.text)
	print("expected: {}".format(expected))
	bdd_util.assert_list(expected, actual)
#
# @when(u'{webapp_user_name}用抽奖码{lottery_code}参加专项抽奖活动"{lottery_name}"于"{date}"')
# def step_impl(context,webapp_user_name,lottery_code,lottery_name,date):
#     lottery_id = __get_exlottery_id(lottery_name)
#     exlottery_participance = ExlotteryParticipance.objects(
#         member_id=context.member.id,
#         belong_to=str(lottery_id),
#         created_at=datetime.now(),
#         code=lottery_code,
#         status=0
#     )
# 	context.execute_steps(u"when %s用抽奖码'%s'参加专项抽奖活动'%s'" % (webapp_user_name, lottery_code, lottery_name))

	# date = bdd_util.get_date(date)
	# lotteryparticipance = ExlotteryParticipance.objects.get(member_id=context.member.id,belong_to=str(lottery_id))
	# lotteryparticipance.update(set__lottery_date=date)
	# lotteryparticipance.save()
	# lotterycontrol = lotteryControl.objects.filter(member_id=context.member.id,belong_to=str(lottery_id))
	# if lotterycontrol:
	# 	lotterycontrol.delete()
	# lottoryrecord = lottoryRecord.objects(member_id=context.member.id,belong_to=str(lottery_id)).first()
	# lottoryrecord.update(set__created_at=date)

# @then(u"{webapp_user_name}获得抽奖结果")
# def step_impl(context,webapp_user_name):
# 	lottery_result = context.lottery_result['data']
# 	type2name = {
# 		'integral': u'积分',
# 		'coupon': u'优惠券',
# 		'entity': u'实物',
# 		'no_prize': u'谢谢参与'
# 	}
# 	# 构造实际数据
# 	actual = []
# 	actual.append({
# 		"prize_grade": lottery_result['result'],
# 		"prize_type": type2name[lottery_result['prize_type']],
# 		"prize_name": lottery_result['prize_name']
# 	})
# 	print("actual_data: {}".format(actual))
# 	expected = json.loads(context.text)
# 	print("expected: {}".format(expected))
# 	bdd_util.assert_list(expected, actual)
#
# @then(u"{webapp_user_name}获得抽奖错误提示'{message}'")
# def step_impl(context,webapp_user_name,message):
# 	actual = context.lottery_result['errMsg']
# 	context.tc.assertEquals(message, actual)
#
# @When(u"{webapp_user_name}把{webapp_owner_name}的微信抽奖活动'{lottery_name}'的活动链接分享到朋友圈")
# def step_impl(context, webapp_user_name, webapp_owner_name,lottery_name):
# 	lottery_id = __get_exlottery_id(lottery_name)
# 	webapp_owner_id = context.webapp_owner_id
# 	url = '/m/apps/lottery/m_lottery/?webapp_owner_id=%s&id=%s' % (webapp_owner_id, lottery_id)
# 	url = bdd_util.nginx(url)
# 	context.shared_url = url
# 	print('context.shared_url:',context.shared_url)
#
# @When(u"{webapp_user_name}点击{shared_webapp_user_name}分享的微信抽奖活动'{lottery_name}'的活动链接")
# def step_impl(context, webapp_user_name, shared_webapp_user_name,lottery_name):
# 	lottery_id = __get_exlottery_id(lottery_name)
# 	webapp_owner_id = context.webapp_owner_id
# 	user = User.objects.get(id=context.webapp_owner_id)
# 	openid = "%s_%s" % (webapp_user_name, user.username)
# 	__get_into_lottery_pages(context,webapp_owner_id,lottery_id,openid)

# @When(u"微信用户批量参加{webapp_owner_name}的专项抽奖活动")
# def step_impl(context, webapp_owner_name):
# 	for row in context.table:
# 		webapp_user_name = row['member_name']
# 		if webapp_user_name[0] == u'-':
# 			webapp_user_name = webapp_user_name[1:]
# 			#clear last member's info in cookie and context
# 			context.execute_steps(u"When 清空浏览器")
# 		else:
# 			context.execute_steps(u"When 清空浏览器")
# 			context.execute_steps(u"When %s访问%s的webapp" % (webapp_user_name, webapp_owner_name))
# 		data = {
# 			'name': row['name'],
# 			'webapp_user_name': webapp_user_name,
# 			'prize_grade': row['prize_grade'],
# 			'prize_name': row['prize_name'],
# 			'lottery_time': row['lottery_time'],
# 			'receive_status': row['receive_status'],
#             'lottery_code': row['lottery_code']
# 		}
# 		context.execute_steps(u'when %s用抽奖码"%s"参加专项抽奖活动"%s"于"%s"' % (webapp_user_name, data['lottery_code'], data['name'], data['lottery_time']))