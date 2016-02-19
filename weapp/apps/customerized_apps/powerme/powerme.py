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
from utils.cache_util import delete_cache

import models as app_models
import export
from apps import request_util
from mall import export as mall_export
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api
import termite.pagestore as pagestore_manager

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class PowerMe(resource.Resource):
	app = 'apps/powerme'
	resource = 'powerme'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			project_id = 'new_app:powerme:%s' % request.GET.get('related_page_id', 0)
			try:
				powerme = app_models.PowerMe.objects.get(id=request.GET['id'])
			except:
				c = RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
					'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
					'third_nav_name': mall_export.MALL_APPS_POWERME_NAV,
					'is_deleted_data': True,
				})

				return render_to_response('powerme/templates/editor/workbench.html', c)
			is_create_new_data = False

			name = powerme.name
		else:
			powerme = None
			is_create_new_data = True
			project_id = 'new_app:powerme:0'
			name = u'微助力'

		_, app_name, real_project_id = project_id.split(':')
		if real_project_id != '0':
			pagestore = pagestore_manager.get_pagestore('mongo')
			pages = pagestore.get_page_components(real_project_id)
			if not pages:
				c = RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
					'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
					'third_nav_name': mall_export.MALL_APPS_POWERME_NAV,
					'is_deleted_data': True,
				})

				return render_to_response('powerme/templates/editor/workbench.html', c)
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': mall_export.MALL_APPS_POWERME_NAV,
			'powerme': powerme,
			'title_name': name,
			'is_create_new_data': is_create_new_data,
			'project_id': project_id,
		})
		
		return render_to_response('powerme/templates/editor/workbench.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		data['qrcode'] = json.loads(request.POST['qrcode'])

		powerme = app_models.PowerMe(**data)
		powerme.save()
		error_msg = None
		
		data = json.loads(powerme.to_json())
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
		data['qrcode'] = json.loads(request.POST['qrcode'])

		update_data = {}
		# update_fields = set(['name', 'start_time', 'end_time', 'timing', 'desc', 'reply_content', 'material_image', 'qrcode'])
		update_fields = data.keys()
		for key, value in data.items():
			if key in update_fields:
				if key == "timing":
					value = bool2Bool(value)
				update_data['set__'+key] = value
				print key,value,"$$$$$$$$$"
		app_models.PowerMe.objects(id=request.POST['id']).update(**update_data)

		#更新后清除缓存
		cache_key = 'apps_powerme_%s_html' % request.POST['id']
		delete_cache(cache_key)
		
		response = create_response(200)
		return response.get_response()
	
	@login_required
	def api_delete(request):
		"""
		响应DELETE
		"""
		app_models.PowerMe.objects(id=request.POST['id']).delete()
		
		response = create_response(200)
		return response.get_response()

def bool2Bool(bo):
	"""
	JS字符串布尔值转化为Python布尔值
	"""
	bool_dic = {'true':True,'false':False,'True':True,'False':False}
	if bo:
		result = bool_dic[bo]
	else:
		result = None
	return result