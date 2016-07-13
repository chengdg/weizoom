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
import apps_step_utils as app_utils
from weixin.message.material import models as material_models

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
			"ex_code": lottery_code,
			"id": lottery_id
		}
	})
	return response

def __get_into_exlottery_home_page(context):
	"""
	进入抽奖主页
	@param context:
	@return:
	"""
	return app_utils.get_response(context, {
		"app": "m/apps/exlottery",
		"resource": "m_exlottery_page",
		"method": "get",
		"args": {
			"webapp_owner_id": context.webapp_owner_id,
			"id": context.exlottery_id
		}
	})

# @then(u"{user}获得'{exlottery_name}'系统回复的消息")
# def step_impl(context, user, exlottery_name):
# 	answer = context.text.strip()
# 	result = context.qa_result["data"]
#
# 	if answer.find('<br />') != -1:
# 		answer_list =  answer.split('<br />')
# 		if result.find(answer_list[0]) != -1 and result.find(answer_list[1]) != -1:
# 			exlottery_url = result[result.find("href='") + 6 : result.find("'>")]
# 			exlottery_url = bdd_util.nginx(exlottery_url)
# 			context.exlottery_url = exlottery_url
# 		else:
# 			context.tc.assertEquals(True, False)
# 	else:
# 		if result.find(answer) != -1:
# 			pass
# 		else:
# 			context.tc.assertEquals(True, False)

@then(u"{webapp_user_name}获得专项抽奖结果")
def step_impl(context, webapp_user_name):
	try:
		#抽奖成功获得奖励
		expected = json.loads(context.text)
		lottery_result = context.lottery_result['data']

		type2name = {
			'integral': u'积分',
			'coupon': u'优惠券',
			'entity': u'实物',
			'no_prize': u'谢谢参与'
		}
		# 构造实际数据
		actual = {
			"prize_grade": lottery_result['result'],
			"prize_type": type2name[lottery_result['prize_type']],
			"prize_name": lottery_result['prize_name']
		}

		bdd_util.assert_dict(expected, actual)
	except:
		#抽奖失败获得错误提示
		expected = context.text.strip()
		errMsg = context.lottery_result['errMsg']
		if errMsg == u'该抽奖码已经被使用过~':
			errMsg = u'该抽奖码已使用'

		context.tc.assertEquals(expected, errMsg)

# @when(u"{webapp_user_name}点击'立即抽奖'进入'{lottery_name}'活动页面")
# def step_impl(context, webapp_user_name, lottery_name):
# 	exlottery_url = context.exlottery_url
#
# 	webapp_owner_id_index = exlottery_url.find('webapp_owner_id=')
# 	lottery_id_index = exlottery_url.find('&id=')
# 	code_index = exlottery_url.find('&ex_code=')
# 	webapp_owner_id = exlottery_url[webapp_owner_id_index + len('webapp_owner_id='):lottery_id_index]
# 	lottery_id = exlottery_url[lottery_id_index + len('&id='):code_index]
# 	code = exlottery_url[code_index + len('&ex_code='):]
#
# 	user = User.objects.get(id=webapp_owner_id)
# 	openid = "%s_%s" % (webapp_user_name, user.username)
# 	context.openid = openid
# 	__get_into_lottery_pages(context, webapp_owner_id, lottery_id, code)
#
# 	context.exlottery_detail = {
# 		'webapp_owner_id': webapp_owner_id,
# 		'id': lottery_id,
# 		'code': code
# 	}

@when(u"{webapp_user_name}把{user}的'{lottery_name}'活动链接分享到朋友圈")
def step_impl(context, webapp_user_name, user, lottery_name):
	url = "/m/apps/exlottery/m_exlottery/?webapp_owner_id={}&id={}&code={}".format(context.webapp_owner_id, context.exlottery_id, context.exlottery_code)
	context.exlottery_share_url = url

