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
			isPC = int(request.GET.get('isPC',0))
			isPC = True if isPC else False
			isMember = request.member.is_subscribed
			if isMember:
				auth_appid_info = None
			else:
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
				if isMember:
						auth_appid_info = None
				else:
					from weixin.user.util import get_component_info_from
					component_info = get_component_info_from(request)
					auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.GET['webapp_owner_id'])[0]
					auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
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
					'auth_appid_info': auth_appid_info
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

	surveies = app_models.surveyParticipance.objects(belong_to=id)
	member_survey_termite = app_models.surveyParticipance.objects.filter(belong_to=id,member_id=member_id).order_by('-created_at').first().termite_data
	member_termite_select = {}
	member_termite_shortcuts = {}
	for k,member_termite in member_survey_termite.items():
		value = member_survey_termite[k]
		if value['type'] == 'appkit.selection':
			for select,isSelect in value['value'].items():
				member_termite_select[select] = isSelect['isSelect']
		if value['type'] == 'appkit.shortcuts':
			member_termite_shortcuts[k] = value['value']
	q_survey =OrderedDict()
	result_list = []

	for survey in surveies:
		termite_data = survey.termite_data
		for k in sorted(termite_data.keys()):
			value = termite_data[k]
			if value['type'] == 'appkit.selection':
				if not q_survey.has_key(k):
					q_survey[k] = [value['value']]
				else:
					q_survey[k].append(value['value'])
			if value['type'] == 'appkit.shortcuts':
				q_survey[k] = []
	for k,v in q_survey.items():
		a_isSelect = {}
		result = {}
		total_count = len(v)
		value_list = []

		v_a = {}
		for a in v:
			v_a=a
			print v_a
			for a_k,a_v in a.items():
				if a_v:
					if not a_isSelect.has_key(a_k):
						a_isSelect[a_k] = 0
					if a_v['isSelect'] == True:
						a_isSelect[a_k] += 1
				else:
					a_isSelect[a_k] = []
		for a_k in sorted(v_a.keys()):
			value ={}
			name = a_k.split('_')[1]
			value['name'] = name
			value['id_name'] = a_k
			value['count'] = a_isSelect[a_k]
			value['per'] =  '%d' % (a_isSelect[a_k]*100/float(total_count))
			value['isSelect'] = member_termite_select[a_k]
			value_list.append(value)
		title_name = k.split('_')[1]
		isShortcuts = False
		if title_name in SHORTCUTS_TEXT.keys():
			isShortcuts = True
			value_list = member_termite_shortcuts[k]
			title_name = SHORTCUTS_TEXT[title_name]
		result['title'] = title_name
		result['values'] = value_list
		result['isShortcuts'] = isShortcuts
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