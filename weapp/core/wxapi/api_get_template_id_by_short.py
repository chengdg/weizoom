# -*- coding: utf-8 -*-

__author__ = 'aix'

from utils.url_helper import complete_get_request_url
import api_settings

""""
	调用用户信息api:
	http请求方式: POST
	https://api.weixin.qq.com/cgi-bin/template/api_add_template?access_token=ACCESS_TOKEN

	{
		"template_id_short":"TM00015"
	}
	
	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi
	 {
		"errcode":0,
		"errmsg":"ok",
		"template_id":"Doclyl5uP7Aciu-qZ7mJNPtWkbkYnWBWVja26EGbNyk"
	 }

	3.格式化请求结果

"""


GET_TEMPLATE_ID_URI = 'cgi-bin/template/api_add_template'
class WeixinTemplateIdGetApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) >= 3 and len(varargs) == 0:
			raise ValueError(u'WeixinTemplateIdGetApi.get_get_request_url_and_api_info error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinTemplateIdGetApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'获取模板列表'

	def parse_response(self, api_response):
		#TODO parse
		print api_response
		return api_response

	def parese_post_param_json_str(self, args):
		if len(args) == 0 or len(args) < 2:
			raise ValueError(u'WeixinTemplateIdGetApi param MassMessage illegal')

		return '{"template_id_short": "%s"}' % args[0]

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL, 
				api_settings.WEIXIN_API_DOMAIN,
				GET_TEMPLATE_ID_URI,
				param_dict
				)

	def is_retry(self, args):
		if len(args) == 2:
			return True if args[0] is True else False
		return False