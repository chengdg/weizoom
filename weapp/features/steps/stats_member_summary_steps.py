# -*- coding: utf-8 -*-
"""
数据统计(BI)之会员概况分析的BDD steps

"""

__author__ = 'duhao'

from test import bdd_util
from behave import *
#from django.test.client import Client

import json
#from core import dateutil


def convert_readable_dict(readable_dict):
	"""
	将可读的dict转成与API结果一致的dict
	"""
	expected = {}
	expected['total_member_count'] = readable_dict[u'会员总数']
	expected['subscribed_member_count'] = readable_dict[u'关注会员']
	expected['new_member_count'] = readable_dict[u'新增会员']
	expected['binding_phone_member_count'] = readable_dict[u'手机绑定会员']
	expected['bought_member_count'] = readable_dict[u'下单会员']
	expected['repeat_buying_member_rate'] = readable_dict[u'会员复购率']
	expected['ori_qrcode_member_count'] = readable_dict[u'发起扫码会员']
	expected['share_url_member_count'] = readable_dict[u'发起分享链接会员']
	expected['member_from_qrcode_count'] = readable_dict[u'扫码新增会员']
	expected['self_follow_member_count'] = readable_dict[u'直接关注']
	expected['member_from_share_url_count'] = readable_dict[u'分享链接新增会员']
	expected['member_recommend_rate'] = readable_dict[u'会员推荐率']
	return expected	

@when(u"{user}设置筛选日期")
def step_impl(context, user):
	date_dict = json.loads(context.text)
	context.date_dict = date_dict


@then(u"{user}获得基础数据和会员来源数据")
def step_impl(context, user):
	start_date = bdd_util.get_date_str(context.date_dict['start_date'])
	end_date = bdd_util.get_date_str(context.date_dict['end_date'])

	url = '/stats/api/member_summary/?start_date=%s&end_date=%s' % (start_date, end_date)
	response = context.client.get(url)
	bdd_util.assert_api_call_success(response)
	results = json.loads(response.content)
	print("results: {}".format(results))
	actual = results['data']['items']

	expected_dict = {}
	for row in context.table:
		expected_dict[row['item']] = row['quantity']
	expected = convert_readable_dict(expected_dict)

	bdd_util.assert_dict(expected, actual)


@then(u"{user}获得分享链接排行Top10")
def step_impl(context, user):
	start_date = bdd_util.get_date_str(context.date_dict['start_date'])
	end_date = bdd_util.get_date_str(context.date_dict['end_date'])
	
	url = '/stats/api/member_share_url_rank/?start_date=%s&end_date=%s' % (start_date, end_date)
	response = context.client.get(url)
	results = json.loads(response.content)
	actual_list = results['data']['items']

	actual = {}
	for item in actual_list:
		actual[item['username']] = item['followers']

	expected = {}
	for row in context.table:
		expected[row['username']] = int(row['followers'])

	bdd_util.assert_dict(expected, actual)


@then(u"{user}获得会员增长趋势数据")
def step_impl(context, user):
	start_date = bdd_util.get_date_str(context.date_dict['start_date'])
	end_date = bdd_util.get_date_str(context.date_dict['end_date'])
	
	url = '/stats/api/member_increasement/?start_date=%s&end_date=%s' % (start_date, end_date)
	response = context.client.get(url)
	bdd_util.assert_api_call_success(response)
	results = json.loads(response.content)
	actual_new_member_list = results['data']['series'][0]['data']
	actual_bought_member_list = results['data']['series'][1]['data']

	actual = [actual_new_member_list, actual_bought_member_list]

	expected = []
	expected_new_member_list = []
	expected_bought_member_list = []
	for row in context.table:
		expected_new_member_list.append(int(row['new_member_count']))
		expected_bought_member_list.append(int(row['bought_member_count']))
	expected = [expected_new_member_list, expected_bought_member_list]

	bdd_util.assert_list(expected, actual)


@then(u"{user}获得会员详细数据")
def step_impl(context, user):
	start_date = bdd_util.get_date_str(context.date_dict['start_date'])
	end_date = bdd_util.get_date_str(context.date_dict['end_date'])

	url = '/stats/api/member_detail_data/?start_date=%s&end_date=%s' % (start_date, end_date)
	response = context.client.get(url)
	bdd_util.assert_api_call_success(response)
	results = json.loads(response.content)
	print("results: {}".format(results))
	actual = results['data']['items']

	expected = []
	for row in context.table:
		expected_dict = {}
		expected_dict['date'] = bdd_util.get_date_str(row['date'])
		expected_dict['new_member_count'] = row['new_member']
		expected_dict['binding_phone_member_count'] = row['mobile_phone_member']
		expected_dict['share_url_member_count'] = row['launch_share_link_member']
		expected_dict['member_from_share_url_count'] = row['share_link_new_member']
		expected_dict['ori_qrcode_member_count'] = row['launch_spreading_code_member']
		expected_dict['member_from_qrcode_count'] = row['spreading_code_new_member']
		expected_dict['bought_member_count'] = row['order_member']

		expected.append(expected_dict)

	bdd_util.assert_list(expected, actual)

