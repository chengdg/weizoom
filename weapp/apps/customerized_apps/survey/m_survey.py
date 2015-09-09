# -*- coding: utf-8 -*-

import json
from datetime import datetime
from collections import OrderedDict

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
import weixin.user.models as weixin_models

SHORTCUTS_TEXT={
	'phone': u'手机',
	'name': u'姓名',
	'email': u'邮箱'
}
class Msurvey(resource.Resource):
	app = 'apps/survey'
	resource = 'm_survey'
	
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			id = request.GET['id']
			isPC = request.GET.get('isPC',0)
			isMember = False
			auth_appid_info = None
			permission = ''
			share_page_desc = ''
			thumbnails_url = '/static_v2/img/thumbnails_survey.png'
			if not isPC:
				isMember = request.member and request.member.is_subscribed
				if not isMember:
					from weixin.user.util import get_component_info_from
					component_info = get_component_info_from(request)
					auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.GET['webapp_owner_id'])[0]
					auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
			participance_data_count = 0
			if 'new_app:' in id:
				project_id = id
				activity_status = u"未开始"
			else:
				#termite类型数据
				record = app_models.survey.objects.get(id=id)
				activity_status = record.status_text
				share_page_desc =record.name
				now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
				data_start_time = record.start_time.strftime('%Y-%m-%d %H:%M')
				data_end_time = record.end_time.strftime('%Y-%m-%d %H:%M')
				if record.status <= 1:
					if data_start_time <= now_time and now_time < data_end_time:
						record.update(set__status=app_models.STATUS_RUNNING)
						activity_status = u'进行中'
					elif now_time >= data_end_time:
						record.update(set__status=app_models.STATUS_STOPED)
						activity_status = u'已结束'

				project_id = 'new_app:survey:%s' % record.related_page_id
				if request.member:
					participance_data_count = app_models.surveyParticipance.objects(belong_to=id, member_id=request.member.id).count()
				if participance_data_count == 0 and request.webapp_user:
					participance_data_count = app_models.surveyParticipance.objects(belong_to=id, webapp_user_id=request.webapp_user.id).count()
				pagestore = pagestore_manager.get_pagestore('mongo')
				page = pagestore.get_page(record.related_page_id, 1)
				permission = page['component']['components'][0]['model']['permission']
			is_already_participanted = (participance_data_count > 0)
			if  is_already_participanted:
				member_id = request.member.id
				survey_detail,result_list = get_result(id,member_id)
				c = RequestContext(request, {
					'survey_detail': survey_detail,
					'record_id': id,
					'page_title': '用户调研',
					'app_name': "survey",
					'resource': "survey",
					'q_survey': result_list,
					'hide_non_member_cover': True, #非会员也可使用该页面
					'isMember': isMember,
					'auth_appid_info': auth_appid_info
				})
				return render_to_response('survey/templates/webapp/result_survey.html', c)
			else:
				request.GET._mutable = True
				request.GET.update({"project_id": project_id})
				request.GET._mutable = False
				html = pagecreater.create_page(request, return_html_snippet=True)

				c = RequestContext(request, {
					'record_id': id,
					'activity_status': activity_status,
					'is_already_participanted': (participance_data_count > 0),
					'page_title': '用户调研',
					'page_html_content': html,
					'app_name': "survey",
					'resource': "survey",
					'hide_non_member_cover': True, #非会员也可使用该页面
					'isPC': isPC,
					'isMember': isMember,
					'auth_appid_info': auth_appid_info,
					'permission': permission,
					'share_page_desc': share_page_desc,
					'share_img_url': thumbnails_url
				})

				return render_to_response('workbench/wepage_webapp_page.html', c)
		else:
			record = None
			c = RequestContext(request, {
				'record': record
			});
			return render_to_response('survey/templates/webapp/m_survey.html', c)

def get_result(id,member_id):
	survey_detail ={}
	survey_survey = app_models.survey.objects.get(id=id)
	survey_detail['name'] = survey_survey['name']
	survey_detail['start_time'] = survey_survey['start_time'].strftime('%Y-%m-%d %H:%M')
	survey_detail['end_time'] = survey_survey['end_time'].strftime('%Y-%m-%d %H:%M')

	member_survey_termite = app_models.surveyParticipance.objects.filter(belong_to=id,member_id=member_id).order_by('-created_at').first().termite_data
	result_list = []

	for title in sorted(member_survey_termite.keys()):
		title_type = member_survey_termite[title]['type']
		result = {}
		title_name = title.split('_')[1]
		if title_type == 'appkit.shortcuts':
			title_name = SHORTCUTS_TEXT[title_name]
		result['title'] = title_name
		result['type'] = title_type
		values = member_survey_termite[title]['value']

		if title_type == 'appkit.selection':
			select_values = []
			for select_title in sorted(values.keys()):
				select_value = {}
				select_value['name'] = select_title.split('_')[1]
				select_value['type'] = values[select_title]['type']
				select_value['isSelect'] = values[select_title]['isSelect']
				select_values.append(select_value)
			values = select_values
		result['values'] = values
		result_list.append(result)


	related_page_id = survey_survey.related_page_id

	pagestore = pagestore_manager.get_pagestore('mongo')
	page = pagestore.get_page(related_page_id, 1)
	page_info = page['component']['components'][0]['model']
	survey_detail['subtitle'] = page_info['subtitle']
	survey_detail['description'] = page_info['description']
	prize_type = page_info['prize']['type']
	survey_detail['prize_type'] = prize_type
	if prize_type == 'coupon':
		prize_data = page_info['prize']['data']['name']
	else:
		prize_data = page_info['prize']['data']
	survey_detail['prize_data'] = prize_data

	return survey_detail,result_list