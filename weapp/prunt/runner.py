# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
import logging

import registry


def run(targets):
	for target in targets:
		task_func = registry.get_task(target)
		if task_func:
			logger.info('run task "%s"', target)
			task_func()
		else:
			logger.warn('no task named "%s"', target)


if __name__ == '__main__':
	#init logging
	FORMAT = '[%(levelname)s:%(filename)s:%(name)s]:  %(message)s'
	logging.basicConfig(level=logging.NOTSET, format=FORMAT)
	logger = logging.getLogger('core')

	cur_dir = os.getcwd()
	prunt_file_path = os.path.join(cur_dir, 'Pruntfile.py')
	sys.path.insert(0, cur_dir)
	module = __import__('Pruntfile', {}, {}, ['*',])
	targets = sys.argv[1:]
	run(targets)