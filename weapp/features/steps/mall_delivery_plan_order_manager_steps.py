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

@then(u"{user}通过后台管理系统可以看到配送套餐订单列表")
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
		actural_order['price'] = order_item['total_price']
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

	#配置当前日期
	now = datetime.now()
	context.current_date = now.strftime('%Y-%m-%d')

	expected = json.loads(context.text)

	bdd_util.assert_list(expected, actual_orders)

@When(u"修改系统时间为")
def step_impl(context, user):
	#os.system("date 2012-07-24")
	now = datetime.now()
	target_date = json.loads(context.text)
	if target_date['date'] == u'今天+两天':
		delta = timedelta(days=2)		
	elif target_date['date'] == u'今天+四天':
		delta = timedelta(days=4)
	next_date = (now + delta).strftime('%Y-%m-%d')
	os.system("date %s" %(next_date))