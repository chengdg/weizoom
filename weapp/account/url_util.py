# -*- coding: utf-8 -*-

__author__ = 'chuter'

"""
系统中对webapp和api的url的构造规则为：

http://domian/[m]/resource/[api]/[...]/?appid=1&other_query_string

其中m标识所访问的是否是webapp
api标识访问的是api服务

1. 对于api的访问（全部是在js中通过ajax方式发起的）
   构造模板：http://wx.weizoom.com/[resource_desc]/api/[resource_type]/[op_type]/?[specific_resource_desc]
   其中resource_desc表示api所操作的资源描述，例如location描述操作的地域相关的资源
       resource_typ表示所操作的资源名称，例如province表示进行省份api操作
       op_type表示操作类型，包括get/create/delete/modify, 分别为查询、创建、删除、修改
       specific_resource_desc表示所操作的具体资源的描述，
       例如id=1&appid=2表示对id为2的app中id为1的资源进行操作

   如果是公共的api，那么query_string中没有appid

2. 对于webapp的访问
   示例：http://wx.weizoom.com/m/products/?appid=1

3. pc端商城的url构造规则为:
http://domian/pcmall/[webapp id]/?query_string
示例：示例：http://wx.weizoom.com/pcmall/3189/
"""

import re
from hashlib import md5

from django.conf import settings

APPID_QUERY_STR_KEY = 'appid'
def get_webappid_from_request(request):
	if hasattr(request, 'user_profile') and request.user_profile:
		return request.user_profile.webapp_id
	elif hasattr(request, 'app') and request.app and request.app.appid:
		return request.app.appid
	else:
		"""
		直接从query str中解析出appid参数信息
		"""
		query_str = request.META['QUERY_STRING']
		
		if query_str.find(APPID_QUERY_STR_KEY+'=') >= 0:
			key_value_pairs = query_str.split('&')
			for key_value_pair in key_value_pairs:
				if key_value_pair.startswith(APPID_QUERY_STR_KEY+'='):
					key_value = key_value_pair.split('=')
					if len(key_value) == 2:
						return key_value[1]

			return None
		else:
			return None

def __get_request_url(request):
	return request.get_full_path()

def is_pay_request(request):
	url = __get_request_url(request)
	return ('/webapp/wxpay/' in url) or ('/webapp/alipay/' in url) or ('/pay/' in url)

def is_pay_callback_request(request):
	url = __get_request_url(request)
	return ('/alipay/mall/pay_result/' in url)

def is_paynotify_request(request):
	url = __get_request_url(request)
	return ('/pay_notify_result/' in url) or ('/wxpay/warning' in url) or ('/wxpay/feedback' in url)

def is_request_for_api(request):
	url = __get_request_url(request)
	return url.find('/api/') >= 0

def is_request_for_webapp(request):
	url = __get_request_url(request)
	return ('/weixin/message/material/news_detail/mshow/' in url) or ('/termite2/webapp_page/' in url) or ('/jqm/preview/' in url) or ('/project_api/call' in url) or is_pay_request(request) or ('weshop/api/mall' in url) or is_pay_callback_request(request)

def is_request_for_webapp_api(request):
	url = __get_request_url(request)
	return ('/webapp/api/project_api/call/' in url)

def is_request_for_pcmall(request):
	url = __get_request_url(request)
	return url.find('/pcmall/') >= 0

def is_request_for_temporary_qrcode_image(request):
	'''
	是否是生成临时二维码的接口
	by liupeiyu 15.6.26
	'''
	url = __get_request_url(request)
	return ('/termite2/qrcode_image/' in url)


#是否是后台编辑请求
def is_request_for_editor(request):
	# request_domain = request.META.get('HTTP_HOST', None)

	# if request_domain is None:
	# 	request_domain = request.META.get('SERVER_NAME', '')
	if is_request_for_temporary_qrcode_image(request):
		return True

	return  (not is_request_for_api(request)) and\
				(not is_request_for_webapp(request)) and\
				(not is_request_for_pcmall(request)) and\
				(not is_pay_request(request))

def is_request_for_weixin(request):
	url = __get_request_url(request)
	return url.find('/weixin/') >= 0

def is_request_for_oauth(request):
	url = __get_request_url(request)
	return url.find('/oauth/') >= 0

def is_js_config(request):
	url = __get_request_url(request)
	if url.find('js/config/') > -1 or url.find('js/renovate/') > -1:
		return True
	else:
		return False