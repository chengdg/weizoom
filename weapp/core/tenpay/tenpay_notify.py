# -*- coding: utf-8 -*-

__author__ = 'chuter'

import urllib2 

from django.http import HttpResponse

from tenpay_core import build_str_params
from tenpay_config import *
from tenpay_request_params import *

from account.models import UserTenpayOrderConfig
from watchdog.utils import watchdog_fatal, watchdog_alert
from core.exceptionutil import unicode_full_stack

from BeautifulSoup import BeautifulSoup

class TenpayNotify(object):
	TENPAY_VERIFY_URL_TMPL = "https://gw.tenpay.com/gateway/simpleverifynotifyid.xml"

	def __init__(self, request):
		if request is NOne:
			raise ValueError('request can not be None')

		self.notify_request = request
		self.verified_result_soup = self._get_verify_soup_response()

	def _get_sign(self):
		sign = self.notify_request.GET.get(TenpayRequestParams.SIGN, None)
		if None == sign:
			return self.notify_post_request.POST[TenpayRequestParams.SIGN]

	def _get_partner_id(self):
		return self.notify_request.GET.get(TenpayRequestParams.PARTNER, '')

	def _get_notify_id(self):
		return self.notify_request.GET.get(TenpayRequestParams.NOTIFY_ID, '')

	def _build_verify_request_params(self):
		params = {}

		params[TenpayRequestParams.SIGN] = self._get_sign()
		params[TenpayRequestParams.PARTNER] = self._get_partner_id()
		params[TenpayRequestParams.INPUT_CHARSET] = TenpayConfig.input_charset

		params[TenpayRequestParams.NOTIFY_ID] = self._get_notify_id()

		return params

	def _get_verify_soup_response(self):
		"""用财付通宝返回的notify_id调用相应接口验证是否是财付通发来的请求"""

		if hasattr(self, 'notify_data_soup'):
			return self.notify_data_soup

		params = self._build_verify_request_params()
		str_params = build_str_params(params, self.tenpay_config)
		verity_url = "{}?{}".format(self.TENPAY_VERIFY_URL_TMPL, urlencode(str_params))

		try:
			verify_response = urllib2.urlopen(verity_url)
			verified_result = verify_response.read().strip()
			return BeautifulSoup(verified_result)
		except:
			notify_message = u"向财付通确认是否是财付通的请求失败, request.GET:{}, cause:\n"\
				.format(self.notify_request.GET, unicode_full_stack())
			watchdog_fatal(notify_message)
			return None

	#验证反馈信息的确来自财付通
	def _is_valid_request(self):
		if self.verified_result_soup is None:
			return False
		else:
			try:
				return int(self.verified_result_soup.retcode.text) == 0
			except:
				notify_message = u"解析财付通确认结果失败, 确认结果:{}, cause:\n"\
					.format(self.verified_result_soup, unicode_full_stack())
				watchdog_alert(notify_message)
				return False

	def get_notify_data_soup(self):
		if not self._is_valid_request():
			return None

		notify_xml = """
		<xml>
			<trade_status>{}</trade_status>
			<out_trade_no>{}</out_trade_no>
		</xml>
		""".format(
				self.notify_request.GET['trade_state'],
				self.notify_request.GET['out_trade_no'],
			)

		return BeautifulSoup(notify_data)

	def is_pay_succeed(self):
		if not self._is_valid_request():
			return False

		return int(self.notify_request.GET.get(TenpayRequestParams.TRADE_STATE, 1)) == 0

	#当支付失败则通过该接口获取财付通反馈的支付失败原因
	def get_pay_info(self):
		return self.notify_request.GET.get(TenpayRequestParams.PAY_INFO, '')

	def get_order_payment_info(self):
		return None

	def get_payed_order_id(self):
		return self.notify_request.GET.get(TenpayRequestParams.OUT_TRADE_NO, None)

	def get_reply_response(self):
		return 'Success'