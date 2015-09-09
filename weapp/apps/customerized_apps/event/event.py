# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
from mall import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

class event(resource.Resource):
	app = 'apps/event'
	resource = 'event'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			event = app_models.event.objects.get(id=request.GET['id'])
			is_create_new_data = False
			project_id = 'new_app:event:%s' % request.GET.get('related_page_id', 0)
		else:
			event = None
			is_create_new_data = True
			project_id = 'new_app:event:0'
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_customerized_apps(request),
			'second_nav_name': 'events',
			'event': event,
			'is_create_new_data': is_create_new_data,
			'project_id': project_id,
			'app_name': 'event'
		});
		
		return render_to_response('event/templates/editor/workbench.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		event = app_models.event(**data)
		event.save()
		
		data = json.loads(event.to_json())
		data['id'] = data['_id']['$oid']
		response = create_response(200)
		response.data = data
		return response.get_response()
	
	@login_required
	def api_post(request):
		"""
		响应POST
		"""
		data = request_util.get_fields_to_be_save(request)
		update_data = {}
		update_fields = set(['name', 'start_time', 'end_time'])
		for key, value in data.items():
			if key in update_fields:
				update_data['set__'+key] = value
		app_models.event.objects(id=request.POST['id']).update(**update_data)
		
		response = create_response(200)
		return response.get_response()
	
	@login_required
	def api_delete(request):
		"""
		响应DELETE
		"""
		app_models.event.objects(id=request.POST['id']).delete()
		
		response = create_response(200)
		return response.get_response()

