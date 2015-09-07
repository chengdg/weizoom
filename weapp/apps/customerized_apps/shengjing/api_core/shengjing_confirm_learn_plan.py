# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import json
import base64
import urllib2, urllib
import qrcode, time, os, random
from django.conf import settings

from api_config import *
from api_params import *

from watchdog.utils import watchdog_info, watchdog_error, watchdog_fatal, watchdog_notice
from core.exceptionutil import unicode_full_stack

class ShengjingConfirmLearnPlan(object):
	'''
	http://218.240.128.124/ESignIn/Switches?
		Param={
			"Method":"ConfirmLearnPlan",
			"Version":"1.0",
			"AppID":"88888888",
			"Key":"99999999",
			"Params":{
				"phone_number": "139888888888",
				"id": 333,				# 学习计划ID
				"webapp_user_id": 2		# 手机中的用户
			}
		}
	'''

	def __init__(self, session_id, phone, learn_id, webapp_user_id):
		self.phone = phone
		self.learn_id = learn_id
		self.webapp_user_id = webapp_user_id

		self.shengjing_config = ShengjingAPIConfig(session_id)
		self.shengjing_params = ShengjingAPIParams()

		self.api_url = self.shengjing_params.api_url()

	def _confirm_learn_plan_response(self):
		"""使用sessionID和phone学习计划确认"""

		param_json_data = {
			self.shengjing_params.METHOD: self.shengjing_config.method_confirm_learn_plan,
			self.shengjing_params.VERSION: self.shengjing_config.version,
			self.shengjing_params.APPID: self.shengjing_config.app_id,
			self.shengjing_params.APPKEY: self.shengjing_config.get_app_key(),
			self.shengjing_params.PARAMS: {
				self.shengjing_params.PHONE_NUMBER: self.phone,
				self.shengjing_params.WEBAPP_USER_ID: self.webapp_user_id,
				self.shengjing_params.ID: self.learn_id
			}
		}
		# 将params的json转换为字符串
		param_str = json.dumps(param_json_data)
		# print param_str
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
			# print '3333333333333333444444444444'
			message_info = u"盛景confirm_learn_plan url: {}, param_data: {}, result:{}".format(self.api_url, param_data, verified_result)
			watchdog_info(message_info, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		except:
			watchdog_error(u'从Shengjing获取confirm learn_plan失败，url:{}, data:{}, 原因:{}'.format(self.api_url,
				param_data,
				unicode_full_stack()), 
				self.shengjing_params.WATCHDOG_TYPE_SHENGJING)

		return verified_result

	def _get_confirm_learn_plan(self):
		result = self._confirm_learn_plan_response()
		data = self._parse_result(result.strip())
		return data

	def _parse_result(self, result):
		data = None
		try:
			data = json.loads(result)
		except:
			notify_message = u'shengjing解析confirm_learn_plan失败，url:{},原因:{}'.format(result, unicode_full_stack())
			watchdog_fatal(notify_message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)

		return data

	def get_confirm_learn_plan(self):
		data = self._get_confirm_learn_plan()
		watchdog_info(u"shengjing 确认学习计划接口 get_confirm_learn_plan data:\n{}".format(data), self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		return data
