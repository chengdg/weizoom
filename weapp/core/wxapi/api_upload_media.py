# -*- coding: utf-8 -*-

__author__ = 'paco bert'

import os
import urllib
from django.conf import settings
from utils.url_helper import complete_get_request_url
from util import ObjectAttrWrapedInDict
from custom_message import build_custom_message_json_str, TextCustomMessage

import api_settings
  
""""
	调用用户信息api:
	http请求方式: POST/FORM
	http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token=ACCESS_TOKEN&type=TYPE
	
	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果

	4.格式化post数据

	参数信息：
		image：文件流
"""
class MediaType(object):
	TYPE = 'type'
	IMAGE = 'image'
	VOICE = 'voice'
	VIDEO = 'video'
	THUMB = 'thumb'

def build_post_json(media_path, type):
	post_data = {}
	
	if media_path.startswith('http'):
		media_yun_path = media_path
		if media_path.find('upload') > -1:
			media_path = media_path[media_path.find('upload')+6:]
			media_path = settings.UPLOAD_DIR+media_path
			if os.path.isfile(media_path) is False:
				data = urllib.urlopen(media_yun_path).read()  
				f = file(media_path,"wb")  
				f.write(data)
				f.close()
	data = open(media_path, 'rb')
	post_data[type] = data
	return post_data

UPLOAD_NEWS_URI = 'cgi-bin/media/upload'
class WeixinUploadMediaImageApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) > 3 and len(varargs) == 1:
			raise ValueError(u'WeixinUploadMediaImageApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinUploadMediaImageApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'上传媒体文件：image'

	def parse_response(self, api_response):
		return api_response

	def parese_post_param_json_str(self, args):
		if len(args) != 2:
			raise ValueError(u'WeixinUploadMediaImageApi param number illegal')

		return build_post_json(args[0], MediaType.IMAGE)

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		param_dict[MediaType.TYPE] = MediaType.IMAGE
		
		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL, 
				api_settings.WEIXIN_API_DOMAIN,
				UPLOAD_NEWS_URI,
				param_dict
				)

	def is_retry(self, args):
		if len(args) == 2:
			return True if args[1] is True else False
		return False

	def is_for_form(self):
		return True

class WeixinUploadMediaVoiceApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) > 3 and len(varargs) == 1:
			raise ValueError(u'WeixinUploadMediaVoiceApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinUploadMediaVoiceApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'上传媒体文件：voice'

	def parse_response(self, api_response):
		return api_response

	def parese_post_param_json_str(self, args):
		if len(args) != 2:
			raise ValueError(u'WeixinUploadMediaVoiceApi param number illegal')

		return build_post_json(args[0], MediaType.VOICE)

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		param_dict[MediaType.TYPE] = MediaType.VOICE

		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL,
				api_settings.WEIXIN_API_DOMAIN,
				UPLOAD_NEWS_URI,
				param_dict
				)

	def is_retry(self, args):
		if len(args) == 2:
			return True if args[1] is True else False
		return False

	def is_for_form(self):
		return True

UPLOAD_MEDIA_URI = 'cgi-bin/media/uploadimg'
class WeixinUploadContentMediaImageApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) > 3 and len(varargs) == 1:
			raise ValueError(u'WeixinUploadMediaImageApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinUploadMediaImageApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'上传媒体文件：image'

	def parse_response(self, api_response):
		return api_response

	def parese_post_param_json_str(self, args):
		if len(args) != 2:
			raise ValueError(u'WeixinUploadMediaImageApi param number illegal')

		return build_post_json(args[0], MediaType.IMAGE)

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		param_dict[MediaType.TYPE] = MediaType.IMAGE
		
		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL, 
				api_settings.WEIXIN_API_DOMAIN,
				UPLOAD_MEDIA_URI,
				param_dict
				)

	def is_retry(self, args):
		if len(args) == 2:
			return True if args[1] is True else False
		return False

	def is_for_form(self):
		return True