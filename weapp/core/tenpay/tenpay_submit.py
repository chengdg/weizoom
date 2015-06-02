# -*- coding: utf-8 -*-

__author__ = 'chuter'

import urllib2
from urllib import urlencode
from urllib import unquote

from django.conf import settings

from sign import md5_sign
from tenpay_core import *
from tenpay_config import *
from tenpay_request_params import *

from account.models import UserTenpayOrderConfig

from BeautifulSoup import BeautifulSoup

class RealTenpaySubmit(object):

	TENPAY_GATEWAY = 'https://gw.tenpay.com/gateway/pay.htm'

	V = '1.0'

	def __init__(self, config_id, pay_order, call_back_url, notify_url):
		if not pay_order or not call_back_url or not notify_url:
			raise ValueError('pay_order, call_back_url, notify_url can not be None neither')

		self.pay_order = pay_order
		self.total_pay = int(float(pay_order.final_price) * 100) #以分为单位
		self.call_back_url = call_back_url
		self.notify_url = notify_url

		try:
			self.tenpay_config = UserTenpayOrderConfig.objects.get(id=config_id)
		except:
			raise ValueError(u"不存在id为{}的财付通支付信息".format(config_id))
		# self.tenpay_config = TenpayConfig

	def _build_pay_request_request_param_without_sign(self):
		params = {}

		params[TenpayRequestParams.PARTNER] = self.tenpay_config.partner
		params[TenpayRequestParams.INPUT_CHARSET] = self.tenpay_config.input_charset

		params[TenpayRequestParams.CALL_BACK_URL] = self.call_back_url
		params[TenpayRequestParams.NOTIFY_URL] = self.notify_url
		params[TenpayRequestParams.BODY] = self.pay_order.order_id
		params[TenpayRequestParams.OUT_TRADE_NO] = self.pay_order.order_id
		params[TenpayRequestParams.TOTAL_FEE] = self.total_pay
		params[TenpayRequestParams.SPBILL_CREATE_IP] = '.'

		return params

	def _build_request_sign(self, params):
		assert_param(params)

		link_str = create_link_str(params)
		if self.tenpay_config.sign_type != 'MD5':
			raise ValueError('Only surpport md5 sign right now')

		return md5_sign(link_str, self.tenpay_config.key)


	def _build_request_param_with_sign(self, params):
		assert_param(params)

		# 除去请求参数中的空值和签名参数
		filltered_params = filter_tenpay_request_params_to_build_sign(params)
		# 生成签名结果
		mysign = self._build_request_sign(filltered_params)
		# 签名结果与签名方式加入请求提交参数信息中
		filltered_params[TenpayRequestParams.SIGN] = mysign

		return filltered_params

	def _build_request_url(self, base_url, params):
		assert (base_url)
		assert_param(params)
		
		str_params = build_str_params(params)
		return "{}?{}".format(base_url, urlencode(str_params))

	def submit(self):
		request_params = self._build_pay_request_request_param_without_sign()
		request_params_with_sign = self._build_request_param_with_sign(request_params)

		return self._build_request_url(self.TENPAY_GATEWAY, request_params_with_sign)


class MockTenpaySubmit(object):
	def __init__(self, config_id, pay_order, call_back_url, notify_url):
		self.config_id = config_id
		self.order_id = pay_order.order_id
		self.price = pay_order.final_price
		self.call_back_url = call_back_url.replace('weapp.weizoom.com', settings.DOMAIN)
		
	def submit(self):
		return 'http://pay.weapp.com:8003/mockapi/tenpay/pay/?config_id=%d&order_id=%s&price=%s&call_back_url=%s' % (self.config_id, self.order_id, self.price, self.call_back_url)



#根据模式切换TenpaySubmit的实现
if settings.USE_MOCK_PAY_API:
	TenpaySubmit =  MockTenpaySubmit
else:
	TenpaySubmit = RealTenpaySubmit

# class DummyOrder(object):
# 	def __init__(self):
# 		self.order_id = '1234567891'
# 		self.final_price = 0.01

# submit = RealTenpaySubmit(DummyOrder(), 'http://www.babydami.com', 'http://www.babydami.com', 'None')
# print submit.submit()