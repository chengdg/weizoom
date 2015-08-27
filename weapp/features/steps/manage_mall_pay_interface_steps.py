# -*- coding: utf-8 -*-

from behave import when, then, given
from features.testenv.model_factory import json

from test import bdd_util
from mall.models import PayInterface, PAY_INTERFACE_WEIXIN_PAY, PAY_INTERFACE_ALIPAY, PAY_INTERFACE_COD, \
	PAY_INTERFACE_WEIZOOM_COIN
import steps_db_util


@when(u"{user}添加支付方式")
def step_impl(context, user):
	client = context.client
	pay_interfaces = json.loads(context.text)
	data = {}
	context.client.get('/mall2/pay_interface_list/')
	is_only_one_pay_interface = len(pay_interfaces) == 1
	for pay_interface in pay_interfaces:
		__add_pay_interface(context, pay_interface)
		if is_only_one_pay_interface:
			break


@given(u"{user}已添加了支付方式")
def step_impl(context, user):
	"""与 '{user}已添加支付方式'重复 """
	# client = context.client
	pay_interfaces = json.loads(context.text)
	# data = {}
	context.client.get('/mall2/pay_interface_list/')
	for pay_interface in pay_interfaces:
		__add_pay_interface(context, pay_interface)


@then(u"{user}能获得支付方式")
def step_impl(context, user):
	"""
	列出支付方式的详细信息
	"""
	url = '/mall2/pay_interface_list/'
	response = context.client.get(url)
	print("pay_interface_list: {}".format(response.context['pay_interfaces']))

	expected = json.loads(context.text)
	if expected['type'] == u'微信支付':
		pay_interface_type = PAY_INTERFACE_WEIXIN_PAY
	elif expected['type'] == u'货到付款':
		pay_interface_type = PAY_INTERFACE_COD
	elif expected['type'] == u'微众卡支付':
		pay_interface_type = PAY_INTERFACE_WEIZOOM_COIN
	elif expected['type'] == u'支付宝':
		pay_interface_type = PAY_INTERFACE_ALIPAY

	target_pay_interface = None
	for pay_interface in response.context['pay_interfaces']:
		if pay_interface.type == pay_interface_type:
			target_pay_interface = pay_interface
			break

	actual = target_pay_interface
	actual.is_active = u'启用' if actual.is_active else u'停用'

	configs = {}
	if hasattr(actual, 'configs'):
		for actual_config in actual.configs:
			the_key = actual_config['name']
			the_value = actual_config['value']
			configs[the_key] = the_value

	if actual.type == PAY_INTERFACE_WEIXIN_PAY:
		actual.type = u'微信支付'
		actual.weixin_appid = configs[u"AppID"]
		actual.weixin_partner_id = configs[u"合作商户ID"]
		actual.weixin_partner_key = configs[u"合作商户密钥"]
		actual.weixin_sign = configs[u"支付专用签名串"]
	elif actual.type == PAY_INTERFACE_ALIPAY:
		actual.type = u'支付宝'
		actual.description = u'我的支付宝'
		actual.partner = configs[u'合作者身份ID']
		actual.key = configs[u'交易安全检验码']
		actual.ali_public_key = configs[u'支付宝公钥']
		actual.private_key = configs[u'商户私钥']
		actual.seller_email = configs[u'邮箱']

	elif actual.type == PAY_INTERFACE_COD:
		actual.type = u'货到付款'
	elif actual.type == PAY_INTERFACE_WEIZOOM_COIN:
		actual.type = u'微众卡支付'
	else:
		pass

	print("expected: {}".format(expected))
	print("actual: {}".format(actual))

	bdd_util.assert_dict(expected, actual)


def __name_to_type(name):
	"""
	将支付方式的名字转成ID
	"""
	pay_interface_type = None
	if name == u'微信支付':
		pay_interface_type = PAY_INTERFACE_WEIXIN_PAY
	elif name == u'货到付款':
		pay_interface_type = PAY_INTERFACE_COD
	elif name == u'微众卡支付':
		pay_interface_type = PAY_INTERFACE_WEIZOOM_COIN
	elif name == u'支付宝':
		pay_interface_type = PAY_INTERFACE_ALIPAY
	return pay_interface_type


def __type_to_name(type_id):
	"""
	将type ID转成名字
	"""
	name = None
	if type_id == PAY_INTERFACE_WEIXIN_PAY:
		name = u'微信支付'
	elif type_id == PAY_INTERFACE_COD:
		name = u'货到付款'
	elif type_id == PAY_INTERFACE_ALIPAY:
		name = u'支付宝'
	elif type_id == PAY_INTERFACE_WEIZOOM_COIN:
		name = u'微众卡支付'
	return name	


