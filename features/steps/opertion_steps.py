@then(u"'{user}'批量激活订单'{order_number}'卡片")
def step_impl(context,user):
	weizoomcardorder = WeizoomCardOrder(order_number=order_number)
	data = {
		'orderId': weizoomcardorder.id,
		'is_activation':0,
	}
	url = 'card/orders_list'
	response = context.client.get(url, data)
	bdd_util.assert_api_call_success(response)

@then(u"'{user}'批量停用订单'{order_number}'卡片")
def step_impl(context,user):
	weizoomcardorder = WeizoomCardOrder(order_number=order_number)
	data = {
		'orderId': weizoomcardorder.id,
		'is_activation':1,
	}
	url = 'card/orders_list'
	response = context.client.get(url, data)
	bdd_util.assert_api_call_success(response)

@then(u"'{user}'取消订单'{order_number}'")
def step_impl(context,user):
	weizoomcardorder = WeizoomCardOrder(order_number=order_number)
	data = {
		'orderId': weizoomcardorder.id,
		'is_activation':-1,
	}
	url = 'card/orders_list'
	response = context.client.get(url, data)
	bdd_util.assert_api_call_success(response)