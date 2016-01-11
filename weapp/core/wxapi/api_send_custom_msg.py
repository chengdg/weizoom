# -*- coding: utf-8 -*-

__author__ = 'paco bert'

from utils.url_helper import complete_get_request_url
import api_settings
from util import ObjectAttrWrapedInDict
from custom_message import build_custom_message_json_str, TextCustomMessage, ImageCustomMessage, VoiceCustomMessage, NewsCustomMessage

""""
	调用用户信息api:
	http请求方式: GET
	https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=ACCESS_TOKEN

	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果

	4.格式化post数据

	参数信息：
		sendto_openid, custom_msg_instance
		接收者opend  , 发送客服的消息(TextCustomMessage 对象)
"""

SEND_CUSTOM_MSG_URI = 'cgi-bin/message/custom/send'
class WeixinSendCustomMsgApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) > 3 and len(varargs) == 1:
			raise ValueError(u'WeixinSendCustomMsgApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinSendCustomMsgApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'发送客服消息'

	def parse_response(self, api_response):
		return api_response

	###############################################################################
	#	args 参数：args =（sendto_openid, custom_msg_instance	
	###############################################################################
	def parese_post_param_json_str(self, args):
		if len(args) != 2:
			raise ValueError(u'WeixinSendCustomMsgApi param number illegal')

		if isinstance(args[1], TextCustomMessage) is False and isinstance(args[1], ImageCustomMessage) is False and isinstance(args[1], VoiceCustomMessage) is False and isinstance(args[1], NewsCustomMessage) is False:
			print 'error+++++++++++++++++++++++'
			raise ValueError(u'WeixinSendCustomMsgApi param illegal')

		return build_custom_message_json_str(args[0], args[1])

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL, 
				api_settings.WEIXIN_API_DOMAIN,
				SEND_CUSTOM_MSG_URI,
				param_dict
				)

	def is_retry(self, args):
		if len(args) == 3:
			return True if args[2] is True else False
		return False