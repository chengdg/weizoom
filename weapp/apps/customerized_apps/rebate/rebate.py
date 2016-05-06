# -*- coding: utf-8 -*-

import json
import random
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.conf import settings

from core import resource
from core import paginator
from core.jsonresponse import create_response
from utils.cache_util import delete_cache

import models as app_models
import export
from apps import request_util
from mall import export as mall_export
from modules.member import integral as integral_api
import termite.pagestore as pagestore_manager
from core.wxapi import get_weixin_api
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from core.wxapi.api_create_qrcode_ticket import QrcodeTicket

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class RedPacket(resource.Resource):
	app = 'apps/rebate'
	resource = 'rebate'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			project_id = 'new_app:rebate:%s' % request.GET.get('related_page_id', 0)
			try:
				rebate = app_models.Rebate.objects.get(id=request.GET['id'])
			except:
				c = RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
					'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
					'third_nav_name': mall_export.MALL_APPS_REBATE_NAV,
					'is_deleted_data': True,
				})
				return render_to_response('rebate/templates/editor/create_rebate_rule.html', c)
			is_create_new_data = False

			name = rebate.name
		else:
			rebate = None
			is_create_new_data = True
			project_id = 'new_app:rebate:0'
			name = u'返利活动'

		_, app_name, real_project_id = project_id.split(':')
		if real_project_id != '0':
			pagestore = pagestore_manager.get_pagestore('mongo')
			pages = pagestore.get_page_components(real_project_id)
			if not pages:
				c = RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
					'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
					'third_nav_name': mall_export.MALL_APPS_REBATE_NAV,
					'is_deleted_data': True,
				})

				return render_to_response('rebate/templates/editor/create_rebate_rule.html', c)
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': mall_export.MALL_APPS_REBATE_NAV,
			'rebate': rebate,
			'title_name': name,
			'is_create_new_data': is_create_new_data,
			'project_id': project_id,
		})
		
		return render_to_response('rebate/templates/editor/create_rebate_rule.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		rebate = app_models.Rebate(**data)
		rebate.save()

		error_msg = None
		data = json.loads(rebate.to_json())
		data['id'] = data['_id']['$oid']

		if error_msg:
			data['error_msg'] = error_msg

		if settings.MODE != 'develop':
			mp_user = get_binding_weixin_mpuser(request.manager)
			mpuser_access_token = get_mpuser_accesstoken(mp_user)
			weixin_api = get_weixin_api(mpuser_access_token)

			try:
				qrcode_ticket = weixin_api.create_qrcode_ticket(int(data['id']), QrcodeTicket.PERMANENT)
				ticket = qrcode_ticket.ticket
			except Exception, e:
				print 'get qrcode_ticket fail:', e
				ticket = ''
		else:
			ticket = ''
		rebate.ticket = ticket
		rebate.save()
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
		pagestore = pagestore_manager.get_pagestore('mongo')
		project_id = request.GET.get('project_id', 0)
		_, app_name, real_project_id = project_id.split(':')
		page = pagestore.get_page(real_project_id, 1)
		update_data = {}
		update_fields = set(['name', 'start_time', 'end_time', 'timing', 'rebate_type', 'random_total_money','random_packets_number','regular_packets_number','regular_per_money','money_range','reply_content', 'material_image','share_description', 'qrcode'])

		app_models.Rebate.objects(id=request.POST['id']).update(**update_data)

		pagestore.save_page(real_project_id, 1, page['component'])
		#更新后清除缓存
		cache_key = 'apps_rebate_%s_html' % request.POST['id']
		delete_cache(cache_key)
		response = create_response(200)
		return response.get_response()
	
	@login_required
	def api_delete(request):
		"""
		响应DELETE
		"""
		app_models.Rebate.objects(id=request.POST['id']).delete()
		
		response = create_response(200)
		return response.get_response()
