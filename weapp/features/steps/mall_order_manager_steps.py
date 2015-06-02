# -*- coding: utf-8 -*-
import os
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from webapp.modules.mall.models import *

@When(u"{webapp_user_name}点击支付")
def step_impl(context, webapp_user_name):
	url = '/workbench/jqm/preview/%s' % context.pay_result_url[2:]
	response = context.client.get(bdd_util.nginx(url), follow=True)

	actual_order = response.context['order']
	context.create_order_id = actual_order.id

@then(u"{user}可以看到订单列表")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	response = context.client.get('/mall/api/orders/get/?version=1&sort_attr=-created_at&count_per_page=15&page=1')
	items = json.loads(response.content)['data']['items']

	actual_orders = []
	for order_item in items:
		actural_order = {}
		actural_order['status'] = order_item['status']
		actural_order['price'] = order_item['pay_money']
		actural_order['customer_message'] = order_item['customer_message']
		actural_order['buyer'] = order_item['buyer_name']

		order_id = order_item['id']
		buy_product_response = context.client.get('/mall/api/order_products/get/?version=1&order_id=%d&timestamp=1406172500320' %(order_id))
		buy_products = json.loads(buy_product_response.content)['data']['products']
		buy_product_results = []
		for buy_product in buy_products:
			buy_product_result = {}
			buy_product_result['product_name'] = buy_product['name']
			buy_product_result['count'] = buy_product['count']
			buy_product_result['total_price'] = buy_product['total_price']
			buy_product_results.append(buy_product_result)

		actural_order['products'] = buy_product_results
		actual_orders.append(actural_order)

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual_orders)

@Then(u"{user}对订单列表按待支付状态搜索")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	response = context.client.get('/mall/api/orders/get/?version=1&sort_attr=-created_at&filter_attr=status&filter_value=0&count_per_page=15&page=1')
	items = json.loads(response.content)['data']['items']

	actual_orders = []
	for order_item in items:
		actural_order = {}
		actural_order['status'] = order_item['status']
		actural_order['price'] = order_item['total_price']
		actural_order['customer_message'] = order_item['customer_message']
		actural_order['buyer'] = order_item['buyer_name']

		order_id = order_item['id']
		buy_product_response = context.client.get('/mall/api/order_products/get/?version=1&order_id=%d&timestamp=1406172500320' %(order_id))
		buy_products = json.loads(buy_product_response.content)['data']['products']
		buy_product_results = []
		for buy_product in buy_products:
			buy_product_result = {}
			buy_product_result['product_name'] = buy_product['name']
			buy_product_result['count'] = buy_product['count']
			buy_product_result['total_price'] = buy_product['total_price']
			buy_product_results.append(buy_product_result)

		actural_order['products'] = buy_product_results
		actual_orders.append(actural_order)

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual_orders)

@Then(u"{user}对订单列表按货到付款状态搜索")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	response = context.client.get('/mall/api/orders/get/?version=1&sort_attr=-created_at&filter_attr=pay_interface_type&filter_value=9&count_per_page=15&page=1')
	items = json.loads(response.content)['data']['items']

	actual_orders = []
	for order_item in items:
		actural_order = {}
		actural_order['status'] = order_item['status']
		actural_order['price'] = order_item['total_price']
		actural_order['customer_message'] = order_item['customer_message']
		actural_order['buyer'] = order_item['buyer_name']

		order_id = order_item['id']
		buy_product_response = context.client.get('/mall/api/order_products/get/?version=1&order_id=%d&timestamp=1406172500320' %(order_id))
		buy_products = json.loads(buy_product_response.content)['data']['products']
		buy_product_results = []
		for buy_product in buy_products:
			buy_product_result = {}
			buy_product_result['product_name'] = buy_product['name']
			buy_product_result['count'] = buy_product['count']
			buy_product_result['total_price'] = buy_product['total_price']
			buy_product_results.append(buy_product_result)

		actural_order['products'] = buy_product_results
		actual_orders.append(actural_order)

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual_orders)


@Then(u"{user}可以获得最新订单详情")
def step_impl(context, user):
	order = Order.objects.all().order_by('-id')[0]
	context.latest_order_id = order.id
	client = context.client
	response = context.client.get('/mall/editor/order/get/?order_id=%d' %(context.latest_order_id))

	order = response.context['order']
	order.order_type = ORDER_TYPE2TEXT[order.type]
	order.total_price = float(order.final_price)
	order.ship_area = order.area + ' ' + order.ship_address
	from webapp.modules.mall.templatetags import mall_filter
	actions = mall_filter.get_order_actions(order)
	order.actions = dict([(action['name'], 1) for action in actions])
	if order.status == ORDER_STATUS_PAYED_SHIPED or order.status == ORDER_STATUS_SUCCESSED:
		order.actions[u'修改物流'] = 1
	for product in order.products:
		product['total_price'] = float(product['total_price'])
	order.status = STATUS2TEXT[order.status]
	actual = order
	actual.reason = order.reason


	expected = json.loads(context.text)
	actions = expected['actions']
	expected['actions'] = dict([(action, 1) for action in actions])
	bdd_util.assert_dict(expected, actual)


