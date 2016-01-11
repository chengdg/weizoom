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
from core.dateutil import get_today

from models import *
from account.models import *


# Termite GENERATED START: mobile_views
# MODULE START: {{instanceName}}
########################################################################
# show_index: 显示show首页
########################################################################
def show_index(request, webapp_id):
	profile = UserProfile.objects.get(webapp_id=webapp_id)

	c = RequestContext(request, {
		'page_title': u'{{entityName}}列表',
		'webapp_id': webapp_id
	})
	return render_to_response('{{app}}/index.html', c)


########################################################################
# list_{{pluralInstanceName}}: 显示"{{entityName}}列表"页面
########################################################################
def list_{{pluralInstanceName}}(request, webapp_id):
	profile = UserProfile.objects.get(webapp_id=webapp_id)

	{{pluralInstanceName}} = {{className}}.objects.filter(owner_id=profile.user_id).order_by('display_index')
	query = None
	{% ifequal isEnableSearch "yes" %}
	if 'search_field' in request.GET:
		search_field = request.GET['search_field']
		query = request.GET['query']
		if query:
			conditions = {}
			conditions['%s__contains' % search_field] = query
			{{pluralInstanceName}} = {{pluralInstanceName}}.filter(**conditions)
	{% endifequal %}

	c = RequestContext(request, {
		'webapp_id': webapp_id,
		'{{pluralInstanceName}}': {{pluralInstanceName}},
		'query': query
	})
	return render_to_response('{{app}}/{{pluralInstanceName}}.html', c)


########################################################################
# show_{{instanceName}}: 显示“{{entityName}}详情”页面
########################################################################
def show_{{instanceName}}(request, webapp_id, {{instanceName}}_id):
	profile = UserProfile.objects.get(webapp_id=webapp_id)

	try:
		if 'is_preview' in request.GET:
			session = request.COOKIES.get('sessionid', 'unknown')
			{{instanceName}} = {{previewClassName}}.objects.get(owner_id=profile.user_id, session=session)
			{% ifequal hasSwipeImages "yes" %}
			swipe_images = {{previewClassName}}SwipeImage.objects.filter(
				session=session, 
				preview_{{instanceName}}_id={{instanceName}}.id
			)
			{% endifequal %}
		else:
			{{instanceName}} = {{className}}.objects.get(owner_id=profile.user_id, id={{instanceName}}_id)
			{% ifequal hasSwipeImages "yes" %}
			swipe_images = {{className}}SwipeImage.objects.filter(
				{{instanceName}}_id={{instanceName}}.id
			)
			{% endifequal %}
	except:
		{{instanceName}} = {'is_deleted': True}
		{% ifequal hasSwipeImages "yes" %}
		swipe_images = []
		{% endifequal %}

	{% ifequal hasSwipeImages "yes" %}
	swipe_images = [{'url':img.pic_url, 'caption':''} for img in swipe_images]\
	{% endifequal %}

	c = RequestContext(request, {
		'webapp_id': webapp_id,
		{% ifequal hasSwipeImages "yes" %}
		'swipe_images': swipe_images,
		'swipe_images_json': json.dumps(swipe_images),
		{% endifequal %}
		'{{instanceName}}': {{instanceName}}
	})
	return render_to_response('{{app}}/{{instanceName}}_detail.html', c)
# MODULE END: {{instanceName}}
# Termite GENERATED END: mobile_views