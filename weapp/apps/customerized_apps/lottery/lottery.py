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

class lottery(resource.Resource):
	app = 'apps/lottery'
	resource = 'lottery'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			lottery = app_models.lottery.objects.get(id=request.GET['id'])
			is_create_new_data = False
			project_id = 'new_app:lottery:%s' % request.GET.get('related_page_id', 0)
		else:
			lottery = None
			is_create_new_data = True
			project_id = 'new_app:lottery:0'
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_customerized_apps(request),
			'second_nav_name': 'lotteries',
			'lottery': lottery,
			'is_create_new_data': is_create_new_data,
			'project_id': project_id,
		})
		
		return render_to_response('lottery/templates/editor/workbench.html', c)

	@login_required
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		data = add_extra_data(data, request.POST)
		lottery = app_models.lottery(**data)
		lottery.save()
		error_msg = None
		
		data = json.loads(lottery.to_json())
		data['id'] = data['_id']['$oid']
		if error_msg:
			data['error_msg'] = error_msg
		response = create_response(200)
		response.data = data
		return response.get_response()
	
	@login_required
	def api_post(request):
		"""
		响应POST
		"""
		data = request_util.get_fields_to_be_save(request)
		data = add_extra_data(data, request.POST)
		update_data = {}
		update_fields = set(['name', 'start_time', 'end_time', 'expend', 'delivery', 'delivery_setting', 'limitation', 'chance', 'type', 'prize'])
		for key, value in data.items():
			if key in update_fields:
				update_data['set__'+key] = value
		app_models.lottery.objects(id=request.POST['id']).update(**update_data)
		
		response = create_response(200)
		return response.get_response()
	
	@login_required
	def api_delete(request):
		"""
		响应DELETE
		"""
		app_models.lottery.objects(id=request.POST['id']).delete()
		
		response = create_response(200)
		return response.get_response()

def add_extra_data(data, post):
	print post
	data['expend'] = int(post.get('expend', 0))
	data['delivery'] = int(post.get('delivery', 0))
	data['delivery_setting'] = post.get('delivery_setting', 'true')
	data['limitation'] = post.get('limitation', 'once_per_user')
	data['chance'] = int(post.get('chance', 0))
	data['allow_repeat'] = post.get('allow_repeat', 'true')
	return data
