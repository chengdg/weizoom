# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import json
import urllib2 

from urllib import unquote
from BeautifulSoup import BeautifulSoup

from qq_config import *
from qq_request_params import *

from core.exceptionutil import full_stack
from account.models import UserAlipayOrderConfig
from watchdog.utils import watchdog_fatal

from core.exceptionutil import unicode_full_stack
from account.social_account.models import QQAccountInfo

class QQUserInfo(object):
	'''
	https://graph.qq.com/user/get_user_info?access_token=YOUR_ACCESS_TOKEN&oauth_consumer_key=YOUR_APP_ID&openid=YOUR_OPENID
	'''
	QQ_GET_USER_INFO_TMPL ="https://graph.qq.com/user/get_user_info?access_token={}" \
	                     "&oauth_consumer_key={}&openid={}"


	def __init__(self, user_profile, social_account):
		self.authorize_post_request = None

		self.qq_config = QQConfig(user_profile)
		self.qq_params = QQRequestParams
		self.access_token = social_account.access_token
		self.open_id = social_account.openid


	def _verify_response(self, ):
		"""获取get_user_info,发送请求"""

		verity_url = self.QQ_GET_USER_INFO_TMPL.format(self.access_token, self.qq_config.app_id, self.open_id)
		
		verified_result = ''
		verify_response = None
		try:
			verify_response = urllib2.urlopen(verity_url)
			verified_result = verify_response.read().strip()
		except:
			notify_message = u'从QQ获取user_info失败，url:{},原因:{}'.format(verity_url, unicode_full_stack())
			watchdog_fatal(notify_message)

		return verified_result


	def _is_verified_open_id(self,):
		result = self._verify_response()
		data = self._parse_result(result.strip())
		return data


	def _parse_result(self, result):
		data = None
		try:
			data = json.loads(result)
			if int(data.get('ret')) != 0:
				notify_message = u'获取QQ的user_info失败，url:{},返回数据：{}。原因:{}。'.format(result, data, data.get('msg'))
				watchdog_fatal(notify_message)
		except:
			notify_message = u'解析QQ获取的user_info失败，url:{},原因:{}'.format(result, unicode_full_stack())
			watchdog_fatal(notify_message)
		return data


	def get_user_info_data(self):
		data = self._is_verified_open_id()
		return data


	def get_qq_account_info(self):
		try:
			data = self.get_user_info_data()
			nickname = data['nickname']
			head_img = data['figureurl']
			return nickname, head_img
		except:
			return '', ''

