# -*- coding: utf-8 -*-

__author__ = 'aix'

from core.jsonresponse import create_response

def bind_phone(request):
	"""
	绑定手机的api请求
	@param request:
	@return:
	"""
	#TODO
	response = create_response(200)
	return response.get_response()

def exchange_card(request):
	"""
	兑换卡的api请求
	@param request:
	@return:
	"""
	#TODO
	response = create_response(200)
	return response.get_response()