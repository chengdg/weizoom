# -*- coding: utf-8 -*-
from collections import OrderedDict

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from apps.customerized_apps.vote.vote_statistic import get_vote_title_select_datas
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
				vote_detail,result_list = get_result(request,member_id)
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


# class resultVote(resource.Resource):
# 	app = 'apps/vote'
# 	resource = 'result_vote'
#
# 	def get(request):
# 		print request.GET
# 		if 'id' in request.GET:
# 			id = request.GET['id']
# 			isMember = request.GET.get('isMember',0)
# 			member_id = request.member.id
# 			auth_appid_info = None
# 			# if not isMember:
# 			# 	from weixin.user.util import get_component_info_from
# 			# 	component_info = get_component_info_from(request)
# 			# 	auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.GET['webapp_owner_id'])[0]
# 			# 	auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
# 			vote_detail,result_list = get_result(request,member_id)
# 			c = RequestContext(request, {
# 				'vote_detail': vote_detail,
# 				'record_id': id,
# 				'page_title': '微信投票',
# 				'app_name': "vote",
# 				'resource': "vote",
# 				'q_vote': result_list,
# 				'hide_non_member_cover': True, #非会员也可使用该页面
# 				'isMember': isMember,
# 				'auth_appid_info': auth_appid_info,
# 			})
# 			return render_to_response('vote/templates/webapp/result_vote.html', c)


def get_result(request,member_id):
	'''
	@param request:
	@param member_id: 会员的id
	member_vote_participance: 当前会员的投票信息
	title: 标题
	select_vlaue: 某标题的选项信息
	select_title_name: 选项名
	@return:
	'''
	id = request.GET['id']
	vote_detail ={}
	vote_vote = app_models.vote.objects.get(id=id)
	vote_detail['name'] = vote_vote['name']
	vote_detail['start_time'] = vote_vote['start_time'].strftime('%Y-%m-%d %H:%M')
	vote_detail['end_time'] = vote_vote['end_time'].strftime('%Y-%m-%d %H:%M')

	member_vote_participance = app_models.voteParticipance.objects.filter(belong_to=id,member_id=member_id).order_by('-created_at').first().termite_data
	member_termite_select = {}
	member_termite_shortcuts = {}
	for title,member_termite in member_vote_participance.items():
		if member_termite['type'] in ['appkit.selection','appkit.textselection','appkit.imageselection']:
			select_vlaue = member_termite['value']
			select_title_index = 0
			for select in sorted(select_vlaue.keys()):
				select_title = select.split('_')[1]
				if len(str(select_title_index))< 2:
					select_title = '0%s_%s' % (str(select_title_index), select_title)
				else:
					select_title = '%s_%s' % (str(select_title_index), select_title)
				select_title_name = title+select_title
				isSelect = select_vlaue[select]
				if member_termite['type'] in ['appkit.selection','appkit.textselection']:
					member_termite_select[select_title_name] = {
						'isSelect': isSelect['isSelect'],
						'type': isSelect['type']
					}
				else:
					member_termite_select[select_title_name] = {
						'isSelect': isSelect['isSelect'],
						'type': isSelect['type'],
						'image': isSelect['image'],
						'mt': isSelect['mt']
					}
				select_title_index += 1
		if member_termite['type'] in['appkit.textlist', 'appkit.shortcuts']:
			member_termite_shortcuts[title] = {
				'member_id': member_id,
				'value': member_termite['value']
			}

	vote_title_select_datas = get_vote_title_select_datas(request)

	#如果当前活动有参与人信息的填写项
	#将填写项合并到选项统计的list中
	if member_termite_shortcuts:
		for shortcut_title, shortcut_value in member_termite_shortcuts.items():
			vote_title_select_datas.append({
				'title_name': shortcut_title,
				'title_value': member_termite_shortcuts[shortcut_title]['value'],
				'selectionType': u'shortcuts'
			})
	#重新按title_name正序排序
	vote_title_select_datas = sorted(vote_title_select_datas, cmp=None, key=lambda vote_title_select_data:vote_title_select_data['title_name'], reverse=False)
	for data in vote_title_select_datas:
		title = data['title_name'].split('_')[1]
		if data.get('selectionType',None) == u'shortcuts':
			if SHORTCUTS_TEXT.has_key(title):
				title = SHORTCUTS_TEXT[title]

		data['title'] = title
		if type(data['title_value']) == list:
			for d in data['title_value']:
				d['name'] = d['item_name'].split('_')[1]
				d['isSelect'] = member_termite_select[data['title_name']+d['item_name']]['isSelect']
				if data['type'] == u'单选':
					d['type'] = u'radio'
				else:
					d['type'] = u'checkbox'
				if 'image' in d.keys():
					data['selectionType'] = 'image'
				else:
					data['selectionType'] = 'text'

				d['id_name'] = data['title_name']+d['item_name']


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

	return vote_detail,vote_title_select_datas