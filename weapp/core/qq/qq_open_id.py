# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import json
import urllib2 

from urllib import unquote
from BeautifulSoup import BeautifulSoup

from qq_config import *
from qq_request_params import *
from account.models import UserAlipayOrderConfig
from watchdog.utils import watchdog_fatal

from core.exceptionutil import full_stack
from core.exceptionutil import unicode_full_stack

class QQOpenID(object):
	'''
	https://graph.qq.com/oauth2.0/me?access_token=YOUR_ACCESS_TOKEN
	'''
	QQ_OPEN_ID_URL_TMPL ="https://graph.qq.com/oauth2.0/me?access_token={}"


	def __init__(self, request, access_token):
		self.authorize_post_request = request

		self.qq_config = QQConfig(request.user_profile)
		self.qq_params = QQRequestParams
		self.access_token = access_token


	def _verify_response(self, ):
		"""用登陆返回的code，获取access_token,发送请求"""

		verity_url = self.QQ_OPEN_ID_URL_TMPL.format(self.access_token)
		
		verified_result = ''
		verify_response = None
		try:
			verify_response = urllib2.urlopen(verity_url)
			verified_result = verify_response.read().strip()
		except:
			try:
				notify_message = u'从QQ获取open_id失败，url:{},原因:{}'.format(verity_url, unicode_full_stack())
				watchdog_fatal(notify_message)
			except:
				pass

		return verified_result


	def _is_verified_open_id(self,):
		result = self._verify_response()
		data = self._parse_result(result.strip())
		return data

	def _parse_result(self, result):
		data = None
		try:
			if result[0: 8] == "callback":
				start = result.find('(')
				end = result.find(')')
				result = result[start+1:end]
				data = json.loads(result)
		except:
			notify_message = u'解析QQ获取的open_id失败，url:{},原因:{}'.format(result, unicode_full_stack())
			watchdog_fatal(notify_message)
		return data


	def get_open_id_data(self):
		data = self._is_verified_open_id()
		if data == {}:
			return None
		else:
			return data
