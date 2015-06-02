# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django import template
from termite.utils import resource_util
#from django.template.loaders.filesystem import _loader


EMPTY_LIST = list()


#===============================================================================
# webapp_template ： 获得webapp模板
#===============================================================================
def webapp_template(request):
	if request.user.is_authenticated() and not request.user.is_superuser:
		profile = request.user.get_profile()
		webapp_template_info_module = '%s.webapp_template_info' % profile.webapp_template
		try:
			module = __import__(webapp_template_info_module, {}, {}, ['*',])
			return {'webapp_template': profile.webapp_template, 'webapp_editor_nav': module.NAV}
		except:
			import sys
			import traceback
			type, value, tb = sys.exc_info()
			print type
			print value
			traceback.print_tb(tb)
			return {'webapp_template': 'unknown', 'webapp_editor_nav': {}}
	else:
		return {'webapp_template': 'unknown', 'webapp_editor_nav': {}}


#===============================================================================
# css_name ： 获取当前使用的css文件
#===============================================================================
def css_name(request):
	return {'css_name': 'webapp_default.css'}


#===============================================================================
# termite_dialogs ： 获取termite的dialog集合
#===============================================================================
def termite_dialogs(request):
	items = []
	for dialog in resource_util.get_termite_dialogs():
		items.append(dialog['template_source'])
		items.append('<script type="text/javascript" src="%s"></script>' % dialog['js_url_path'])
		items.append('\n')

	return {'termite_dialogs': '\n'.join(items)}