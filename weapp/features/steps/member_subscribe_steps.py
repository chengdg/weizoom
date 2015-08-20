# -*- coding: utf-8 -*-
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

def __get_user(user_name):
	return User.objects.get(username=user_name)

@given(u'{user}设置积分策略')
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	profile = UserProfile.objects.get(user_id=user.id)
	json_data = json.loads(context.text)

	integral_detail = {};
	integral = {}

	for key, value in  json_data[0].items():
		if key != 'member_integral_strategy_settings_detail':
			integral[key] = value

	if json_data[0].has_key('member_integral_strategy_settings_detail'):
		integral_detail = json_data[0]['member_integral_strategy_settings_detail'][0]

	if IntegralStrategySttings.objects.filter(webapp_id=profile.webapp_id).count() > 0:
		IntegralStrategySttings.objects.filter(webapp_id=profile.webapp_id).update(**integral)
	for key, value in integral_detail.items():
		if key == 'is_used':
			if value == u'否':
				integral_detail[key] = False
			else:
				integral_detail[key] = True
		else:
			integral_detail[key] = float(value[value.find('+')+1:value.find('*')])

	integral_detail['webapp_id'] = profile.webapp_id
	if IntegralStrategySttingsDetail.objects.filter(webapp_id=profile.webapp_id).count() > 0 and integral_detail:
		IntegralStrategySttingsDetail.objects.filter(webapp_id=profile.webapp_id).update(**integral_detail)
	elif integral_detail:
		pass

# def __get_user(user_name):
# 	return User.objects.get(username=user_name)

# @given(u'{user}设置积分策略')
# def step_impl(context, user):
# 	"""
# 	此方法要删除掉 换成 设定会员积分策略
# 	"""
# 	# if hasattr(context, 'client'):
# 	# 	context.client.logout()
# 	# context.client = bdd_util.login(user)
# 	# client = context.client
# 	# user = UserFactory(username=user)
# 	user = context.client.user
# 	profile = UserProfile.objects.get(user_id=user.id)
# 	json_data = json.loads(context.text)

# 	integral_detail = {};
# 	integral = {}

# 	for key, value in  json_data[0].items():
# 		if key != 'member_integral_strategy_settings_detail':
# 			integral[key] = value

# 	if json_data[0].has_key('member_integral_strategy_settings_detail'):
# 		integral_detail = json_data[0]['member_integral_strategy_settings_detail'][0]

# 	if IntegralStrategySttings.objects.filter(webapp_id=profile.webapp_id).count() > 0:
# 		IntegralStrategySttings.objects.filter(webapp_id=profile.webapp_id).update(**integral)
# 	for key, value in integral_detail.items():
# 		if key == 'is_used':
# 			if value == u'否':
# 				integral_detail[key] = False
# 			else:
# 				integral_detail[key] = True
# 		else:
# 			integral_detail[key] = float(value[value.find('+')+1:value.find('*')])

# 	integral_detail['webapp_id'] = profile.webapp_id
# 	if IntegralStrategySttingsDetail.objects.filter(webapp_id=profile.webapp_id).count() > 0 and integral_detail:
# 		IntegralStrategySttingsDetail.objects.filter(webapp_id=profile.webapp_id).update(**integral_detail)
# 	elif integral_detail:
# 		IntegralStrategySttingsDetail.objects.create(**integral_detail)

@then(u'{user}可以获得会员列表')
def step_impl(context, user):
	json_data = json.loads(context.text)
	Member.objects.all().update(is_for_test=False)
	url = '/member/api/members/get/?design_mode=0&version=1&status=-1&count_per_page=50&page=1&enable_paginate=1'
	response = context.client.get(bdd_util.nginx(url))
	items = json.loads(response.content)['data']['items']
	actual_members = []
	for member_item in items:
		member_item['name'] = member_item['username']
		if member_item['is_subscribed']:
			member_item['status'] = u"已关注"
		else:
			member_item['status'] = u"已取消"
		member_item['member_rank'] = member_item['grade_name']
		actual_members.append(member_item)
	for data in json_data:
		if 'experience' in data:
			del data['experience']

	bdd_util.assert_list(json_data, actual_members)


@Given(u'{webapp_owner_name}调{webapp_user_name}等级为{grade_name}')
def step_impl(context, webapp_owner_name, webapp_user_name, grade_name):
	user = context.client.user
	member = bdd_util.get_member_for(webapp_user_name, context.webapp_id)
	db_grade = MemberGrade.objects.get(name=grade_name, webapp_id=user.get_profile().webapp_id)
	context.client.post('/member/api/tag/update/', {
		'checked_ids':	db_grade.id, 'member_id': member.id, 'type': 'grade'})

@then(u'{webapp_owner_name}能获得{webapp_user_name}的积分日志')
def step_impl(context, webapp_owner_name, webapp_user_name):
	webapp_user_member = bdd_util.get_member_for(webapp_user_name, context.webapp_id)
	url = '/member/api/member_logs/get/?design_mode=0&version=1&member_id=%d&count_per_page=10&page=1&enable_paginate=1' % webapp_user_member.id
	response = context.client.get(url)
	member_logs = json.loads(response.content)['data']['items']
	actual = [{"content":log['event_type'], "integral":log['integral_count']} for log in member_logs]

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


@when(u'{member_a}取消关注{user}的公众号')
def step_impl(context, member_a, user):
	# if hasattr(context, 'client'):
	# 	context.client.logout()
	# context.client = bdd_util.login(user)
	# client = context.client
	user = UserFactory(username=user)
	# user = context.client.user
	user_profile = user.get_profile()
	openid = '%s_%s' % (member_a, user)
	post_data = """
				<xml><ToUserName><![CDATA[weizoom]]></ToUserName>
				<FromUserName><![CDATA[%s]]></FromUserName>
				<CreateTime>1405079048</CreateTime>
				<MsgType><![CDATA[event]]></MsgType>
				<Event><![CDATA[unsubscribe]]></Event>
				<EventKey><![CDATA[]]></EventKey>
				</xml>
	""" % openid
	url = '/weixin/%s/'% user_profile.webapp_id
	context.client.post(url, post_data, "text/xml; charset=\"UTF-8\"")


