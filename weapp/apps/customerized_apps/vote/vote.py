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

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class vote(resource.Resource):
	app = 'apps/vote'
	resource = 'vote'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			vote = app_models.vote.objects.get(id=request.GET['id'])
			is_create_new_data = False
			project_id = 'new_app:vote:%s' % request.GET.get('related_page_id', 0)
		else:
			vote = None
			is_create_new_data = True
			project_id = 'new_app:vote:0'
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
			'third_nav_name': export.MALL_APPS_VOTE_NAV,
			'vote': vote,
			'is_create_new_data': is_create_new_data,
			'project_id': project_id,
		});
		
		return render_to_response('vote/templates/editor/workbench.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		vote = app_models.vote(**data)
		vote.save()
		
		data = json.loads(vote.to_json())
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
		app_models.vote.objects(id=request.POST['id']).update(**update_data)
		
		response = create_response(200)
		return response.get_response()
	
	@login_required
	def api_delete(request):
		"""
		响应DELETE
		"""
		app_models.vote.objects(id=request.POST['id']).delete()
		
		response = create_response(200)
		return response.get_response()

