{% load code_filter %}
# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth

from core.jsonresponse import JsonResponse, create_response
from core import paginator

from models import *


# Termite GENERATED START: views
# MODULE START: {{instanceName}}
{{navItem|to_nav_name}} = '{{navItem}}'

########################################################################
# list_{{pluralInstanceName}}: 显示{{entityName}}列表
########################################################################
@login_required
def list_{{pluralInstanceName}}(request):
	shop_id = request.user.get_profile().webapp_id
	{{pluralInstanceName}} = {{className}}.objects.filter(owner=request.user).order_by('display_index')
	c = RequestContext(request, {
		'nav_name': {{navItem|to_nav_name}},
		'{{pluralInstanceName}}': {{pluralInstanceName}}
	})
	return render_to_response('{{app}}/editor/{{pluralInstanceName}}.html', c)


########################################################################
# add_{{instanceName}}: 添加{{entityName}}
########################################################################
@login_required
def add_{{instanceName}}(request):
	if request.POST:
		{{instanceName}} = {{className}}.objects.create(
			owner = request.user,
			{% for property in properties %}
			{% with property|to_data_type as data_type %}
			{% ifequal data_type 'bool' %}
			{{property.name}} = True if request.POST.get('{{property.name}}', '') == '1' else False{% if not forloop.last %},{% endif %}
			{% endifequal %}
			{% ifequal data_type 'text' %}
			{{property.name}} = request.POST.get('{{property.name}}', ''){% if not forloop.last %},{% endif %}
			{% endifequal %}
			{% endwith %}
			{% endfor %}
		)
		{% ifequal listinfo.isEnableSort "yes" %}
			{% ifequal listinfo.isSortByDesc "yes" %}
		{{instanceName}}.display_index = 0-{{instanceName}}.id
			{% else %}
		{{instanceName}}.display_index = {{instanceName}}.id
			{% endifequal %}
		{{instanceName}}.save()
		{% endifequal %}

		{% ifequal hasSwipeImages "yes" %}
		{% for property in properties %}
		{% ifequal property.type "swipe_images_input" %}
		{{property.name}} = request.POST.get('{{property.name}}', None)
		if {{property.name}}:
			image_urls = json.loads({{property.name}})
			for index, image_url in enumerate(image_urls):
				{{className}}SwipeImage.objects.create(
					owner = request.user,
					{{instanceName}} = {{instanceName}},
					pic_url = image_url,
					display_index = index + 1
				)
		{% endifequal %}
		{% endfor %}
		{% endifequal %}

		return HttpResponseRedirect('/{{app}}/editor/{{pluralInstanceName}}/')
	else:
		c = RequestContext(request, {
			'nav_name': {{navItem|to_nav_name}},
			'webapp_id': request.user.get_profile().webapp_id
		})
		return render_to_response('{{app}}/editor/edit_{{instanceName}}.html', c)


########################################################################
# update_{{instanceName}}: 更新{{entityName}}
########################################################################
@login_required
def update_{{instanceName}}(request, {{instanceName}}_id):
	if request.POST:
		{{className}}.objects.filter(owner=request.user, id={{instanceName}}_id).update(
			{% for property in properties %}
			{% with property|to_data_type as data_type %}
			{% ifequal data_type 'bool' %}
			{{property.name}} = True if request.POST.get('{{property.name}}', '') == '1' else False{% if not forloop.last %},{% endif %}
			{% endifequal %}
			{% ifequal data_type 'text' %}
			{{property.name}} = request.POST.get('{{property.name}}', ''){% if not forloop.last %},{% endif %}
			{% endifequal %}
			{% endwith %}
			{% endfor %}
		)

		{% ifequal hasSwipeImages "yes" %}
		{% for property in properties %}
		{% ifequal property.type "swipe_images_input" %}
		{{className}}SwipeImage.objects.filter(owner=request.user, {{instanceName}}_id={{instanceName}}_id).delete()
		{{property.name}} = request.POST.get('{{property.name}}', None)
		if {{property.name}}:
			image_urls = json.loads({{property.name}})
			for index, image_url in enumerate(image_urls):
				{{className}}SwipeImage.objects.create(
					owner = request.user,
					{{instanceName}}_id = {{instanceName}}_id,
					pic_url = image_url,
					display_index = index + 1
				)
		{% endifequal %}
		{% endfor %}
		{% endifequal %}

		return HttpResponseRedirect('/{{app}}/editor/{{pluralInstanceName}}/')
	else:
		{{instanceName}} = {{className}}.objects.get(owner=request.user, id={{instanceName}}_id)

		{% ifequal hasSwipeImages "yes" %}
		swipe_images = list({{className}}SwipeImage.objects.filter(
			owner = request.user,
			{{instanceName}} = {{instanceName}}
		))
		swipe_images.sort(lambda x,y: cmp(x.display_index, y.display_index))
		swipe_images = [{'id':img.id, 'url':img.pic_url} for img in swipe_images]
		{% endifequal %}

		c = RequestContext(request, {
			'nav_name': {{navItem|to_nav_name}},
			'{{instanceName}}': {{instanceName}},
			{% ifequal hasSwipeImages "yes" %}
			'swipe_images_json': json.dumps(swipe_images),
			{% endifequal %}
			'webapp_id': request.user.get_profile().webapp_id
		})
		return render_to_response('{{app}}/editor/edit_{{instanceName}}.html', c)


########################################################################
# delete_{{instanceName}}: 删除{{entityName}}
########################################################################
@login_required
def delete_{{instanceName}}(request, {{instanceName}}_id):
	{{className}}.objects.filter(id={{instanceName}}_id).delete()

	return HttpResponseRedirect(request.META['HTTP_REFERER'])
# MODULE END: {{instanceName}}
# Termite GENERATED END: views