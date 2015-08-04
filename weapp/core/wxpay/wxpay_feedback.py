# -*- coding: utf-8 -*-

__author__ = 'chuter'

from BeautifulSoup import BeautifulSoup

#
#微信支付维权
#
class WxpayFeedback(object):

	def __init__(self, request):
		if request is None:
			raise ValueError('request can not be None')

		self.feedback_request = request

	def get_feedback_data_soup(self):
		if hasattr(self, '_notify_post_data_soup'):
			return self._notify_post_data_soup

		if hasattr(self.feedback_request, 'raw_post_data'):
			notify_post_data = self.feedback_request.raw_post_data
		else:
			notify_post_data = self.feedback_request.body

		self._notify_post_data_soup = BeautifulSoup(notify_post_data)

		return self._notify_post_data_soup