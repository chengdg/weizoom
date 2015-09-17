# -*- coding: utf-8 -*-

import sys
import os

from django.conf import settings

wapi_path = os.path.join(settings.PROJECT_HOME, '..', 'wapi')
for f in os.listdir(wapi_path):
	f_path = os.path.join(wapi_path, f)
	if os.path.isdir(f_path):
		resource_json_path = os.path.join(f_path, 'resource.json')
		if not os.path.exists(resource_json_path):
			continue

		module_name = 'wapi.%s' % f
		module = __import__(module_name, {}, {}, ['*',])


from core import api_resource

class ApiNotExistError(Exception):
	pass

def __call(method, app, resource, data):
	key = '%s-%s' % (app, resource)

	resource = api_resource.APPRESOURCE2CLASS.get(key, None)
	if not resource:
		raise ApiNotExistError('%s:%s' % (key, method))

	func = getattr(resource['cls'], method, None)
	if not func:
		raise ApiNotExistError('%s:%s' % (key, method))		

	return func(data)


def get(app, resource, data):
	return __call('get', app, resource, data)


def post(app, resource, data):
	return __call('get', app, resource, data)


def put(app, resource, data):
	return __call('get', app, resource, data)


def delete(app, resource, data):
	return __call('get', app, resource, data)