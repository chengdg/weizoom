# -*- coding: utf-8 -*-
__STRIPPER_TAG__

import json
from datetime import datetime
__STRIPPER_TAG__

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

__STRIPPER_TAG__
from core import resource
from core import paginator
from core.jsonresponse import create_response

__STRIPPER_TAG__
import models as app_models
import export
from apps import request_util
from termite2 import pagecreater

__STRIPPER_TAG__
class M{{resource.class_name}}(resource.Resource):
	app = 'apps/{{app_name}}'
	resource = 'm_{{resource.lower_name}}'

	{% if resource.actions.get %}
	__STRIPPER_TAG__
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			{% if resource.enable_termite %}
			id = request.GET['id']
			participance_data_count = 0
			if 'new_app:' in id:
				project_id = id
				activity_status = u"未开启"
			else:
				#termite类型数据
				record = app_models.{{resource.class_name}}.objects.get(id=id)
				activity_status = record.status_text

				__STRIPPER_TAG__
				now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
				data_start_time = record.start_time.strftime('%Y-%m-%d %H:%M')
				data_end_time = record.end_time.strftime('%Y-%m-%d %H:%M')
				if data_start_time <= now_time and now_time < data_end_time:
					record.update(set__status=app_models.STATUS_RUNNING)
					activity_status = u'进行中'
				elif now_time >= data_end_time:
					record.update(set__status=app_models.STATUS_STOPED)
					activity_status = u'已结束'
				__STRIPPER_TAG__

				project_id = 'new_app:{{app_name}}:%s' % record.related_page_id

				__STRIPPER_TAG__
				{% if resource.need_check_user_participant %}
				if request.member:
					participance_data_count = app_models.{{resource.class_name}}Participance.objects(belong_to=id, member_id=request.member.id).count()
				if participance_data_count == 0 and request.webapp_user:
					participance_data_count = app_models.{{resource.class_name}}Participance.objects(belong_to=id, webapp_user_id=request.webapp_user.id).count()
				{% endif %}

			__STRIPPER_TAG__
			request.GET._mutable = True
			request.GET.update({"project_id": project_id})
			request.GET._mutable = False
			html = pagecreater.create_page(request, return_html_snippet=True)

			__STRIPPER_TAG__
			c = RequestContext(request, {
				'record_id': id,
				'activity_status': activity_status,
				'is_already_participanted': (participance_data_count > 0),
				'page_title': '用户调研',
				'page_html_content': html,
				'app_name': "{{app_name}}",
				'resource': "{{resource.lower_name}}",
				'hide_non_member_cover': True #非会员也可使用该页面
			})

			__STRIPPER_TAG__
			return render_to_response('workbench/wepage_webapp_page.html', c)
			{% else %}
			record = app_models.{{resource.class_name}}.objects.get(id=request.GET['id'])
			record = json.loads(record.to_json())
			record['id'] = request.GET['id']

			__STRIPPER_TAG__
			c = RequestContext(request, {
				'record': record
			});
			
			__STRIPPER_TAG__
			return render_to_response('{{app_name}}/templates/webapp/m_{{resource.lower_name}}.html', c)
			{% endif %}
		else:
			record = None
			c = RequestContext(request, {
				'record': record
			});
			
			__STRIPPER_TAG__
			return render_to_response('{{app_name}}/templates/webapp/m_{{resource.lower_name}}.html', c)
	{% endif %}
