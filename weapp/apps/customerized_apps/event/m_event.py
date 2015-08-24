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
from termite2 import pagecreater
from termite import pagestore as pagestore_manager

class Mevent(resource.Resource):
	app = 'apps/event'
	resource = 'm_event'
	
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			id = request.GET['id']
			isPC = int(request.GET.get('isPC',0))
			isPC = True if isPC else False
			participance_data_count = 0
			if 'new_app:' in id:
				project_id = id
				activity_status = u"未开始"
			else:
				#termite类型数据
				record = app_models.event.objects.get(id=id)
				activity_status = record.status_text

				now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
				data_start_time = record.start_time.strftime('%Y-%m-%d %H:%M')
				data_end_time = record.end_time.strftime('%Y-%m-%d %H:%M')
				if data_start_time <= now_time and now_time < data_end_time:
					record.update(set__status=app_models.STATUS_RUNNING)
					activity_status = u'进行中'
				elif now_time >= data_end_time:
					record.update(set__status=app_models.STATUS_STOPED)
					activity_status = u'已结束'
				project_id = 'new_app:event:%s' % record.related_page_id
				
				if request.member:
					participance_data_count = app_models.eventParticipance.objects(belong_to=id, member_id=request.member.id).count()
				if participance_data_count == 0 and request.webapp_user:
					participance_data_count = app_models.eventParticipance.objects(belong_to=id, webapp_user_id=request.webapp_user.id).count()
			is_already_participanted = (participance_data_count > 0)
			if  is_already_participanted:
				event_detail,activity_status = get_result(id,request.member.id)
				c = RequestContext(request, {
					'event_detail': event_detail,
					'record_id': id,
					'activity_status': activity_status,
					'page_title': '活动报名',
					'app_name': "event",
					'resource': "event",
					'hide_non_member_cover': True #非会员也可使用该页面
				})
				return render_to_response('event/templates/webapp/is_already_participanted.html', c)
			else:
				request.GET._mutable = True
				request.GET.update({"project_id": project_id})
				request.GET._mutable = False
				html = pagecreater.create_page(request, return_html_snippet=True)
				
				c = RequestContext(request, {
					'record_id': id,
					'activity_status': activity_status,
					'is_already_participanted': (participance_data_count > 0),
					'page_title': '活动报名',
					'page_html_content': html,
					'app_name': "event",
					'resource': "event",
					'hide_non_member_cover': True, #非会员也可使用该页面
					'isPC': isPC
				})
				
				return render_to_response('workbench/wepage_webapp_page.html', c)
		else:
			record = None
			c = RequestContext(request, {
				'record': record
			});
			
			return render_to_response('event/templates/webapp/m_event.html', c)

def get_result(id,member_id):
	event_detail ={}
	event_event = app_models.event.objects.get(id=id)
	event_detail['name'] = event_event['name']
	event_detail['end_time'] = event_event['end_time'].strftime('%Y-%m-%d')

	related_page_id = event_event.related_page_id
	activity_status = event_event.status_text

	pagestore = pagestore_manager.get_pagestore('mongo')
	page = pagestore.get_page(related_page_id, 1)
	page_info = page['component']['components'][0]['model']
	event_detail['subtitle'] = page_info['subtitle']
	event_detail['description'] = page_info['description']

	return event_detail,activity_status