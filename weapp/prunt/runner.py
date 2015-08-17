# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
import logging
import traceback

import registry
import config

CUR_DIR = ''
logger = logging.getLogger('core')


def load_builtin_tasks():
	logger.info('load builtin tasks')
	builtin_dir = os.path.join(CUR_DIR, 'prunt', 'builtin')
	print builtin_dir
	for file_name in os.listdir(builtin_dir):
		file_path = os.path.join(builtin_dir, file_name)
		if not os.path.isdir(file_path):
			continue

		if not os.path.exists(os.path.join(file_path, 'task.py')):
			continue

		task_module_path = 'prunt.builtin.%s.task' % file_name
		module = __import__(task_module_path, {}, {}, ['*',])


def load_pruntfile():
	prunt_file_path = os.path.join(CUR_DIR, 'Pruntfile.py')
	module = __import__('Pruntfile', {}, {}, ['*',])


def run_task(targets, config_dict=None):
	import prunt
	import sys
	has_error = False
	for target in targets:
		task = sys.modules['registry'].get_task(target)
		if task:
			#获取task集合
			task_type = type(task)
			if task_type == list:
				tasks = task
			else:
				tasks = [task]

			#遍历每个task，执行之
			for task in tasks:
				if type(task) == dict:
					original_task_name = task['original_name']
				else:
					original_task_name = target

				#获取真正的task function
				while type(task) == dict:
					if type(task['task_func']) != dict:
						break
					else:
						task = task['task_func']

				if type(task) == dict:
					target = task['original_name']
					if task.get('config_dict', None):
						config_dict = task['config_dict']
					func = task['task_func']
				else:
					func = task

				logger.info('run task "%s"', original_task_name)
				if config_dict:
					env = config.PruntEnv(target, config_dict)
				else:
					env = config.PruntEnv(target, prunt.get_config_for(target))
				func(env)
		else:
			logger.error('no task named "%s"', target)
			has_error = True
			prunt.set_error()

	return not has_error


def run(targets, config_dict=None):
	load_builtin_tasks()
	load_pruntfile()
	return run_task(targets, config_dict)
	


if __name__ == '__main__':
	#init logging
	FORMAT = '[%(levelname)s:%(filename)s:%(name)s]:  %(message)s'
	logging.basicConfig(level=logging.NOTSET, format=FORMAT)
	logger = logging.getLogger('core')

	CUR_DIR = os.getcwd()
	sys.path.insert(0, CUR_DIR)
	targets = sys.argv[1:]
	if not targets:
		targets = ['default']

	import prunt		
	try:
		run(targets)
	except:
		type, value, tb = sys.exc_info()
		print type
		print value
		traceback.print_tb(tb)
		prunt.set_error()

	if prunt.has_error():
		logger.warn('build FAILED!!!')
	else:
		logger.info('build SUCCESS')