# -*- coding: utf-8 -*-

__author__ = 'paco bert'

from utils.url_helper import complete_get_request_url
import api_settings
from util import ObjectAttrWrapedInDict

""""
http请求方式: POST（请使用https协议）
https://api.weixin.qq.com/shakearound/device/applyid?access_token=ACCESS_TOKEN
POST数据格式：json
POST数据例子：
{
   "quantity":3,	
   "apply_reason":"测试",	
   "comment":"测试专用",
   "poi_id":1234	
}
   
"""


COMPONENT_URI = 'shakearound/device/applyid'
class WeixinShakeAroundDeviceApplyid(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) == 0:
			raise ValueError(u'WeixinShakeAroundDeviceApplyid.get_get_request_url error, param illegal')

		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'申请设备id'

	def parse_response(self, api_response):
		return api_response

	###############################################################################
	#	args 参数：args =（scene_id, ticket_type=QrcodeTicket.TEMPORARY, is_retry=False）	
	###############################################################################
	def parese_post_param_json_str(self, args):
		if len(args) == 0 or len(args) > 3:
			raise ValueError(u'WeixinShakeAroundDeviceApplyid param number illegal')
		return '{"quantity": %d, "apply_reason": "%s"}' % (args[0], args[1])

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