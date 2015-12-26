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
				# if not isMember:
				# 	from weixin.user.util import get_component_info_from
				# 	component_info = get_component_info_from(request)
				# 	auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.GET['webapp_owner_id'])[0]
				# 	auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
			participance_data_count = 0
			if 'new_app:' in id:
				project_id = id
				activity_status = u"未开始"
			else:
				#termite类型数据
				try:
					record = app_models.vote.objects.get(id=id)
				except:
					c = RequestContext(request, {
						'is_deleted_data': True
					})
					return render_to_response('workbench/wepage_webapp_page.html', c)
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
					'isPC': False if request.member else True,
					'isMember': isMember,
					'auth_appid_info': auth_appid_info,
					'permission': permission,
					'share_page_desc': share_page_desc,
					'share_img_url': thumbnails_url
				})
				return render_to_response('vote/templates/webapp/m_vote.html', c)
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
			# if not isMember:
			# 	from weixin.user.util import get_component_info_from
			# 	component_info = get_component_info_from(request)
			# 	auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.GET['webapp_owner_id'])[0]
			# 	auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
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
	member_termite_textselect = {}
	member_termite_imageselect = {}
	member_termite_shortcuts = {}
	for k,member_termite in member_vote_termite.items():
		value = member_vote_termite[k]
		if value['type'] == 'appkit.selection':
			for select,isSelect in value['value'].items():
				member_termite_select[k+select] = {
					'isSelect': isSelect['isSelect'],
					'type': isSelect['type']
				}
		if value['type'] == 'appkit.textselection':
			for select,isSelect in value['value'].items():
				member_termite_textselect[k+select] = {
					'isSelect': isSelect['isSelect'],
					'type': isSelect['type']
				}
		if value['type'] == 'appkit.imageselection':
			for select,isSelect in value['value'].items():
				member_termite_imageselect[k+select] = {
					'isSelect': isSelect['isSelect'],
					'type': isSelect['type'],
					'image': isSelect['image'],
					'mt': isSelect['mt']
				}
		if value['type'] in['appkit.textlist', 'appkit.shortcuts']:
			member_termite_shortcuts[k] = value['value']
	questions =OrderedDict()
	result_list = []
	title_disp_type = {}

	#合并字典
	member_termite_select = dict(member_termite_select, **(dict(member_termite_textselect, **member_termite_imageselect)))

	for vote in votes:
		termite_data = vote.termite_data
		for title in sorted(termite_data.keys()):
			value = termite_data[title]
			if value['type'] in ['appkit.selection', 'appkit.imageselection', 'appkit.textselection']:
				if not questions.has_key(title):
					questions[title] = [value['value']]
				else:
					questions[title].append(value['value'])
				if value.has_key('display_type'):
					display_type = value['display_type']
					title_disp_type[title] = display_type #若title重复则会覆盖！！
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
			is_select =False
			v_title_index = 0
			for v_title in sorted(value.keys()):
				v_value = value[v_title]
				select_title = v_title.split('_')[1]
				if len(str(v_title_index))< 2:
					select_title = '0' + str(v_title_index) + select_title
				else:
					select_title = str(v_title_index) + select_title
				select_title_name = q_title+select_title

				if v_value:
					if not value_isSelect.has_key(select_title_name):
						value_isSelect[select_title_name] = 0
					if v_value['isSelect'] == True:
						value_isSelect[select_title_name] += 1
						is_select = True
				else:
					value_isSelect[select_title_name] = 0
				v_title_index += 1
			if is_select:
				total_count += 1
		timp_k_index = 0
		for timp_k in sorted(timp_vlaue.keys()):
			value ={}
			name = timp_k.split('_')[1]
			if len(str(timp_k_index))< 2:
				timp_title = '0' + str(timp_k_index) + name
			else:
				timp_title = str(timp_k_index) + name
			timp_title_name = q_title+timp_title
			value['name'] = name
			value['id_name'] = timp_title_name
			value['count'] = value_isSelect[timp_title_name]
			value['per'] =  '%d' % (value_isSelect[timp_title_name]*100/float(total_count) if total_count else 0)
			value['isSelect'] = member_termite_select[q_title+timp_k]['isSelect']
			value['type'] = member_termite_select[q_title+timp_k]['type']
			if member_termite_select[q_title+timp_k].has_key('image'):
				value['image'] = member_termite_select[q_title+timp_k]['image']
				value['mt'] = member_termite_select[q_title+timp_k]['mt']
			value_list.append(value)
			timp_k_index += 1
		title_name = q_title.split('_')[1]
		isShortcuts = False
		if title_name in SHORTCUTS_TEXT.keys():
			isShortcuts = True
			value_list = member_termite_shortcuts[q_title]
			title_name = SHORTCUTS_TEXT[title_name]
		result['title'] = title_name
		result['values'] = value_list
		if 'image' in value_list[0]:
			result['selectionType'] = 'image'
			result['display_type'] = title_disp_type.get(q_title, '')
		elif isShortcuts:
			result['selectionType'] = 'shortcuts'
		else:
			result['selectionType'] = 'text'
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