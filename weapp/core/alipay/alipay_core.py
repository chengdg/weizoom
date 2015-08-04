# -*- coding: utf-8 -*-

__author__ = 'chuter'

from alipay_config import *
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
		if params[key] == '' or None == params[key] or AlipayRequestParams.SIGN_TYPE == key:
			continue

		filtered_params[key] = params[key]

	return filtered_params

def build_str_params(params, alipay_config):
	assert_param(params)

	str_params = {}
	for key, val in params.iteritems():
		if type(val) == type(u''):
			val = val.encode(alipay_config.input_charset)
		str_params[key] = val

	return str_params

#===========================================================
# create_link_str : 按照参数名称进行排序，并按照“参数=参数
# 值”的模式用“&”字符拼接成字符串
#===========================================================
def create_link_str(request_params, alipay_config):
	assert_param(request_params)

	str_params = build_str_params(request_params, alipay_config)

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