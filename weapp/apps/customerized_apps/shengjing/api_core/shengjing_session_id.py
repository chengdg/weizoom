# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import json
import base64
import urllib2, urllib

from urllib import unquote
from BeautifulSoup import BeautifulSoup

from api_config import *
from api_params import *

from watchdog.utils import watchdog_info, watchdog_error, watchdog_fatal
from core.exceptionutil import unicode_full_stack


class ShengjingSessionID(object):
	'''
	http://218.240.128.124/ESignIn/Switches?
		param={
			"Method":"WhoAmI",
			"Version":"1.0",
			"AppID":"88888888",
			"Key": "99999999",
			"Params": null
		}
	'''

	def __init__(self):
		self.shengjing_config = ShengjingAPIConfig()
		self.shengjing_params = ShengjingAPIParams()

		self.api_url = self.shengjing_params.api_url()

	def _session_response(self):
		"""使用appId和初始令牌获取sessionID"""

		param_json_data = {
			self.shengjing_params.METHOD: self.shengjing_config.method_who_am_I,
			self.shengjing_params.VERSION: self.shengjing_config.version,
			self.shengjing_params.APPID: self.shengjing_config.app_id,
			self.shengjing_params.APPKEY: self.shengjing_config.get_app_key(),
			self.shengjing_params.PARAMS: None
		}
		# 将params的json转换为字符串
		param_str = json.dumps(param_json_data)

		param_data = {
			self.shengjing_params.PARAM: param_str
		}
		verified_result = ''
		try:
			param_data = urllib.urlencode(param_data)
			# print '-------------------------------------------'
			# print param_data

			request = urllib2.Request(self.api_url, param_data)
			response = urllib2.urlopen(request)
			file = response.read()
			verified_result = file
			watchdog_info(u"get_session_id_data url: %s ,"
				u"param_data: %s" % (self.api_url, param_data), self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		except:
			watchdog_error(u'从Shengjing获取session id失败，url:{},data:{},原因:{}'.format(self.api_url,
				param_data,
				unicode_full_stack()))
			notify_message = u'从Shengjing获取session id失败，url:{},data:{},原因:{}'.format(self.api_url,
				param_data,
				unicode_full_stack())
			watchdog_fatal(notify_message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)

		return verified_result

	# def _json_to_string(self, json):
	# 	items = []
	# 	for key, value in json.items():  
	# 		# items.append("\"%s\":\"%s\"" % (key, value))
	# 		if value:
	# 			items.append("%22{}%22:%22{}%22".format(key, value))
	# 		else:
	# 			items.append("%22{}%22:null".format(key))

	# 	return u'{'+ ','.join(items) + '}'

	def _session_id(self):
		result = self._session_response()
		data = self._parse_result(result.strip())
		return data

	def _parse_result(self, result):
		data = None
		try:
			data = json.loads(result)
		except:
			notify_message = u'shengjing解析session id失败，url:{},原因:{}'.format(result, unicode_full_stack())
			watchdog_fatal(notify_message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)

		return data


	#===============================================================================
	# _resolve_session_id_json : 解析session_id
	#===============================================================================
	def _resolve_session_id_json(self, data):
		session_id = data.get('SessionID', None)
		try:		
			if data.get('Header').get('Code') == 0:
				return session_id
			else:
				message = u'_resolve_session_id_json解析session异常, data:\n{}'.format(data)
				watchdog_fatal(message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
				return None
		except:
			message = u'_resolve_session_id_json解析session异常, data:\n{}, cause:\n{}'.format(data, unicode_full_stack())
			watchdog_fatal(message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
			return None


	def get_session_id_data(self):
		data = self._session_id()
		watchdog_info(u"get_session_id_data data:\n{}".format(data), self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		session_id = self._resolve_session_id_json(data)
		# print '>>>>>>>>>>>>>>>>>>>>>>>'
		# print session_id
		return session_id
