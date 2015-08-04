# -*- coding: utf-8 -*-
"""@package pay.weixin.api.api_pay_openid
授权获取openid API

HTTP请求方式: POST

URL: `https://api.weixin.qq.com/sns/oauth2/access_token`

操作步骤:

 1. 获得api请求地址
 2. 获得请求结果  注:异常信息统交给WeixinPayApi
 3. 格式化请求结果
 4. 格式化POST数据

参数信息:

| 参数  | 必需 | 说明 |
| :----------- | :---: | :-------------------------------------------- |
| appid      | 是	    | 公众号appid    |
| secret | 是 | 公众号appsecret |
| code | 是 | 用户同意授权code参数  |
| grant_type | 是 | authorization_code |

举例:

	{
	"appid": wxe687652b9b2d651a,
	"secret": fde956fb41cee5f2f741ed748a903d7e, 
	"code": 01104b7d1efc25f6e16881023d4b109T,
	"grant_type": "authorization_code "
	}
"""

__author__ = 'slzhu'

import json
import api_settings
 
from utils.url_helper import complete_get_request_url

class OpenidMessage(object):
	def __init__(self, appid, secret, code, grant_type='authorization_code'):
		if appid == None or appid == '':
			raise ValueError(u'appid con not be none or ""')

		if secret == None or secret == '':
			raise ValueError(u'secret con not be none or ""')
		
		if code == None or code == '':
			raise ValueError(u'code con not be none or ""')
		
		self.appid = appid
		self.secret = secret
		self.code = code
		self.grant_type = grant_type
	
	def get_message_json_str(self):
		return json.dumps({"appid" : self.appid, "secret":self.secret, "code":self.code, "grant_type":self.grant_type})


GET_OPENID_MSG_URI = 'sns/oauth2/access_token'
class WeixinPayOpenidApi(object):
	
	def get_get_request_url_and_api_info(self, access_token=None, is_for='xml', varargs=()):
		if len(varargs) >= 3 or len(varargs) == 0:
			raise ValueError(u'WeixinPayOpenidApi.get_get_request_url error, param illegal')
		if access_token is None:
			raise ValueError(u'WeixinPayOpenidApi get_get_request_url_and_api_info：access_token is None')
		param_dict = {}
		param_dict['appid'] = varargs[0].appid
		param_dict['secret'] = varargs[0].secret
		param_dict['code'] = varargs[0].code
		param_dict['grant_type'] = varargs[0].grant_type
		return self._complete_weixin_api_get_request_url(access_token, is_for, param_dict), u'授权接口api'

	def parse_response(self, api_response):
		return api_response

	###############################################################################
	#	args 参数：args = custom_msg_instance
	###############################################################################
	def parese_post_param_json_str(self, args):
		
		if isinstance(args[0], OpenidMessage) is False:
			raise ValueError(u'WeixinPayOpenidApi param OpenidMessage illegal')			

		return args[0].get_message_json_str()

	def request_method(self):
		return api_settings.API_GET

	def _complete_weixin_api_get_request_url(self, access_token, is_for, param_dict):
		if is_for == 'json':
			domain = api_settings.WEIXIN_API_DOMAIN
		else:
			domain = api_settings.WEIXIN_API_V3_DOMAIN
		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL, 
				domain,
				GET_OPENID_MSG_URI,
				param_dict
				)