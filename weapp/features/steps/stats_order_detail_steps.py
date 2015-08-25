#coding: utf8
"""
数据统计(BI)之销售订单分析的BDD steps

"""

import json
#import time
from test import bdd_util
from core import dateutil
from market_tools.tools.activity.models import *
from modules.member.models import Member, SOURCE_SELF_SUB, SOURCE_MEMBER_QRCODE, SOURCE_BY_URL
from behave import *
#from features.testenv.model_factory import *
from django.test.client import Client
#from market_tools.tools.delivery_plan.models import *

from core import dateutil
#from util import dateutil as util_dateutil

@then(u'{user}获得订单占比统计数据')
def step_impl(context, user):
	expected = json.loads(context.text)
	print("expected: {}".format(expected))
	actual = {}
	data = context.stats_data
	actual['result_order_count'] = str(data['return_count'])
	actual['result_order_proportion'] = str(data['percent'])
	print("actual: {}".format(actual))
	
	bdd_util.assert_dict(expected, actual)

@then(u'{user}获得订单统计列表')
def step_impl(context, user):
	expected = []
	for row in context.table:
		tmp_dict = {}
		tmp_dict['product_name'] = row['product_name']
		tmp_dict['order_id'] = row['order_id']
		tmp_dict['discount_amount'] = float(row['discount_amount'])
		tmp_dict['freight'] = float(row['freight'])
		tmp_dict['paid_amount'] = float(row['paid_amount'])
		tmp_dict['payment_method'] = row['payment_method']
		tmp_dict['consumer'] = row['consumer']
		tmp_dict['order_datetime'] = bdd_util.get_date_str(row['order_datetime'])
		tmp_dict['order_status'] = row['order_status']
		expected.append(tmp_dict)
	
	items = context.stats_data['items']
	actual = []
	for item in items:
		tmp_dict = {}
		products = item['products']
		product_names = ''
		for product in products:
			product_names += product['name'] + ','
		tmp_dict['product_name'] = product_names.rstrip(',')
		tmp_dict['order_id'] = item['order_id']
		tmp_dict['discount_amount'] = float(item['save_money'])
		tmp_dict['freight'] = float(item['postage'])
		tmp_dict['paid_amount'] = float(item['pay_money'])
		tmp_dict['payment_method'] = item['pay_interface_type']
		tmp_dict['consumer'] = item['buyer_name']
		created_at = item['created_at'].split(' ')[0].replace('/', '-')
		tmp_dict['order_datetime'] = created_at
		tmp_dict['order_status'] = item['order_status']
		actual.append(tmp_dict)
	
	bdd_util.assert_list(expected, actual)

@given(u'{user}设置分页查询参数')
def step_impl(context, user):
	param = json.loads(context.text)
	context.count_per_page = param.get('count_per_page')

@when(u'{user}查询订单明细统计')
def step_impl(context, user):
	url = '/stats/api/order_list/?'
	dict = context.param_dict
	for key in dict.keys():
		url = url + key + '=' + dict[key] + '&'
	
	if hasattr(context, 'count_per_page'):
		url += 'count_per_page=' + str(context.count_per_page)
	
	if hasattr(context, 'target_page'):
		if context.target_page > 0:
			url += '&page=' + str(context.target_page)
	
	# print 'param dict -------', dict
	# print 'url ----------\n', url
	
	response = context.client.get(url)
	bdd_util.assert_api_call_success(response)

	result = json.loads(response.content)
	context.stats_data = result['data']
	# print 'result -----------', result
	# raise 'debug test -------------------------'

@then(u'{user}获取订单统计列表显示共{count}页')
def step_impl(context, user, count):
	data = context.stats_data
	pageinfo = data['pageinfo']
	context.tc.assertEquals(int(count), pageinfo['max_page'])

@when(u'{user}浏览第{target_page}页')
def step_impl(context, user, target_page):
	context.target_page = target_page
	context.execute_steps(u"When %s查询订单明细统计" % user)

@when(u'{user}浏览上一页')
def step_impl(context, user):
	data = context.stats_data
	pageinfo = data['pageinfo']
	cur_page = int(pageinfo['cur_page'])
	context.target_page = cur_page - 1
	context.execute_steps(u"When %s查询订单明细统计" % user)

@when(u'{user}浏览下一页')
def step_impl(context, user):
	data = context.stats_data
	pageinfo = data['pageinfo']
	cur_page = int(pageinfo['cur_page'])
	context.target_page = cur_page + 1
	context.execute_steps(u"When %s查询订单明细统计" % user)
	
@given(u'{user}设置订单统计查询条件')
def step_impl(context, user):
	raw_dict = json.loads(context.text)
	start_date = raw_dict.get('begin_date')
	end_date = raw_dict.get('end_date')
	
	dict = {}
	if start_date and end_date:
		dict['date_interval'] = bdd_util.get_date_str(start_date) + '|' + bdd_util.get_date_str(end_date)
	
	product_name = raw_dict.get('product_name')
	if product_name:
		dict['product_name'] = product_name
	
	payment_method = raw_dict.get('payment_method')
	if payment_method == u'支付宝':
		dict['pay_type'] = '1'
	elif payment_method == u'微信支付':
		dict['pay_type'] = '2'
	elif payment_method == u'货到付款':
		dict['pay_type'] = '3'
	
	order_status = raw_dict.get('order_status')
	if order_status:
		if u'待发货' in order_status:
			dict['iswait_send'] = '1'
		if u'已发货' in order_status:
			dict['isalready_send'] = '1'
		if u'已完成' in order_status:
			dict['isalready_complete'] = '1'
	
	pref_deduction = raw_dict.get('preferential_deduction')
	if pref_deduction:
		if u'微众卡支付' in pref_deduction:
			dict['iswzcard_pay'] = '1'
		if u'积分抵扣' in pref_deduction:
			dict['isintegral_deduction'] = '1'
		if u'优惠券' in pref_deduction:
			dict['isfavorable_coupon'] = '1'
		if u'微众卡+积分' in pref_deduction:
			dict['iswzcard_integral'] = '1'
		if u'微众卡+优惠券' in pref_deduction:
			dict['iswzcard_discountcoupon'] = '1'
	
	re_purchase = raw_dict.get('re_purchase')
	if re_purchase == u'购买一次':
		dict['repeat_buy'] = '1'
	elif re_purchase == u'购买多次':
		dict['repeat_buy'] = '2'
	
	buyers_source = raw_dict.get('buyers_source')
	if buyers_source == u'直接关注购买':
		dict['buyer_source'] = '0'
	elif buyers_source == u'推荐扫码关注购买':
		dict['buyer_source'] = '1'
	elif buyers_source == u'分享链接关注购买':
		dict['buyer_source'] = '2'
	elif buyers_source == u'其他':
		dict['buyer_source'] = '3'
	
	order_id = raw_dict.get('order_id')
	if order_id:
		dict['query'] = order_id
	
	context.param_dict = dict
