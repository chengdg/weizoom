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
from apps.customerized_apps.scratch.models import Scratch, ScratchParticipance, ScratchControl ,ScratchRecord
from utils.string_util import byte_to_hex
import json
import re
import time

def __get_scratch_id(scratch_name):
	return Scratch.objects.get(name=scratch_name).id

def __get_into_scratch_pages(context,webapp_owner_id,scratch_id,openid):
	#进入微助力活动页面
	url = '/m/apps/scratch/m_scratch/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s' % (webapp_owner_id, scratch_id, context.member.token, openid)
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

@when(u"{webapp_user_name}参加刮刮卡活动'{scratch_name}'")
def step_impl(context,webapp_user_name,scratch_name):
	scratch_id = __get_scratch_id(scratch_name)
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	__get_into_scratch_pages(context,webapp_owner_id,scratch_id,openid)
	params = {
		'webapp_owner_id': webapp_owner_id,
		'id': scratch_id,
		'fmt':context.member.token,
		'opid':openid
	}
	response = context.client.post('/m/apps/scratch/api/scratch_prize/?_method=put', params)
	context.scratch_result = json.loads(response.content)
	time.sleep(2)

@when(u'{webapp_user_name}参加刮刮卡活动"{scratch_name}"于"{date}"')
def step_impl(context,webapp_user_name,scratch_name,date):
	context.execute_steps(u"when %s参加刮刮卡活动'%s'" % (webapp_user_name, scratch_name))
	scratch_id = __get_scratch_id(scratch_name)
	date = bdd_util.get_date(date)
	scratchparticipance = ScratchParticipance.objects.get(member_id=context.member.id,belong_to=str(scratch_id))
	scratchparticipance.update(set__scratch_date=date)
	scratchparticipance.save()
	scratchcontrol = ScratchControl.objects.filter(member_id=context.member.id,belong_to=str(scratch_id))
	if scratchcontrol:
		scratchcontrol.delete()
	scratchrecord = ScratchRecord.objects(member_id=context.member.id,belong_to=str(scratch_id)).first()
	scratchrecord.update(set__created_at=date)

@then(u"{webapp_user_name}获得刮刮卡结果")
def step_impl(context,webapp_user_name):
	scratch_result = context.scratch_result['data']
	type2name = {
		'integral': u'积分',
		'coupon': u'优惠券',
		'entity': u'实物',
		'no_prize': u'谢谢参与'
	}
	import logging
	logging.info('------------------123')
	logging.info("{}".format(scratch_result))
	# 构造实际数据
	actual = []
	actual.append({
		"prize_grade": scratch_result['result'],
		"prize_type": type2name[scratch_result['prize_type']],
		"prize_name": scratch_result['prize_name']
	})
	print("actual_data: {}".format(actual))
	expected = json.loads(context.text)
	print("expected: {}".format(expected))
	bdd_util.assert_list(expected, actual)

@then(u"{webapp_user_name}获得刮刮卡错误提示'{message}'")
def step_impl(context,webapp_user_name,message):
	actual = context.scratch_result['errMsg']
	context.tc.assertEquals(message, actual)

@When(u"{webapp_user_name}把{webapp_owner_name}的刮刮卡活动'{scratch_name}'的活动链接分享到朋友圈")
def step_impl(context, webapp_user_name, webapp_owner_name,scratch_name):
	scratch_id = __get_scratch_id(scratch_name)
	webapp_owner_id = context.webapp_owner_id
	url = '/m/apps/scratch/m_scratch/?webapp_owner_id=%s&id=%s' % (webapp_owner_id, scratch_id)
	url = bdd_util.nginx(url)
	context.shared_url = url
	print('context.shared_url:',context.shared_url)

@When(u"{webapp_user_name}点击{shared_webapp_user_name}分享的刮刮卡活动'{scratch_name}'的活动链接")
def step_impl(context, webapp_user_name, shared_webapp_user_name,scratch_name):
	scratch_id = __get_scratch_id(scratch_name)
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	__get_into_scratch_pages(context,webapp_owner_id,scratch_id,openid)

@When(u"微信用户批量参加{webapp_owner_name}的刮刮卡活动")
def step_impl(context, webapp_owner_name):
	for row in context.table:
		webapp_user_name = row['member_name']
		if webapp_user_name[0] == u'-':
			webapp_user_name = webapp_user_name[1:]
			#clear last member's info in cookie and context
			context.execute_steps(u"When 清空浏览器")
		else:
			context.execute_steps(u"When 清空浏览器")
			context.execute_steps(u"When %s访问%s的webapp" % (webapp_user_name, webapp_owner_name))
		data = {
			'name': row['name'],
			'webapp_user_name': webapp_user_name,
			'prize_grade': row['prize_grade'],
			'prize_name': row['prize_name'],
			'scratch_time': row['lottery_time'],
			'receive_status': row['receive_status']
		}
		context.execute_steps(u'when %s参加刮刮卡活动"%s"于"%s"' % (webapp_user_name, data['name'], data['scratch_time']))