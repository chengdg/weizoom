# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
import logging

import registry

logger = logging.getLogger('core')


class PruntConfig(object):
	def __init__(self, task_name, dict):
		self.task_name = task_name
		self._dict = dict

	def __getitem__(self, key):
		return self._dict[key]

	def __setitem__(slef, key, value):
		raise RuntimeError("not support set operation in PruntConfig")

	def require(self, key):
		if not key in self._dict:
			raise RuntimeError("task '%s' require '%s' in it's config object" % (self.task_name, key))


class PruntEnv(object):
	def __init__(self, task_name, config={}):
		self.config = PruntConfig(task_name, config)
		self.task_name = task_name

		import prunt
		self.run_task = prunt.run_task
		self.set_last_result = prunt.set_last_result
		self.get_last_result = prunt.get_last_result

