# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import given, then, when
from test import bdd_util
from member_selection_steps import get_url_option_by_content
from member_subscribe_steps import get_actual_members_data, get_members_dict_by_context

@when(u'{user}设置发优惠券记录查询条件')
def step_impl(context, user):
	data = json.loads(context.text)
	name = data.get('name', '')
	coupon_type_name = data.get('type', '')
	coupon_type_code = -1
	if coupon_type_name == '全体':
		coupon_type_code = -1
	elif coupon_type_name == '单品券':
		coupon_type_code = 2
	elif coupon_type_name == '全体券':
		coupon_type_code = 1
	start_date = data.get('start_send_time', '')
	end_date = data.get('end_send_time', '')
	send_coupon_record_options_url = "name=%s&couponType=%s&startDate=%s&endDate=%s" % (
			name, str(coupon_type_code), start_date, end_date
		)
	context.send_coupon_record_options_url = send_coupon_record_options_url


@then(u'{user}获得发优惠券记录列表')
def step_impl(context, user):
	expected = json.loads(context.text)
	init_url = "/mall2/api/issuing_coupons_record_list/?"
	print context.send_coupon_record_options_url
	response = context.client.get(init_url+context.send_coupon_record_options_url)
	actual = []
	items = json.loads(response.content)['data']['items']
	for item in items:
		actual_data = {
			"coupon_name": item['coupon_name'],
			"type": "全体券" if item['limit_product'] else "单品券",
			"money": item['money'],
			"send_counts": item['coupon_count'],
			"send_time": item['send_time'].split(" ")[0],
			"send_memeber": item['person_count'],
			"used_counts": item['used_count']
		}
		actual.append(actual_data)
	bdd_util.assert_dict(expected, actual)

@when(u"{user}为会员发放优惠券于'{date}'")
def step_impl(context, user, date):	
	pass

def init_url(context):
	init_url = '/member/api/member_list/?filter_value='
	if context.text:
		options_url = get_url_option_by_content(context)
	else:
		options_url = []
	init_url = init_url +'|'.join(options_url)
	if hasattr(context, 'count_per_page'):
		print "-8-"*10
		print "context.count_per_page", context.count_per_page
		print "-8-"*10
		init_url += '&count_per_page=' + str(context.count_per_page)
	else:
		init_url += '&count_per_page=' + '50'
	if hasattr(context, 'page'):
		init_url += '&page=' + str(context.page)
	else:
		context.page = '1'
	context.url = init_url
	context.filter_str = "&filter_value=" + '|'.join(options_url)

@when(u"{user}设置发送优惠券选择会员查询条件")
def step_impl(context, user):
	init_url(context)

@then(u"{user}获得发送优惠券选择会员列表")
def step_impl(context, user):
	expected = get_members_dict_by_context(context)
	response_data = get_actual_members_data(context)
	actual = []

	for item in response_data:
		data = {}
		for key in expected[0].keys():
			data[key] = item[key]
		actual.append(data)

	print "++"*10
	print expected
	print actual
	print "++"*10
	bdd_util.assert_list(expected, actual)

@when(u"{user}浏览发送优惠券选择会员列表第'{page_count}'页")
def step_impl(context, user, page_count):
	context.page = page_count
	init_url(context)

@when(u"{user}浏览优惠券选择会员列表的下一页")
def step_impl(context, user):
	context.page = str(int(context.page) + 1)
	init_url(context)

@when(u"{user}浏览优惠券选择会员列表的上一页")
def step_impl(context, user):
	context.page = str(int(context.page) - 1)
	init_url(context)