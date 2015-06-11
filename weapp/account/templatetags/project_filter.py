# -*- coding:utf-8 -*-

#import time
import os
import json
#from datetime import timedelta, datetime, date

from django import template
#from django.core.cache import cache
#from django.contrib.auth.models import User
from django.conf import settings
#from django.db.models import Q
#from core import emotion

#from datetime import datetime

register = template.Library()

@register.filter(name='load_termite_dialog')
def load_termite_dialog(name):
	dialog_dir_path = os.path.join(settings.TERMITE_HOME, 'termite/js/dialog', name)
	if not os.path.isdir(dialog_dir_path):
		return ''

	template_path = os.path.join(dialog_dir_path, 'dialog.html')
	src_file = open(template_path, 'rb')
	template_source = src_file.read()
	src_file.close()

	js = '<script type="text/javascript" src="/termite_static/termite/js/dialog/%s/dialog.js"></script>' % name
	
	return '%s\n%s' % (template_source, str(js))


ALL_TEMPLATES_CONTENT = None
@register.filter(name='load_templates')
def load_templates_v1(name):
	global ALL_TEMPLATES_CONTENT
	if not ALL_TEMPLATES_CONTENT:
		templates_file_path = os.path.join(settings.PROJECT_HOME, '../templates/all_merged_templates.html')
		src_file = open(templates_file_path)
		ALL_TEMPLATES_CONTENT = src_file.read()
		src_file.close()

	return ALL_TEMPLATES_CONTENT


V1_ALL_TEMPLATES_CONTENT = None
@register.filter(name='load_templates_v1')
def load_templates_v1(name):
	global V1_ALL_TEMPLATES_CONTENT
	if not V1_ALL_TEMPLATES_CONTENT:
		templates_file_path = os.path.join(settings.PROJECT_HOME, '../templates/all_merged_templates_v1.html')
		src_file = open(templates_file_path)
		V1_ALL_TEMPLATES_CONTENT = src_file.read()
		src_file.close()

	return V1_ALL_TEMPLATES_CONTENT


V2_ALL_TEMPLATES_CONTENT = None
@register.filter(name='load_templates_v2')
def load_templates_v2(name):
	global V2_ALL_TEMPLATES_CONTENT
	if not V2_ALL_TEMPLATES_CONTENT:
		templates_file_path = os.path.join(settings.PROJECT_HOME, '../templates/all_merged_templates_v2.html')
		src_file = open(templates_file_path)
		V2_ALL_TEMPLATES_CONTENT = src_file.read()
		src_file.close()

	return V2_ALL_TEMPLATES_CONTENT


@register.filter(name='format_json')
def format_json(obj):
	content = json.dumps(obj)
	return content


@register.filter(name="satisfy_permission")
def satisfy_permission(permission_or_nav, request):
	"""
	检查request.user是否拥有nav.need_permissions中需要的权限
	"""
	# return True
	if request.user.id == request.manager.id:
		# return request.user.no_permission
		return True
	else:
		if 'need_permissions' in permission_or_nav:
			if len(permission_or_nav['need_permissions']) == 0:
				return True
			return request.user.has_perm(permission_or_nav['need_permissions'])
		else:
			return request.user.has_perm(permission_or_nav)