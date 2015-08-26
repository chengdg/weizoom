# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
import logging
logger = logging.getLogger('core')

NAME2TASK = {}

def register(name, task):
	global NAME2TASK
	NAME2TASK[name] = task
	logger.info('register task "%s"', name)

def get_task(name):
	global NAME2TASK
	return NAME2TASK.get(name, None)

def dump():
	global NAME2TASK
	names = list(NAME2TASK.keys())
	names.sort()
	for name in names:
		func = NAME2TASK[name]
		if type(func) == dict or type(func) == list:
			print '\t%s' % name
		else:
			print '\t%s\t%s' % (name, func.func_doc.strip() if func.func_doc else '')