# -*- coding: utf-8 -*-

from datetime import datetime

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from core import resource
from core.jsonresponse import create_response
from utils.cache_util import GET_CACHE, SET_CACHE

import models as app_models
from termite2 import pagecreater



class Mscratch(resource.Resource):
	app = 'apps/scratch'
	resource = 'm_scratch'

	def get(request):
		"""
		响应GET
		"""
		id = request.GET['id']
		is_pc = request.GET.get('isPC', None)
		expend = 0
		auth_appid_info = None
		share_page_desc = ''
		thumbnails_url = '/static_v2/img/thumbnails_lottery.png'
		cache_key = 'apps_scratch_%s_html' % id
		record = None
		member = request.member
		if 'new_app:' in id:
			project_id = id
			activity_status = u"未开始"
		else:
			# if not is_pc:
			# 	#从redis缓存获取静态页面
			# 	cache_data = GET_CACHE(cache_key)
			# 	if cache_data:
			# 		print 'redis---return'
			# 		return HttpResponse(cache_data)

			try:
				record = app_models.Scratch.objects.get(id=id)
			except:
				c = RequestContext(request,{
					'is_deleted_data': True
				})
				return render_to_response('scratch/templates/webapp/m_scratch.html', c)

			expend = record.expend
			share_page_desc = record.name
			activity_status, record = update_scratch_status(record)
			project_id = 'new_app:scratch:%s' % record.related_page_id

		request.GET._mutable = True
		request.GET.update({"project_id": project_id})
		request.GET._mutable = False
		html = pagecreater.create_page(request, return_html_snippet=True)
		c = RequestContext(request, {
			'expend_integral': expend,
			'record_id': id,
			'activity_status': activity_status,
			'page_title': record.name if record else u'刮刮卡',
			'page_html_content': html,
			'app_name': "scratch",
			'resource': "scratch",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': True if is_pc else False,
			'auth_appid_info': auth_appid_info,
			'share_page_desc': share_page_desc,
			'share_img_url': thumbnails_url
		})
		response = render_to_string('scratch/templates/webapp/m_scratch.html', c)
		# if not is_pc:
		# 	SET_CACHE(cache_key, response)
		return HttpResponse(response)


	def api_get(request):
		"""
		响应GET
		"""
		record_id = request.GET.get('id',None)
		scratch_status = False
		can_play_count = 0
		member = request.member
		response = create_response(500)

		if not record_id or not member:
			response.errMsg = u'活动信息出错'
			return response.get_response()

		record = app_models.Scratch.objects(id=record_id)
		if record.count() <= 0:
			response.errMsg = 'is_deleted'
			return response.get_response()

		record = record.first()
		member_id = member.id
		isMember = member.is_subscribed
		activity_status, record = update_scratch_status(record)

		scratch_participance = app_models.ScratchParticipance.objects(belong_to=record_id, member_id=member_id)
		participance_data_count = scratch_participance.count()
		if participance_data_count != 0 and record.limitation_times != -1:
			scratch_participance = scratch_participance[0]
			total_count = scratch_participance.total_count
			#再次进入抽奖活动页面，根据抽奖规则限制以及当前日期和最近一次抽奖日期，更新can_play_count
			now_date_str = datetime.today().strftime('%Y-%m-%d')
			last_scratch_date_str = scratch_participance.scratch_date.strftime('%Y-%m-%d')
			if record.limitation == 'once_per_user' and total_count > 0:
				scratch_participance.update(set__can_play_count=0)
				can_play_count = 0
			if now_date_str != last_scratch_date_str:
				if record.limitation == 'once_per_day':
					scratch_participance.update(set__can_play_count=1)
					can_play_count = 1
				elif record.limitation == 'twice_per_day':
					scratch_participance.update(set__can_play_count=2)
					can_play_count = 2
			else:
				can_play_count = scratch_participance.can_play_count
			scratch_participance.reload()
		else:
			can_play_count = record.limitation_times
		if can_play_count != 0:
			scratch_status = True

		#会员信息
		member_info = {
			'isMember': isMember,
			'member_id': member_id,
			'remained_integral': member.integral,
			'activity_status': activity_status,
			'scratch_status': scratch_status if activity_status == u'进行中' else False,
			'can_play_count': can_play_count if scratch_status else 0
		}
		#历史中奖记录
		all_prize_type_list = ['integral', 'coupon', 'entity']
		scratches = app_models.ScratchRecord.objects(belong_to=record_id, member_id=member_id, prize_type__in=all_prize_type_list)

		scratch_history = [{
			'created_at': l.created_at.strftime('%Y-%m-%d'),
			'prize_name': l.prize_name,
			'prize_title': l.prize_title
		} for l in scratches]

		response = create_response(200)
		response.data = {
			'scratch_history': scratch_history,
			'member_info': member_info
		}
		return response.get_response()

def update_scratch_status(scratch):
	activity_status = scratch.status_text
	now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
	data_start_time = scratch.start_time.strftime('%Y-%m-%d %H:%M')
	data_end_time = scratch.end_time.strftime('%Y-%m-%d %H:%M')
	data_status = scratch.status
	if data_status <= 1:
		if data_start_time <= now_time and now_time < data_end_time:
			scratch.update(set__status=app_models.STATUS_RUNNING)
			activity_status = u'进行中'
		elif now_time >= data_end_time:
			scratch.update(set__status=app_models.STATUS_STOPED)
			activity_status = u'已结束'
		scratch.reload()
	return activity_status, scratch