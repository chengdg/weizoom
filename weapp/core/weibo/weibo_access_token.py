# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import json
import base64
import urllib2

from urllib import unquote
from BeautifulSoup import BeautifulSoup

from weibo_config import *
from weibo_request_params import *

from watchdog.utils import watchdog_info, watchdog_error, watchdog_fatal
from core.exceptionutil import full_stack

from account.models import UserAlipayOrderConfig
from core.exceptionutil import unicode_full_stack


class WeiboAccessToken(object):
	'''
	https://api.weibo.com/oauth2/access_token?
		client_id=YOUR_CLIENT_ID&
		client_secret=YOUR_CLIENT_SECRET&
		grant_type=authorization_code&
		redirect_uri=YOUR_REGISTERED_REDIRECT_URI&
		code=CODE
	'''
	WEIBO_AUTHORIZE_URL_TMPL ="https://api.weibo.com/oauth2/access_token"

	DATA_PARAM = "client_id={}&client_secret={}&grant_type=authorization_code&redirect_uri={}&code={}"

	NOTIFY_DATA_PARAM_NAME = 'notify_data'

	def __init__(self, request, code):
		self.authorize_post_request = request

		self.weibo_config = WeiboConfig(request.user_profile)
		self.weibo_params = WeiboRequestParams
		self.code = code
		self.redirect_uri = self.weibo_config.get_login_callback_redirect_uri(request)

	def _verify_response(self):
		"""用登陆返回的code，获取access_token,发送请求"""
		param_data = {'client_id': self.weibo_config.app_id,
		        'client_secret': self.weibo_config.app_secret,
		        'grant_type': 'authorization_code',
				'redirect_uri': self.redirect_uri,
		        'code': self.code}
		verified_result = ''
		try:
			data = urllib.urlencode(param_data)
			request = urllib2.Request(self.WEIBO_AUTHORIZE_URL_TMPL,data)
			response = urllib2.urlopen(request)
			file = response.read()
			verified_result = file
			watchdog_info(u"get_access_token_data url: %s ,"
			                          u"param_data: %s" % (self.WEIBO_AUTHORIZE_URL_TMPL, data))
		except:
			watchdog_error(u'从Weibo获取access token失败，url:{},data:{},原因:{}'.format(self.WEIBO_AUTHORIZE_URL_TMPL,
				param_data,
				unicode_full_stack()))
			notify_message = u'从Weibo获取access token失败，url:{},data:{},原因:{}'.format(self.WEIBO_AUTHORIZE_URL_TMPL,
				param_data,
				unicode_full_stack())
			watchdog_fatal(notify_message)

		return verified_result


	def _verify_sign(self):
		pass


	def _is_verified_authorize(self):
		result = self._verify_response()
		data = self._parse_result(result.strip())
		return data

	def _parse_result(self, result):
		data = None
		try:
			data = json.loads(result)
		except:
			notify_message = u'解析access token失败，url:{},原因:{}'.format(result, unicode_full_stack())
			watchdog_fatal(notify_message)

		return data

	def get_access_token_data(self):
		data = self._is_verified_authorize()
		watchdog_info(u"get_access_token_data data:\n{}".format(data))
		return data
