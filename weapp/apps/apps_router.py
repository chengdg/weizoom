# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.core.urlresolvers import Resolver404

from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack

from apps import FIRST_NAV_NAME
from models import *

from apps_manager import manager

from app_status_response_util import *
from core import resource as resource_util

RESTFUL_APPS = set()
VALID_METHODS = set(['get', 'post', 'put', 'delete', 'api_get', 'api_post', 'api_put', 'api_delete'])

def __load_app_resource_urls():
	if len(RESTFUL_APPS) > 0:
		return
	import os
	from django.conf import settings
	apps_dir = os.path.join(settings.PROJECT_HOME, '../apps/customerized_apps')
	for file_name in os.listdir(apps_dir):
		app_dir = os.path.join(apps_dir, file_name)
		if os.path.isfile(app_dir):
			continue

		module_name = 'apps.customerized_apps.%s' % file_name
		module = __import__(module_name, {}, {}, ['*',])
		is_restful_app = getattr(module, 'is_restful_app', False)
		if not is_restful_app:
			continue

		urls_module_name = 'apps.customerized_apps.%s.urls' % file_name
		__import__(urls_module_name, {}, {}, ['*',])
		RESTFUL_APPS.add(file_name)		


def __raise_404(path, app_resource, method):
		tried = []
		tried.append([{'regex':{'pattern': 'target: path="{}", resource="{}:{}"'.format(path, app_resource, method)}}])
		if len(resource_util.APPRESOURCE2CLASS) > 0:
			for app_resource, class_info in resource_util.APPRESOURCE2CLASS.items():
				for key, value in class_info['cls'].__dict__.items():
					if not key in VALID_METHODS:
						continue
					tried.append([{'regex':{'pattern': '^{}:{}'.format(app_resource, key)}}])
		else:
			tried.append([{'regex':{'pattern': 'None'}}])
			
		raise Resolver404({'tried': tried, 'path' : path})

def resolve(request, app_name, path):
	#确定method
	method = request.META['REQUEST_METHOD']
	if method == 'POST' and '_method' in request.REQUEST:
		_method = request.REQUEST['_method']
		method = _method.upper()
	if '/api/' in path:
		method = 'api_%s' % method

	#确定resource
	path = path.strip()
	if path[-1] != '/':
		path = '%s/' % path
	items = path.split('/')
	resource = items[-2]
	
	app_resource = 'apps/%s-%s' % (app_name, resource)
	print 'app_resource: ', app_resource
	print 'method: ', method
	class_info = resource_util.APPRESOURCE2CLASS.get(app_resource, None)
	if class_info:
		if not class_info['instance']:
			class_info['instance'] = class_info['cls']
		resource_instance = class_info['instance']
		func = getattr(resource_instance, method.lower(), None)
		if func:
			return func
		else:
			__raise_404(path, app_resource, method)
	else:
		__raise_404(path, app_resource, method)

	
#=====================================================
#
# 调用针对定制app中具体资源的特定操作代码
#
# 其中request path格式为：
# /apps/123/?module=erp&resource=project&action=get&id=1
# 各参数定义：
# 123: 为定制的app的id
# module: 操作的资源所在的模块
# resource: 操作的资源
# action: 操作类型
# query str中其它参数为具体资源属性
#
#=====================================================
def process_resource(request, app_name, app_module=None):
	try:
		target_app = CustomizedApp.objects.get(name=app_name)
	except:
		raise Http404(u"不存在该定制化APP")

	#检查app的当前状态
	if CustomizedappStatus.INACTIVE == target_app.status or \
		CustomizedappStatus.UNINSTALLED == target_app.status:
		return show_inactive_app(request, target_app)
	elif CustomizedappStatus.STOPEED == target_app.status or \
		CustomizedappStatus.STOPPING == target_app.status or \
		CustomizedappStatus.STARTING == target_app.status:
		return show_stopped_app(request, target_app)
	elif CustomizedappStatus.UPDATING == target_app.status:
		return show_updating_app(request, target_app)
	elif CustomizedappStatus.WITHERROR == target_app.status:
		#TODO 进行预警
		pass
	else:
		#正常运行
		pass

	__load_app_resource_urls()
	if app_name in RESTFUL_APPS:
		func = resolve(request, app_name, request.path)
		return func(request)
	else:
		resource = request.GET.get('resource', None)
		if resource is None:
			resource = request.GET.get('model', None)

		is_request_for_mobile_resource = getattr(request, 'is_request_for_mobile_resource', False)
		if is_request_for_mobile_resource:
			resource = 'mobile_{}'.format(resource)

		app_module = app_module if app_module is not None else request.GET['module']
			
		try:
			target_resource_process_func = manager.get_view_func(
				target_app,
				app_module,
				resource,
				request.GET['action']
				)
			return target_resource_process_func(request)
		except:
			raise
			alert_msg = u"调用app:{}的处理:['module':{}, 'resource':{}, 'action':{}]失败, cause:\n{}".format(
					app_name,
					app_module,
					resource,
					request.GET['action'],
					unicode_full_stack()				
				)
			watchdog_alert(alert_msg, request.user_profile.user.id)
			raise Http404(u"不存在该定制化APP") 

class AppApiResponseStatusCode(object):
	def __init__(self):
		raise NotImplementedError

	STOPPED = 900
	UPDATING = 901
	INACTIVE = 902


def call_resource_process_api(request, app_name, module, resource, action):
	try:
		target_app = CustomizedApp.objects.get(name=app_name)
	except:
		response = create_response(404)
		return response.get_response()

	#检查app的当前状态
	if CustomizedappStatus.INACTIVE == target_app.status or \
		CustomizedappStatus.UNINSTALLED == target_app.status:
		return create_response(AppApiResponseStatusCode.INACTIVE).get_response()
	elif CustomizedappStatus.STOPEED == target_app.status or \
		CustomizedappStatus.STOPPING == target_app.status or \
		CustomizedappStatus.STARTING == target_app.status:
		return create_response(AppApiResponseStatusCode.STOPPED).get_response()
	elif CustomizedappStatus.UPDATING == target_app.status:
		return create_response(AppApiResponseStatusCode.UPDATING).get_response()
	elif CustomizedappStatus.WITHERROR == target_app.status:
		#TODO 进行预警
		pass
	else:
		#正常运行
		pass

	try:
		is_request_for_mobile_resource = getattr(request, 'is_request_for_mobile_resource', False)
		if is_request_for_mobile_resource:
			resource = 'mobile_{}'.format(resource)
			
		target_resource_process_func = manager.get_api_func(
			target_app,
			module,
			resource,
			action
			)
		return target_resource_process_func(request)
	except:
		raise
		alert_msg = u"调用app:{}的处理:['module':{}, 'resource':{}, 'action':{}]失败, cause:\n{}".format(
				app_name,
				module,
				resource,
				action,
				unicode_full_stack()				
			)
		watchdog_alert(alert_msg, request.user_profile.user.id)

		response = create_response(400)
		response.errMsg = u'不存在该APP'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()