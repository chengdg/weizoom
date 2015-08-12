# -*- coding: utf-8 -*-

__author__ = 'robert'

from prunt.decorator import register_task

print 'load Pruntfile.py'

@register_task('hello')
def hello(prunt):
	print 'hello prunt'