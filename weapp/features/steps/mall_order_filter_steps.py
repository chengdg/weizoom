# -*- coding: utf-8 -*-
import os
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from tools.express import util as express_util

@When(u"{user}创建类型为'{filter_name}'的标签")
def step_impl(context, user, filter_name):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	filter_names = filter_name.split(',')
	filter_value = _get_filter_value_by_name(client, filter_names)

	url = u'/mall/api/order_filter/save/?filter_name={}&filter_value={}'.format('-'.join(filter_names), filter_value)

	response = context.client.get(bdd_util.nginx(url))

def _get_filter_value_by_name(client, filter_names):
	data_value = _get_filter_value_all(client)
	filter_values = dict()
	for item in data_value.get('status'):
		for name in filter_names:
			if item['name'] == name:
				value = item['value']
				if filter_values.get('status') >= 0:
					value = '{}^{}'.format(filter_values.get('status'), value)
				filter_values['status'] = value

	for item in data_value.get('source'):
		for name in filter_names:
			if item['name'] == name:
				value = item['value']
				if filter_values.get('source') >= 0:
					value = '{}^{}'.format(filter_values.get('source'), value)
				filter_values['source'] = value

	for item in data_value.get('type'):
		for name in filter_names:
			if item['name'] == name:
				value = item['value']
				if filter_values.get('type') >= 0:
					value = '{}^{}'.format(filter_values.get('type'), value)
				filter_values['type'] = value

	for item in PAYTYPE2NAME:
		for name in filter_names:
			if PAYTYPE2NAME[item] == name:
				value = item
				if filter_values.get('pay_interface_type') >= 0:
					value = '{}^{}'.format(filter_values.get('pay_interface_type'), value)
				filter_values['pay_interface_type'] = value

	array = []
	for item in filter_values:
		array.append('{}:{}'.format(item, filter_values[item]))
	filter_value = '|'.join(array)

	return filter_value

def _get_filter_value_by_name_str(client, filter_dict):
	args = []
	filter_values = []
	data_value = _get_filter_value_all(client)

	if filter_dict.get('type'):
		for types in data_value['type']:
			if types.get('name') == filter_dict.get('type'):
				filter_values.append(u'type:{}'.format(types.get('value')))

	if filter_dict.get('source'):
		for source in data_value['source']:
			if source.get('name') == filter_dict.get('source'):
				filter_values.append('source:{}'.format(source.get('value')))

	if filter_dict.get('status'):
		for status in data_value['status']:
			if status.get('name') == filter_dict.get('status'):
				filter_values.append('status:{}'.format(status.get('value')))

	if filter_dict.get('methods_of_payment'):
		for pay_interface_type in data_value['pay_interface_type']:
			if pay_interface_type.get('pay_name') == filter_dict.get('methods_of_payment'):
				filter_values.append('pay_interface_type:{}'.format(pay_interface_type.get('data_value')))

	if filter_dict.get('order_no'):
		args.append(u'query={}'.format(filter_dict.get('order_no')))

	if filter_dict.get('ship_name'):
		args.append(u'ship_name={}'.format(filter_dict.get('ship_name')))

	if filter_dict.get('ship_tel'):
		args.append(u'ship_tel={}'.format(filter_dict.get('ship_tel')))

	if filter_dict.get('order_time'):
		args.append(u'date_interval={}'.format(filter_dict.get('order_time')))

	if filter_dict.get('express_number'):
		args.append(u'express_number={}'.format(filter_dict.get('express_number')))

	if filter_dict.get('product_name'):
		args.append(u'productName={}'.format(filter_dict.get('product_name')))

	if len(filter_values):
		args.append(u'filter_value={}'.format('|'.join(filter_values)))

	return '&'.join(args)

def _get_filter_value_all(client):
	url = '/mall/api/order_filter_params/get/'
	response = client.get(bdd_util.nginx(url))
	items = json.loads(response.content)['data']
	return items

