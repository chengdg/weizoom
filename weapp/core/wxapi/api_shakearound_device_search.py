# -*- coding: utf-8 -*-

__author__ = 'paco bert'

from utils.url_helper import complete_get_request_url
import api_settings
from util import ObjectAttrWrapedInDict


COMPONENT_URI = 'shakearound/device/search'
class WeixinShakeAroundDeviceSearch(object):
	""""
	http请求方式: POST（请使用https协议）
	https://api.weixin.qq.com/shakearound/device/search?access_token=ACCESS_TOKEN
	POST数据格式：json
	POST数据例子：
	查询指定设备时：
	{
	    "device_identifiers":[
	 		{
				"device_id":10100,	
				"uuid":"FDA50693-A4E2-4FB1-AFCF-C6EB07647825",		
				"major":10001,
				"minor":10002
			}
		]
	}

	需要分页查询或者指定范围内的设备时：
	{
	    "begin": 0,		
	    "count": 3
	}

	当需要根据批次ID查询时：
	{
	    "apply_id": 1231,
	    "begin": 0,		
	    "count": 3
	}
	"""

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) == 0:
			raise ValueError(u'WeixinShakeAroundDeviceSearch.get_get_request_url error, param illegal')

		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'编辑设备信息'

	def parse_response(self, api_response):
		return api_response

	###############################################################################
	#	args 参数：args =（scene_id, ticket_type=QrcodeTicket.TEMPORARY, is_retry=False）	
	###############################################################################
	def parese_post_param_json_str(self, args):
		if len(args) == 0 or len(args) > 3:
			raise ValueError(u'WeixinShakeAroundDeviceSearch param number illegal')
		return '{"device_identifiers": [{"device_id": %d ,"uuid":"%s","major":%d,"minor":%d}]}' % (args[0], args[1], args[2], args[3])

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
			api_settings.WEIXIN_API_PROTOCAL, 
			api_settings.WEIXIN_API_DOMAIN,
			COMPONENT_URI,
			param_dict
			)

	def is_retry(self, args):
		if len(args) == 3:
			return True if args[2] is True else False
		
		return False