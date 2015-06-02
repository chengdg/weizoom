# -*- coding: utf-8 -*-

__author__ = 'chuter'


import unittest

def init_test_env_with_db():
	print ' start init test environment '.center(100, '*')
	import os
	import sys
	path = os.path.abspath(os.path.join('.', '..'))
	sys.path.append(path)
	path = os.path.abspath('.')
	sys.path.append(path)

	from weapp import settings
	os.environ['DJANGO_SETTINGS_MODULE'] = 'weapp.settings'
	settings.DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

def init_test_env_without_db():
	print ' start init test environment '.center(100, '*')
	import os
	import sys
	path = os.path.abspath(os.path.join('.', '..'))
	sys.path.append(path)
	path = os.path.abspath('.')
	sys.path.append(path)

def getTestUser():
	from django.contrib.auth.models import User
	return User.objects.get(id=2)

def getTestUserProfile():
	from account.models import UserProfile
	from django.contrib.auth.models import User
	return UserProfile.objects.get(user=User.objects.get(id=2))
	
import logging
import inspect

def __get_test_info():
	cur_frame = inspect.currentframe()
	test_module_frame = cur_frame.f_back.f_back

	test_file = test_module_frame.f_globals['__file__']
	test_names = []
	for attr in test_module_frame.f_globals.keys():
		value = test_module_frame.f_globals[attr]
		if attr.startswith('test_') and inspect.isfunction(value):
			test_names.append(attr)
		elif inspect.isclass(value) and issubclass(value, unittest.TestCase):
			test_names.append(attr)

	return test_file, test_names

def run_test():
	nose2_argv = ["-v", "--no-user-config", "--log-level=%d" % logging.WARNING]

	test_file, test_names = __get_test_info()
	nose2_argv.insert(0, test_file)
	nose2_argv.extend(test_names)

	import nose2
	nose2.main(argv=(nose2_argv))

def run_test_with_db():
	from django.conf import settings
	from django.db import connection
	from django.test.utils import setup_test_environment, teardown_test_environment
	from django.core.management import call_command

	old_database_name = None
	verbosity = 0
	
	try:
		setup_test_environment()
		settings.DEBUG = False    

		old_database_name = settings.DATABASES['default']['NAME']
		connection.creation.create_test_db(verbosity)

		# call_command('loaddata', 'devdata/initial_dev_data.json')

		nose2_argv = ["-v", "--no-user-config", "--log-level=%d" % logging.WARNING]

		test_file, test_names = __get_test_info()
		nose2_argv.insert(0, test_file)
		nose2_argv.extend(test_names)

		import nose2
		nose2.main(argv=(nose2_argv))
	finally:
		connection.creation.destroy_test_db(old_database_name, verbosity)
		teardown_test_environment()