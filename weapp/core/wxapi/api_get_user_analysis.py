# -*- coding: utf-8 -*-

__author__ = 'paco bert'

from utils.url_helper import complete_get_request_url
import api_settings
from util import ObjectAttrWrapedInDict
from custom_message import build_custom_message_json_str, TextCustomMessage, ImageCustomMessage, VoiceCustomMessage, NewsCustomMessage


SUMMARY_URI = 'datacube/getusersummary'
class WeixinGetUserSummaryApi(object):
	""""
	获取用户增减数据:
	http请求方式: GET
	https://api.weixin.qq.com/datacube/getusersummary?access_token=ACCESS_TOKEN

	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果

	4.格式化post数据

	参数信息：
		{ 
		    "begin_date": "2014-12-02", 
			"end_date": "2014-12-07"
		}

	"""
	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) > 3 and len(varargs) == 1:
			raise ValueError(u'WeixinGetUserSummaryApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinGetUserSummaryApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'发送客服消息'

	def parse_response(self, api_response):
		return api_response

	###############################################################################
	#	args 参数：args =（sendto_openid, custom_msg_instance	
	###############################################################################
	def parese_post_param_json_str(self, args):
		
		return '{"begin_date": "%s", "end_date": "%s"}' % (args[0], args[1])

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL, 
				api_settings.WEIXIN_API_DOMAIN,
				SUMMARY_URI,
				param_dict
				)

	def is_retry(self, args):
		if len(args) == 3:
			return True if args[2] is True else False
		return False


CUMULATE_URI = 'datacube/getusercumulate'
class WeixinGetUserCumulateApi(object):
	""""
	获取累计用户数据:
	http请求方式: GET
	https://api.weixin.qq.com/datacube/getusercumulate?access_token=ACCESS_TOKEN

	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果

	4.格式化post数据

	参数信息：
		{ 
		    "begin_date": "2014-12-02", 
			"end_date": "2014-12-07"
		}

	"""
	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) > 3 and len(varargs) == 1:
			raise ValueError(u'WeixinGetUserCumulateApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinGetUserCumulateApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'发送客服消息'

	def parse_response(self, api_response):
		return api_response

	###############################################################################
	#	args 参数：args =（sendto_openid, custom_msg_instance	
	###############################################################################
	def parese_post_param_json_str(self, args):
		
		return '{"begin_date": "%s", "end_date": "%s"}' % (args[0], args[1])

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL, 
				api_settings.WEIXIN_API_DOMAIN,
				CUMULATE_URI,
				param_dict
				)

	def is_retry(self, args):
		if len(args) == 3:
			return True if args[2] is True else False
		return False