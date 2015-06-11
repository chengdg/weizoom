# -*- coding: utf-8 -*-

__author__ = 'chuter'

from core.jsonresponse import create_response

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_alert

from apps_manager import manager

from models import CustomizedApp

def __parse_request_appname(request):
	workspace_id = request.GET['workspace_id']
	#workspace_id形如: apps:${app_name}
	app_names_parts = workspace_id.split(':')
	return app_names_parts[1]

def __build_empty_link_targets_response():
	response = create_response(200)
	response.data = []
	return response.get_response()

########################################################################
# get_link_targets: 获取可链接的目标
########################################################################
def get_link_targets(request):
	if (request is None) or (not request.user.is_authenticated()):
		return []

	try:
		app_name = __parse_request_appname(request)
	except:
		alert_msg = u"解析获取可链接目标的目标app名称失败，request:\n{}\ncause:\n{}".format(
				request.GET,
				unicode_full_stack()				
			)
		watchdog_alert(alert_msg, request.user.id)
		return __build_empty_link_targets_response()

	try:
		app = CustomizedApp.objects.get(name=app_name)
	except:
		response = create_response(400)
		response.errMsg = u"不存在该定制APP"
		return response.get_response()

	app_module = manager.get_app_module(app)
	try:
		return app_module.export.get_link_targets(request)
	except:
		raise
		alert_msg = u"调用APP:{}的get_link_targets失败，cause:\n{}".format(
				app.__unicode__(),
				unicode_full_stack()
			)
		watchdog_alert(alert_msg, request.user.id)
		return __build_empty_link_targets_response()


def get_webapp_usage_link(webapp_owner_id, member):
	"""
	获得webapp使用情况的链接
	"""
	#获取当前owner所持有的所有定制化app
	owned_apps = list(CustomizedApp.objects.filter(owner_id=webapp_owner_id))
	owned_app_modules = []
	for owned_app in owned_apps:
		app_module = manager.get_app_module(owned_app)
		if app_module is not None:
			owned_app_modules.append(app_module)

	#组织所有的定制化app webapp使用情况的链接信息
	all_links = []
	for app_module in owned_app_modules:
		if hasattr(app_module.export, 'get_webapp_usage_link'):
			app_webapp_usage_link = app_module.export.get_webapp_usage_link(webapp_owner_id, member)
			if isinstance(app_webapp_usage_link, list):
				all_links += app_webapp_usage_link
			elif isinstance(app_webapp_usage_link, dict):
				all_links.append(app_webapp_usage_link)
			else:
				pass

	return all_links

###################################################################
# get_market_tool_webapp_usage_links: 获取webapp的用户中心中显示的营销工具使用情况链接
###################################################################
def get_market_tool_webapp_usage_links(webapp_owner_id, member=None):
	if webapp_owner_id <= 0:
		return []

	#使用每个营销工具中的export.get_webapp_usage_link获得信息
	all_market_tool_webapp_usage_links = []
	
	user_market_tool_modules = get_market_tool_modules_for_user_id(webapp_owner_id)

	for tool_module in ToolModule.all_tool_modules():
		try:
			tool_module_export = tool_module.export
		except:
			continue

		if not tool_module.module_name in user_market_tool_modules:
			#无权限，跳过
			continue

		if tool_module_export and hasattr(tool_module_export, 'get_webapp_usage_link'):
			all_market_tool_webapp_usage_links.append(
				tool_module_export.get_webapp_usage_link(webapp_owner_id, member)
				)

	return all_market_tool_webapp_usage_links