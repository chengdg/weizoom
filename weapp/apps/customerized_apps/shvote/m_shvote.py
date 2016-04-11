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
import weixin.user.models as weixin_models

class MShvote(resource.Resource):
	app = 'apps/shvote'
	resource = 'm_shvote'
	
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			id = request.GET['id']
			isPC = request.GET.get('isPC',0)
			participance_data_count = 0
			isMember = False
			auth_appid_info = None
			if not isPC:
				isMember = request.member and request.member.is_subscribed
			
			if 'new_app:' in id:
				project_id = id
				activity_status = u"未开启"
			else:
				#termite类型数据
				try:
					record = app_models.Shvote.objects.get(id=id)
				except:
					c = RequestContext(request,{
						'is_deleted_data': True
					})
					return render_to_response('shvote/templates/webapp/m_shvote.html', c)
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
				
				project_id = 'new_app:shvote:%s' % record.related_page_id
				
				if request.member:
					participance_data_count = app_models.ShvoteParticipance.objects(belong_to=id, member_id=request.member.id).count()
			
			request.GET._mutable = True
			request.GET.update({"project_id": project_id})
			request.GET._mutable = False
			html = pagecreater.create_page(request, return_html_snippet=True)
			
			c = RequestContext(request, {
				'record_id': id,
				'activity_status': activity_status,
				'is_already_participanted': (participance_data_count > 0),
				'page_title': "上海投票",
				'page_html_content': html,
				'app_name': "shvote",
				'resource': "shvote",
				'hide_non_member_cover': True, #非会员也可使用该页面
				'isPC': isPC,
				'isMember': isMember,
				'auth_appid_info': auth_appid_info
			})
			
			return render_to_response('shvote/templates/webapp/m_shvote.html', c)
		else:
			record = None
			c = RequestContext(request, {
				'record': record
			});
			
			return render_to_response('shvote/templates/webapp/m_shvote.html', c)

