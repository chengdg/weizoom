	#coding: utf8
"""
数据统计(BI)之营销数据分析的BDD steps

"""

__author__ = 'victor'

import json
import time
from test import bdd_util
from market_tools.tools.activity.models import *

from behave import *
#from features.testenv.model_factory import *
from django.test.client import Client
#from market_tools.tools.delivery_plan.models import *
from market_tools.tools.lottery.models import Lottery
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings
from modules.member.models import MemberMarketUrl

from core import dateutil

@when(u"微信用户已参加'微信抽奖'营销活动")
def step_impl(context):
	"""
	处理批量参加微信抽奖用户的情况
	"""
	for row in context.table:
		activity_name = row['activity_name']
		#lottery = bdd_util.get_lottery_setting(activity_name)
		#assert lottery is not None
		#owner_id = lottery.owner_id

		user_name = row['participant']
		responsible_person = row['responsible_person']

		member_source = row.get('member_source')
		print('member_source: [{}]'.format(member_source))
		if member_source == u'会员分享':
			share_link_attention = row['share_link_attention']
			some_user,activity = share_link_attention.split(',')
			# 模拟通过微信抽奖关注
			context.execute_steps(u"Given %s关注%s的公众号" % (user_name, responsible_person))

			# 模拟在MemberMarketUrl中添加记录。实际应该在oauth_shared_url_service中添加记录。
			webapp_id = bdd_util.get_webapp_id_for(responsible_person)

			member = bdd_util.get_member_for(user_name, webapp_id)
			if MemberMarketUrl.objects.filter(member=member).count()==0:
				# 只在创建时添加记录
				MemberMarketUrl.objects.create(
					member = member,
					market_tool_name = 'lottery',
					url = share_link_attention,
					page_title = '微信抽奖新增会员记录',
					follower_member_token = '-',
					created_at = row['start_time'],
				)

		context.execute_steps(u"When %s参加抽奖活动'%s'" % (user_name, activity_name))


@when(u"访问'微信抽奖'营销传播分析页面")
def step_impl(context):
	"""
	"""
	# 获取页面上返回的数据
	client = context.client
	context.response = client.get('/stats/api/activity_analysis/?design_mode=0&version=1&type=lottery&sort_attr=id&count_per_page=%d&page=1&enable_paginate=1' % (100))
	bdd_util.assert_api_call_success(context.response)
	results = json.loads(context.response.content)
	context.data = results['data']


@then(u"获取'微信抽奖'营销传播分析数据")
def step_impl(context):
	"""
	"""
	items = context.data['items']  # 结果列表
	print("items: {}".format(items))

	index = 0
	for row in context.table:
		real = items[index]
		index+=1

		# 按照row.headings()构造2个dict
		#print("row: {}".format(row))
		#print("headings: {}".format(row.headings))
		expected_dict = {key: row[key] for key in row.headings}
		#real_dict = {key: real[key] for key in row.headings}
		real_dict = real
		# 特殊字段特殊处理
		expected_dict['start_at'] = dateutil.get_date_string(expected_dict['start_at'])
		expected_dict['end_at'] = dateutil.get_date_string(expected_dict['end_at'])

		print("real_dict: {}".format(real_dict))
		print("expected_dict: {}".format(expected_dict))
		bdd_util.assert_dict(expected_dict, real_dict)


@then(u"获取'渠道扫码'营销活动分析列表")
def step_impl(context):
	"""
	"""
	# 获取页面上返回的数据
	client = context.client
	context.response = client.get('/stats/api/activity_analysis/?type=qrcode&sort_attr=name&count_per_page=%d&page=1&enable_paginate=1' % (100))
	bdd_util.assert_api_call_success(context.response)
	#print("content: {}".format(context.response.content))
	results = json.loads(context.response.content)
	assert results.has_key('data')
	items = results['data']['items']  # 结果列表
	#print("items: {}".format(items))

	index = 0
	for row in context.table:
		real = items[index]
		index+=1

		# 按照row.headings()构造2个dict
		#print("row: {}".format(row))
		#print("headings: {}".format(row.headings))
		expected_dict = {key: row[key] for key in row.headings}
		real_dict = {key: real[key] for key in row.headings}
		# 特殊字段特殊处理
		#expected_dict['start_at'] = dateutil.get_date_string(expected_dict['start_at'])
		#expected_dict['end_at'] = dateutil.get_date_string(expected_dict['end_at'])
		#real_dict['start_at'] = dateutil.get_date_string(real_dict['start_at'])

		print("real_dict: {}".format(real_dict))
		print("expected_dict: {}".format(expected_dict))
		bdd_util.assert_dict(expected_dict, real_dict)



@when(u"微信用户已参加'渠道扫码'营销活动")
def step_impl(context):
	"""
	处理批量参加渠道扫码的用户
	"""
	for row in context.table:
		activity_name = row['activity_name']
		#owner = row['responsible_person']
		user_name = row['participant']
		context.execute_steps(u"When %s通过扫描'%s'二维码关注" % (user_name, activity_name))


@given(u"微信用户已批量关注{webapp_user}成为会员")
def step_impl(context, webapp_user):
	"""
	"""
	for row in context.table:
		name = row['name']
		context.execute_steps(u"When %s关注%s的公众号" % (name, webapp_user))


@then(u"获得'{type}'营销分析中'{activity_name}'的'参与传播'信息")
def step_impl(context, type, activity_name):
	expected_dict = json.loads(context.text)
	client = context.client

	if type==u'微信抽奖':
		lottery = Lottery.objects.get(name=activity_name)
		url = '/stats/api/activity_network/?design_mode=0&version=1&id={}&type=lottery'.format(lottery.id)
	elif type==u'渠道扫码':
		setting = ChannelQrcodeSettings.objects.get(name=activity_name)
		url = '/stats/api/activity_network/?design_mode=0&version=1&id={}&type=qrcode'.format(setting.id)
	response = client.get(url)
	bdd_util.assert_api_call_success(response)
	data = json.loads(response.content)['data']
	real_children = data['series'][0]['data'][0]['children']
	print("real: {}".format(real_children))

	expected_list = expected_dict['children']
	expected_list.sort()
	real_list = [child['name'] for child in real_children]
	real_list.sort()

	bdd_util.assert_list(expected_list, real_list)


@then(u"获得'{type}'营销分析中'{activity_name}'的'结果分析'信息")
def step_impl(context, type, activity_name):
	expected_dict = json.loads(context.text)
	client = context.client

	if type==u'微信抽奖':
		lottery = Lottery.objects.get(name=activity_name)
		url = '/stats/api/activity_stats/?design_mode=0&version=1&id={}&type=lottery'.format(lottery.id)
	elif type == u'渠道扫码':
		setting = ChannelQrcodeSettings.objects.get(name=activity_name)
		url = '/stats/api/activity_stats/?design_mode=0&version=1&id={}&type=qrcode'.format(setting.id)
	response = client.get(url)
	bdd_util.assert_api_call_success(response)
	data = json.loads(response.content)['data']
	print("data: {}".format(data))
	stats_list = data['stats']
	#print("stats_list: {}".format(stats_list))
	real_dict = {e['name']: e['value'] for e in stats_list}
	real_dict[u'复购总金额'] = float(real_dict.get(u'复购总金额',0))
	real_dict[u'被推荐用户下单金额'] = float(real_dict.get(u'被推荐用户下单金额',0))
	print("real_dict: {}".format(real_dict))

	bdd_util.assert_dict(expected_dict, real_dict)
