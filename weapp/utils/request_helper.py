# -*- coding: utf-8 -*-

__author__ = 'chuter'

def get_request_host(request):
	if request is None:
		return None

	request_host = request.META.get('HTTP_HOST', None)

	if request_host is None:
		request_host = request.META.get('SERVER_NAME', None)

	return request_host