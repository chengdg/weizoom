# -*- coding: utf-8 -*-

__author__ = 'chuter'

import urllib2
from urllib import urlencode
from urllib import unquote

from django.conf import settings

from sign import md5_sign
from alipay_core import *
from alipay_config import *
from alipay_request_params import *

from account.models import UserAlipayOrderConfig

from BeautifulSoup import BeautifulSoup

class RealAlipaySubmit(object):
	TRADE_CREATE_SERVICE = 'alipay.wap.trade.create.direct'
	AUTH_AND_EXECUTE_SERVICE = 'alipay.wap.auth.authAndExecute'
	ALIPAY_GATEWAY = 'http://wappaygw.alipay.com/service/rest.htm'

	FORMAT = 'xml'
	V = '2.0'

	def __init__(self, config_id, pay_order, call_back_url, notify_url):
		if not pay_order or not call_back_url or not notify_url:
			raise ValueError('pay_order, call_back_url, notify_url can not be None neither')

		self.pay_order = pay_order
		self.total_pay = float(pay_order.final_price)
		self.call_back_url = call_back_url
		self.notify_url = notify_url
		self.config_id = config_id

		try:
			"""
				TODO:
					修改表结构 对应 webapp_id
			"""
			self.alipay_config = UserAlipayOrderConfig.objects.get(id=config_id)
		except:
			raise ValueError(u"不存在id为{}的阿里支付信息".format(config_id))

	def _build_trade_create_raw_request_param(self):
		params = {}
		params[AlipayRequestParams.SERVICE] = self.TRADE_CREATE_SERVICE
		params[AlipayRequestParams.PARTNER] = self.alipay_config.partner
		params[AlipayRequestParams.INPUT_CHARSET] = self.alipay_config.input_charset
		params[AlipayRequestParams.SEC_ID] = self.alipay_config.sign_type
		params[AlipayRequestParams.FORMAT] = self.FORMAT
		params[AlipayRequestParams.V] = self.V
		params[AlipayRequestParams.REQ_ID] = self.pay_order.order_id

		req_data_token = """
		<direct_trade_create_req>
		<notify_url>{}</notify_url>
		<call_back_url>{}</call_back_url>
		<seller_account_name>{}</seller_account_name>
		<out_trade_no>{}</out_trade_no>
		<subject>{}</subject>
		<total_fee>{}</total_fee>
		<merchant_url></merchant_url>
		</direct_trade_create_req>
		""".format(self.notify_url, self.call_back_url, self.alipay_config.seller_email, \
			self.pay_order.order_id, self.pay_order.order_id, str(self.total_pay))

		params[AlipayRequestParams.REQ_DATA] = req_data_token

		return params

	def _build_auth_and_execute_raw_request_param(self, token):
		assert (token)

		params = {}
		params[AlipayRequestParams.SERVICE] = self.AUTH_AND_EXECUTE_SERVICE
		params[AlipayRequestParams.PARTNER] = self.alipay_config.partner
		params[AlipayRequestParams.INPUT_CHARSET] = self.alipay_config.input_charset
		params[AlipayRequestParams.SEC_ID] = self.alipay_config.sign_type
		params[AlipayRequestParams.FORMAT] = self.FORMAT
		params[AlipayRequestParams.V] = self.V
		
		req_data = "<auth_and_execute_req><request_token>{}</request_token></auth_and_execute_req>".format(token)

		params[AlipayRequestParams.REQ_DATA] = req_data

		return params

	def _build_request_sign(self, params):
		assert_param(params)

		link_str = create_link_str(params, self.alipay_config)
		if self.alipay_config.sign_type != 'MD5':
			raise ValueError('Only surpport md5 sign right now')

		return md5_sign(link_str, self.alipay_config.key)


	def _build_request_param_with_sign(self, params):
		assert_param(params)

		# 除去请求参数中的空值和签名参数
		filltered_params = filter_alipay_request_params_to_build_sign(params)
		# 生成签名结果
		mysign = self._build_request_sign(filltered_params)
		# 签名结果与签名方式加入请求提交参数信息中
		filltered_params[AlipayRequestParams.SIGN] = mysign
		if params[AlipayRequestParams.SERVICE] != self.TRADE_CREATE_SERVICE and \
			params[AlipayRequestParams.SERVICE] != self.AUTH_AND_EXECUTE_SERVICE:
			filltered_params[AlipayRequestParams.SIGN_TYPE] = self.alipay_config.sign_type

		return filltered_params

	def _extract_token_from_response(self, response_data):
		assert (response_data)

		# 以“&”字符切割字符串
		name_value_pairs = response_data.split('&')
		# 把切割后的字符串数组变成变量与数值组合的字典数组
		params = {}
		for name_value_pair in name_value_pairs:
			# 获得第一个=字符的位置
			pos = name_value_pair.find('=')
			name = name_value_pair[:pos]
			value = name_value_pair[pos+1:]
			params[name] = value

		res_data = params[AlipayRequestParams.RES_DATA]
		res_data_soup = BeautifulSoup(res_data)
		return res_data_soup.request_token.text

	def _get_token(self):
		trade_create_request_params = self._build_trade_create_raw_request_param()
		request_params_with_sign = self._build_request_param_with_sign(trade_create_request_params)
		request_url = self._build_request_url(self.ALIPAY_GATEWAY, request_params_with_sign)

		response_data = None
		response = None
		try:
			req = urllib2.Request(request_url)
			response = urllib2.urlopen(req)
			response_data = response.read()
		finally:
			if response:
				try:
					response.close()
				except:
					pass

		assert (response_data)

		# 对支付宝结果进行url decode
		response_data = unquote(response_data).decode(self.alipay_config.input_charset)

		try:
			return self._extract_token_from_response(response_data)
		except:
			raise ValueError(u"请求token时支付宝报错，order_id={}, UserAlipayOrderConfig_id={}\n返回结果：\n{}".format(self.pay_order.order_id, self.config_id, response_data))

	def _build_request_url(self, base_url, params):
		assert (base_url)
		assert_param(params)
		
		str_params = build_str_params(params, self.alipay_config)
		return "{}?{}".format(base_url, urlencode(str_params))

	def submit(self):
		token = self._get_token()

		auth_and_execute_requst_params = self._build_auth_and_execute_raw_request_param(token)
		request_params_with_sign = self._build_request_param_with_sign(auth_and_execute_requst_params)
		return self._build_request_url(self.ALIPAY_GATEWAY, request_params_with_sign)


class MockAlipaySubmit(object):
	def __init__(self, config_id, pay_order, call_back_url, notify_url):
		self.config_id = config_id
		self.order_id = pay_order.order_id
		self.price = pay_order.final_price
		self.call_back_url = call_back_url.replace('weapp.weizoom.com', settings.DOMAIN)
		
	def submit(self):
		return 'http://pay.weapp.com:8003/mockapi/alipay/do_pay/?config_id=%d&order_id=%s&price=%s&call_back_url=%s' % (self.config_id, self.order_id, self.price, self.call_back_url)


#根据模式切换AlipaySubmit的实现
if settings.USE_MOCK_PAY_API:
	AlipaySubmit = MockAlipaySubmit
else:
	AlipaySubmit = RealAlipaySubmit
