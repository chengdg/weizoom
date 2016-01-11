{% load code_filter %}
# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from termite.core.jsonresponse import JsonResponse, create_response
from termite.core import dateutil

from models import *


# Termite GENERATED START: api_views
# MODULE START: {{instanceName}}
{% ifequal listinfo.isEnableSort "yes" %}
########################################################################
# update_{{instanceName}}_display_index: 修改排列顺序
########################################################################
@login_required
def update_{{instanceName}}_display_index(request):
	print 'update display index...'
	ids = request.GET['ids'].split('_')
	for index, id in enumerate(ids):
		{{className}}.objects.filter(id=id).update(display_index=index+1)

	response = create_response(200)
	return response.get_response()
{% endifequal %}


{% ifequal isEnablePreview "yes" %}
########################################################################
# craete_preview_{{instanceName}}: 创建用于预览的{{entityName}}
########################################################################
@login_required
def craete_preview_{{instanceName}}(request):
	session = request.COOKIES.get('sessionid', 'unknown')
	try:
		{{instanceName}} = {{previewClassName}}.objects.get(owner=request.user, session=session)
		
		{% for property in properties %}
		{% with property|to_data_type as data_type %}
		{% ifequal data_type 'bool' %}
		{{instanceName}}.{{property.name}} = True if request.POST.get('{{property.name}}', '') == '1' else False
		{% endifequal %}
		{% ifequal data_type 'text' %}
		{{instanceName}}.{{property.name}} = request.POST.get('{{property.name}}', '')
		{% endifequal %}
		{% endwith %}
		{% endfor %}
		{{instanceName}}.save()
	except:
		{{instanceName}} = {{previewClassName}}.objects.create(
			owner = request.user,
			session = session,
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
	{{previewClassName}}SwipeImage.objects.filter(session = session, preview_{{instanceName}}_id={{instanceName}}.id).delete()
	{{property.name}} = request.POST.get('{{property.name}}', None)
	if {{property.name}}:
		image_urls = json.loads({{property.name}})
		for index, image_url in enumerate(image_urls):
			{{previewClassName}}SwipeImage.objects.create(
				owner = request.user,
				session = session,
				preview_{{instanceName}}_id = {{instanceName}}.id,
				pic_url = image_url,
				display_index = index + 1
			)
	{% endifequal %}
	{% endfor %}
	{% endifequal %}

	response = create_response(200)
	return response.get_response()
{% endifequal %}
# MODULE END: {{instanceName}}
# Termite GENERATED END: api_views