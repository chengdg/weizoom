# -*- coding: utf-8 -*-

__author__ = 'paco bert'

from utils.url_helper import complete_get_request_url
import api_settings
from util import ObjectAttrWrapedInDict

""""
	创建二维码ticket，api:
	http请求方式: post
	https://api.weixin.qq.com/cgi-bin/qrcode/create

	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果

	4.格式化post数据

	参数信息：
		a.scene_id为定义的二维码所使用的场景值ID，临时二维码时为32位非0整型，
		b.永久二维码时最大值为1000（目前参数只支持1--100000）
		c.ticket_type为二维码类型，默认为临时类型
"""

"""
微信Api提供的二维码Ticket信息，包括以下属性：
ticket: 获取的二维码ticket，凭借此ticket可以在有效时间内换取二维码
expire_seconds: 二维码的有效时间，以秒为单位。最大不超过1800
"""
class QrcodeTicket(ObjectAttrWrapedInDict):
	TEMPORARY = 'QR_SCENE'
	PERMANENT = 'QR_LIMIT_SCENE'
	MAX_EXPIRE_SECONDS = 604800

	def __init__(self, src_dict):
		super(QrcodeTicket, self).__init__(src_dict)	

QRCODE_CREATE_URI = 'cgi-bin/qrcode/create'
class WeixinCreateQrcodeTicketApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) == 0:
			raise ValueError(u'WeixinCreateQrcodeTicketApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinCreateQrcodeTicketApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'获取二维码ticket'

	def parse_response(self, api_response):
		return QrcodeTicket(api_response)

	###############################################################################
	#	args 参数：args =（scene_id, ticket_type=QrcodeTicket.TEMPORARY, is_retry=False）	
	###############################################################################
	def parese_post_param_json_str(self, args):
		if len(args) == 0 or len(args) > 3:
			raise ValueError(u'WeixinCreateQrcodeTicketApi param number illegal')
		
		try:
			int(args[0])
		except:
			raise ValueError(u'WeixinCreateQrcodeTicketApi scene_id type illegal')

		if len(args) == 1:
			return '{"expire_seconds": %d, "action_name": "%s", "action_info": {"scene": {"scene_id": %d}}}'%(
				QrcodeTicket.MAX_EXPIRE_SECONDS, QrcodeTicket.TEMPORARY, args[0])
		if len(args) == 2 or len(args) == 3:
			return '{"expire_seconds": %d, "action_name": "%s", "action_info": {"scene": {"scene_id": %d}}}'%(
				QrcodeTicket.MAX_EXPIRE_SECONDS, args[1], args[0])

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
			api_settings.WEIXIN_API_PROTOCAL, 
			api_settings.WEIXIN_API_DOMAIN,
			QRCODE_CREATE_URI,
			param_dict
			)

	def is_retry(self, args):
		if len(args) == 2:
			return True if args[1] is True else False
		if len(args) == 3:
			return True if args[2] is True else False
		return False