@then(u"{user}能获得支付方式列表")
def step_impl(context, user):
	"""
	只列出有效的支付方式列表
	"""
	expected = json.loads(context.text)

	response = context.client.get('/mall2/pay_interface_list/')
	interfaces = list(response.context['pay_interfaces'])
	result = []
	for pay_interface in interfaces:
		if pay_interface.is_active:
			_actual = {
				'type': __type_to_name(pay_interface.type)
			}
			result.append(_actual)
			
	print("expected: {}".format(expected))
	print("actual: {}".format(result))
	bdd_util.assert_list(expected, result)

@then(u"{user}获取全部支付方式列表")
def step_impl(context, user):
	"""
	只列出支付方式列表
	"""
	expected = json.loads(context.text)

	response = context.client.get('/mall2/pay_interface_list/')
	interfaces = list(response.context['pay_interfaces'])
	result = []
	for pay_interface in interfaces:
		_actual = {
			'type': __type_to_name(pay_interface.type),
			'is_active': u"启用" if pay_interface.is_active else u"停用"
		}
		result.append(_actual)
			
	print("expected: {}".format(expected))
	print("actual: {}".format(result))
	bdd_util.assert_list(expected, result)

@given(u"{user}已添加支付方式")
def step_impl(context, user):
	# client = context.client
	pay_interfaces = json.loads(context.text)
	# data = {}
	context.client.get('/mall2/pay_interface_list/')
	for pay_interface in pay_interfaces:
		__add_pay_interface(context, pay_interface)


def __fill_post_data(pay_interface):
	data = {}
	data['description'] = pay_interface.get('description', '描述')
	data['is_active'] = "false" if pay_interface.get('is_active', '') == u'停用' else "true"

	type = pay_interface['type']
	if type == u'微信支付':
		version = pay_interface.get('version', 2)
		if version == 2:  # v2
			data['type'] = PAY_INTERFACE_WEIXIN_PAY
			data['pay_version'] = 0
			data['app_id'] = pay_interface.get('weixin_appid', '1')
			data['partner_id'] = pay_interface.get('weixin_partner_id', '2')
			data['partner_key'] = pay_interface.get('weixin_partner_key', '3')
			data['paysign_key'] = pay_interface.get('weixin_sign', '4')
		else:  # v3
			data['type'] = PAY_INTERFACE_WEIXIN_PAY
			data['pay_version'] = 1
			data['app_id'] = pay_interface.get('weixin_appid', '11')
			data['app_secret'] = '22'
			data['mch_id'] = '33'  # mch_id
			data['api_key'] = '44'  # api_key
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


def __add_pay_interface(context, pay_interface):
	data = __fill_post_data(pay_interface)
	db_pay_interface = steps_db_util.get_pay_interface(context.webapp_owner_id, type=data['type'])
	pay_interface_id = db_pay_interface.id
	response = context.client.post('/mall2/pay_interface/?id=%d&_method=put' % pay_interface_id, data)

	return response



@when(u"{user}更新支付方式'{pay_interface_name}'")
def step_impl(context, user, pay_interface_name):
	data = json.loads(context.text)

	pay_interface_type = __name_to_type(pay_interface_name)
	owner_id = bdd_util.get_user_id_for(user)
	# 按照名字获取ID
	interface = PayInterface.objects.get(owner_id=owner_id, type=pay_interface_type)

	#response = context.client.get('/mall2/pay_interface/', {'id': interface.id})
	#pay_interface = response.context['pay_interface'] # 参考pay_interface.py
	param = {}
	if pay_interface_type == PAY_INTERFACE_WEIXIN_PAY:
		# 微信支付
		#weixin_pay_config = pay_interface.related_config
		param['type'] = pay_interface_type
		param['app_id'] = data['weixin_appid']
		param['partner_id'] = data['weixin_partner_id']
		param['partner_key'] = data['weixin_partner_key']
		param['paysign_key'] = data['weixin_sign']
		if 'version' in data:
			param["pay_version"] = 0 if data['version'] == 'V2' else 1 # V3=>1
	response = context.client.post('/mall2/pay_interface/?id=%d' % interface.id, param)

@when(u"{user}\"{action}\"支付方式\"{pay_interface_name}\"")
def step_impl(context, user, action, pay_interface_name):
	"""
	停用/开启支付方式
	"""
	pay_interface_type = __name_to_type(pay_interface_name)
	owner_id = bdd_util.get_user_id_for(user)
	# 按照名字获取ID
	interface = PayInterface.objects.get(owner_id=owner_id, type=pay_interface_type)

	is_enable = None
	if action == u"开启":
		is_enable = True
	elif action == u"停用":
		is_enable = False
	param = {
		"id": interface.id,
		"is_enable": is_enable
	}

	response = context.client.post('/mall2/api/pay_interface/', param)
	bdd_util.assert_api_call_success(response)
