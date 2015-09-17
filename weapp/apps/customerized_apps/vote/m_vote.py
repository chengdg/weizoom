# -*- coding: utf-8 -*-
from collections import OrderedDict

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
import weixin.user.models as weixin_models

SHORTCUTS_TEXT={
	'phone': u'手机',
	'name': u'姓名',
	'email': u'邮箱',
	'qq':u'QQ号',
	'job':u'职位',
	'addr':u'地址'
}


class Mvote(resource.Resource):
	app = 'apps/vote'
	resource = 'm_vote'
	
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
			thumbnails_url = '/static_v2/img/thumbnails_vote.png'
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
				record = app_models.vote.objects.get(id=id)
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

				project_id = 'new_app:vote:%s' % record.related_page_id
				if request.member:
					participance_data_count = app_models.voteParticipance.objects(belong_to=id, member_id=request.member.id).count()
				if participance_data_count == 0 and request.webapp_user:
					participance_data_count = app_models.voteParticipance.objects(belong_to=id, webapp_user_id=request.webapp_user.id).count()
				pagestore = pagestore_manager.get_pagestore('mongo')
				page = pagestore.get_page(record.related_page_id, 1)
				permission = page['component']['components'][0]['model']['permission']

			is_already_participanted = (participance_data_count > 0)
			if  is_already_participanted:
				member_id = request.member.id
				vote_detail,result_list = get_result(id,member_id)
				c = RequestContext(request, {
					'vote_detail': vote_detail,
					'record_id': id,
					'page_title': '微信投票',
					'app_name': "vote",
					'resource': "vote",
					'q_vote': result_list,
					'hide_non_member_cover': True, #非会员也可使用该页面
					'isMember': isMember,
					'auth_appid_info': auth_appid_info
				})
				return render_to_response('vote/templates/webapp/result_vote.html', c)
			else:
				request.GET._mutable = True
				request.GET.update({"project_id": project_id})
				request.GET._mutable = False
				html = pagecreater.create_page(request, return_html_snippet=True)

				c = RequestContext(request, {
					'record_id': id,
					'member_id': request.member.id if request.member else "",
					'activity_status': activity_status,
					'is_already_participanted': is_already_participanted,
					'page_title': '微信投票',
					'page_html_content': html,
					'app_name': "vote",
					'resource': "vote",
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
			})
			return render_to_response('vote/templates/webapp/m_vote.html', c)


class resultVote(resource.Resource):
	app = 'apps/vote'
	resource = 'result_vote'

	def get(request):
		print request.GET
		if 'id' in request.GET:
			id = request.GET['id']
			isMember = request.GET.get('isMember',0)
			member_id = request.GET['member_id']
			auth_appid_info = None
			if not isMember:
				from weixin.user.util import get_component_info_from
				component_info = get_component_info_from(request)
				auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.GET['webapp_owner_id'])[0]
				auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
			vote_detail,result_list = get_result(id,member_id)
			c = RequestContext(request, {
				'vote_detail': vote_detail,
				'record_id': id,
				'page_title': '微信投票',
				'app_name': "vote",
				'resource': "vote",
				'q_vote': result_list,
				'hide_non_member_cover': True, #非会员也可使用该页面
				'isMember': isMember,
				'auth_appid_info': auth_appid_info,
			})
			return render_to_response('vote/templates/webapp/result_vote.html', c)


def get_result(id,member_id):
	vote_detail ={}
	vote_vote = app_models.vote.objects.get(id=id)
	vote_detail['name'] = vote_vote['name']
	vote_detail['start_time'] = vote_vote['start_time'].strftime('%Y-%m-%d %H:%M')
	vote_detail['end_time'] = vote_vote['end_time'].strftime('%Y-%m-%d %H:%M')

	votes = app_models.voteParticipance.objects(belong_to=id)
	member_vote_termite = app_models.voteParticipance.objects.filter(belong_to=id,member_id=member_id).order_by('-created_at').first().termite_data
	member_termite_select = {}
	member_termite_shortcuts = {}
	for k,member_termite in member_vote_termite.items():
		value = member_vote_termite[k]
		if value['type'] == 'appkit.selection':
			for select,isSelect in value['value'].items():
				member_termite_select[select] = {
					'isSelect': isSelect['isSelect'],
					'type': isSelect['type']
				}
		if value['type'] in['appkit.textlist', 'appkit.shortcuts']:
			member_termite_shortcuts[k] = value['value']
	questions =OrderedDict()
	result_list = []

	for vote in votes:
		termite_data = vote.termite_data
		for title in sorted(termite_data.keys()):
			value = termite_data[title]
			if value['type'] == 'appkit.selection':
				if not questions.has_key(title):
					questions[title] = [value['value']]
				else:
					questions[title].append(value['value'])
			if value['type'] in['appkit.textlist', 'appkit.shortcuts']:
				questions[title] = []
	for q_title,values in questions.items():
		value_isSelect = {}
		result = {}
		value_list = []
		total_count = 0
		timp_vlaue = {}
		for value in values:
			timp_vlaue = value
			for v_title,v_value in value.items():
				if v_value:
					if not value_isSelect.has_key(v_title):
						value_isSelect[v_title] = 0
					if v_value['isSelect'] == True:
						value_isSelect[v_title] += 1
						total_count += 1
				else:
					value_isSelect[v_title] = []
		for timp_k in sorted(timp_vlaue.keys()):
			value ={}
			name = timp_k.split('_')[1]
			value['name'] = name
			value['id_name'] = timp_k
			value['count'] = value_isSelect[timp_k]
			value['per'] =  '%d' % (value_isSelect[timp_k]*100/float(total_count))
			value['isSelect'] = member_termite_select[timp_k]['isSelect']
			value['type'] = member_termite_select[timp_k]['type']
			value_list.append(value)
		title_name = q_title.split('_')[1]
		isShortcuts = False
		if title_name in SHORTCUTS_TEXT.keys():
			isShortcuts = True
			value_list = member_termite_shortcuts[q_title]
			title_name = SHORTCUTS_TEXT[title_name]
		result['title'] = title_name
		result['values'] = value_list
		result['isShortcuts'] = isShortcuts
		result_list.append(result)

	related_page_id = vote_vote.related_page_id

	pagestore = pagestore_manager.get_pagestore('mongo')
	page = pagestore.get_page(related_page_id, 1)
	page_info = page['component']['components'][0]['model']
	vote_detail['subtitle'] = page_info['subtitle']
	vote_detail['description'] = page_info['description']
	prize_type = page_info['prize']['type']
	vote_detail['prize_type'] = prize_type
	if prize_type == 'coupon':
		prize_data = page_info['prize']['data']['name']
	else:
		prize_data = page_info['prize']['data']
	vote_detail['prize_data'] = prize_data

	return vote_detail,result_list