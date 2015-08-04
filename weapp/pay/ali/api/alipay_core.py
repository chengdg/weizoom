# -*- coding: utf-8 -*-

__author__ = 'chuter'

import api_settings

from sign import md5_sign
from urllib import urlencode

from alipay_request_params import *

def assert_param(params):
	if None == params:
		raise ValueError('params can not be None')

	if type(params) != type({}):
		raise ValueError('params must be dict type')

#========================================================
# filter_alipay_request_params_to_build_sign : 除去
# 支付宝支付参数信息中的空值和签名参数
#========================================================
def filter_alipay_request_params_to_build_sign(params):
	assert_param(params)

	# 首先除去空值和签名参数
	filtered_params = {}
	for key in params.keys():
		if params[key] == '' or None == params[key] or 'sign_type' == key:
			continue

		filtered_params[key] = params[key]

	return filtered_params

def build_str_params(params, input_charset):
	assert_param(params)

	str_params = {}
	for key, val in params.iteritems():
		if type(val) == type(u''):
			val = val.encode(input_charset)
		str_params[key] = val

	return str_params

#===========================================================
# create_link_str : 按照参数名称进行排序，并按照“参数=参数
# 值”的模式用“&”字符拼接成字符串
#===========================================================
def create_link_str(request_params, input_charset):
	assert_param(request_params)

	str_params = build_str_params(request_params, input_charset)

	param_keys = str_params.keys()
	param_keys.sort()

	key_value_pairs_list = []
	for key in param_keys:
		key_value_pairs_list.append("{}={}".format(key, str_params[key]))

	return '&'.join(key_value_pairs_list)

#===========================================================
# create_link_str_not_sort : 请求参数按照固定参数排序，以“参数=参数值”
# 的模式用“&”字符拼接成字符串
#===========================================================
def create_link_str_not_sort(request_params):
	assert_param(request_params)

	str_params = request_params(request_params)

	select_params = {}
	select_params[AlipayRequestParams.SERVICE] = str_params[AlipayRequestParams.SERVICE]
	select_params[AlipayRequestParams.V] = str_params[AlipayRequestParams.V]
	select_params[AlipayRequestParams.SEC_ID] = str_params[AlipayRequestParams.SEC_ID]
	select_params[AlipayRequestParams.NOTIFY_DATA] = str_params[AlipayRequestParams.NOTIFY_DATA]
	
	key_value_pairs_list = []
	for key in select_params:
		key_value_pairs_list.append("{}={}".format(key, select_params[key]))

	return '&'.join(key_value_pairs_list)

def build_request_param_with_sign(params):
	assert_param(params)

	# 除去请求参数中的空值和签名参数
	filltered_params = filter_alipay_request_params_to_build_sign(params)
	# 生成签名结果
	mysign = build_request_sign(filltered_params)
	# 签名结果与签名方式加入请求提交参数信息中
	filltered_params[AlipayRequestParams.SIGN] = mysign
	if params[AlipayRequestParams.SERVICE] != api_settings.TRADE_CREATE_SERVICE and \
		params[AlipayRequestParams.SERVICE] != api_settings.AUTH_AND_EXECUTE_SERVICE:
		filltered_params[AlipayRequestParams.SIGN_TYPE] = params[AlipayRequestParams.SEC_ID]

	return filltered_params

def build_request_sign(params):
	assert_param(params)

	link_str = create_link_str(params, params[AlipayRequestParams.INPUT_CHARSET])
	if params[AlipayRequestParams.SEC_ID] != 'MD5':
		raise ValueError('Only surpport md5 sign right now')

	return md5_sign(link_str, params['key'])

def build_request_url(base_url, params):
	assert (base_url)
	assert_param(params)
	
	str_params = build_str_params(params, params[AlipayRequestParams.INPUT_CHARSET])
	return "{}?{}".format(base_url, urlencode(str_params))