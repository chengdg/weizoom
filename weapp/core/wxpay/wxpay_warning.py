# -*- coding: utf-8 -*-

__author__ = 'chuter'

from BeautifulSoup import BeautifulSoup

class WxpayWarningNotify(object):
	"""
	微信支付告警通知
	"""

	def __init__(self, request):
		if request is None:
			raise ValueError('request can not be None')

		self.warning_notify_request = request

	def get_notify_data_soup(self):
		if hasattr(self, '_notify_post_data_soup'):
			return self._notify_post_data_soup

		if hasattr(self.warning_notify_request, 'raw_post_data'):
			notify_post_data = self.warning_notify_request.raw_post_data
		else:
			notify_post_data = self.warning_notify_request.body

		self._notify_post_data_soup = BeautifulSoup(notify_post_data)

		return self._notify_post_data_soup

	def get_reply_response(self):
		return 'success'