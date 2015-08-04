# -*- coding: utf-8 -*-

__author__ = 'chuter'

import urllib2
from urllib import urlencode
from urllib import unquote

from core.alipay.sign import md5_sign
from core.alipay.alipay_core import *
from core.alipay.alipay_config import *
from core.alipay.alipay_request_params import *

from account.models import UserAlipayOrderConfig
from watchdog.utils import watchdog_info
from BeautifulSoup import BeautifulSoup

class PCAlipaySubmit(object):
	TRADE_CREATE_SERVICE = 'create_direct_pay_by_user'
	PC_ALIPAY_GATEWAY = 'https://mapi.alipay.com/gateway.do'

	def __init__(self, pay_order, call_back_url, notify_url, user_profile):
		if not pay_order or not call_back_url or not notify_url or not user_profile:
			raise ValueError('pay_order, call_back_url, notify_url and user_profile can not be None neither')

		self.pay_order = pay_order
		self.total_pay = float(pay_order.total_price)
		self.call_back_url = call_back_url
		self.notify_url = notify_url

		user = user_profile.user
		try:
			self.alipay_config = UserAlipayOrderConfig.objects.get(owner=user)
		except:
			raise ValueError(u"不存在用户{}的阿里支付信息".format(user.username))

	def _build_trade_create_raw_request_param(self):
		params = {}
		params[AlipayRequestParams.INPUT_CHARSET] = self.alipay_config.input_charset
		params[AlipayRequestParams.OUT_TRADE_NO] = self.pay_order.order_id
		params[AlipayRequestParams.PARTNER] = self.alipay_config.partner
		params[AlipayRequestParams.SUBJECT] = self.pay_order.order_id
		params[AlipayRequestParams.NOTIFY_URL] = self.notify_url
		params[AlipayRequestParams.RETURN_URL] = self.call_back_url
		params[AlipayRequestParams.TOTAL_FEE] = self.total_pay
		params[AlipayRequestParams.SERVICE] = self.TRADE_CREATE_SERVICE
		params[AlipayRequestParams.SELLER_EMAIL] = self.alipay_config.seller_email
		params['payment_type'] = 1
		params['body'] = self.pay_order.order_id

#		params[AlipayRequestParams.SIGN_TYPE] = self.alipay_config.sign_type
#		params[AlipayRequestParams.SIGN] = self._build_request_sign(sign_source)

		return params


	def _build_request_param_with_sign(self, params):
		assert_param(params)

		# 除去请求参数中的空值和签名参数
		filltered_params = filter_alipay_request_params_to_build_sign(params)
		# 生成签名结果
		mysign = self._build_request_sign(filltered_params)
		# 签名结果与签名方式加入请求提交参数信息中
		filltered_params[AlipayRequestParams.SIGN] = mysign
		if params[AlipayRequestParams.SERVICE] == self.TRADE_CREATE_SERVICE:
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
		if res_data:
			res_data_soup = BeautifulSoup(res_data)
			return res_data_soup.request_token.text
		else:
			return ''

	def _build_request_sign(self, params):
		assert_param(params)

		link_str = create_link_str(params, self.alipay_config)
		if self.alipay_config.sign_type != 'MD5':
			raise ValueError('Only surpport md5 sign right now')

		return md5_sign(link_str, self.alipay_config.key)

	def _build_request_url(self, base_url, params):
		assert (base_url)
		assert_param(params)

		str_params = build_str_params(params, self.alipay_config)
		return "{}?{}".format(base_url, urlencode(str_params))

	def submit(self):
#		sign_source = self._generated_for_sign_string()
		auth_and_execute_requst_params = self._build_trade_create_raw_request_param()
		request_params_with_sign = self._build_request_param_with_sign(auth_and_execute_requst_params)
		return self._build_request_url(self.PC_ALIPAY_GATEWAY, request_params_with_sign)

#		request_params_with_sign = self._build_trade_create_raw_request_param(sign_source)
#		watchdog_info(u'pc alipay submit, sign_source: %s, params:%s, url: %s' %
#		                          (sign_source,  request_params_with_sign, self.PC_ALIPAY_GATEWAY))
#		return self._build_request_url(self.PC_ALIPAY_GATEWAY, request_params_with_sign)
