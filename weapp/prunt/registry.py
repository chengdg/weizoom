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
