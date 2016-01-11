# -*- coding: utf-8 -*-

__author__ = 'paco bert'

from utils.url_helper import complete_get_request_url
import api_settings
from util import ObjectAttrWrapedInDict

""""
	调用用户信息api:
	http请求方式: GET
	https://api.weixin.qq.com/cgi-bin/groups/get?access_token=ACCESS_TOKEN

	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果
"""


GET_GROUP_URL = 'https://api.weixin.qq.com/cgi-bin/groups/get?access_token={}'
class WeixinGroupsApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		
		if mpuser_access_token is None:
			raise ValueError(u'WeixinGroupsApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'通过access_token获取全部分组'

	def parse_response(self, api_response):
		return api_response

	def parese_post_param_json_str(self, args):
		pass

	def request_method(self):
		return api_settings.API_GET

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		return GET_GROUP_URL.format(mpuser_access_token.access_token)

	def is_retry(self, args):
		if len(args) == 1:
			return True if args[0] is True else False
		return False