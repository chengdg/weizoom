# -*- coding: utf-8 -*-

__author__ = 'chuter'

import json

import api_settings

from core.jsonresponse import decode_json_str
from core.exceptionutil import unicode_full_stack

from watchdog.utils import watchdog_error

from pay.util import ObjectAttrWrapedInDict

from urllib import unquote

class AliPayApiError(Exception):
	def __init__(self, ali_error_response):
		self.error_response = ali_error_response

	def __unicode__(self):
		if hasattr(self.error_response, 'detail'):
			detail = self.error_response.detail
		else:
			detail = ''
		return u"errcode:{}\nerrmsg:{}\ndetail:{}".format(
			self.error_response.code,
			self.error_response.msg,
			detail
			)

	def __str__(self):
		return self.__unicode__().encode('utf-8')

"""
支付宝Api错误信息，包含以下属性：
errorcode : 错误代码，全部错误代码请参见weixin_error_codes
errmsg : 错误信息
detail : 异常堆栈
"""
class AliPayErrorResponse(ObjectAttrWrapedInDict):
	def __init__(self, src_dict):
		print src_dict
		super(AliPayErrorResponse, self).__init__(src_dict)

		if not hasattr(self, 'detail'):
			self.detail = ''

def build_system_exception_response():
	response_dict = {}
	response_dict['code'] = 995995
	response_dict['msg'] = u'系统自身异常'
	response_dict['detail'] = unicode_full_stack()
	
	return AliPayErrorResponse(response_dict)

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
def call_api(ali_pay_api, api_instance_class):

	def _call_api(*agrs):
		# 获得该api的请求方式： get or post
		try:
			request_method = api_instance_class.request_method()
		except:
			raise ValueError(u'request method illegality')
		request_url, api_desc = api_instance_class.get_get_request_url_and_api_info(agrs)
		api_response = None
		try:
			# get 
			if request_method == api_settings.API_GET:
				api_response = ali_pay_api.ali_http_client.get(request_url)
			# post	
			if request_method == api_settings.API_POST:
				post_param_json_str = api_instance_class.parese_post_param_json_str(agrs)
				api_response = ali_pay_api.ali_http_client.post(request_url, post_param_json_str)
		except:
			ali_pay_api._raise_system_error(api_desc)

		result = api_response
		
		return api_instance_class.parse_response(api_response)

	return _call_api

class AliPayApi(object):
	def __init__(self, ali_http_client):
		self.ali_http_client = ali_http_client

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
		notify_msg = u"支付宝api调用失败，api:{}\n错误信息:{}".format(api_name, apierror.__unicode__())
		watchdog_error(notify_msg,user_id=user_id)

	def _raise_system_error(self, api_name='', user_id=0):
		system_error_response = build_system_exception_response()
		apierror = AliPayApiError(system_error_response)

		self._notify_api_request_error(apierror, api_name, user_id)		

import urllib2
class AliHttpClient(object):
	def __init__(self):
		super(AliHttpClient, self).__init__()

	def get(self, url):
		ali_response = urllib2.urlopen(url)
		try:
			return self._parse_response(unquote(ali_response.read()).decode('utf-8'))
		except:
			return self._parse_response(ali_response.read())
		finally:
			if ali_response:
				try:
					ali_response.close()
				except:
					pass

	def post(self, url, post_param, is_for='form'):
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