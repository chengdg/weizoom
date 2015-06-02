# -*- coding: utf-8 -*-
"""
映射API的views

举例：

 * API的URL为 `http://host/webapp/api/unread_count_notify/get/` 由apiurl()映射成 `views.get_unread_count_notify()`。

"""

#import sys
import os
#import traceback
#import StringIO
#import cProfile
#import time
import types
from django.conf import settings
#from datetime import timedelta, datetime, date

from django.core.urlresolvers import ResolverMatch, Resolver404
#from django.contrib.auth.models import User
#from django.contrib.sessions.models import Session
#from django.http import HttpResponseRedirect, HttpResponse
#from django.template import RequestContext
#from django.conf import settings

class DataObj(object):
	def __init__(self):
		self.pattern = ''

class ApiURLPattern(object):
	def __init__(self, app_dir):
		self.app_dir = app_dir
		self.is_func_loaded = False
		self.name2func = {}
		self.loaded_file_set = None
		self.regex = DataObj()
		self.callback = None
		self.default_args = []
		self.name = app_dir

	def __should_update_loaded_files(self):
		if settings.MODE != 'develop':
			return False

		loaded_file_set, _ = self.__load_api_view_files(is_load_module=False)
		if len(loaded_file_set - self.loaded_file_set) > 0:
			return True
		else:
			return False

	def __load_api_view_files(self, is_load_module=False):
		base_dir = settings.PROJECT_HOME
		api_modules = []
		loaded_file_set = set()
		#files = []
		for f in os.listdir(os.path.join(base_dir, '..', self.app_dir)):
			if f.endswith('api_views.py'):
				if is_load_module:
					api_module_name = '{}.{}'.format(self.app_dir, f[:-3])
					module = __import__(api_module_name, {}, {}, ['*',])
					api_modules.append(module)
				loaded_file_set.add(f)
		return loaded_file_set, api_modules

	def __load_api_func(self):
		if self.is_func_loaded:
			return

		self.loaded_file_set, api_modules = self.__load_api_view_files(is_load_module=True)

		for module in api_modules:
			module_name = module.__name__
			module_vars = vars(module)
			if not module_vars:
				continue

			for key, value in vars(module).items():
				if not hasattr(value, '__module__'):
					continue

				if value.__module__ != module_name:
					continue

				if not isinstance(value, types.FunctionType):
					continue

				self.name2func[key] = value

		self.is_func_loaded = True

	def __get_api_func(self, path):
		items = path.split('/')
		items.reverse()
		items = [item for item in items if len(item) > 0]
		func_name = '_'.join(items)

		return self.name2func.get(func_name, None)

	def resolve(self, path):
		self.regex.pattern = '{}/{}'.format(self.app_dir, path)
		if not self.is_func_loaded:
			self.__load_api_func()
		func = self.__get_api_func(path)
		if func:
			return ResolverMatch(func, (), {}, path)
		else:
			if self.__should_update_loaded_files():
				self.is_func_loaded = False
				self.loaded_file_set = None
				self.name2func = {}
				return self.resolve(path)
			else:
				tried = []
				for key in self.name2func:
					tried.append([{'regex':{'pattern': '^{}/$'.format(key)}}])
				raise Resolver404({'tried': tried, 'path' : path})


class ApiUrl(object):
	def __init__(self, app_dir):
		self.app_dir = app_dir
		self.api_url_patterns = None

	@property
	def urlpatterns(self):
		if not self.api_url_patterns:
			self.api_url_patterns = [ApiURLPattern(self.app_dir)]

		return self.api_url_patterns


def apiurl(app_name):
	return (ApiUrl(app_name), app_name, '')
	