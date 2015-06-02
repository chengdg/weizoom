# -*- coding: utf-8 -*-

from datetime import datetime
import json
__STRIPPER_TAG__
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
__STRIPPER_TAG__
from core.jsonresponse import JsonResponse, create_response
from apps.register import view_func
from apps import viper_util
from {{app_name}}.settings import FIRST_NAV_NAME
from {{app_name}}.settings import LEFT_NAVS as SECOND_NAVS
from {{app_name}} import settings as app_settings
from {{app_name}}.models import *
from {{app_name}}.mysql_models import *
__STRIPPER_TAG__
__STRIPPER_TAG__

{% for page in pages %}
{% if page.component.model.type == 'edit_page'  or page.component.model.type == 'dialog_page' %}
{{page.component.model.title|upper}}_TARGET_RESOURCE = "{{page.component.model.title}}"
__STRIPPER_TAG__
__STRIPPER_TAG__
{% endif %}
{% endfor %}


{% for page in pages %}


{% with page.top_level_page.component.model.title as top_level_resource %}
{% with page.component as resource %}



	{% if resource.model.type == 'edit_page' %}
	{% with resource.model.title as resource_name %}
	{% with resource.model.storeEngine as store_engine %}
#===============================================================================
# __save_record_hook : 存储record时的hook函数
#===============================================================================
def __save_record_hook(request, record):
	pass
__STRIPPER_TAG__
__STRIPPER_TAG__
#===============================================================================
# __get_record_hook : 存储record时的hook函数
#===============================================================================
def __get_record_hook(request, record):
	pass
__STRIPPER_TAG__
__STRIPPER_TAG__
#===============================================================================
# create_record : 创建记录
#===============================================================================
@login_required
@view_func(resource='{{resource_name}}', action='create')
def create_record(request):
	request.target_resource = {{page.component.model.title|upper}}_TARGET_RESOURCE
	if request.POST:
		request.__save_record_hook = __save_record_hook
		{% if store_engine == 'mysql' %}
		request.model_class = {{resource.model.className}}
		{% endif %}
		viper_util.create_record(request, app_settings)
		return HttpResponseRedirect('/apps/{{app_name}}/?module={{resource.model.module}}&resource={{top_level_resource}}&action=get')
	else:
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': SECOND_NAVS,
			'second_nav_name': '{{page.component.model.module}}'
		})
		return render_to_response('{{app_name}}/templates/editor/{{resource_name}}.html', c)
__STRIPPER_TAG__
__STRIPPER_TAG__
#===============================================================================
# update_record : 更新记录
#===============================================================================
@login_required
@view_func(resource='{{resource_name}}', action='update')
def update_record(request):
	request.target_resource = {{page.component.model.title|upper}}_TARGET_RESOURCE
	if request.POST:
		request.__save_record_hook = __save_record_hook
		{% if store_engine == 'mysql' %}
		request.model_class = {{resource.model.className}}
		{% endif %}
		viper_util.update_record(request, app_settings)
		return HttpResponseRedirect('/apps/{{app_name}}/?module={{resource.model.module}}&resource={{top_level_resource}}&action=get')
	else:
		request.__get_record_hook = __get_record_hook
		{% if store_engine == 'mysql' %}
		request.model_class = {{resource.model.className}}
		{% endif %}
		record = viper_util.get_record(request, app_settings)
		jsons = []
		jsons.append({
			"name": "record",
			"content": json.dumps(record)
		})
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': SECOND_NAVS,
			'second_nav_name': '{{page.component.model.module}}',
			'record': record,
			'jsons': jsons
		})
		return render_to_response('{{app_name}}/templates/editor/{{resource_name}}.html', c)
__STRIPPER_TAG__
__STRIPPER_TAG__
#===============================================================================
# delete_record : 删除记录
#===============================================================================
@login_required
@view_func(resource='{{resource_name}}', action='delete')
def delete_record(request):
	request.target_resource = {{page.component.model.title|upper}}_TARGET_RESOURCE
	{% if store_engine == 'mysql' %}
	request.model_class = {{resource.model.className}}
	{% endif %}
	viper_util.delete_record(request, app_settings)
	return HttpResponseRedirect('/apps/{{app_name}}/?module={{resource.model.module}}&resource={{top_level_resource}}&action=get')
__STRIPPER_TAG__
__STRIPPER_TAG__
	{% endwith %}
	{% endwith %}
	{% endif %}





	{% if resource.model.type == 'dialog_page' %}
	{% with resource.model.title as resource_name %}
	{% with resource.model.storeEngine as store_engine %}
#===============================================================================
# __save_record_hook : 存储record时的hook函数
#===============================================================================
def __save_record_hook(request, record):
	pass
__STRIPPER_TAG__
__STRIPPER_TAG__
#===============================================================================
# __get_record_hook : 存储record时的hook函数
#===============================================================================
def __get_record_hook(request, record):
	pass
__STRIPPER_TAG__
__STRIPPER_TAG__
#===============================================================================
# create_record : 创建记录
#===============================================================================
@login_required
@view_func(resource='{{resource_name}}', action='create')
def create_record(request):
	request.target_resource = {{page.component.model.title|upper}}_TARGET_RESOURCE
	request.__save_record_hook = __save_record_hook
	{% if store_engine == 'mysql' %}
	request.model_class = {{resource.model.className}}
	{% endif %}
	viper_util.create_record(request, app_settings)
	return create_response(200).get_response()
__STRIPPER_TAG__
__STRIPPER_TAG__
#===============================================================================
# delete_record : 删除记录
#===============================================================================
@login_required
@view_func(resource='{{resource_name}}', action='delete')
def delete_record(request):
	request.target_resource = {{page.component.model.title|upper}}_TARGET_RESOURCE
	{% if store_engine == 'mysql' %}
	request.model_class = {{resource.model.className}}
	{% endif %}
	viper_util.delete_record(request, app_settings)
	return create_response(200).get_response()
__STRIPPER_TAG__
__STRIPPER_TAG__
	{% endwith %}
	{% endwith %}
	{% endif %}





	{% if resource.model.type == 'top_level_page' %}
	{% with resource.model.title as resource_name %}
#===============================================================================
# get_record_list : 获取记录集合
#===============================================================================
@login_required
@view_func(resource='{{resource_name}}', action='get')
def get_record_list(request):
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': SECOND_NAVS,
		'second_nav_name': '{{page.component.model.module}}',
	})
	return render_to_response('{{app_name}}/templates/editor/{{resource_name}}.html' , c)
__STRIPPER_TAG__
__STRIPPER_TAG__
	{% endwith %}
	{% endif %}

{% endwith %}
{% endwith %}

{% endfor %}

