# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import json
import urllib2 

from urllib import unquote
from BeautifulSoup import BeautifulSoup

from weibo_config import *
from weibo_request_params import *

from watchdog.utils import watchdog_info, watchdog_fatal
from core.exceptionutil import full_stack
from account.models import UserAlipayOrderConfig
from core.exceptionutil import unicode_full_stack

class WeiboTokenInfo(object):
	'''
	https://api.weibo.com/oauth2/get_token_info
	access_token 	string 	采用OAuth授权方式为必填参数，其他授权方式不需要此参数，OAuth授权后获得。
	'''
	WEIBO_GET_TOKEN_INFO_TMPL ="https://api.weibo.com/oauth2/get_token_info"

	DATA_PARAM = "access_token={}"

	def __init__(self, request, access_token):
		self.authorize_post_request = request

		self.weibo_config = WeiboConfig(request.user_profile)
		self.weibo_params = WeiboRequestParams
		self.access_token = access_token


	def _verify_response(self):
		"""获取get_token_info,发送请求"""

		param_data = {'access_token': self.access_token}

		verified_result = ''
		try:
			data = urllib.urlencode(param_data)
			request = urllib2.Request(self.WEIBO_GET_TOKEN_INFO_TMPL,data)
			response = urllib2.urlopen(request)
			file = response.read()
			verified_result = file

			watchdog_info(u"get_open_id_data verified_result: %s" % verified_result)
		except:
			notify_message = u'从weibo获取token_info失败，url:{},原因:{}'.format(self.WEIBO_GET_TOKEN_INFO_TMPL, unicode_full_stack())
			watchdog_fatal(notify_message)

		return verified_result


	def _is_verified_open_id(self,):
		result = self._verify_response()
		data = self._parse_result(result.strip())
		return data

	def _parse_result(self, result):
		data = None
		try:
			data = json.loads(result.strip())
		except:
			notify_message = u'解析微博token_info失败，url:{},原因:{}'.format(result, unicode_full_stack())
			watchdog_fatal(notify_message)

		return data


	def get_open_id_data(self):
		data = self._is_verified_open_id()
		return data
