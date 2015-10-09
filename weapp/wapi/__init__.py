# -*- coding: utf-8 -*-

import sys
import os

from django.conf import settings
from wapi_utils import wapi_log

wapi_path = os.path.join(settings.PROJECT_HOME, '..', 'wapi')
for f in os.listdir(wapi_path):
	f_path = os.path.join(wapi_path, f)
	if os.path.isdir(f_path):
		init_file_path = os.path.join(f_path, '__init__.py')
		if not os.path.exists(init_file_path):
			continue

		module_name = 'wapi.%s' % f
		module = __import__(module_name, {}, {}, ['*',])


from core import api_resource

class ApiNotExistError(Exception):
	pass

def __call(method, app, resource, data):
	resource_name = resource
	key = '%s-%s' % (app, resource)
	#print("called WAPI: {}/{}, param: {}".format(app, resource, data))

	resource = api_resource.APPRESOURCE2CLASS.get(key, None)
	if not resource:
		wapi_log(app, resource_name, method, data, -1)
		raise ApiNotExistError('%s:%s' % (key, method))

	func = getattr(resource['cls'], method, None)
	if not func:
		wapi_log(app, resource_name, method, data, -1)
		raise ApiNotExistError('%s:%s' % (key, method))

	response = func(data)
	wapi_log(app, resource_name, method, data, 0)
	return response


def get(app, resource, data):
	return __call('get', app, resource, data)


def post(app, resource, data):
	return __call('post', app, resource, data)


def put(app, resource, data):
	return __call('put', app, resource, data)


def delete(app, resource, data):
	return __call('delete', app, resource, data)
