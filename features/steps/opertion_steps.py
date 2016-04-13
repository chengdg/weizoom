# -*- coding: utf-8 -*-
import bdd_util
from card.models import *

@when(u"{user}批量激活订单'{id}'的卡")
def step_impl(context,user,id):
	order = WeizoomCardOrder.objects.get(order_number=id)
	data = {
		"orderId": order.id,
		"is_activation":0,
	}
	response = context.client.post('/order/api/rule_order/', data)
	bdd_util.assert_api_call_success(response)

@when(u"{user}批量停用订单'{id}'的卡")
def step_impl(context,user,id):
	order = WeizoomCardOrder.objects.get(order_number=id)
	data = {
		"orderId": order.id,
		"is_activation":1,
	}
	response = context.client.post('/order/api/rule_order/', data)
	bdd_util.assert_api_call_success(response)

@when(u"{user}取消订单'{id}'")
def step_impl(context,user,id):
	order = WeizoomCardOrder.objects.get(order_number=id)
	data = {
		"orderId": order.id,
		"status":0,
	}
	response = context.client.post('/order/api/rule_order/', data)
	bdd_util.assert_api_call_success(response)

# @then(u"{user}批量停用订单'{id}'的卡")
# def step_impl(context,user,id):
# 	data = {
# 		'orderId':id,
# 		'is_activation':1,
# 	}
# 	url = 'card/orders_list'
# 	response = context.client.get(url, data)
# 	bdd_util.assert_api_call_success(response)

# @then(u"{user}取消订单'{id}'")
# def step_impl(context,user,id):
# 	data = {
# 		'orderId': id,
# 		'is_activation':-1,
# 	}
# 	url = 'card/orders_list'
# 	response = context.client.get(url, data)
# 	bdd_util.assert_api_call_success(response)