# -*- coding: utf-8 -*-

__author__ = 'chuter'

import urllib2 

from urllib import unquote
from BeautifulSoup import BeautifulSoup

from alipay_config import *
from alipay_request_params import *

from account.models import UserAlipayOrderConfig
from watchdog.utils import watchdog_error, watchdog_info
from core.exceptionutil import full_stack

class AlipayNotify(object):
	ALIPAY_VERIFY_URL_TMPL = "https://mapi.alipay.com/gateway.do?service=notify_verify&partner={}&notify_id={}"
	NOTIFY_DATA_PARAM_NAME = 'notify_data'
	ERROR_NOTIFY_DATA_PARAM_NAME = 'notify_data'

	def __init__(self, request, config):
		if request is None:
			raise ValueError('request can not be None neither')
		self.config = config
		self.notify_request = request
		self.notify_data_soup = self._get_notify_data_soup()

	def _get_notify_data_soup(self):
		url_encoded_notify_data = self.notify_request.POST[self.NOTIFY_DATA_PARAM_NAME]
		notify_xml = unquote(url_encoded_notify_data).decode(self.config.input_charset)
		return BeautifulSoup(notify_xml)

	def _get_sign(self):
		return self.notify_request.POST.get(AlipayRequestParams.SIGN, None)
		
	def _verify_response(self):
		"""用支付宝返回的notify_id调用支付宝相应接口验证是否是支付宝发来的请求"""

		verity_url = self.ALIPAY_VERIFY_URL_TMPL.format(self.config.partner, self.notify_data_soup.notify_id.text)
		
		verified_result = 'false'
		verify_response = None
		try:
			verify_response = urllib2.urlopen(verity_url)
			verified_result = verify_response.read().strip()
		except:
			try:
				watchdog_error(u'从支付宝验证失败' + full_stack())
			except:
				pass

		return verified_result

	def _verify_sign(self):
		pass

	def _is_valid_request(self):
		if hasattr(self, 'is_valid_request'):
			return self.is_valid_request

		self.is_valid_request = self._verify_response() == 'true'
		return self.is_valid_request

	def get_notify_data_soup(self):
		return self.notify_data_soup

	def is_pay_succeed(self):
		if not self._is_valid_request():
			return False

		trade_status = self.notify_data_soup.trade_status.text
		return ('TRADE_FINISHED' == trade_status) or ('TRADE_SUCCESS' == trade_status) \
			or ('TRADE_FINISHED' == trade_status)

	def get_order_payment_info(self):
		return None

	def get_pay_info(self):
		return ''

	def get_payed_order_id(self):
		return self.notify_data_soup.out_trade_no.text

	def get_reply_response(self):
		return 'success'

	@staticmethod
	def parse_order_id(notify_request):
		if notify_request is None:
			return None

		try:
			url_encoded_notify_data = notify_request.POST[AlipayNotify.NOTIFY_DATA_PARAM_NAME]
			notify_xml = unquote(url_encoded_notify_data).decode('utf-8')
			notify_soup = BeautifulSoup(notify_xml)
			return notify_soup.out_trade_no.text
		except:
			return None


