# -*- coding: utf-8 -*-

__author__ = 'chuter'

import urllib2 

from django.http import HttpResponse

from wxpay_core import build_str_params
from wxpay_config import *
from wxpay_request_params import *

from watchdog.utils import watchdog_fatal, watchdog_alert
from core.exceptionutil import unicode_full_stack

from BeautifulSoup import BeautifulSoup

class WxPaymentInfo(object):
	def __init__(self, 
		transaction_id, #交易号
		appid, #公众平台账户的AppId
		openid, #购买用户的OpenId
		out_trade_no, #该平台中订单号
		):
		self.transaction_id = transaction_id
		self.appid = appid
		self.openid = openid
		self.out_trade_no = out_trade_no

class WxpayNotify(object):

	def __init__(self, request):
		if request is None:
			raise ValueError('request can not be None')

		self.notify_request = request
		self.notify_post_data_soup = self.get_notify_data_soup()

	def _get_sign(self):
		sign = self.notify_request.REQUEST.get(WxpayRequestParams.SIGN, None)
		if sign == None and self.notify_post_data_soup.sign:
			sign = self.notify_post_data_soup.sign.text
		return sign

	def _get_partner_id(self):
		partner_id = self.notify_request.GET.get(WxpayRequestParams.PARTNER, '')
		if partner_id == '' and self.notify_post_data_soup.mch_id:
			partner_id = self.notify_post_data_soup.mch_id.text
		return partner_id

	def _get_notify_id(self):
		return self.notify_request.GET.get(WxpayRequestParams.NOTIFY_ID, '')

	#验证反馈信息的确来自财付通
	def _is_valid_request(self):
		#TODO 需要实际访问微信api确认订单状态是否已经完成支付
		return True

	def _get_transaction_id(self):
		transaction_id = self.notify_request.GET.get(WxpayRequestParams.TRANSACTION_ID, None)
		if transaction_id == None and self.notify_post_data_soup.transaction_id:
			transaction_id = self.notify_post_data_soup.transaction_id.text
		return transaction_id
	
	def _get_appid(self):
		appid = self.notify_request.GET.get(WxpayRequestParams.APPID, None)
		if appid == None and self.notify_post_data_soup.appid:
			appid = self.notify_post_data_soup.appid.text
		return appid
	
	def _get_openid(self):
		openid = self.notify_request.GET.get(WxpayRequestParams.OPENID, None)
		if openid == None and self.notify_post_data_soup.openid:
			openid = self.notify_post_data_soup.openid.text
		return openid

	def get_order_payment_info(self):
		transaction_id = self._get_transaction_id()
		out_trade_no = self.get_payed_order_id()
		appid = self._get_appid()
		openid = self._get_openid()
		return 	WxPaymentInfo(
				transaction_id,
				appid,
				openid,
				out_trade_no
			)	

	def get_notify_data_soup(self):
		if not self._is_valid_request():
			return None

		if hasattr(self, '_notify_post_data_soup'):
			return self._notify_post_data_soup

		if hasattr(self.notify_request, 'raw_post_data'):
			notify_post_data = self.notify_request.raw_post_data
		else:
			notify_post_data = self.notify_request.body

		self._notify_post_data_soup = BeautifulSoup(notify_post_data)

		return self._notify_post_data_soup

	def is_pay_succeed(self):
		if not self._is_valid_request():
			return False
		trade_state = self.notify_request.GET.get(WxpayRequestParams.TRADE_STATE, -1)
		if trade_state == -1 and self.notify_post_data_soup.return_code and self.notify_post_data_soup.result_code:
			if self.notify_post_data_soup.return_code.text == 'SUCCESS' and self.notify_post_data_soup.result_code.text == 'SUCCESS':
				trade_state = 0
			else:
				trade_state = 1
		return int(trade_state) == 0

	#当支付失败则通过该接口获取微信反馈的支付失败原因
	def get_pay_info(self):
		pay_info = self.notify_request.GET.get(WxpayRequestParams.PAY_INFO, '')
		if pay_info == '' and self.notify_post_data_soup.return_msg: 
			pay_info = self.notify_post_data_soup.return_msg.text
		return pay_info

	def get_payed_order_id(self):
		order_id = self.notify_request.GET.get(WxpayRequestParams.OUT_TRADE_NO, None)
		if order_id == None and self.notify_post_data_soup.out_trade_no:
			order_id = self.notify_post_data_soup.out_trade_no.text
		return order_id

	def get_reply_response(self):
		return 'success'