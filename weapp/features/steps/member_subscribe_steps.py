# -*- coding: utf-8 -*-
# __editor__='justing'
# edit_time:2015/09/06,删除‘可以获得会员列表’中的访问会员详情页
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

def get_actual_members_data(context):
	# 处理url
	if not hasattr(context, 'url'):
		context.url = '/member/api/member_list/?design_mode=0&version=1&status=1&enable_paginate=1'
		if hasattr(context, 'count_per_page'):
			context.url += '&count_per_page=' + str(context.count_per_page)
		else:
			context.url += '&count_per_page=' + '50'
		if hasattr(context, 'page'):
			context.url += '&page=' + str(context.page)
		if hasattr(context, 'filter_str'):
			context.url += context.filter_str

	# 向服务器请求数据，并处理
	response = context.client.get(bdd_util.nginx(context.url))
	items = json.loads(response.content)['data']['items']
	actual_members = []
	for member_item in items:
		member_item['name'] = member_item['username']
		member_item['attention_time'] = member_item['created_at']
		member_item['tags'] = [item['name'] for item in member_item['tags']]
		member_item['member_rank'] = member_item['grade_name']
		if member_item['is_subscribed']:
			member_item['status'] = u"已关注"
		else:
			member_item['status'] = u"已取消"
		#member_item['member_rank'] = member_item['grade_name']
		if member_item['source'] == 0:
			member_item['source'] = u"直接关注"
		elif member_item['source'] == 1:
			member_item['source'] = u"推广扫码"
		elif member_item['source'] == 2:
			member_item['source'] = u"会员分享"
		actual_members.append(member_item)
	return actual_members

def get_members_dict_by_context(context):
	if context.text:
		expected = json.loads(context.text)
		for data in expected:
			if 'experience' in data:
				del data['experience']
			if data.has_key('attention_time') and data['attention_time'] == '今天':
				data['attention_time'] = time.strftime('%Y-%m-%d')
		return expected
	elif context.table:
		grades_dict = {}
		tags_dict = {}
		response = context.client.get('/member/api/members_filter_params/')
		for item in json.loads(response.content)['data']['grades']:
			grades_dict[item['name']] = item['id']
		for item in json.loads(response.content)['data']['tags']:
			tags_dict[item['name']] = item['id']

		expected = []
		for row in context.table:
			adict = {}
			if hasattr(row, 'name') or row.get('name', None):
				adict['name'] = row['name']
			if hasattr(row, 'member_rank') or row.get('member_rank', None):
				adict['member_rank'] = row['member_rank']
			if hasattr(row, 'friend_count') or row.get('friend_count', None):
				adict['friend_count'] = int(row['friend_count'])
			if hasattr(row, 'integral') or row.get('integral', None):
				adict['integral'] = int(row['integral'])
			if hasattr(row, 'pay_money') or row.get('pay_money', None):
				adict['pay_money'] = row['pay_money']
			if hasattr(row, 'unit_price') or row.get('unit_price', None):
				adict['unit_price'] = row['unit_price']
			if hasattr(row, 'pay_times') or row.get('pay_times', None):
				adict['pay_times'] = int(row['pay_times'])
			if hasattr(row, 'attention_time') or row.get('attention_time', None):
				if row['attention_time'] == u'今天':
					adict['attention_time'] = time.strftime('%Y-%m-%d')
				else:
					adict['attention_time'] = row['attention_time']
			if hasattr(row, 'source') or row.get('source', None):
				adict['source'] = row['source']
			if hasattr(row, 'tags') or row.get('tags', None):
				adict['tags'] = row['tags']
			expected.append(adict)
		return expected

@then(u'{user}可以获得会员列表')
def step_impl(context, user):
	Member.objects.all().update(is_for_test=False)
	# 获得服务器的数据
	actual_members = get_actual_members_data(context)

	# 处理feature文件中数据
	expected_data = get_members_dict_by_context(context)

	# 我也不知道这段为什么会这样！！！
	# 好像是根据不同的数据类型来组织actual_data
	if context.text:
		actual_data = actual_members
	elif context.table:
		actual_data = []
		for row in actual_members:
			adict = {}
			adict['name'] = row['username']
			adict['member_rank'] = row['grade_name']
			adict['friend_count'] = row['friend_count']
			adict['integral'] = row['integral']
			adict['pay_money'] = row['pay_money']
			adict['unit_price'] = row['unit_price']
			adict['pay_times'] = row['pay_times']
			adict['attention_time'] = row['attention_time']
			adict['source'] = row['source']
			adict['tags'] = ','.join(row['tags'])
			actual_data.append(adict)

	bdd_util.assert_list(expected_data, actual_data)


@Given(u'{webapp_owner_name}调{webapp_user_name}等级为{grade_name}')
def step_impl(context, webapp_owner_name, webapp_user_name, grade_name):
	user = context.client.user
	member = bdd_util.get_member_for(webapp_user_name, context.webapp_id)
	db_grade = MemberGrade.objects.get(name=grade_name, webapp_id=user.get_profile().webapp_id)
	context.client.post('/member/api/update_member_tag_or_grade/', {
		'checked_ids':	db_grade.id, 'member_id': member.id, 'type': 'grade'})

@then(u'{webapp_owner_name}能获得{webapp_user_name}的积分日志')
def step_impl(context, webapp_owner_name, webapp_user_name):
	webapp_user_member = bdd_util.get_member_for(webapp_user_name, context.webapp_id)
	url = '/member/api/integral_logs/?design_mode=0&version=1&member_id=%d&count_per_page=10&page=1&enable_paginate=1' % webapp_user_member.id
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


@when(u'{username}访问会员列表第{page_count}页')
def step_impl(context, username, page_count):
	if hasattr(context, "url"):
		delattr(context, "url")
	context.page = page_count
