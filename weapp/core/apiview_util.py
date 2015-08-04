# -*- coding: utf-8 -*-

__author__ = 'robert'

def call_api(apis):
	def inner_call_api(request):
		print '===== in call_api ====='
		items = request.path.split('/')
		print items
		if items[-1]:
			resource = items[-2]
			action = items[-1]
		else:
			resource = items[-3]
			action = items[-2]

		api_function = '%s_%s' % (action, resource)
		for key in apis:
			print key
		print api_function
		print apis[api_function]


	return inner_call_api


def get_api_function(request, apis):
	items = request.path.split('/')
	if items[-1]:
		resource = items[-2]
		action = items[-1]
	else:
		resource = items[-3]
		action = items[-2]

	api_function = '%s_%s' % (action, resource)
	return apis[api_function]
