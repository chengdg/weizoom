# -*- coding: utf-8 -*-

__author__ = 'liupeiyu, chuter'

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User

from models import *
from core.jsonresponse import create_response, JsonResponse
from core.exceptionutil import unicode_full_stack

from watchdog.utils import watchdog_alert

from apps_manager import manager

@login_required
def create_installed_app(request):
	appid = request.POST.get('id')

	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()


	#暂时关闭gevent的异步操作，直接修改数据库状态
	#TODO 进行操作记录记录？
	# if app.status in [CustomizedappStatus.INACTIVE, CustomizedappStatus.UNINSTALLED]:
	# 	try:
	# 		manager.install_app_asyc(app)
	# 	except:
	# 		alert_msg = u"安装app:{}失败，cause:\n{}".format(
	# 				app.__unicode__(),
	# 				unicode_full_stack()
	# 			)
	# 		watchdog_alert(alert_msg, app.owner.id)
	if app.status in [CustomizedappStatus.INACTIVE, CustomizedappStatus.UNINSTALLED]:
		try:
			manager.start_app(app)
		except:
			alert_msg = u"安装(直接启动)app:{}失败，cause:\n{}".format(
					app.__unicode__(),
					unicode_full_stack()
				)
			watchdog_alert(alert_msg, app.owner.id)

	response = create_response(200)
	response.data.status = app.status
	return response.get_response()

@login_required
def create_uninstalled_app(request):
	appid = request.POST.get('id')

	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	#TODO 进行操作记录记录？
	if app.status in [CustomizedappStatus.STOPEED]:
		try:
			manager.uninstall_app_asyc(app)
		except:
			alert_msg = u"卸载app:{}失败，cause:\n{}".format(
					app.__unicode__(),
					unicode_full_stack()
				)
			watchdog_alert(alert_msg, app.owner.id)

	response = create_response(200)
	response.data.status = app.status
	return response.get_response()

@login_required
def create_stopped_app(request):
	appid = request.POST.get('id')

	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	#TODO 进行操作记录记录？
	if app.status in [CustomizedappStatus.RUNNING, CustomizedappStatus.WITHERROR]:
		try:
			manager.stop_app(app)
		except:
			alert_msg = u"停止app:{}失败，cause:\n{}".format(
					app.__unicode__(),
					unicode_full_stack()
				)
			watchdog_alert(alert_msg, app.owner.id)

	response = create_response(200)
	response.data.status = app.status
	return response.get_response()

@login_required
def create_started_app(request):
	appid = request.POST.get('id')

	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	#TODO: 进行操作记录记录？
	if CustomizedappStatus.STOPEED == app.status:
		try:
			manager.start_app(app)
		except:
			alert_msg = u"启动app:{}失败，cause:\n{}".format(
					app.__unicode__(),
					unicode_full_stack()
				)
			watchdog_alert(alert_msg, app.owner.id)

	response = create_response(200)
	response.data.status = app.status
	return response.get_response()

@login_required
def create_updated_app(request):
	appid = request.POST.get('id')

	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	#TODO 进行操作记录记录？
	if CustomizedappStatus.RUNNING == app.status:
		try:
			manager.update_app_asyc(app)
		except:
			alert_msg = u"更新app:{}失败，cause:\n{}".format(
					app.__unicode__(),
					unicode_full_stack()
				)
			watchdog_alert(alert_msg, app.owner.id)

	response = create_response(200)
	response.data.status = app.status
	return response.get_response()

@login_required
def delete_app(request):
	appid = request.POST.get('id')

	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	#TODO 进行操作记录记录？
	try:
		app.delete()
	except:
		alert_msg = u"删除app:{}失败，cause:\n{}".format(
			app.__unicode__(),
			unicode_full_stack()
		)
		watchdog_alert(alert_msg, app.owner.id)

	response = create_response(200)
	return response.get_response()

@login_required
def get_app_status(request):
	appid = request.POST.get('id')
	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	response = create_response(200)
	response.data.status = app.status
	return response.get_response()

def __app_status_list_to_json(apps):
	if apps is None or len(apps) == 0:
		return {}

	apps_status_json = {}
	for app in apps:
		apps_status_json[app.id] = app.status

	return apps_status_json

@login_required
def get_all_app_status(request):
	all_user_apps = list(CustomizedApp.objects.all())

	response = create_response(200)
	response.data.status_list = __app_status_list_to_json(all_user_apps)
	return response.get_response()

from core import apiview_util

def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)

@login_required
def select_app_status(request):
	id = request.POST.get('id')
	response = create_response(200)
	is_refresh = False
	try:
		infos = CustomizedAppInfo.objects.filter(id=id)
		if infos.count() > 0:
			customized_app = infos[0].customized_app
			if customized_app.status == CustomizedappStatus.RUNNING:
				is_refresh = True
	except:
		response = create_response(500)
		response.errMsg = u'系统繁忙，请稍后重试'
		response.innerErrMsg = unicode_full_stack()

	response.data.is_refresh = is_refresh
	return response.get_response()