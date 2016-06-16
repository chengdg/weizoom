# -*- coding: utf-8 -*-
# 签到详情
# author: dgl
# 需要打开apiserver

import json
import logging
from behave import *
from test import bdd_util
from modules.member import module_api as member_api
from utils.string_util import byte_to_hex
from modules.member.models import Member
from apps.customerized_apps.sign.models import Sign

def __date2time(date_str):
	"""
	字符串 今天/明天……
	转化为字符串 "%Y-%m-%d %H:%M"
	"""
	cr_date = date_str
	p_time = "{}".format(bdd_util.get_date_str(cr_date))
	return p_time

@then(u"{webapp_owner_name}获得'{webapp_user_name}'参加'{webapp_name}'的优惠券明细列表")
def step_impl(context, webapp_owner_name, webapp_user_name, webapp_name):


	member = Member.objects.get(username_hexstr=byte_to_hex(webapp_user_name))
	sign = Sign.objects.get(name=webapp_name)
	data = {
		'id': member.id,
		'design_mode': 0,
		'project_id': 'new_app:sign:%s'%sign.related_page_id,
	}
	if hasattr(context, 'filter_dict'):
		# logging.info('------set filter_dict____')
		data = dict(data, **context.filter_dict)

	response = context.client.get('/member/api/member_coupon/', data)
	response_data = json.loads(response.content)['data']['items']
	actual = []
	# logging.info('..............123')
	# logging.info("%s"%response_data)
	for item in response_data:# 格式化得到的数据
		provided_time = item['provided_time']

		collection_time = provided_time.split()[0]
		actual.append({
			'collection_time': collection_time.replace('/','-'),	
			'name': item['coupon_name'],
			'coupon_id': item['coupon_id'],
			'type': item['coupon_detail'].split()[1],
			'status': item['coupon_state'],
			})

	expected = json.loads(context.text)
	for item in expected:
		item['collection_time'] = __date2time(item['collection_time'])

	

	bdd_util.assert_list(expected, actual)

COUPON_STATUS = {
	u'未使用': 0,
	u'已使用': 1,
	u'已过期': 2,
				}

@when(u"{webapp_owner_name}获得'{webapp_user_name}'参加'{webapp_name}'的优惠券明细列表默认查询条件")
def step_impl(context, webapp_owner_name, webapp_user_name, webapp_name):
	context_json = json.loads(context.text)
	filter_dict = {}
	for filter_row in context_json:
		if 'status' in filter_row.keys() and filter_row['status'] != u"全部":
			filter_dict['filter_attr'] = 'status'
			filter_dict['filter_value'] = COUPON_STATUS[filter_row['status']]

	context.filter_dict = filter_dict
