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

	def api_get(request):
		"""
		加载动态数据
		"""
		record_id = request.GET.get('recordId', None)
		member = request.member
		response = create_response(500)
		if not record_id or not member:
			response.errMsg = u'活动信息出错'
			return response.get_response()

		record = app_models.Shvote.objects(id=record_id)
		if record.count() <= 0:
			response.errMsg = 'is_deleted'
			return response.get_response()

		record = record.first()
		member_id = member.id
		isMember = member.is_subscribed
		activity_status, record = update_shvote_status(record)
		votecount_per_one = record.votecount_per_one

		#增加访问数
		record.visits += 1
		record.save()

		#获取已报名人数
		member_datas = app_models.ShvoteParticipance.objects(belong_to=record_id, status=app_models.MEMBER_STATUS['PASSED'])
		total_parted = member_datas.count()
		total_counts = member_datas.aggregate_sum('count')
		total_visits = record.visits

		#获取当前会员可投票的次数(默认每人每天可投票次数)
		groups = record.groups
		control = app_models.ShvoteControl.objects(member_id=member_id, belong_to=record_id, created_at_str=datetime.now().strftime('%Y-%m-%d'))
		if control.count() > 0:
			can_vote_count = votecount_per_one - control.first().vote_count
		else:
			can_vote_count = votecount_per_one
		member_info = {
			'can_play_info': can_vote_count,
			'isMember': isMember
		}
		record_info = {
			'total_parted': total_parted,
			'total_counts': total_counts,
			'total_visits': total_visits,
			'groups': groups,
			'end_date': record.end_time.strftime('%Y-%m-%d')
		}

		response = create_response(200)
		response.data = {
			'activity_status': activity_status,
			'member_info': member_info,
			'record_info': record_info
		}
		return response.get_response()

	def get(request):
		"""
		响应GET
		"""
		id = request.GET['id']
		isPC = request.GET.get('isPC',0)
		isMember = False
		share_page_desc = ""
		auth_appid_info = None
		record = None
		recordName = ""
		mpUserPreviewName = None
		if not isPC:
			isMember = request.member and request.member.is_subscribed
		if 'new_app:' in id:
			project_id = id
			activity_status = u"未开启"
		else:
			try:
				record = app_models.Shvote.objects.get(id=id)
				recordName = record.name
				#获取公众号昵称
				mpUserPreviewName = request.webapp_owner_info.auth_appid_info.nick_name
			except:
				c = RequestContext(request,{
					'is_deleted_data': True
				})
				return render_to_response('shvote/templates/webapp/m_shvote.html', c)

			activity_status, record = update_shvote_status(record)
			share_page_desc = record.name
			project_id = 'new_app:shvote:%s' % record.related_page_id

		request.GET._mutable = True
		request.GET.update({"project_id": project_id})
		request.GET._mutable = False
		html = pagecreater.create_page(request, return_html_snippet=True)

		c = RequestContext(request, {
			'record_id': id,
			'activity_status': activity_status,
			'page_title': u"投票活动",
			'page_html_content': html,
			'app_name': "shvote",
			'resource': "shvote",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': True if isPC else False,
			'isMember': isMember,
			'auth_appid_info': auth_appid_info,
			'share_page_title': mpUserPreviewName if mpUserPreviewName else recordName,
			'share_img_url': record.share_image if record else '',
			"share_page_desc": share_page_desc,
			"groups": record.groups if record else []
		})

		return render_to_response('shvote/templates/webapp/m_shvote.html', c)

def update_shvote_status(shvote):
	activity_status = shvote.status_text
	now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
	data_start_time = shvote.start_time.strftime('%Y-%m-%d %H:%M')
	data_end_time = shvote.end_time.strftime('%Y-%m-%d %H:%M')
	data_status = shvote.status
	if data_status <= 1:
		if data_start_time <= now_time and now_time < data_end_time:
			shvote.update(set__status=app_models.STATUS_RUNNING)
			activity_status = u'进行中'
		elif now_time >= data_end_time:
			shvote.update(set__status=app_models.STATUS_STOPED)
			activity_status = u'已结束'
		shvote.reload()
	return activity_status, shvote

def left_pad(num):
	"""
	三位数，不够在左侧加0 ，例如 001，032，100
	@param str:
	@return:
	"""
	num = int(num)
	return num if num >= 100 else '0%d'%num if num >= 10 else '00%d'%num