@When(u"{user}支付最新订单")
def step_impl(context, user):
	url = '/mall/editor/order_status/update/?order_id={}&action=pay'.format(context.latest_order_id)
	context.client.get(url, HTTP_REFERER='/')


@When(u"{user}对最新订单进行发货")
def step_impl(context, user):
	#点击发货:mall/editor/order_express/add/?order_id=87&express_company_name=shentong&express_number=123456789
	response = context.client.get('/mall/editor/order_express/add/?order_id=%d&express_company_name=shentong&express_number=123456789&leader_name=%s&is_update_express=false' %(context.latest_order_id, user))


# @Then(u"{user}通过后台管理系统可以看到订单状态为")
# def step_impl(context, user):
# 	try:
# 		response = context.client.get('/mall/api/orders/get/?version=1&sort_attr=-created_at&count_per_page=15&page=1')
# 	except:
# 		pass
# 	order = Order.objects.get(id=context.create_order_id)
# 	actural = {}
# 	actural['status'] = STATUS2TEXT[order.status]
# 	expected = json.loads(context.text)

# 	bdd_util.assert_dict(expected, actural)

# 	if hasattr(context, 'current_date'):
# 		os.system('date %s' %(context.current_date))


@When(u"{user}完成最新订单")
def step_impl(context, user):
	url = '/mall/editor/order_status/update/?order_id=%d&action=finish' %(context.latest_order_id)
	response = context.client.get(url, HTTP_REFERER='/')


@When(u"{user}取消最新订单")
def step_impl(context, user):
	order = Order.objects.all().order_by('-id')[0]
	if hasattr(context, 'caller_step_cancel_reason'):
		data = context.caller_step_cancel_reason
	else:
		data = json.loads(context.text)
	reason = data['reason']

	url = '/mall/order/update/?order_id=%d&action=cancel&reason=%s' % (order.id, reason)
	response = context.client.get(url, HTTP_REFERER='/')


@When(u"{user}设置未付款订单过期时间")
def step_impl(context, user):
	config = json.loads(context.text)
	no_payment_order_expire_day = config['no_payment_order_expire_day'][:-1]
	from webapp.modules.mall.models import MallConfig
	MallConfig.objects.filter(owner=context.client.user).update(order_expired_day=no_payment_order_expire_day)


@When(u"{user}填写订单信息")
def step_impl(context, user):
	orders = json.loads(context.text)
	orders = _handle_fahuo_data(orders)
	from mall import module_api as mall_api
	mall_api.batch_handle_order(orders, context.client.user)

def _handle_fahuo_data(orders):
	data = []
	for order in orders:
		item = dict()
		item['order_id'] = order['order_no']
		item['express_company_name'] = order['logistics']
		item['express_number'] = order['number']
		data.append(item)

	return data


@when(u"{webapp_owner_user}填写发货信息")
def step_fill_delivery(context, webapp_owner_user):
	"""
	顺丰速递 must be provided
		{
			'order_no': '2134654646',
			'express_company_name': 'shunfeng',
			'express_number': '13654546684',
			'leader_name': 'bill'
		}
	"""
	expected = json.loads(context.text)
	url =  '/mall/api/order_delivery/update/'
	order_id = expected[0].get('order_no')
	from mall.models import Order
	id = Order.objects.get(order_id=order_id).id
	del Order
	the_kwargs = {}
	the_kwargs['order_id'] = id
	the_kwargs['express_company_name'] =  'shunfeng' if expected[0].get('顺丰速递') else '0'
	the_kwargs['express_number'] = expected[0].get('number', -1)
	the_kwargs['leader_name'] = expected[0].get('ship_name', -1)
	context.client.get(url, the_kwargs)


@then(u"{webapp_user_name}查看个人中心全部订单")
def step_visit_personal_orders(context, webapp_user_name):
	"""
		[{
			"status": "",
			"final_price": 30.00,
			"products": [{
				"name": "商品1",
				"price": "10.00"
			},{
				"name": "商品2",
				"price": "20.00"

			}]
		},{
			"status": "待发货",
			"final_price": 30.00,
			"products":[{
				"name": "商品1",
				"price": "10.00"
			},{
				"name": "商品2",
				"price": "20.00"
			}]
		}]
	"""
	expected = json.loads(context.text)
	actual = []

	from mall.models import STATUS2TEXT

	url = '/workbench/jqm/preview/?woid=%d&module=mall&model=order_list&action=get&member_id=%d&workspace_id=mall&type=-1' % (context.webapp_owner_id, context.member.id)
	response = context.client.get(bdd_util.nginx(url), follow=True)
	orders = response.context['orders']
	for order in orders:
		a_order = {}
		a_order['final_price'] = order.final_price
		a_order['status'] = STATUS2TEXT[order.status]
		a_order['products'] = []
		for product in order.get_products:
			a_product = {}
			a_product['name'] = product.product.name
			a_product['price'] = product.total_price
			a_order['products'].append(a_product)
		actual.append(a_order)
	bdd_util.assert_list(expected, actual)
