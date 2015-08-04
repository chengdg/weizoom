# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
import fnmatch

if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

	os.environ['DJANGO_SETTINGS_MODULE'] = 'viper.settings'	

import unittest

from django.db.models import get_app
from django.utils.importlib import import_module

UNITTEST_FILE_PATTERN = '*_tests.py'
SELENIUM_TEST_FILE_NAME = 'selenium_tests.py'
SKIP_DIRS = ['pageobject', 'templates', 'templatetags', 'sql']

def _get_all_test_file_pathes(root_path):
	all_test_file_pathes = []
	for root, dirs, files in os.walk(root_path):
		should_skip = False
		for skip_dir in SKIP_DIRS:
			if root.find(skip_dir) > 0:
				should_skip = True
				break

		if should_skip:
			continue

		for filename in fnmatch.filter(files, UNITTEST_FILE_PATTERN):
			if SELENIUM_TEST_FILE_NAME == filename:
				continue

			all_test_file_pathes.append(os.path.join(root, filename))
	return all_test_file_pathes

def _build_test_module_full_names(test_file_pathes):
	def build_test_module_full_name(test_file_path):
		test_file_path = test_file_path.replace(os.sep, '.')

		if test_file_path.startswith('..'):
			test_file_path = test_file_path[2:-3] #remove .py and leading .
		elif test_file_path.startswith('.'):
			test_file_path = test_file_path[1:-3] #remove .py and leading .
		else:
			test_file_path = test_file_path[:-3] #remove .py

		return test_file_path

	return [build_test_module_full_name(test_file_path) for test_file_path in test_file_pathes]

def _load_test_modules(app_name, test_module_full_names):
	def load_test_module(test_module_full_name):
		return import_module('.'.join(prefix + [test_module_full_name]))

	app_module = get_app(app_name)
	parts = app_module.__name__.split('.')
	prefix = parts[1:-1]

	return [load_test_module(test_module_full_name) for test_module_full_name in test_module_full_names]

def load_testsuits_from_app(app_name):
	all_test_files = _get_all_test_file_pathes(app_name)
	test_module_full_names = _build_test_module_full_names(all_test_files)
	test_modules = _load_test_modules(app_name, test_module_full_names)

	test_suites = []
	for test_module in test_modules:
		test_suites.append(unittest.defaultTestLoader.loadTestsFromModule(test_module))
	return unittest.TestSuite(test_suites)

def build_test_suite_from(test_cases):
    """
    Returns a single or group of unittest test suite(s) that's ready to be
    run. The function expects a list of classes that are subclasses of
    TestCase.

    The function will search the module where each class resides and
    build a test suite from that class and all subclasses of it.
    """
    test_suites = []
    for test_case in test_cases:
        mod = __import__(test_case.__module__)
        components = test_case.__module__.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        tests = []
        for item in mod.__dict__.values():
            if type(item) is type and issubclass(item, test_case):
                tests.append(item)
        test_suites.append(unittest.TestSuite(map(unittest.TestLoader().loadTestsFromTestCase, tests)))
    return unittest.TestSuite(test_suites)