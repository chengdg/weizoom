# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
__STRIPPER_TAG__
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_alert, watchdog_fatal
__STRIPPER_TAG__
from apps.register import mobile_view_func
from termite import pagestore as pagestore_manager
from apps import viper_util
from {{app_name}}.models import *
from {{app_name}}.mysql_models import *
from {{app_name}} import settings as app_settings
__STRIPPER_TAG__
__STRIPPER_TAG__

{% for page in pages %}
{% if page.component.model.type == 'edit_page' %}
{{page.component.model.title|upper}}_TARGET_RESOURCE = "{{page.component.model.title}}"
__STRIPPER_TAG__
__STRIPPER_TAG__
{% endif %}
{% endfor %}


{% for page in pages %}
{% with page.component as resource %}
	{% if resource.model.type == 'edit_page' %}
	{% with resource.model.title as resource_name %}
################################################
# 获取账单明细
################################################
@mobile_view_func(resource='{{resource_name}}', action='get')
def get_{{resource_name}}(request):
	request.target_resource = {{page.component.model.title|upper}}_TARGET_RESOURCE
	record = viper_util.get_record(request, app_settings)
	#filter __${variable} from record
	data = {}
	for key in record:
		if key.startswith('__'):
			continue

		data[key] = record[key]

	c = RequestContext(request, {
		'record': data,
		'hide_non_member_cover': True #非会员也可使用该页面
	})
	return render_to_response('{{app_name}}/templates/webapp/{{resource_name}}.html' , c)
__STRIPPER_TAG__
__STRIPPER_TAG__
	{% endwith %}
	{% endif %}
{% endwith %}
{% endfor %}