def _get_order_filter_all(context):
	url = '/mall/api/order_filters/get/'
	response = context.client.get(bdd_util.nginx(url))
	items = json.loads(response.content)['data']['filters']
	return items

@then(u"{user}获取标签的名称")
def step_impl(context, user):
	items = _get_order_filter_all(context)
	actual_filters = []
	for item in items:
		actual_filters.append({'tag_name': item.get('name')})

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual_filters)


@When(u"{user}点击标签'{filter_name}'")
def step_impl(context, user, filter_name):
	items = _get_order_filter_all(context)
	for item in items:
		if item.get('name') == filter_name:
			context.client.filter_value = item.get('value')

	context.client.filter_name = filter_name

@When(u"{user}选择条件为")
def step_impl(context, user):
	filter_dict = json.loads(context.text)
	filter_value = _get_filter_value_by_name_str(context.client, filter_dict)
	# print('+++++++++++++++++++++++')
	# print(filter_value)
	context.client.filter_value = filter_value

@then(u"{user}获取对应的订单")
def step_impl(context, user):
	filter_value = context.client.filter_value

	url = '/mall/api/orders/get/?{}&sort_attr=-created_at&count_per_page=15&page=1'.format(filter_value)
	response = context.client.get(bdd_util.nginx(url))
	items = json.loads(response.content)['data']['items']

	actual_orders = _get_actual_orders(items, context)
	expected_order = json.loads(context.text)
	# print(actual_orders)
	# print('-------------------')
	bdd_util.assert_list(expected_order, actual_orders)

# 组织数据
def _get_actual_orders(json_items, context):
	actual_orders = []
	source = {'mine_mall': u'本店', 'weizoom_mall': u'商城'}
	for item in json_items:
		url = '/mall/order_detail/get/?order_id={}'.format(item.get('id'))
		response = context.client.get(bdd_util.nginx(url))
		order = response.context['order']
		actual_order = dict()
		actual_order['order_no'] = order.order_id
		actual_order['status'] = ORDERSTATUS2TEXT[order.status]
		if actual_order['status'] == '已发货' or actual_order['status'] == '已完成':
			actual_orders.append({
				'order_no': order.order_id,
				'member': item.get('buyer_name'),
				'status': ORDERSTATUS2TEXT[int(order.status)],
				'order_time': item.get('created_at'),
				'methods_of_payment': item.get('pay_interface_name'),
				'sources': source[item.get('come')],
				'ship_name': item.get('ship_name'),
				'ship_tel': order.ship_tel,
				"logistics": express_util.get_name_by_value(order.express_company_name),
				"number": order.express_number,
				"shipper":""
			})
		else:
			actual_orders.append({
				'order_no': order.order_id,
				'member': item.get('buyer_name'),
				'status': ORDERSTATUS2TEXT[int(order.status)],
				'order_time': item.get('created_at'),
				'methods_of_payment': item.get('pay_interface_name'),
				'sources': source[item.get('come')],
				'ship_name': item.get('ship_name'),
				'ship_tel': order.ship_tel
			})

	return actual_orders

@then(u"{user}导出订单获取订单信息")
def step_impl(context, user):
	filter_value = context.client.filter_value

	if filter_value:
		url = '/mall/editor/orders/export/?{}'.format(filter_value)
		response = context.client.get(bdd_util.nginx(url))
		# print(response)
		# items = json.loads(response.content)['data']['items']
		# actual_orders = _get_actual_orders(items)
		# expected_order = json.loads(context.text)
		# bdd_util.assert_list(expected_order, actual_orders)

@When(u"{user}删除'{filter_name}'标签")
def step_impl(context, user, filter_name):
	filter_id = 0
	filters = UserHasOrderFilter.objects.filter(filter_name=filter_name)
	if filters.count() > 0:
		filter_id = filters[0].id

	url = '/mall/api/order_filter/delete/?&id={}'.format(filter_id)
	context.client.get(bdd_util.nginx(url))
