# -*- coding: utf-8 -*-
import json
import time
import urllib

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *


@then(u'{webapp_user_name}在webapp中能使用以下支付方式')
def step_impl(context, webapp_user_name):
	url = '/workbench/jqm/preview/?woid=%s&module=mall&model=pay_interfaces&action=list&order_id=0&ignore_template=1' % context.webapp_owner_id
	response = context.client.get(bdd_util.nginx(url), follow=True)
	pay_interfaces = response.context['pay_interfaces']

	expected = json.loads(context.text)
	actual = [pay_interface.name for pay_interface in pay_interfaces]
	bdd_util.assert_list(expected, actual)


def __get_js_value_from_html_page(html_page, variable):
	pos = html_page.find(variable)
	beg = html_page.find('"', pos)
	end = html_page.find('"', beg+1)
	return html_page[beg+1:end]


WEIXIN_PAY_NOTIFY_POST_DATA = """
<xml>
	<OpenId><![CDATA[111222]]></OpenId>
	<AppId><![CDATA[%(appid)s]]></AppId>
	<IsSubscribe>1</IsSubscribe>
	<TimeStamp>1369743511</TimeStamp>
	<NonceStr><![CDATA[abcdefg]]></NonceStr>
	<AppSignature><![CDATA[1234567890]]></AppSignature>
	<SignMethod><![CDATA[sha1]]></SignMethod>
</xml>
"""


def __do_weixin_pay(context, pay_url):
	pay_url = '{}&code={}'.format(pay_url, time.time())

	pay_url_response = context.client.get(pay_url, follow=True)
	html_page = pay_url_response.content

	is_sync = True
	if context.text != None:
		pay_info = json.loads(context.text)
		is_sync = pay_info['is_sync']

	if is_sync:
		#同步支付
		pay_interface_type = __get_js_value_from_html_page(html_page, 'var payInterfaceType')
		order_id = __get_js_value_from_html_page(html_page, 'var orderId')
		webapp_owner_id = __get_js_value_from_html_page(html_page, 'var webappOwnerId')
		related_config_id = __get_js_value_from_html_page(html_page, 'var payInterfaceRelatedConfigId')
		url = '/termite/workbench/jqm/preview/?module=mall&model=pay_result&action=get&pay_interface_type=%s&order_id=%s&order_id=%s&woid=%s&related_config_id=%s' % (pay_interface_type, order_id, order_id, webapp_owner_id, related_config_id)
		return url
	else:
		#异步支付
		app_id = __get_js_value_from_html_page(html_page, "var appId")
		order_id = __get_js_value_from_html_page(html_page, 'var orderId')
		domain = __get_js_value_from_html_page(html_page, 'var domain')
		webapp_owner_id = __get_js_value_from_html_page(html_page, 'var webappOwnerId')
		related_config_id = __get_js_value_from_html_page(html_page, 'var payInterfaceRelatedConfigId')
		notify_url = "http://%s/wxpay/mall/pay_notify_result/get/%s/%s/?transaction_id=123321&trade_state=0&out_trade_no=%s&pay_info=" % (domain, webapp_owner_id, related_config_id, order_id)
		client = Client()
		data = WEIXIN_PAY_NOTIFY_POST_DATA % {"appid":app_id}
		notify_url_response = client.post(notify_url, data, "application/xml")
		assert 200 == notify_url_response.status_code
		assert 'success' ==  notify_url_response.content.strip()
		return None



@when(u"{webapp_user_name}使用支付方式'{pay_interface_name}'进行支付")
def step_impl(context, webapp_user_name, pay_interface_name):
	order = Order.objects.get(order_id=context.created_order_id)
	data = {
		"webapp_owner_id": context.webapp_owner_id,
		"module": "mall",
		"target_api": "order/pay",
		"order_id": order.id
	}
	from mall.models import PayInterface, PAYTYPE2NAME
	pay_interfaces = PayInterface.objects.all()

	for pay_interface in pay_interfaces:
		if PAYTYPE2NAME[pay_interface.type] != pay_interface_name:
			continue

		data.setdefault('interface_type', pay_interface.type)
		data.setdefault('interface_id', pay_interface.id)
		break

	url = '/webapp/api/project_api/call/'
	response = context.client.post(url, data)
	bdd_util.assert_api_call_success(response)

	# if pay_interface.type == PAY_INTERFACE_WEIZOOM_COIN:
	# 	_pay_weizoom_card(context, data, order)
	if pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
		response_data = json.loads(response.content)['data']
		pay_url = response_data['url']
		pay_result_url = __do_weixin_pay(context, pay_url)
		if pay_result_url:
			context.client.get(pay_result_url, follow=True)
	elif pay_interface.type == PAY_INTERFACE_COD:
		response_data = json.loads(response.content)['data']
		context.pay_result_url = response_data['url']
		url = '/workbench/jqm/preview/%s' % context.pay_result_url[2:]
		response = context.client.get(bdd_util.nginx(url), follow=True)
		context.pay_result = response.context
	# 直接修改数据库的订单状态
	elif pay_interface.type == PAY_INTERFACE_ALIPAY:#ali
		url = '/termite/workbench/jqm/preview/?module=mall&model=pay_result&action=get&pay_interface_type=%s&out_trade_no=%s&woid=%s&result=success' % (data['interface_type'], order.order_id, context.webapp_owner_id)
		context.client.get(bdd_util.nginx(url), follow=True)

	if hasattr(context, 'order_payment_time'):
		order.payment_time = context.order_payment_time
		order.save()

	context.pay_order_id = order.order_id

