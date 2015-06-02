# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import json
import urllib2 

from urllib import unquote
from BeautifulSoup import BeautifulSoup

from weibo_config import *
from weibo_request_params import *

from core.exceptionutil import full_stack
from account.models import UserAlipayOrderConfig
from watchdog.utils import watchdog_fatal

from core.exceptionutil import unicode_full_stack
from account.social_account.models import SinaWeiboAccountInfo

class WeiboUserInfo(object):
	'''
	https://api.weibo.com/2/users/show.json
	source 	false 	string 	采用OAuth授权方式不需要此参数，其他授权方式为必填参数，数值为应用的AppKey。
	access_token 	false 	string 	采用OAuth授权方式为必填参数，其他授权方式不需要此参数，OAuth授权后获得。
	uid 	false 	int64 	需要查询的用户ID。
	screen_name 	false 	string 	需要查询的用户昵称。
	'''
	WEIBO_GET_USER_INFO_TMPL ="https://api.weibo.com/2/users/show.json?access_token={}&uid={}"


	def __init__(self, user_profile, social_account):
#		self.authorize_post_request = request

		self.weibo_config = WeiboConfig(user_profile)
		self.weibo_params = WeiboRequestParams
		self.access_token = social_account.access_token
		self.uid = social_account.openid


	def _verify_response(self, ):
		"""获取get_user_info,发送请求"""

		verity_url = self.WEIBO_GET_USER_INFO_TMPL.format(self.access_token, self.uid)

		verified_result = ''
		verify_response = None
		try:
			verify_response = urllib2.urlopen(verity_url)
			verified_result = verify_response.read().strip()
		except:
			notify_message = u'从weibo获取user_info失败，url:{},原因:{}'.format(verity_url, unicode_full_stack())
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
			if data.get('error_code'):
				notify_message = u'从weibo获取user_info失败，url:{},返回数据：{}。原因:{}。'.format(result, data, data.get('error_code'))
				watchdog_fatal(notify_message)
		except:
			notify_message = u'解析微博user_info失败，url:{},原因:{}'.format(result, unicode_full_stack())
			watchdog_fatal(notify_message)

		return data


	def get_user_info_data(self):
		data = self._is_verified_open_id()
		return data


	def get_weibo_account_info(self):
		try:
			data = self.get_user_info_data()
			nickname = data['screen_name']
			head_img = data['profile_image_url']
			return nickname, head_img
		except:
			return '', ''

