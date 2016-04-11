# -*- coding: utf-8 -*-
@then(u"{user}批量激活订单'{id}'的卡")
def step_impl(context,user,id):
	data = {
		'orderId': id,
		'is_activation':0,
	}
	url = 'card/orders_list'
	response = context.client.get(url, data)
	bdd_util.assert_api_call_success(response)

@then(u"{user}批量停用订单'{id}'的卡")
def step_impl(context,user,id):
	data = {
		'orderId':id,
		'is_activation':1,
	}
	url = 'card/orders_list'
	response = context.client.get(url, data)
	bdd_util.assert_api_call_success(response)

@then(u"{user}取消订单'{id}'")
def step_impl(context,user,id):
	data = {
		'orderId': id,
		'is_activation':-1,
	}
	url = 'card/orders_list'
	response = context.client.get(url, data)
	bdd_util.assert_api_call_success(response)