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

class ShengjingGetLearnPlan(object):
	'''
	http://218.240.128.124/ESignIn/Switches?
		Param={
			"Method":"GetLearnPlan",
			"Version":"1.0",
			"AppID":"88888888",
			"Key":"99999999",
			"Params":{
				"phone_number": "139888888888",
				"company_name": "微众传媒",
				"status": "2"			# 0：未开课、1：已开课、2：全部
			}
		}
	'''

	def __init__(self, session_id, phone, company_name, status=2):
		self.phone = phone
		self.company_name = company_name
		self.status = status

		self.shengjing_config = ShengjingAPIConfig(session_id)
		self.shengjing_params = ShengjingAPIParams()

		self.api_url = self.shengjing_params.api_url()

	def _learn_plan_list_response(self):
		"""使用sessionID和phone获取学习计划列表"""

		param_json_data = {
			self.shengjing_params.METHOD: self.shengjing_config.method_get_learn_plan_list,
			self.shengjing_params.VERSION: self.shengjing_config.version,
			self.shengjing_params.APPID: self.shengjing_config.app_id,
			self.shengjing_params.APPKEY: self.shengjing_config.get_app_key(),
			self.shengjing_params.PARAMS: {
				self.shengjing_params.PHONE_NUMBER: self.phone,
				self.shengjing_params.COMPANY_NAME: self.company_name,
				self.shengjing_params.STATUS: self.status
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
			watchdog_info(u"盛景learn_plan url: %s ,"
				u"param_data: %s" % (self.api_url, param_data), self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		except:
			watchdog_error(u'从Shengjing获取learn_plan list失败，url:{},data:{},原因:{}'.format(self.api_url,
				param_data,
				unicode_full_stack()), 
				self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
			# notify_message = u'从Shengjing获取learn_plan list失败，url:{},data:{},原因:{}'.format(self.api_url,
			# 	param_data,
			# 	unicode_full_stack())
			# watchdog_fatal(notify_message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)

		return verified_result

	def _learn_plan_list(self):
		result = self._learn_plan_list_response()
		data = self._parse_result(result.strip())
		return data

	def _parse_result(self, result):
		data = None
		try:
			data = json.loads(result)
		except:
			notify_message = u'shengjing解析learn_plan list失败，url:{},原因:{}'.format(result, unicode_full_stack())
			watchdog_fatal(notify_message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)

		return data

	def get_learn_plan_list(self):
		data = self._learn_plan_list()
		watchdog_info(u"shengjing 访问学习计划列表 get_learn_plan_list data:\n{}".format(data), self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		return data
