# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *

def __fill_post_data(pay_interface):
	data = {}
	data['description'] = pay_interface.get('description', '描述')
	data['is_active'] = "false" if pay_interface.get('is_active', '') == u'停用' else "true"

	type = pay_interface['type']
	if type == u'微信支付':
		version = pay_interface.get('version', 2)
		if version == 2: #v2
			data['type'] = PAY_INTERFACE_WEIXIN_PAY
			data['pay_version'] = 0
			data['app_id'] = pay_interface.get('weixin_appid', '1')
			data['partner_id'] = pay_interface.get('weixin_partner_id', '2')
			data['partner_key'] = pay_interface.get('weixin_partner_key', '3')
			data['paysign_key'] = pay_interface.get('weixin_sign', '4')
		else: #v3
			data['type'] = PAY_INTERFACE_WEIXIN_PAY
			data['pay_version'] = 1
			data['app_id'] = pay_interface.get('weixin_appid', '11')
			data['app_secret'] = '22'
			data['mch_id'] = '33' #mch_id
			data['api_key'] = '44' #api_key
			data['paysign_key'] = '55'
	elif type == u'支付宝':
		data['type'] = PAY_INTERFACE_ALIPAY
		data['partner'] = pay_interface.get('partner', '1')
		data['key'] = pay_interface.get('key', '2')
		data['ali_public_key'] = pay_interface.get('ali_public_key', '3')
		data['private_key'] = pay_interface.get('private_key', '4')
		data['seller_email'] = pay_interface.get('seller_email', '5@a.com')
	elif type == u'货到付款':
		data['type'] = PAY_INTERFACE_COD
	elif type == u'微众卡支付':
		data['type'] = PAY_INTERFACE_WEIZOOM_COIN
	else:
		pass

	return data
#
#
# def __add_pay_interface(context, pay_interface):
# 	data = __fill_post_data(pay_interface)
# 	db_pay_interface = PayInterface.objects.get(owner_id=context.webapp_owner_id, type=data['type'])
# 	pay_interface_id = db_pay_interface.id
# 	response = context.client.post('/mall/pay_interface/create/?id=%d' % pay_interface_id, data)
# 	return response

# @when(u"{user}添加支付方式")
# def step_impl(context, user):
# 	client = context.client
# 	pay_interfaces = json.loads(context.text)
# 	data = {}
# 	context.client.get('/mall/pay_interfaces/get/')
# 	is_only_one_pay_interface = len(pay_interfaces) == 1
# 	for pay_interface in pay_interfaces:
# 		__add_pay_interface(context, pay_interface)
# 		if is_only_one_pay_interface:
# 			break


# @given(u"{user}已添加了支付方式")
# def step_impl(context, user):
# 	"""与 '{user}已添加支付方式'重复 """
# 	#client = context.client
# 	pay_interfaces = json.loads(context.text)
# 	#data = {}
# 	context.client.get('/mall/pay_interfaces/get/')
# 	for pay_interface in pay_interfaces:
# 		__add_pay_interface(context, pay_interface)







'''
@then(u"{user}能获得支付方式列表")
def step_impl(context, user):
	expected = json.loads(context.text)
 	if expected['type'] == u'微信支付':
 		pay_interface_type = PAY_INTERFACE_WEIXIN_PAY
 	elif expected['type'] == u'货到付款':
 		pay_interface_type = PAY_INTERFACE_COD
 	elif expected['type'] == u'微众卡支付':
 		pay_interface_type = PAY_INTERFACE_WEIZOOM_COIN
 	elif expected['type'] == u'支付宝':
 		pay_interface_type = PAY_INTERFACE_ALIPAY

	url = "/mall2/pay_interface_list/"
	response = context.client.get(url)
	context = response.context
	pay_interfaces = context['pay_interfaces'] # 参考 pay_interface.py

	actual = []
	for interface in pay_interfaces:
		data = {
			'type': interface.name
		}
		actual.append(data)


	bdd_util.assert_dict(expected, actual)
'''


