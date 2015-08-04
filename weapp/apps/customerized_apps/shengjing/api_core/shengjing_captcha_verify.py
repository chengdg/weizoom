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


class ShengjingCaptchaVerify(object):
	'''
	http://218.240.128.124:8080/ESignIn/Switches?
		param={
			"Method":"CaptchaVerify",
			"Version":"1.0",
			"AppID":"88888888",
			"Key": "99999999",
			"Params": {
				"MPhone":"13988888888",
				"Verify": "****"
			}
		}
	'''

	def __init__(self, session_id, phone, captcha):
		self.shengjing_config = ShengjingAPIConfig(session_id)
		self.shengjing_params = ShengjingAPIParams()

		self.api_url = self.shengjing_params.api_url()
		self.phone = phone
		self.captcha = captcha
		self.param_data = None

	def _captcha_verify_response(self):
		"""使用MPhone获取captcha"""
		param_json_data = {
			self.shengjing_params.METHOD: self.shengjing_config.method_captcha_verify,
			self.shengjing_params.VERSION: self.shengjing_config.version,
			self.shengjing_params.APPID: self.shengjing_config.app_id,
			self.shengjing_params.APPKEY: self.shengjing_config.get_app_key(),
			self.shengjing_params.PARAMS: {
				self.shengjing_params.PARAM_MPHONE: self.phone,
				self.shengjing_params.Captcha: self.captcha
			}
		}
		# 将params的json转换为字符串
		param_str = json.dumps(param_json_data)

		param_data = {
			self.shengjing_params.PARAM: param_str
		}
		verified_result = ''
		try:
			param_data = urllib.urlencode(param_data)
			self.param_data = param_data
			print '------------------ShengjingCaptchaVerify-------------------------'
			print self.api_url
			print param_data

			request = urllib2.Request(self.api_url, param_data)
			response = urllib2.urlopen(request)
			file = response.read()
			verified_result = file
			watchdog_info(u"captcha_verify url: %s ,"
				u"param_data: %s" % (self.api_url, param_data), self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		except:
			watchdog_error(u'从Shengjing获取captcha_verify失败，url:{},data:{},原因:{}'.format(self.api_url,
				param_data,
				unicode_full_stack()))
			notify_message = u'从Shengjing获取captcha_verify失败，url:{},data:{},原因:{}'.format(self.api_url,
				param_data,
				unicode_full_stack())
			watchdog_fatal(notify_message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)

		return verified_result

	def _captcha_verify(self):
		result = self._captcha_verify_response()
		data = self._parse_result(result.strip())
		return data

	def _parse_result(self, result):
		data = None
		try:
			data = json.loads(result)
		except:
			notify_message = u'shengjing解析captcha_verify失败，url:{},原因:{}'.format(result, unicode_full_stack())
			watchdog_fatal(notify_message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)

		return data

	def get_captcha_verify_data(self):
		captcha_json = self._captcha_verify()
		watchdog_info(u"盛景验证手机号 captcha_verify \n url:\n{}?{}\n data:\n{}".format(
			self.api_url, self.param_data, captcha_json), self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		print '>>>>>>>>>>>>>>>>>>>>>>>'
		print captcha_json
		return captcha_json
