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

class ShengjingGetInvitationList(object):
	'''
	http://218.240.128.124/ESignIn/Switches?
		Param={
			"Method":"GetInvitationList",
			"Version":"1.0",
			"AppID":"88888888",
			"Key":"99999999",
			"Params":{
				"MPhone":"139888888888"
			}
		}
	'''

	def __init__(self, session_id, phone):
		self.phone = phone
		self.shengjing_config = ShengjingAPIConfig(session_id)
		self.shengjing_params = ShengjingAPIParams()

		self.api_url = self.shengjing_params.api_url()

	def _invitation_list_response(self):
		"""使用sessionID和phone获取二维码签到列表"""

		param_json_data = {
			self.shengjing_params.METHOD: self.shengjing_config.method_get_invitation_list,
			self.shengjing_params.VERSION: self.shengjing_config.version,
			self.shengjing_params.APPID: self.shengjing_config.app_id,
			self.shengjing_params.APPKEY: self.shengjing_config.get_app_key(),
			self.shengjing_params.PARAMS: {
				self.shengjing_params.PARAM_MPHONE : self.phone
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
			watchdog_info(u"get_session_id_data url: %s ,"
				u"param_data: %s" % (self.api_url, param_data), self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		except:
			watchdog_error(u'从Shengjing获取invitation list失败，url:{},data:{},原因:{}'.format(self.api_url,
				param_data,
				unicode_full_stack()), 
				self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
			notify_message = u'从Shengjing获取invitation list失败，url:{},data:{},原因:{}'.format(self.api_url,
				param_data,
				unicode_full_stack())
			watchdog_fatal(notify_message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)

		return verified_result

	def _invitation_list(self):
		result = self._invitation_list_response()
		data = self._parse_result(result.strip())
		return data

	def _parse_result(self, result):
		data = None
		try:
			data = json.loads(result)
		except:
			notify_message = u'shengjing解析invitation list失败，url:{},原因:{}'.format(result, unicode_full_stack())
			watchdog_fatal(notify_message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)

		return data


	#===============================================================================
	# _resolve_invitation_list_json : 解析invitation_list
	#===============================================================================
	def _resolve_invitation_list_json(self, data):
		try:		
			if int(data.get('Header').get('Code')) == 0:
				json_list = data.get('InvitationList', [])
				return self._reload_invitation_json(json_list)
			else:
				message = u'_resolve_invitation_list_json解析 Code不为0, phone:{}\n, data:\n{}'.format(self.phone, data)
				watchdog_notice(message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
				return None
		except:
			message = u'_resolve_invitation_list_json解析异常 except, phone:{}\n, data:\n{}, cause:\n{}'.format(self.phone, data, unicode_full_stack())
			watchdog_fatal(message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
			return None
			

	def _reload_invitation_json(self, json):
		data = []
		for item in json:
			one = {
				"customer": item["Customer"],
				"student": item["Student"],
				"course": item["Course"],
				"start_date": item["StartDate"],
				"qrcode_img": self._generate_qrcode_img(item["QRCode"])
			}
			data.append(one)
		return data

	#===============================================================================
	# _generate_qrcode_img : 生成二维码
	#===============================================================================
	def _generate_qrcode_img(self, qrcode_str):
		qr = qrcode.QRCode(
			version=3,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=10,
			border=4
		)
		qr.add_data(qrcode_str)
		img = qr.make_image()

		file_name = '{}_{}.png'.format(time.strftime("%Y%m%d%H%M%S"), random.randrange(0,1001))
		dir_path = os.path.join(settings.UPLOAD_DIR, 'shengjing_invitation_qrcode')
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)

		file_path = os.path.join(dir_path, file_name)
		img.save(file_path)

		return '/static/upload/shengjing_invitation_qrcode/%s' % file_name


	def get_invitation_list(self):
		data = self._invitation_list()
		watchdog_info(u"shengjing 访问二维码列表 get_invitation_list data:\n{}".format(data), self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
		data = self._resolve_invitation_list_json(data)
		return data
