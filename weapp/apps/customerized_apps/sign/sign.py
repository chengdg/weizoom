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
import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

class Sign(resource.Resource):
	app = 'apps/sign'
	resource = 'sign'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		owner_id = request.user.id
		sign = app_models.Sign.objects(owner_id=owner_id)
		if sign.count()>0:
			sign = sign[0]
			is_create_new_data = False
			project_id = 'new_app:sign:%s' % sign.related_page_id
		else:
			sign = None
			is_create_new_data = True
			project_id = 'new_app:sign:0'
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': 'sign',
			'sign': sign,
			'is_create_new_data': is_create_new_data,
			'project_id': project_id,
			'webapp_owner_id': owner_id,
		})
		
		return render_to_response('sign/templates/editor/workbench.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应PUT
		"""
		data = export.get_sing_fields_to_save(request)
		status = request.POST['status']
		if status:
			data['status'] = 0 if status == 'off' else 1
		data['related_page_id'] = request.POST['related_page_id']
		sign = app_models.Sign(**data)
		sign.save()
		error_msg = None
		
		data = json.loads(sign.to_json())
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
		print request.POST
		if request.POST.get('status', None):
			status = 1 if request.POST['status'] == 'on' else 0
			app_models.Sign.objects(id=request.POST['signId']).update(set__status=status)
			response = create_response(200)
			return response.get_response()

		data = export.get_sing_fields_to_save(request)
		update_data = {}
		print data
		update_fields = set(['name', 'share', 'reply', 'prize_settings'])
		for key, value in data.items():
			if key in update_fields:
				update_data['set__'+key] = value
		app_models.Sign.objects(id=request.POST['id']).update(**update_data)
		
		response = create_response(200)
		return response.get_response()