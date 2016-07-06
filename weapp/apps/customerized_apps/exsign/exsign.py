# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from utils.cache_util import delete_cache

import models as app_models
import export
from mall import export as mall_export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api


FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class Sign(resource.Resource):
	app = 'apps/exsign'
	resource = 'exsign'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		owner_id = request.manager.id
		exsign = app_models.exSign.objects(owner_id=owner_id)
		if exsign.count() > 0:
			exsign = exsign[0]
			is_create_new_data = False
			project_id = 'new_app:exsign:%s' % exsign.related_page_id
		else:
			exsign = None
			is_create_new_data = True
			project_id = 'new_app:exsign:0'

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': mall_export.MALL_APPS_EXSIGN_NAV,
			'exsign': exsign,
			'is_create_new_data': is_create_new_data,
			'project_id': project_id,
			'webapp_owner_id': owner_id,
		})

		return render_to_response('exsign/templates/editor/workbench.html', c)


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
		exsign = app_models.exSign(**data)
		exsign.save()

		error_msg = None

		data = json.loads(exsign.to_json())
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
		if request.POST.get('status', None):
			status = 1 if request.POST['status'] == 'on' else 0
			exsigns = app_models.exSign.objects(id=request.POST['exsignId'])
			exsigns.update(set__status=status)
			if status == 1 and exsigns.count() >0:
				#将所有已签到用户的签到状态重置，作为一个新的签到
				exsign = exsigns[0]
				app_models.exSignParticipance.objects(belong_to=str(exsign.id)).update(set__serial_count=0, set__latest_date=None)
				# app_models.SignControl.objects.all().delete()
			cache_key = 'apps_exsign_%s_html' % str(exsigns[0].owner_id)
		else:
			data = export.get_sing_fields_to_save(request)
			update_data = {}
			update_fields = set(['name', 'share', 'prize_settings'])
			for key, value in data.items():
				if key in update_fields:
					update_data['set__'+key] = value
			exsign = app_models.exSign.objects(id=request.POST['exsignId']).first()
			exsign.update(**update_data)
			cache_key = 'apps_exsign_%s_html' % exsign.owner_id
		#更新后清除redis缓存
		delete_cache(cache_key)

		response = create_response(200)
		return response.get_response()
