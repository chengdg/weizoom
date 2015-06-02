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


class ShengjingSubmitBooking(object):
	'''
	http://218.240.128.124/ESignIn/Switches?
		param={
			"Method":"SubmitBooking",
			"Version":"1.0",
			"AppID":"88888888",
			"Key":"99999999",
			"Params":{
				"Course":"测试团队合作课程",
				"Student":"王芳芳",
				"MPhone":"139888888888",
				"Customer":"北京科技股份公司",
				"Number":1,
				"BookedTime":"2015-01-20 08:51"
			}
		}
	'''

	def __init__(self, session_id, course):
		self.shengjing_config = ShengjingAPIConfig(session_id)
		self.shengjing_params = ShengjingAPIParams()

		self.api_url = self.shengjing_params.api_url()
		self.course = course

	def _submit_booking_response(self):
		"""提交在线预约信息接口"""

		param_json_data = {
			self.shengjing_params.METHOD: self.shengjing_config.method_submit_booking,
			self.shengjing_params.VERSION: self.shengjing_config.version,
			self.shengjing_params.APPID: self.shengjing_config.app_id,
			self.shengjing_params.APPKEY: self.shengjing_config.get_app_key(),
			self.shengjing_params.PARAMS: {
				self.shengjing_params.COURSE: self.course.name,
				self.shengjing_params.STUDENT: self.course.member_name,
				self.shengjing_params.PARAM_MPHONE: self.course.member_phone,
				self.shengjing_params.CUSTOMER: self.course.member_company,
				self.shengjing_params.NUMBER: self.course.number,
				self.shengjing_params.BOOKED_TIME: self.course.date_time
			}
		}
		# 将params的json转换为字符串
		param_str = json.dumps(param_json_data)
		self.param_str = param_str

		param_data = {
			self.shengjing_params.PARAM: param_str
		}
		verified_result = ''
		try:
			param_data = urllib.urlencode(param_data)
			print '-------------------------------------------'
			print param_data

			request = urllib2.Request(self.api_url, param_data)
			response = urllib2.urlopen(request)
			file = response.read()
			verified_result = file
			watchdog_info(u"_submit_booking_response url: %s ,"
				u"param_data: %s" % (self.api_url, param_data), self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		except:
			watchdog_error(u'从Shengjing获取submit booking失败，url:{},data:{},原因:{}'.format(self.api_url,
				param_data,
				unicode_full_stack()), 
				self.shengjing_params.WATCHDOG_TYPE_SHENGJING)

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

	def _submit_booking(self):
		result = self._submit_booking_response()
		data = self._parse_result(result.strip())
		return data

	def _parse_result(self, result):
		data = None
		try:
			data = json.loads(result)
		except:
			notify_message = u'shengjing解析submit booking失败，url:{},原因:{}'.format(result, unicode_full_stack())
			watchdog_fatal(notify_message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)

		return data

	def set_submit_booking(self):
		data = self._submit_booking()
		watchdog_info(u"set_submit_booking data:\n{}".format(data), self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		if data.get('Header').get('Code') != 0:
			watchdog_fatal(u'从Shengjing获取submit booking返回code不为0，url:{}, data:{}'.format(self.api_url, self.param_str), 
			self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		return data
