# -*- coding: utf-8 -*-

__author__ = 'chuter'

from tenpay_config import *
from tenpay_request_params import *

def assert_param(params):
	if None == params:
		raise ValueError('params can not be None')

	if type(params) != type({}):
		raise ValueError('params must be dict type')

#========================================================
# filter_tenpay_request_params_to_build_sign : 除去
# 财付通支付参数信息中的空值和签名参数
#========================================================
def filter_tenpay_request_params_to_build_sign(params):
	assert_param(params)

	# 首先除去空值和签名参数
	filtered_params = {}
	for key in params.keys():
		if params[key] == '' or None == params[key] or TenpayRequestParams.SIGN_TYPE == key:
			continue

		filtered_params[key] = params[key]

	return filtered_params

def build_str_params(params):
	assert_param(params)

	str_params = {}
	for key, val in params.iteritems():
		if type(val) == type(u''):
			val = val.encode(TenpayConfig.input_charset)
		str_params[key] = val

	return str_params

#===========================================================
# create_link_str : 按照参数名称进行排序，并按照“参数=参数
# 值”的模式用“&”字符拼接成字符串
#===========================================================
def create_link_str(request_params):
	assert_param(request_params)

	str_params = build_str_params(request_params)

	param_keys = str_params.keys()
	param_keys.sort()

	key_value_pairs_list = []
	for key in param_keys:
		key_value_pairs_list.append("{}={}".format(key, str_params[key]))

	return '&'.join(key_value_pairs_list)