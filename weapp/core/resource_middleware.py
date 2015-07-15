# -*- coding: utf-8 -*-

import sys
import os
import traceback
import StringIO
import cProfile
import time
import re
#from cStringIO import StringIO
from django.conf import settings
from datetime import timedelta, datetime, date

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.conf import settings

from core import dateutil
from core import resource
from account.models import UserProfile
from watchdog.utils import watchdog_warning, watchdog_fatal
# from watchdog.models import watchdog, WATCHDOG_ERROR, WATCHDOG_OPERATION

RESOURCE_NAMES = set(['termite2', 'weixin2', 'stats'])

#===============================================================================
# RestfulUrlMiddleware : 处理request.path_info的middleware
#===============================================================================
class RestfulUrlMiddleware(object):
	def process_request(self, request):
		path_info = request.path_info
		pos = path_info.find('/', 2)
		app = str(path_info[:pos+1])
		if not app in resource.RESTFUL_APP_SET:
			if app in RESOURCE_NAMES:
				data = {
					'path_info': path_info,
					'app': app,
					'resource': resource.RESTFUL_APP_SET
				}
				watchdog_fatal(str(data), type='RESTFUL_MIDDLEWARE')
			return None

		method = request.META['REQUEST_METHOD']
		if method == 'POST' and '_method' in request.REQUEST:
			_method = request.REQUEST['_method']
			method = _method.upper()

		request.original_path_info = path_info
		if path_info[-1] == '/':
			request.path_info = '%s%s' % (path_info, method)
		else:
			request.path_info = '%s/%s' % (path_info, method)

		# if 'new_weixin' in path_info:
		# 		data = {
		# 			'path_info': path_info,
		# 			'new_path_info': request.path_info,
		# 			'app': app,
		# 			'resource': resource.RESTFUL_APP_SET
		# 		}
		# 		watchdog_info(str(data), type='RESTFUL_MIDDLEWARE')

		return None


#===============================================================================
# ResourceJsMiddleware : 返回resource js文件
#===============================================================================
class ResourceJsMiddleware(object):
	def process_request(self, request):
		if '/resource_js/' == request.path_info:
			from core import resource
			buf = ['ensureNS("W.resource");']
			for _, class_info in resource.APPRESOURCE2CLASS.items():
				buf.append('ensureNS("W.resource");')
				buf.append(class_info['js'])
		
			return HttpResponse('\n'.join(buf), 'text/javascript')


if settings.RESOURCE_LOADED:
	print '[!!!!!!!!!!!!!!!!!!!!!!] already loaded'
else:
	for resource_module in settings.RESOURCES:
		print '[resource middleware] load ', resource
		exec('import %s' % resource_module)
		settings.RESOURCE_LOADED = True