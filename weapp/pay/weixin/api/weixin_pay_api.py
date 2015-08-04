# -*- coding: utf-8 -*-

__author__ = 'chuter'

import json

import api_settings
import weixin_error_codes as errorcodes

from core.jsonresponse import decode_json_str
from core.exceptionutil import unicode_full_stack

from watchdog.utils import watchdog_error

from pay.util import ObjectAttrWrapedInDict

from xml.etree import ElementTree
"""
微信Api

微信平台针对认证后的服务号提供api接口，具体列表和文档登录微信公众
平台后点击左侧导航栏中服务下的我的服务可以看到

该模块对微信平台提供的api接口进行描述，便于在程序中进行微信api的访问
每一个api的调用该模块根据微信平台api的协议进行相应请求的组织，然后
通过weixin_http_client（默认使用WeixinHttpClient）进行实际请求返回处理结果

如果需要测试，给定weixin_http_client的stub或者mock的实现即可

每个接口调用如果发生异常会抛出WeixinApiError, 可通过该异常示例的
error_response属性来获取微信的api反馈信息，error_response包含的信息有：
errorcode: 错误代码
errmsg: 错误信息
detail: 异常详情

-----------------------------------------------------------------------------------------

整体构架及微信api增加步骤：
	1.api_settings 增加 类似'get_user_info': 'core.wxapi.user_info_api.WeixinUserApi'
	2.api类规范如下：
		a.  该方法返回访问该api的请求方式：post or get
			def request_method(self):
			return 'get'

	 	b. 该方法返回当前要访问的api的地址和该api的描述
			def get_get_request_url_and_api_info(self, mpuser_access_token, varargs):
				pass

		c.  该方法处理请求的结果并组织相应结构返回结果
			def parse_response(self, api_response):
				pass
		d. 	该方法针对post方式组织post数据	
			def parse_post_param_json(self, varargs):
				pass
	
"""

class WeixinPayApiError(Exception):
	def __init__(self, weixin_error_response):
		self.error_response = weixin_error_response

	def __unicode__(self):
		if hasattr(self.error_response, 'detail'):
			detail = self.error_response.detail
		else:
			detail = ''
		return u"errcode:{}\nerrmsg:{}\ndetail:{}".format(
			self.error_response.errcode,
			self.error_response.errmsg,
			detail
			)

	def __str__(self):
		return self.__unicode__().encode('utf-8')

"""
微信Api错误信息，包含以下属性：
errorcode : 错误代码，全部错误代码请参见weixin_error_codes
errmsg : 错误信息
detail : 异常堆栈
"""
class WeixinPayErrorResponse(ObjectAttrWrapedInDict):
	def __init__(self, src_dict):
		super(WeixinPayErrorResponse, self).__init__(src_dict)

		if not hasattr(self, 'detail'):
			self.detail = ''

def build_system_exception_response():
	response_dict = {}
	response_dict['errcode'] = errorcodes.SYSTEM_ERROR_CODE
	response_dict['errmsg'] = errorcodes.code2msg[errorcodes.SYSTEM_ERROR_CODE]
	response_dict['detail'] = unicode_full_stack()
	return WeixinPayErrorResponse(response_dict)

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
def call_api(weixin_pay_api, api_instance_class):

	def _call_api(*agrs):
		# 获得该api的请求方式： get or post
		try:
			request_method = api_instance_class.request_method()
		except:
			raise ValueError(u'request method illegality')
		request_url, api_desc = api_instance_class.get_get_request_url_and_api_info(weixin_pay_api.access_token, weixin_pay_api.is_for, agrs)
		api_response = None
		try:
			# get 
			if request_method == api_settings.API_GET:
				api_response = weixin_pay_api.weixin_http_client.get(request_url)
			# post	
			if request_method == api_settings.API_POST:
				post_param_json_str = api_instance_class.parese_post_param_json_str(agrs)
				api_response = weixin_pay_api.weixin_http_client.post(request_url, post_param_json_str, weixin_pay_api.is_for)
		except:
			weixin_pay_api._raise_system_error(api_desc)

		result = api_response
		
		return api_instance_class.parse_response(api_response)

	return _call_api

