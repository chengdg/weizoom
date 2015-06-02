# -*- coding: utf-8 -*-
"""@package pay.ali.api.api_pay_token
获取token API

HTTP请求方式: GET

URL: `http://wappaygw.alipay.com/service/rest.htm`

参数信息:

| 参数  | 必需 | 说明 |
| :----------- | :---: | :-------------------------------------------- |
| partner | 是 | 合作者身份ID |
| key | 是 | 安全校验码 |
| input_charset | 是 | 编码  |
| sign_type | 是 | 签名方式 |
| seller_email | 是 | 支付宝账号 |
| order_id | 是 | 订单号 |
| total_pay | 是 | 交易总金额 |
| notify_url | 是 | 异步通知页面路径 |
| call_back_url | 是 | 支付成功跳转页面路径 |
"""

__author__ = 'slzhu'

import api_settings

from alipay_core import *

class TokenMessage(object):
	def __init__(self, partner, key, input_charset, sign_type, seller_email, order_id, total_pay, notify_url, call_back_url):
		if partner == None or partner == '':
			raise ValueError(u'partner con not be none or ""')
		
		if key == None or key == '':
			raise ValueError(u'key con not be none or ""')

		if input_charset == None or input_charset == '':
			raise ValueError(u'input_charset con not be none or ""')
		
		if sign_type == None or sign_type == '':
			raise ValueError(u'sign_type con not be none or ""')
				
		if seller_email == None or seller_email == '':
			raise ValueError(u'seller_email con not be none or ""')
		
		if order_id == None or order_id == '':
			raise ValueError(u'order_id con not be none or ""')
		
		if total_pay == None or total_pay == '':
			raise ValueError(u'total_pay con not be none or ""')
		
		if notify_url == None or notify_url == '':
			raise ValueError(u'notify_url con not be none or ""')
		
		if call_back_url == None or call_back_url == '':
			raise ValueError(u'call_back_url con not be none or ""')
		
		self.partner = partner
		self.key = key
		self.input_charset = input_charset
		self.sign_type = sign_type
		self.seller_email = seller_email
		self.order_id = order_id
		self.total_pay = total_pay
		self.notify_url = notify_url
		self.call_back_url = call_back_url
	
	def get_message_json_str(self):
		return None


class AliPayTokenApi(object):
	
	def get_get_request_url_and_api_info(self, varargs=()):
		if len(varargs) >= 3 or len(varargs) == 0:
			raise ValueError(u'AliPayTokenApi.get_get_request_url error, param illegal')
		
		params = {}
		params[AlipayRequestParams.PARTNER] = varargs[0].partner
		params['key'] = varargs[0].key
		params[AlipayRequestParams.INPUT_CHARSET] = varargs[0].input_charset
		params[AlipayRequestParams.SEC_ID] = varargs[0].sign_type
		params[AlipayRequestParams.REQ_ID] = varargs[0].order_id
		params[AlipayRequestParams.REQ_DATA] = """
			<direct_trade_create_req>
			<notify_url>{}</notify_url>
			<call_back_url>{}</call_back_url>
			<seller_account_name>{}</seller_account_name>
			<out_trade_no>{}</out_trade_no>
			<subject>{}</subject>
			<total_fee>{}</total_fee>
			<merchant_url></merchant_url>
			</direct_trade_create_req>
			""".format(varargs[0].notify_url, varargs[0].call_back_url, varargs[0].seller_email, \
					varargs[0].order_id, varargs[0].order_id, str(varargs[0].total_pay))
		
		params[AlipayRequestParams.SERVICE] = api_settings.TRADE_CREATE_SERVICE
		params[AlipayRequestParams.FORMAT] = api_settings.FORMAT
		params[AlipayRequestParams.V] = api_settings.V
		
		request_params_with_sign = build_request_param_with_sign(params)
		
		return build_request_url(api_settings.ALIPAY_GATEWAY, request_params_with_sign), u'获取token接口api'

	def parse_response(self, api_response):
		return api_response

	###############################################################################
	#	args 参数：args = custom_msg_instance
	###############################################################################
	def parese_post_param_json_str(self, args):
		
		if isinstance(args[0], TokenMessage) is False:
			raise ValueError(u'AliPayTokenApi param TokenMessage illegal')			

		return args[0].get_message_json_str()

	def request_method(self):
		return api_settings.API_GET