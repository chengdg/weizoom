# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import Context, RequestContext

from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack

from apps import FIRST_NAV_NAME
from models import *

from apps_manager import manager

from app_status_response_util import *

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