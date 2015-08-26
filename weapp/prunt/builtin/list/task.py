# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys

from prunt.decorator import register_task

@register_task('list')
def list(prunt):
	registry = sys.modules['registry']
	print 'Avaliable prunt tasks are:'
	registry.dump()
