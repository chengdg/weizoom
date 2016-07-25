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
from utils.cache_util import delete_cache, delete_pattern

import models as app_models
from mall import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api
import termite.pagestore as pagestore_manager


FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class Egg(resource.Resource):
	app = 'apps/egg'
	resource = 'egg'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			project_id = 'new_app:egg:%s' % request.GET.get('related_page_id', 0)
			try:
				egg = app_models.Egg.objects.get(id=request.GET['id'])
			except:
				c = RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': export.get_promotion_and_apps_second_navs(request),
					'second_nav_name': export.MALL_APPS_SECOND_NAV,
					'third_nav_name': export.MALL_APPS_EGG_NAV,
					'is_deleted_data': True
				})
				return render_to_response('egg/templates/editor/workbench.html', c)

			is_create_new_data = False
		else:
			egg = None
			is_create_new_data = True
			project_id = 'new_app:egg:0'

		_, app_name, real_project_id = project_id.split(':')
		if real_project_id != '0':
			pagestore = pagestore_manager.get_pagestore('mongo')
			pages = pagestore.get_page_components(real_project_id)
			if not pages:
				c = RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': export.get_promotion_and_apps_second_navs(request),
					'second_nav_name': export.MALL_APPS_SECOND_NAV,
					'third_nav_name': export.MALL_APPS_EGG_NAV,
					'is_deleted_data': True
				})
				return render_to_response('egg/templates/editor/workbench.html', c)
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
            'third_nav_name': export.MALL_APPS_EGG_NAV,
			'egg': egg,
			'is_create_new_data': is_create_new_data,
			'project_id': project_id,
		})
		
		return render_to_response('egg/templates/editor/workbench.html', c)

	@login_required
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		data = add_extra_data(data, request.POST)
		egg = app_models.Egg(**data)
		egg.save()
		error_msg = None
		
		data = json.loads(egg.to_json())
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
		app_models.Egg.objects(id=request.POST['id']).update(**update_data)

		#更新后清除缓存
		# cache_key = 'apps_egg_%s_noprizecount' % request.POST['id']
		# delete_cache(cache_key)
		cache_key = "apps_egg_%s_*" % request.POST['id']
		delete_pattern(cache_key)
		
		response = create_response(200)
		return response.get_response()
	
	@login_required
	def api_delete(request):
		"""
		响应DELETE
		"""
		app_models.Egg.objects(id=request.POST['id']).delete()
		
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

class EggPrizeCount(resource.Resource):
	app = 'apps/egg'
	resource = 'egg_prize_count'

	@login_required
	def api_get(request):
		egg = app_models.Egg.objects.get(id=request.GET['id'])
		response = create_response(200)
		response.data = egg.prize
		return response.get_response()


