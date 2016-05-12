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
from termite import pagestore as pagestore_manager

class RedPacketStatus(resource.Resource):
	app = 'apps/red_packet'
	resource = 'red_packet_status'
	
	@login_required
	def api_post(request):
		"""
		响应POST
		"""
		target_status = request.POST['target']
		if target_status == 'stoped':
			target_status = app_models.STATUS_STOPED
			now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
			app_models.RedPacket.objects(id=request.POST['id']).update(set__end_time=now_time)
			pagestore = pagestore_manager.get_pagestore('mongo')
			datas = app_models.RedPacket.objects(id=request.POST['id'])
			for data in datas:
				related_page_id = data.related_page_id
			page = pagestore.get_page(related_page_id, 1)
			page['component']['components'][0]['model']['end_time'] = now_time
			pagestore.save_page(related_page_id, 1, page['component'])
		elif target_status == 'running':
			target_status = app_models.STATUS_RUNNING
		elif target_status == 'not_start':
			target_status = app_models.STATUS_NOT_START
		app_models.RedPacket.objects(id=request.POST['id']).update(set__status=target_status)
		
		response = create_response(200)
		return response.get_response()

	@login_required
	def api_put(request):
		"""
		手动发放单个活动的微众卡
		"""
		record_id = request.GET.get('record_id', None)
		response = create_response(500)
		if not record_id:
			response.errMsg = u"请求参数出错~"
			return response.get_response()
		try:
			record = app_models.Rebate.objects.get(id=record_id, status__ne=app_models.STATUS_NOT_START)
			export.handle_rebate_core([record])
		except:
			response.errMsg = u'活动信息出错~'
			return response.get_response()
