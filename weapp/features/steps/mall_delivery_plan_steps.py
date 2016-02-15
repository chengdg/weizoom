# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *

from webapp.modules.mall import signals as mall_signals
from market_tools.tools.delivery_plan.models import *

@given(u"{user}已添加配送套餐")
def step_impl(context, user):
	user = UserFactory(username=user)
	context.delivery_plans = json.loads(context.text)

	#根据product名称获取product
	for delivery in context.delivery_plans:
		product = Product.objects.get(owner_id=user.id, name=delivery['product'])
		delivery['product_id'] = product.id

		if delivery['type'] == u'月':
			delivery['type'] = 2
		elif delivery['type'] == u'周':
			delivery['type'] = 1
		else:
			delivery['type'] = 0

		#调用配送套餐创建接口，创建配送套餐
		response = context.client.post('/market_tools/delivery_plan/deliver_plan/create/', delivery)

@when(u"{webapp_user_name}购买{webapp_owner_name}的配送套餐")
def step_impl(context, webapp_user_name, webapp_owner_name):
	order_info = json.loads(context.text)	#订单信息
	#组装订单参数
	delivery = DeliveryPlan.objects.get(name=order_info['name'])

	is_delivery_plan = 1
	delivery_dates = []
	first_delivery_time = order_info['first_deliver_time']
	if first_delivery_time == u'今天':

		#根据选择的初次配送时间计算所有配送时间
		type = delivery.type	#配送类型
		frequency = delivery.frequency	#配送频率
		times = delivery.times	#配送次数		
		now = datetime.now()
		for i in range(times):
			if i == 0:				
				today = now.strftime('%Y-%m-%d')
				delivery_dates.append(today)
				continue
			gap = 0
			if type == DAILY:
				gap = 1
			elif type == WEEKLY:
				gap = 7
			else:	#MONTHLY
				gap = 30 
			delta = timedelta(days=frequency * i * gap)
			next_date = (now + delta).strftime('%Y-%m-%d')
			delivery_dates.append(next_date)

	order_info['delivery_plan_id'] = delivery.id
	order_info['is_delivery_plan'] = '1'
	order_info['delivery_dates'] = ','.join(delivery_dates)
	webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)	
	order_info["woid"] = webapp_owner_id
	order_info["module"] = 'mall'
	order_info["target_api"] = 'order/save'
	order_info["product_ids"] = delivery.product_id
	order_info["product_counts"] = '1'
	order_info["product_model_names"] = 'standard'
	order_info['ship_id'] = 0

	if not hasattr(order_info, "ship_name"):
		order_info['ship_name'] = 'bill'
	if not hasattr(order_info, "ship_tel"):
		order_info['ship_tel'] = '1312546586'
	if not hasattr(order_info, "ship_area"):
		order_info['ship_area'] = '北京市 北京市 海淀区'
	order_info['area'] = bdd_util.get_ship_area_id_for(order_info['ship_area'])
	if not hasattr(order_info, "ship_address"):
		order_info['ship_address'] = '泰兴大厦'
	
	url = '/webapp/api/project_api/call/'
	response = context.client.post(url, order_info)
	bdd_util.assert_api_call_success(response)
	response_json = json.loads(response.content)
	if response_json['code'] == 200:
		context.created_order_id = response_json['data']['order_id']
	else:
		context.created_order_id = -1

	context.webapp_owner_name = webapp_owner_name


# @then(u"{webapp_user_name}成功创建配送套餐订单")
# def step_impl(context, webapp_user_name):
# 	expected_dates = json.loads(context.text)
# 	expecteds = []
# 	now = datetime.now()
# 	for expected_date in expected_dates['delevery_date']:
# 		expected = ''
# 		if expected_date == u'今天':
# 			expected = now.strftime('%Y-%m-%d')
# 		elif expected_date == u'今天+1月':
# 			delta = timedelta(days=30)
# 			expected = (now + delta).strftime('%Y-%m-%d')
# 		elif expected_date == u'今天+2月':
# 			delta = timedelta(days=30*2)
# 			expected = (now + delta).strftime('%Y-%m-%d')
# 		elif expected_date == u'今天+1周':
# 			delta = timedelta(days=7)
# 			expected = (now + delta).strftime('%Y-%m-%d')
# 		elif expected_date == u'今天+2周':
# 			delta = timedelta(days=7*2)
# 			expected = (now + delta).strftime('%Y-%m-%d')
# 		elif expected_date == u'今天+3天':
# 			delta = timedelta(days=3)
# 			expected = (now + delta).strftime('%Y-%m-%d')
# 		elif expected_date == u'今天+6天':
# 			delta = timedelta(days=3*2)
# 			expected = (now + delta).strftime('%Y-%m-%d')
# 		expecteds.append(expected)
#
# 	order_id = context.created_order_id
# 	order = Order.objects.get(order_id = order_id)
# 	order_has_delivery_times = OrderHasDeliveryTime.objects.filter(order_id = order.id)
# 	actual_dates = []
# 	for dates in order_has_delivery_times:
# 		actual_dates.append(dates.delivery_date.strftime('%Y-%m-%d'))
#
# 	bdd_util.assert_list(expecteds, actual_dates)