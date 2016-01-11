# -*- coding: utf-8 -*-

__author__ = 'paco bert'

from utils.url_helper import complete_get_request_url
import api_settings
from util import ObjectAttrWrapedInDict
import json
""""
	自定义菜单:
	一、创建接口：
		http请求方式: post
		https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
		参数示例：
			{
			     "button":[
			     {	
			          "type":"click",
			          "name":"今日歌曲",
			          "key":"V1001_TODAY_MUSIC"
			      },
			      {
			           "type":"click",
			           "name":"歌手简介",
			           "key":"V1001_TODAY_SINGER"
			      },
			      {
			           "name":"菜单",
			           "sub_button":[
			           {	
			               "type":"view",
			               "name":"搜索",
			               "url":"http://www.soso.com/"
			            },
			            {
			               "type":"view",
			               "name":"视频",
			               "url":"http://v.qq.com/"
			            },
			            {
			               "type":"click",
			               "name":"赞一下我们",
			               "key":"V1001_GOOD"
			            }]
			       }]
			}
		参数说明

		参数	   是否必须	   说明
		button	     是	       一级菜单数组，个数应为1~3个
		sub_button	 否	       二级菜单数组，个数应为1~5个
		type	     是	       菜单的响应动作类型，目前有click、view两种类型
		name	     是	       菜单标题，不超过16个字节，子菜单不超过40个字节
		key	     click类型必须	 菜单KEY值，用于消息接口推送，不超过128字节
		url	     view类型必须	 网页链接，用户点击菜单可打开链接，不超过256字节

	二、查询接口：
		http请求方式：get
		https://api.weixin.qq.com/cgi-bin/menu/get?access_token=ACCESS_TOKEN

		返回结果说明：
			{"menu":{"button":[{"type":"click","name":"今日歌曲","key":"V1001_TODAY_MUSIC","sub_button":[]},{"type":"click","name":"歌手简介","key":"V1001_TODAY_SINGER","sub_button":[]},{"name":"菜单","sub_button":[{"type":"view","name":"搜索","url":"http://www.soso.com/","sub_button":[]},{"type":"view","name":"视频","url":"http://v.qq.com/","sub_button":[]},{"type":"click","name":"赞一下我们","key":"V1001_GOOD","sub_button":[]}]}]}}

	三、删除借口
		http请求方式：GET
		https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=ACCESS_TOKEN

		对应创建接口，正确的Json返回结果:
		{"errcode":0,"errmsg":"ok"}


	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果

	4.格式化post数据

"""


CUSTOMERIZED_MENU_CREATE_URI = 'cgi-bin/menu/create'
"""
	需要参数：varargs = (menu_json, is_retry(Ture or False))
"""
class WeixinCreateCustomerizedMenuApi(object):
	####################################################
	#WeixinCreateCustomerizedMenuApi需要参数：varargs = (menu_json, is_retry(Ture or False))
	####################################################
	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) == 0 and len(varargs) > 2:
			raise ValueError(u'WeixinCreateCustomerizedMenuApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinCreateCustomerizedMenuApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'创建自定义菜单'

	def parse_response(self, api_response):
		return api_response
	
	def parese_post_param_json_str(self, args):
		if len(args) == 0 or len(args) > 2:
			raise ValueError(u'WeixinCreateCustomerizedMenuApi param number illegal')
		menu_json = args[0]
		if self.__should_change_to_delete_request(menu_json):
			raise ValueError(u'请先调用删除自定义菜单接口')
		
		if isinstance(menu_json, str):
			try:
				menu_json = json.loads(menu_json)
				return menu_json
			except:
				ValueError(u'自定义菜单数据格式错误')

	def request_method(self):
		return api_settings.API_POST

	def is_retry(self, args):
		if len(args) == 2:
			return True if args[1] is True else False
		return False

	def __should_change_to_delete_request(self, menu_json_str):
		if menu_json_str is None:
			return True

		if isinstance(menu_json_str, dict):
			menu_json_str = menu_json_str.__str__()

		try:
			menu_json_str = re.sub('\\s+', '', menu_json_str)
			return menu_json_str == '{}'
		except:
			return False

	def _complete_weixin_api_get_request_url(self,mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
			api_settings.WEIXIN_API_PROTOCAL, 
			api_settings.WEIXIN_API_DOMAIN,
			CUSTOMERIZED_MENU_CREATE_URI,
			param_dict
			)


"""
	需要参数：varargs = (is_retry(Ture or False))
"""
CUSTOMERIZED_MENU_GET_URI = 'cgi-bin/menu/get'
class WeixinGetCustomerizedMenuApi(object):
	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if  len(varargs) > 2:
			raise ValueError(u'WeixinGetCustomerizedMenuApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinGetCustomerizedMenuApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'查询自定义菜单'

	def parse_response(self, api_response):
		return api_response

	def parese_post_param_json_str(self, args):
		pass

	def request_method(self):
		return api_settings.API_GET

	def is_retry(self, args):
		if len(args) == 1:
			return True if args[0] is True else False
		return False

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
			api_settings.WEIXIN_API_PROTOCAL, 
			api_settings.WEIXIN_API_DOMAIN,
			CUSTOMERIZED_MENU_GET_URI,
			param_dict
			)

"""
	需要参数：varargs = (is_retry(Ture or False))
"""
CUSTOMERIZED_MENU_DELETE_URI = 'cgi-bin/menu/delete'
class WeixinDeleteCustomerizedMenuApi(object):
	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if  len(varargs) > 2:
			raise ValueError(u'WeixinDeleteCustomerizedMenuApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinDeleteCustomerizedMenuApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'删除自定义菜单'

	def parse_response(self, api_response):
		return api_response

	def parese_post_param_json_str(self, args):
		pass

	def request_method(self):
		return api_settings.API_GET


	def is_retry(self, args):
		if len(args) == 1:
			return True if args[0] is True else False
		return False

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
			api_settings.WEIXIN_API_PROTOCAL, 
			api_settings.WEIXIN_API_DOMAIN,
			CUSTOMERIZED_MENU_DELETE_URI,
			param_dict
			)