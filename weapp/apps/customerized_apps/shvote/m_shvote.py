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

		#获取已报名人数
		member_datas = app_models.ShvoteParticipance.objects(belong_to=record_id, status=app_models.MEMBER_STATUS['PASSED'])
		total_parted = member_datas.count()
		total_counts = member_datas.sum('count')
		total_visits = record.visits

		#获取当前会员可投票的次数(默认每人每天每组可投票一次)
		groups = record.groups
		group_name2member = {}
		for m in member_datas:
			if group_name2member.has_key(m.group):
				group_name2member[m.group].append(m.vote_log)
			else:
				group_name2member[m.group] = [m.vote_log]
		now_date_str = datetime.now().strftime('%Y-%m-%d')
		#判断当前会员每个组的可投票情况
		group_name2canplay = {}
		for g, log in group_name2member.items():
			if log.has_key(now_date_str) and member_id in log[now_date_str]:
				group_name2canplay[g] = True
			else:
				group_name2canplay[g] = False

		member_info = {
			'can_play_info': group_name2canplay,
			'isMember': isMember
		}
		record_info = {
			'total_parted': total_parted,
			'total_counts': total_counts,
			'total_visits': total_visits,
			'groups': groups
		}
		rank_info = get_rank_list(record_id) #获取排名信息

		response = create_response(200)
		response.data = {
			'activity_status': activity_status,
			'member_info': member_info,
			'record_info': record_info,
			'rank_info': rank_info
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
		if not isPC:
			isMember = request.member and request.member.is_subscribed
		if 'new_app:' in id:
			project_id = id
			activity_status = u"未开启"
		else:
			try:
				record = app_models.Shvote.objects.get(id=id)
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
			'page_title': record.name if record else u"投票",
			'page_html_content': html,
			'app_name': "shvote",
			'resource': "shvote",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': True if isPC else False,
			'isMember': isMember,
			'auth_appid_info': auth_appid_info,
			"share_page_desc": share_page_desc
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

def get_rank_list(record_id):
	"""
	获取排名信息，取前100名
	@param record_id: 活动id
	@return: list
	"""
	datas = app_models.ShvoteParticipance.objects(belong_to=record_id, status=app_models.MEMBER_STATUS['PASSED']).order_by('-count')[:100]
	i = 0
	result_list = []
	for data in datas:
		i += 1
		result_list.append({
			'rank': i,
			'name': data.name,
			'icon': data.icon,
			'count': data.count,
			'group': data.group,
			'serial_number': data.serial_number,
			'details': data.details,
			'pics': data.pics
		})
	return result_list

def left_pad(num):
	"""
	三位数，不够在左侧加0 ，例如 001，032，100
	@param str:
	@return:
	"""
	num = int(num)
	return num if num >= 100 else '0%d'%num if num >= 10 else '00%d'%num
