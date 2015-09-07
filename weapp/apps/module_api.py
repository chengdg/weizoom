# -*- coding: utf-8 -*-

__author__ = 'chuter'


from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from core.jsonresponse import create_response, JsonResponse
from django.contrib.auth.models import User

from apps_router import process_resource, call_resource_process_api

def __parse_appname_and_module_from_webapp_request(request):
	if request is None:
		return None, None

	#webapp请求中module信息格式为：
	#module=apps:${app_name}:${app_module}
	module_from_webapp = request.REQUEST.get('module', None)
	if module_from_webapp is None:
		return None, None

	module_info_parts = module_from_webapp.split(':')
	app_name = module_info_parts[1]
	app_module = module_info_parts[2]

	return app_name, app_module

def get_mobile_response(request):
	app_name, app_module = __parse_appname_and_module_from_webapp_request(request)
	if app_name is None:
		raise Http404(u"不存在该定制化APP")

	request.is_request_for_mobile_resource = True
	return process_resource(
			request, 
			app_name, 
			app_module=app_module
		)

def __parse_resource_and_action_from_webapp_api_request(request):
	if request is None:
		return None, None

	#webapp请求中target_api信息格式为：
	#${resource}/${action}
	target_api = request.REQUEST.get('target_api', None)
	if target_api is None:
		return None, None

	resource_action_pair = target_api.split('/')
	return resource_action_pair[0], resource_action_pair[1]

def get_mobile_api_response(request):
	app_name, app_module = __parse_appname_and_module_from_webapp_request(request)
	if app_name is None:
		response = create_response(400)
		response.errMsg = u"没有解析出APP名称"
		return response.get_response()

	resource, action = __parse_resource_and_action_from_webapp_api_request(request)

	request.is_request_for_mobile_resource = True
	return call_resource_process_api(
			request, 
			app_name, 
			app_module, 
			resource,
			action
		)

#####################################################################################
# get_apps ：获取所有的app
#####################################################################################
from models import CustomizedApp
def get_apps(request):
	if (request is None) or (not request.user.is_authenticated()):
		return []

	ret_apps = CustomizedApp.all_running_apps_list(user=request.user)
	admin_user = User.objects.get(id=1)
	ret_apps.extend([app for app in CustomizedApp.all_running_apps_list(user=admin_user) if not 'markettool:' in app.name])
	ret_apps_info_jsonarray = []
	for app in ret_apps:
		ret_apps_info_jsonarray.append(
				{
					'text': u'定制APP-{}'.format(app.display_name),
					'value': 'app:{}'.format(app.name)
				}
			)

	return ret_apps_info_jsonarray

def get_app_link_url(
	request, 
	app_name,
	module_name,
	resource,
	action,
	query_str=None
	):
	if request is None:
		return None

	workspace_template_info = 'workspace_id=apps:&webapp_owner_id=%d&project_id=0' % request.workspace.owner_id
	link_url = './?module=apps:{}:{}&model={}&resource={}&action={}&{}'.format(
			app_name,
			module_name,
			resource,
			resource,
			action,
			workspace_template_info
		)

	if query_str is not None:
		link_url = '{}&{}'.format(link_url, query_str)

	return link_url


def get_shengjing_app_link_url(
	request, 
	app_name,
	module_name,
	resource,
	action,
	query_str=None
	):
	if request is None:
		return None

	workspace_template_info = 'workspace_id=apps:&webapp_owner_id=%d&project_id=0' % request.user.id
	link_url = './?module=apps:{}:{}&model={}&resource={}&action={}&{}'.format(
			app_name,
			module_name,
			resource,
			resource,
			action,
			workspace_template_info
		)

	if query_str is not None:
		link_url = '{}&{}'.format(link_url, query_str)

	return link_url