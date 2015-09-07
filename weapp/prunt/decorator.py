# -*- coding: utf-8 -*-

__author__ = 'robert'

import logging
import sys

def register_task(name):
	def inner(func):
		def wrapper(prunt=None):
			if not prunt:
				prunt = {}
			func(prunt)
		registry = sys.modules['registry']
		registry.register(name, wrapper)
		wrapper.func_doc = func.func_doc
		return wrapper

	return inner