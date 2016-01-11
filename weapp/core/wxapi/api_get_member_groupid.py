# -*- coding: utf-8 -*-

__author__ = 'paco bert'

import json

from utils.url_helper import complete_get_request_url
import api_settings
from util import ObjectAttrWrapedInDict


""""
	获取用户当前分组 api:
	http请求方式: post
	https://api.weixin.qq.com/cgi-bin/groups/getid?access_token=ACCESS_TOKEN

	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果

	4.格式化post数据

	参数信息：
		a.openid
"""

GROUP_GETID_URI = 'cgi-bin/groups/getid'
class WeixinGetMemberGroupIdApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) == 0:
			raise ValueError(u'WeixinGetMemberGroupIdApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinGetMemberGroupIdApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'获取会员分组id'

	def parse_response(self, api_response):
		return api_response 

	###############################################################################
	#	args 参数：args =（scene_id, ticket_type=QrcodeTicket.TEMPORARY, is_retry=False）	
	###############################################################################
	def parese_post_param_json_str(self, args):
		if len(args) == 0 or len(args) > 3:
			raise ValueError(u'WeixinGetMemberGroupIdApi param number illegal')
		
		openid_full_json = {}
		openid_full_json['openid'] = args[0]
		return json.dumps(openid_full_json)

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
			api_settings.WEIXIN_API_PROTOCAL, 
			api_settings.WEIXIN_API_DOMAIN,
			GROUP_GETID_URI,
			param_dict
			)

	def is_retry(self, args):
		if len(args) == 2:
			return True if args[1] is True else False
		return False