# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import given, then, when
from test import bdd_util

from modules.member.models import Member
from utils.string_util import byte_to_hex
from mall.promotion import models as  promotion_models

from member_selection_steps import get_url_option_by_content
from member_subscribe_steps import get_actual_members_data, get_members_dict_by_context

@when(u'{user}设置发优惠券记录查询条件')
def step_impl(context, user):
	data = json.loads(context.text)
	name = data.get('coupon_name', '')
	coupon_type_name = data.get('type', '')
	coupon_type_code = -1
	if coupon_type_name == '全部':
		coupon_type_code = -1
	elif coupon_type_name == '单品券':
		coupon_type_code = 2
	elif coupon_type_name == '全体券':
		coupon_type_code = 1
	start_date = data.get('start_send_time', '')
	if start_date: start_date += " 00:00"
	end_date = data.get('end_send_time', '')
	if end_date: end_date += " 00:00"
	send_coupon_record_options_url = "name=%s&couponType=%s&startDate=%s&endDate=%s" % (
			name, str(coupon_type_code), start_date, end_date
		)
	context.send_coupon_record_options_url = send_coupon_record_options_url


@then(u'{user}获得发优惠券记录列表')
def step_impl(context, user):
	expected = json.loads(context.text)
	init_url = "/mall2/api/issuing_coupons_record_list/?"
	response = context.client.get(init_url+context.send_coupon_record_options_url)
	actual = []
	items = json.loads(response.content)['data']['items']
	for item in items:
		actual_data = {
			"coupon_name": item['coupon_name'],
			"type": "单品券" if item['limit_product'] else "全体券",
			"money": item['money'],
			"send_counts": item['coupon_count'],
			"send_time": item['send_time'].split(" ")[0],
			"send_memeber": item['person_count'],
			"used_counts": item['used_count']
		}
		actual.append(actual_data)

	bdd_util.assert_list(expected, actual)

@when(u"{user}创建优惠券发放规则发放优惠券于'{date}'")
def step_impl(context, user, date):
	is_success = create_issuing_coupons_record(context)
	if is_success:
		record = promotion_models.CouponRecord.objects.all().order_by('-id')[0]
		record.send_time = date
		record.created_at = date
		record.save()

def init_url(context):
	init_url = '/member/api/member_list/?filter_value='
	if context.text:
		options_url = get_url_option_by_content(context)
	else:
		options_url = []
	init_url = init_url +'|'.join(options_url)
	if hasattr(context, 'count_per_page'):
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

@when(u"{user}创建优惠券发放规则发放优惠券")
def step_impl(context, user):
	create_issuing_coupons_record(context)

def create_issuing_coupons_record(context):
	url = "/mall2/api/issuing_coupons_record/?_method=put"
	data = json.loads(context.text)
	coupon_rule_name = data['name']
	pre_person_count = data['count']
	members = data['members']

	member_ids = []
	for name in members:
		member_ids.append(Member.objects.get(username_hexstr=byte_to_hex(name)).id)

	coupon_rule_id = promotion_models.CouponRule.objects.get(name=coupon_rule_name).id
	post_data = {
		'member_id': json.dumps(member_ids),
		'coupon_rule_id': coupon_rule_id,
		'pre_person_count': pre_person_count
	}
	response = context.client.post(url, post_data)
	try:
		bdd_util.assert_api_call_success(response)
		return True
	except:
		context.response = response
		return False

@then(u"{user}获得发优惠券'{coupon_rule_name}''{date}'的详情")
def step_impl(context, user, coupon_rule_name, date):
	url = "/mall2/api/issuing_coupons_detail/?id="
	coupon_rule_id = promotion_models.CouponRule.objects.get(name=coupon_rule_name).id
	record_id = promotion_models.CouponRecord.objects.get(
		coupon_rule_id=coupon_rule_id,
		send_time=datetime.strptime(date, "%Y-%m-%d")
		).id
	response = context.client.get(url+str(record_id))
	expected = json.loads(context.text)
	actual = []
	items = json.loads(response.content)['data']['items']
	for item in expected:
		item['start_time'] = bdd_util.get_date(item['start_time']).strftime("%Y-%m-%d")
		item['end_time'] = bdd_util.get_date(item['end_time']).strftime("%Y-%m-%d")
		if item['used_time']:
			item['used_time'] = bdd_util.get_date(item['used_time']).strftime("%Y-%m-%d")
	for item in items:
		actual.append(dict(
				coupon_id=item['coupon_id'],
				money=item['money'],
				start_time=item['start_time'].split(" ")[0],
				end_time=item['end_time'].split(" ")[0],
				target=item['member']['username_for_html'],
				used_time=item['use_time'].split(" ")[0] if item.has_key('use_time') else "",
				order_no= item['order_fullid'] if item.has_key('order_fullid') else "",
				status=item['status']
			))

	bdd_util.assert_list(expected, actual)