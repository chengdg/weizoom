# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import urllib2,urllib

from urllib import unquote
from BeautifulSoup import BeautifulSoup

from qq_config import *
from qq_request_params import *

from watchdog.utils import watchdog_error, watchdog_info
from core.exceptionutil import full_stack
from account.models import UserAlipayOrderConfig
from core.exceptionutil import unicode_full_stack

class QQAccessToken(object):
	'''
	https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&
		client_id=[YOUR_APP_ID]&
		client_secret=[YOUR_APP_Key]&
		code=[The_AUTHORIZATION_CODE]&
		state=[The_CLIENT_STATE]&
		redirect_uri=[YOUR_REDIRECT_URI]
	'''
	QQ_AUTHORIZE_URL_TMPL ="https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&client_id={}" \
	                       "&client_secret={}&code={}&redirect_uri={}"

	def __init__(self, request, code):
		self.authorize_post_request = request

		self.qq_config = QQConfig(request.user_profile)
		self.qq_params = QQRequestParams
		self.code = code
		self.redirect_uri = self.qq_config.get_login_callback_redirect_uri(request)

	def _verify_response(self):
		"""用登陆返回的code，获取access_token,发送请求"""
		verity_url = self.QQ_AUTHORIZE_URL_TMPL.format(
			self.qq_config.app_id,
			self.qq_config.app_key,
			self.code,
			urllib.quote(self.redirect_uri, ''),
		)

		verified_result = ''
		verify_response = None
		try:
			verify_response = urllib2.urlopen(verity_url)
			verified_result = verify_response.read().strip()
			watchdog_info(u'从QQ获取access token，url:{}'.format(verity_url))
		except:
			notify_message = u'从QQ获取access token失败，url:{},原因:{}'.format(verity_url, unicode_full_stack())
			watchdog_error(notify_message)

		return verified_result


	def _is_verified_authorize(self):
		result = self._verify_response()
		data = self._parse_result(result.strip())
		return data

	def _parse_result(self, result):
		data = dict()
		for attribute in result.split('&'):
			try:
				attr = attribute.split('=')
				data[attr[0]] = attr[1]
			except:
				notify_message = u'解析QQ获取的access token失败，url:{},原因:{}'.format(result, unicode_full_stack())
				watchdog_error(notify_message)
		return data

	def get_access_token_data(self):
		data = self._is_verified_authorize()
		if data == {}:
			return None
		else:
			return data
