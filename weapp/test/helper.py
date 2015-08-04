# -*- coding: utf-8 -*-

from django.db import connection
import selenium
import urllib

import weapp.settings
from django.contrib.auth.models import User

from account.models import *

group2functions = {}

def register(group):
	def inner_register(func):
		group2functions.setdefault(group, {})[func.__name__] = func
		return func
	return inner_register

def is_registered(group, function_name):
	if group in group2functions:
		return function_name in group2functions[group]
	else:
		return False

class FunctionFilterMixin(object):
	@classmethod
	def filter_function_by_group(cls, group):
		all_functions = [name for name in cls.__dict__ if name.startswith('test_')]
		functions = []
		for function in all_functions:
			if is_registered(group, function):
				functions.append(function)
				
		functions.sort()
		return functions

class TestHelperMixin(object):
	def assert_dict(self, expected, actual):
		for key in expected:
			self.assertEquals(expected[key], actual[key])

	def assert_list(self, expected, actual):
		self.assertEquals(len(expected), len(actual))

		for i in range(len(expected)):
			expected_obj = expected[i]
			actual_obj = actual[i]
			if isinstance(expected_obj, dict):
				self.assert_dict(expected_obj, actual_obj)
			else:
				self.assertEquals(expected_obj, actual_obj)

def execute_sql(sql):
	cursor = connection.cursor()
	cursor.execute(sql)
	connection._commit()

WAIT_SHORT_TIME = 1