# @then(u"{user}能获得支付方式")
# def step_impl(context, user):
# 	url = '/mall/pay_interfaces/get/'
# 	response = context.client.get(url)
#
# 	expected = json.loads(context.text)
# 	if expected['type'] == u'微信支付':
# 		pay_interface_type = PAY_INTERFACE_WEIXIN_PAY
# 	elif expected['type'] == u'货到付款':
# 		pay_interface_type = PAY_INTERFACE_COD
# 	elif expected['type'] == u'微众卡支付':
# 		pay_interface_type = PAY_INTERFACE_WEIZOOM_COIN
# 	elif expected['type'] == u'支付宝':
# 		pay_interface_type = PAY_INTERFACE_ALIPAY
#
# 	db_pay_interface = PayInterface.objects.get(owner_id=context.webapp_owner_id, type=pay_interface_type)
# 	for pay_interface in response.context['pay_interfaces']:
# 		if pay_interface.type == pay_interface_type:
# 			target_pay_interface = pay_interface
# 			break
#
# 	actual = target_pay_interface
# 	actual.is_active = u'启用' if actual.is_active else u'停用'
#
# 	configs = {}
# 	if hasattr(actual, 'configs'):
# 		for actual_config in actual.configs:
# 			the_key = actual_config['name']
# 			the_value = actual_config['value']
# 			configs[the_key] = the_value
#
# 	if actual.type == PAY_INTERFACE_WEIXIN_PAY:
# 		actual.type = u'微信支付'
# 		actual.weixin_appid = configs[u"AppID"]
# 		actual.weixin_partner_id = configs[u"合作商户ID"]
# 		actual.weixin_partner_key = configs[u"合作商户密钥"]
# 		actual.weixin_sign = configs[u"支付专用签名串"]
# 	elif actual.type == PAY_INTERFACE_ALIPAY:
# 		actual.type = u'支付宝'
# 		actual.description = u'我的支付宝'
# 		actual.partner = configs[u'合作者身份ID']
# 		actual.key = configs[u'交易安全检验码']
# 		actual.ali_public_key = configs[u'支付宝公钥']
# 		actual.private_key = configs[u'商户私钥']
# 		actual.seller_email = configs[u'邮箱']
#
# 	elif actual.type == PAY_INTERFACE_COD:
# 		actual.type = u'货到付款'
# 	elif actual.type == PAY_INTERFACE_WEIZOOM_COIN:
# 		actual.type = u'微众卡支付'
# 	else:
# 		pass
#
# 	bdd_util.assert_dict(expected, actual)

# webapp端
@then(u"{user}无法获得支付方式'{pay_interface_type}'")
def step_impl(context, user, pay_interface_type):
	if pay_interface_type == u'微信支付':
		pay_interface_type = PAY_INTERFACE_WEIXIN_PAY
	elif pay_interface_type == u'支付宝':
		pay_interface_type = PAY_INTERFACE_ALIPAY
	elif pay_interface_type == u'货到付款':
		pay_interface_type = PAY_INTERFACE_COD
	elif pay_interface_type == u'微众卡支付':
		pay_interface_type = PAY_INTERFACE_WEIZOOM_COIN
	else:
		pass

	user_id = bdd_util.get_user_id_for(user)
	context.tc.assertEquals(0, PayInterface.objects.filter(owner_id=user_id, type=pay_interface_type).count())


# @then(u"{user}能获得支付方式列表")
# def step_impl(context, user):
# 	response = context.client.get('/mall2/pay_interfaces_list/')
#
# 	expected = json.loads(context.text)
# 	actual = list(response.context['pay_interfaces'])
# 	result = []
# 	for pay_interface in actual:
# 		if pay_interface.is_active:
# 			_actual = {}
# 			if pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
# 				_actual['type'] = u'微信支付'
# 			elif pay_interface.type == PAY_INTERFACE_COD:
# 				_actual['type'] = u'货到付款'
# 			elif pay_interface.type == PAY_INTERFACE_ALIPAY:
# 				_actual['type'] = u'支付宝'
# 			elif pay_interface.type == PAY_INTERFACE_WEIZOOM_COIN:
# 				_actual['type'] = u'微众卡支付'
# 			else:
# 				pass
# 			result.append(_actual)
#
# 	bdd_util.assert_list(expected, result)


# @then(u'{user}"{add_ability}"添加其他支付方式')
# def step_impl(context, user, add_ability):
# 	response = context.client.get('/mall/editor/mall_settings/')
# 	has_other_pay_interface = response.context['has_other_pay_interface']
#
# 	if add_ability == u'还能':
# 		context.tc.assertTrue(has_other_pay_interface)
# 	elif add_ability == u'不能':
# 		context.tc.assertFalse(has_other_pay_interface)
# 	else:
# 		assert False


# @given(u"{user}已添加支付方式")
# def step_impl(context, user):
# 	#client = context.client
# 	pay_interfaces = json.loads(context.text)
# 	#data = {}
# 	context.client.get('/mall/pay_interfaces/get/')
# 	for pay_interface in pay_interfaces:
# 		__add_pay_interface(context, pay_interface)

# 废弃
# @then(u"{user}添加支付方式时{is_can}使用'{pay_interface_type}'")
# def step_impl(context, user, is_can, pay_interface_type):
# 	response = context.client.get('/mall/pay_interface/create/')
# 	pay_interfaces = response.context['pay_interfaces']
#
# 	has_other_pay_interface = False
# 	for pay_interface in pay_interfaces:
# 		print(pay_interface)
# 		if pay_interface_type == PAYTYPE2NAME[pay_interface['type']]:
# 			has_other_pay_interface = True
# 	if is_can == u'可':
# 		context.tc.assertTrue(has_other_pay_interface)
# 	elif is_can == u'不可':
# 		context.tc.assertFalse(has_other_pay_interface)
# 	else:
# 		assert False
