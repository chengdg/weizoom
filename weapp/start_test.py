# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'weapp.settings'

import sys
path = os.path.abspath(os.path.join('.', '..'))
sys.path.insert(0, path)
print sys.path

import unittest
import traceback
import subprocess
from django.conf import settings


def run_test(wanted_apps, action=None, group='all'):
	print 'apps:%s, action:%s, group:%s' % (wanted_apps, str(action), group)
	subprocess.call('python test/init_test_environment.py', shell=True)

	#判断是否要进行全部测试，还是进行部分测试
	run_partial_apps = False
	if isinstance(wanted_apps, set):
		run_partial_apps = True

	for app in settings.INSTALLED_APPS:
		if app.startswith('django'):
			continue				
		
		#pos = app.find('.')
		#app = app[pos+1:]
		
		if run_partial_apps:
			if not app in wanted_apps:
				continue
			
		selenium_module = '%s.selenium_tests' % app
		selenium_file = '%s.py' % selenium_module.replace('.', '/')
		if os.path.exists(selenium_file):
			info = ' START TEST %s ' % selenium_module
			print '\n'
			print info.center(100, '*')
			module = __import__(selenium_module, {}, {}, ['*',])
			if action != None:
				#run action
				action_func = getattr(module, action)
				action_func()
			else:
				#run test
				module.init()
				test_modules = []
				if hasattr(module, 'sub_tests'):
					for sub_test in module.sub_tests:
						test_modules.append(sub_test)
				else:
					test_modules = [module]
				print 'test_modules: ', test_modules
				for test_module in test_modules:
					try:
						result = unittest.TextTestRunner(verbosity=2).run(test_module.suite(group))
					except:
						type, value, tb = sys.exc_info()
						traceback.print_tb(tb)
				module.clear()
		else:
			print 'NO TEST FILE: ', selenium_file


def print_usage():
	print 'Usage : python start_test.py [all|app1 app2 ...] <init|clear|group>'
	sys.exit(1)

	
if __name__ == '__main__':
	arg_count = len(sys.argv)
	if arg_count < 2:
		print_usage()

	if arg_count == 2:
		if sys.argv[1] == 'all':
			run_test('all')
		else:
			wanted_apps = set()
			wanted_apps.add(sys.argv[1])
			run_test(wanted_apps)
	else:
		item = sys.argv[-1]
		group = 'all'
		action = None
		if item == 'init' or item == 'clear':
			wanted_apps = set(sys.argv[1:-1])
			action = item
		elif item.startswith('group-'):
			wanted_apps = set(sys.argv[1:-1])
			group = item[6:]
		else:
			wanted_apps = set(sys.argv[1:])
		run_test(wanted_apps, action, group)	