class WeixinPayApi(object):
	def __init__(self, weixin_http_client, access_token='', is_for='json'):
		if access_token is None:
			raise ValueError(u'缺少授权信息')		
		self.is_for = is_for
		self.access_token = access_token
		self.weixin_http_client = weixin_http_client

	def __getattr__(self, name):
		if not name in api_settings.API_CLASSES.keys():
			raise ValueError(u'api_settings 里不存在该方法{}对应 api'.format(name))
		
		if not hasattr(self.__dict__, name):
			handler_path = api_settings.API_CLASSES[name]

			try:
				handler_module, handler_classname = handler_path.rsplit('.', 1)
			except ValueError:
				raise exceptions.ImproperlyConfigured('%s isn\'t a message handler module' % handler_path)
			from django.utils.importlib import import_module
			try:
				module = import_module(handler_module)
			except ImportError, e:
			 	raise ValueError('Error importing message handler %s: "%s"' % (handler_module, e))

			try:
				handler_api_class = getattr(module, handler_classname)
			except:
				raise ValueError('u error class')

			try:
				api_class_instance = handler_api_class()
			except:
				raise ValueError('u class can not be instance')

			self.__dict__[name] = call_api(self, api_class_instance)

		return self.__dict__[name]		

	def _notify_api_request_error(self, apierror, api_name='' ,user_id=0):
		notify_msg = u"微信api调用失败，api:{}\n错误信息:{}".format(api_name, apierror.__unicode__())
		watchdog_error(notify_msg,user_id=user_id)

	def _raise_system_error(self, api_name='', user_id=0):
		system_error_response = build_system_exception_response()
		apierror = WeixinPayApiError(system_error_response)

		self._notify_api_request_error(apierror, api_name, user_id)		

import urllib2

class WeixinHttpClient(object):
	def __init__(self):
		super(WeixinHttpClient, self).__init__()

	def get(self, url):
		weixin_response = urllib2.urlopen(url)
		try:
			return self._parse_response(weixin_response.read().decode('utf-8'))
		except:
			return self._parse_response(weixin_response.read())
		finally:
			if weixin_response:
				try:
					weixin_response.close()
				except:
					pass

	def post(self, url, post_param, is_for):
		if is_for == 'form':
			# 在 urllib2 上注册 http 流处理句柄
			register_openers()
			# 开始对文件 "DSC0001.jpg" 的 multiart/form-data 编码
			# "xx" 是参数的名字，一般通过 HTML 中的 <input> 标签的 name 参数设置
			# headers 包含必须的 Content-Type 和 Content-Length
			# datagen 是一个生成器对象，返回编码过后的参数
			#{"media": open("d://1.jpg", "rb")}
			datagen, headers = multipart_encode(post_param)
			# 创建请求对象
			request = urllib2.Request(url, datagen, headers)
			# 实际执行请求并取得返回
			weixin_response = urllib2.urlopen(request)#.read()
		elif is_for == 'xml':
			cookies = urllib2.HTTPCookieProcessor()
			opener = urllib2.build_opener(cookies)
			request = urllib2.Request(
				url = url,
				headers = {'Content-Type' : 'text/xml'},
				data = post_param.encode('utf8'))
			weixin_response = opener.open(request)
		else:
			req = urllib2.Request(url)
			opener = urllib2.build_opener()
			post_param_json = decode_json_str(post_param)
			weixin_response = opener.open(req, json.dumps(post_param_json, ensure_ascii=False).encode('utf-8'))

		try:
			if is_for == 'xml':
				response_data = weixin_response.read()
				tree = ElementTree.fromstring(response_data)
				data = {}
				#深度搜索、树的先序遍历
				for node in tree.iter():
					#深度搜索、树的先序遍历该结点下的子树
					for n in node.iter():
						if n.tag == 'xml':
							continue
						data[n.tag]=n.text
					break
				return self._parse_response(json.dumps(data))
			else:
				return self._parse_response(weixin_response.read().decode('utf-8'))
		finally:
			if weixin_response:
				try:
					weixin_response.close()
				except:
					pass

	def upload(self, url, upload_str_data):
		pass

	def download(self, url):
		pass

	def _parse_response(self, response_text):
		response_text = response_text.strip()

		if response_text.startswith(u'{') and response_text.endswith(u'}'):
			try:
				return decode_json_str(response_text)
			except:
				return response_text
		else:
			return response_text