@when(u"{webapp_user_name_new}点击{webapp_user_name}分享的'{lottery_name}'活动链接参加专项抽奖活动")
def step_impl(context, webapp_user_name_new, webapp_user_name, lottery_name):
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name_new, user.username)
	context.openid = openid

	response = app_utils.get_response(context, {
		"app": "m/apps/exlottery",
		"resource": "exlottery_prize",
		"method": "put",
		"type": "api",
		"args": {
			'webapp_owner_id': context.webapp_owner_id,
			'id': context.exlottery_id,
			'code': context.exlottery_code
		}
	})
	context.errMsg = json.loads(response.content)['errMsg']

@when(u"{webapp_user_name}参加专项抽奖活动'{lottery_name}'")
def step_impl(context, webapp_user_name, lottery_name):
	context.exlottery_detail = {
		'webapp_owner_id': context.webapp_owner_id,
		'id': context.exlottery_id,
		'ex_code': context.exlottery_code
	}

	response = app_utils.get_response(context, {
		"app": "m/apps/exlottery",
		"resource": "exlottery_prize",
		"method": "put",
		"type": "api",
		"args": context.exlottery_detail
	})
	context.lottery_result = json.loads(response.content)

@When(u"{webapp_user_name}点击图文'{title}'进入专项抽奖活动页面")
def step_impl(context, webapp_user_name, title):
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	exlottery_name = material_models.News.objects.get(title=title).url
	exlottery_id = __get_exlottery_id(exlottery_name)

	context.exlottery_id = str(exlottery_id)
	context.openid = openid

	#获取抽奖首页
	__get_into_exlottery_home_page(context)

@When(u'{webapp_user_name}于"{date}"点击图文"{title}"进入专项抽奖活动页面')
def step_impl(context, webapp_user_name, date, title):
	context.execute_steps(u"when %s点击图文'%s'进入专项抽奖活动页面" % (webapp_user_name, title))

	date = bdd_util.get_date(date)
	exlottery_name = material_models.News.objects.get(title=title).url
	exlottery_id = __get_exlottery_id(exlottery_name)
	exlottery = Exlottery.objects.get(id=exlottery_id)

	end_time = exlottery.end_time
	if date > end_time:
		#修改为过期
		exlottery.update(set__status=2)
		exlottery.save()


@then(u"{webapp_user_name}在专项抽奖活动首页获得验证码'{verify_code_bdd}'")
def step_impl(context, webapp_user_name, verify_code_bdd):
	#先生成验证码
	app_utils.get_response(context, {
		"app": "m/apps/exlottery",
		"resource": "m_captcha",
		"method": "get",
		"type": "api",
		"args": {
			"webapp_owner_id": context.webapp_owner_id
		}
	})
	#人工修改验证码
	context.verify_code_for_bdd = verify_code_bdd

@when(u"{webapp_user_name}在专项抽奖活动首页中输入验证码'{verify_code}'")
def step_impl(context, webapp_user_name, verify_code):
	context.verify_code = verify_code

@when(u"{webapp_user_name}在专项抽奖活动首页中输入抽奖码'{exlottery_code}'")
def step_impl(context, webapp_user_name, exlottery_code):
	context.exlottery_code = exlottery_code

@when(u"{webapp_user_name}点击'立即抽奖'进入专项抽奖活动内容页")
def step_impl(context, webapp_user_name):
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	context.openid = openid

	response = app_utils.get_response(context, {
		"app": "m/apps/exlottery",
		"resource": "m_exlottery_page",
		"method": "get",
		"type": "api",
		"args": {
			"webapp_owner_id": context.webapp_owner_id,
			"id": context.exlottery_id,
			"excode": context.exlottery_code,
			"verify_code": context.verify_code,
			"verify_code_for_bdd": context.verify_code_for_bdd
		}
	})
	context.errMsg = json.loads(response.content)['errMsg']

@then(u"{webapp_user_name}获得页面提示的消息")
def step_impl(context, webapp_user_name):
	expected = context.text.strip()
	errMsg = context.errMsg
	if errMsg == u'该抽奖码已经被使用过~':
		errMsg = u'该抽奖码已使用'
	context.tc.assertEquals(expected, errMsg)

