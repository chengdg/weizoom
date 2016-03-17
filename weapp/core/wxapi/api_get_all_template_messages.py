# -*- coding: utf-8 -*-

__author__ = 'aix'

from utils.url_helper import complete_get_request_url
import api_settings

""""
	调用用户信息api:
	http请求方式: GET
	https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?access_token=ACCESS_TOKEN
	
	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果

"""


GET_ALL_TEMPLATES_URI = 'cgi-bin/template/get_all_private_template'
class WeixinTemplateMessagesGetApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) >= 3 and len(varargs) == 0:
			raise ValueError(u'WeixinTemplateMessagesGetApi.get_get_request_url_and_api_info error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinTemplateMessagesGetApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'获取模板列表'

	def parse_response(self, api_response):
		#TODO parse
		print api_response
		return api_response

	def parese_post_param_json_str(self, args):
		pass

	def request_method(self):
		return api_settings.API_GET

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL, 
				api_settings.WEIXIN_API_DOMAIN,
				GET_ALL_TEMPLATES_URI,
				param_dict
				)

	def is_retry(self, args):
		if len(args) == 1:
			return True if args[0] is True else False
		return False