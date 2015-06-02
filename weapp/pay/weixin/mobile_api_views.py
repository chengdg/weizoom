# -*- coding: utf-8 -*-

from core import apiview_util

from pay.weixin import request_api_util

########################################################################
# query_order: 查询订单
########################################################################
def query_order(request):
	return request_api_util.query_order(request)


########################################################################
# get_unifiedorder: 获取预支付订单号
########################################################################
def get_unifiedorder(request):
	return request_api_util.get_unifiedorder(request)


########################################################################
# get_openid: 授权获取openid
########################################################################
def get_openid(request):
	return request_api_util.get_openid(request)


def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)