@when(u"{webapp_user_name}使用支付方式'{pay_interface_name}'进行支付订单'{order_code}'")
def step_impl(context, webapp_user_name, pay_interface_name, order_code):
	context.created_order_id = order_code
	context.execute_steps(u"when %s使用支付方式'%s'进行支付" % (webapp_user_name,pay_interface_name))

@when(u"{webapp_user_name}使用支付方式'{pay_interface_name}'进行支付订单'{order_code}'于{payment_time}")
def step_impl(context, webapp_user_name, pay_interface_name, order_code, payment_time):
	context.created_order_id = order_code
	context.order_payment_time = payment_time
	context.execute_steps(u"when %s使用支付方式'%s'进行支付" % (webapp_user_name,pay_interface_name))

# @then(u"{webapp_user_name}支付订单成功")
# def step_impl(context, webapp_user_name):
# 	order, order_has_products = _get_order_has_products(context)
#
# 	actual_order = order
# 	actual_order.ship_area = actual_order.area
# 	actual_order.status = ORDERSTATUS2TEXT[actual_order.status]
# 	actual_order.pay_interface_type = PAYTYPE2NAME[actual_order.pay_interface_type]
#
# 	#获取order的products
# 	actual_order.products = []
# 	for relation in order_has_products:
# 		product = relation.product
# 		product.count = relation.number
# 		product.fill_specific_model('standard')
# 		actual_order.products.append(product)
#
# 	expected = json.loads(context.text)
#
# 	bdd_util.assert_dict(expected, actual_order)
#
# def _get_order_has_products(context):
# 	order = Order.objects.get(order_id=context.pay_order_id)
# 	order_has_products = None
# 	if hasattr(context.response, 'order_has_products'):
# 		order_has_products = context.response.context['order_has_products']
# 	else:
# 		order_has_products = OrderHasProduct.objects.filter(order=order)
# 	return order, order_has_products

def _pay_weizoom_card(context, data, order):
	url = '/webapp/api/project_api/call/'
	card = json.loads(context.text)

	# 1.根据卡号密码获取id
	data['target_api'] = 'weizoom_card/check'
	data['name'] = card['id']
	data['password'] = card['password']
	response = context.client.post(url, data)
	response_json = json.loads(response.content)
	if response_json['code'] == 200:
		card_id = response_json['data']['id']
	else:
		return False

	# 2.确认支付
	data['target_api'] = 'weizoom_card/pay'
	data['card_id'] = card_id
	data['order_id'] = order.order_id
	del data['name']
	del data['password']
	response = context.client.post(url, data)
	response_json = json.loads(response.content)


# @then(u"{webapp_user_name}查看订单")
# def step_impl(context, webapp_user_name):
# 	actual_order = {}
#
# 	if hasattr(context, 'pay_order_id'):
# 		order, order_has_products = _get_order_has_products(context)
#
# 		actual_order = order
# 		actual_order.ship_area = actual_order.area
# 		actual_order.status = ORDERSTATUS2TEXT[actual_order.status]
# 		actual_order.pay_interface_type = PAYTYPE2NAME[actual_order.pay_interface_type]
#
# 		#获取order的products
# 		actual_order.products = []
# 		for relation in order_has_products:
# 			product = relation.product
# 			product.count = relation.number
# 			product.fill_specific_model('standard')
# 			actual_order.products.append(product)
#
# 	expected = json.loads(context.text)
#
# 	bdd_util.assert_dict(expected, actual_order)