class GetRankList(resource.Resource):
	app = 'apps/shvote'
	resource = 'get_rank_list'

	def api_get(request):
		"""
		获取排名信息，取前100名
		@param record_id: 活动id
		@return: list
		"""
		response = create_response(200)
		response.data = {
			'result_list': get_rank_data(request.GET)
		}
		return response.get_response()

class MShvoteRank(resource.Resource):
	app = 'apps/shvote'
	resource = 'm_shvote_rank'

	def get(request):
		shvote = mpUserPreviewName = None
		try:
			shvote = app_models.Shvote.objects.get(id=request.GET["id"])
			#获取公众号昵称
			mpUserPreviewName = request.webapp_owner_info.auth_appid_info.nick_name
		except:
			pass
		c = RequestContext(request, {
			'share_page_title': mpUserPreviewName if mpUserPreviewName else shvote.name,
			'share_img_url': shvote.share_image if shvote else '',
			"share_page_desc": shvote.name if shvote else '',
			"groups": shvote.groups if shvote else [],
			"record_id": request.GET["id"]
		})

		return render_to_response('shvote/templates/webapp/m_shvote_rank.html', c)

	def api_get(request):
		"""
		列表排名
		@return:
		"""
		response = create_response(200)
		response.data = {
			'result_list': get_rank_data(request.GET)
		}
		return response.get_response()

def get_rank_data(data):
	"""
	查询前100排名
	@param params:
	@return:
	"""
	params = {
		'belong_to' : data['recordId'],
		'status' : app_models.MEMBER_STATUS['PASSED']
	}

	if data['current_group'] != '':
		params['group'] = data['current_group']

	if data.get('search_name') != '':
		search_name = data.get('search_name')
		if search_name.isdigit():
			params['serial_number__icontains'] = search_name
		else:
			params['name__icontains'] = search_name
	datas = app_models.ShvoteParticipance.objects(**params).order_by('-count', 'created_at')[:100]
	i = 0
	result_list = []
	for d in datas:
		i += 1
		result_list.append({
			'rank': i,
			'name': d.name,
			'icon': d.icon,
			'count': d.count,
			'group': d.group,
			'serial_number': d.serial_number,
			'member_id': d.member_id,
			'details': d.details,
			'pics': d.pics,
			'id': str(d.id)
		})
	return result_list

class MShvotePlayerDetails(resource.Resource):
	app = 'apps/shvote'
	resource = 'm_player_details'

	def get(request):
		player_id = request.GET['player_id'] 
		id = request.GET['id'] 
		player_details = {}
		record = None
		mpUserPreviewName = None
		isPC = request.GET.get('isPC',0)
		isMember = False
		share_page_desc = ""
		can_vote_count = 0
		member = request.member
		member_id = member.id
		if not isPC:
			isMember = request.member and request.member.is_subscribed
		if 'new_app:' in id:
			project_id = id
			activity_status = u"未开启"
		else:
			try:
				record = app_models.Shvote.objects.get(id=id)
				#获取公众号昵称
				mpUserPreviewName = request.webapp_owner_info.auth_appid_info.nick_name
				votecount_per_one = record.votecount_per_one
				control = app_models.ShvoteControl.objects(member_id=member_id, belong_to=id, created_at_str=datetime.now().strftime('%Y-%m-%d'))
				if control.count() > 0:
					can_vote_count = votecount_per_one - control.first().vote_count
				else:
					can_vote_count = votecount_per_one
			except:
				c = RequestContext(request,{
					'is_deleted_data': True
				})
				return render_to_response('shvote/templates/webapp/m_player_details.html', c)

			activity_status, record = update_shvote_status(record)
			share_page_desc = record.name

		if player_id:
			try:
				player_details = app_models.ShvoteParticipance.objects().get(id = player_id)
			except:
				pass

		c = RequestContext(request, {
			'record_id': id,
			'player_details': player_details,
			'activity_status': activity_status,
			'page_title': u"投票活动",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': True if isPC else False,
			'isMember': isMember,
			"can_vote_count": can_vote_count,
			'share_page_title': mpUserPreviewName if mpUserPreviewName else record.name,
			'share_img_url': record.share_image if record else '',
			"share_page_desc": share_page_desc,
		})

		return render_to_response('shvote/templates/webapp/m_player_details.html', c)