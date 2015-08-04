# -*- coding: utf-8 -*-

__author__ = 'paco bert'

from utils.url_helper import complete_get_request_url
import api_settings
from util import ObjectAttrWrapedInDict

""""
	调用用户信息api:
	http请求方式: GET
	https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=TICKET

	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果
"""

"""
微信Api提供的二维码Ticket信息，包括以下属性：
ticket: 获取的二维码ticket，凭借此ticket可以在有效时间内换取二维码
expire_seconds: 二维码的有效时间，以秒为单位。最大不超过1800
"""
class QrcodeTicket(ObjectAttrWrapedInDict):
	TEMPORARY = 'QR_SCENE'
	PERMANENT = 'QR_LIMIT_SCENE'
	MAX_EXPIRE_SECONDS = 1800

	def __init__(self, src_dict):
		super(QrcodeTicket, self).__init__(src_dict)	

GET_QRCODE_URL = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={}'
class WexinGetQrcodeApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) ==0:
			raise ValueError(u'WexinGetQrcodeApi.get_get_request_url error: param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WexinGetQrcodeApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(varargs), u'通过ticket获取二维码图片'

	def parse_response(self, api_response):
		return api_response

	def parese_post_param_json_str(self, args):
		pass

	def request_method(self):
		return api_settings.API_GET

	def _complete_weixin_api_get_request_url(self, varargs):
		return GET_QRCODE_URL.format(varargs[0])

	def is_retry(self, args):
		if len(args) == 2:
			return True if args[1] is True else False
		return False