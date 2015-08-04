# -*- coding: utf-8 -*-

__author__ = 'chuter'

import urllib2
import json

from urllib import urlencode

from jsonresponse import create_response_from_json_str

class ApiRequestMethod(object):
	GET = "GET"
	POST = "POST"

class ApiOps(object):
	GET    = 'get'
	CREATE = 'create'
	MODIFY = 'modify'
	DELETE = 'delete'

class ApiResponseCode(object):
	SUCCESS = 200
	INVALID_PARAM = 400
	INTERNAL_ERROR = 500

class ApiException(Exception):
	pass

#===============================================================================
# Api : 对应java apiserver的Api
# 对Api的访问必须包含以下信息：
# Api名称（对应的资源名称），
# 所做的操作类型（查询、创建、删除或修改）
# 参数信息
# 
# 例如如下访问地址：
# http://api.weizoom.com/order/get/?order_id=123
# 对应的api名称为order，所做的操作为get（查询），参数中描述了所要查询的
# 资源id
#
# 对Api请求的结果类型为：JsonResponse
#===============================================================================
class Api(object):
	def __init__(self, apiserver_host, apiname, param_dict, op=ApiOps.GET):
		if not apiname or not apiserver_host:
			raise ValueError('the apiname and apiserver_host must be given')

		self.apiserver_host = apiserver_host
		self.apiname = apiname
		self.param_dict = param_dict if param_dict else {}

		if type(self.param_dict) != type({}):
			raise ValueError("param_dict must be dict type")

		if ApiOps.GET != op and ApiOps.DELETE != op and \
				ApiOps.CREATE != op and ApiOps.MODIFY != op:
			raise ValueError("not surpport api operation " + op)

		self.apiop = op

	def request(self, method=ApiRequestMethod.GET):
		if ApiRequestMethod.GET == method:
			return self.__execute_get_request()
		elif ApiRequestMethod.POST == method:
			return self.__execute_post_request()
		else:
			raise ApiException("Not surpport request method %s yet" % method)

	def __execute_get_request(self):
		request_url = "http://%s/api/%s/%s/?%s" % (self.apiserver_host, \
				self.apiname, self.apiop, self.__encode_request_param(self.param_dict))
		from watchdog.utils import watchdog_info
		watchdog_info(request_url)
		response = None
		try:
			response = urllib2.urlopen(request_url)
			return self.__build_json_response(response.read())
		except Exception, e:
			raise ApiException('failed to request ' + request_url, e)
		finally:
			if response:
				response.close()

	def __execute_post_request(self):
		post_url = "http://%s/api/%s/%s/" % (self.apiserver_host, \
				self.apiname, self.apiop,)
		from watchdog.utils import watchdog_info
		watchdog_info(post_url)
		response = None
		try:
			req = urllib2.Request(post_url)
			data = urlencode(self.param_dict)
			opener = urllib2.build_opener()
			response = opener.open(req, data)
			return self.__build_json_response(response.read())
		except Exception, e:
			raise ApiException('failed to do post request ' + post_url, e)
		finally:
			if response:
				response.close()

	def __build_json_response(self, api_response):
		assert (api_response)
		return create_response_from_json_str(api_response)

	def __encode_request_param(self, param_dict):
		assert (param_dict)
		return urlencode(param_dict)
