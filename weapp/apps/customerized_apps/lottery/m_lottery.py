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



class Mlottery(resource.Resource):
	app = 'apps/lottery'
	resource = 'm_lottery'

	def get(request):
		"""
		响应GET
		"""
		id = request.GET['id']
		expend = 0
		auth_appid_info = None
		share_page_desc = ''
		thumbnails_url = '/static_v2/img/thumbnails_lottery.png'
		record = None
		member = request.member
		if 'new_app:' in id:
			project_id = id
			activity_status = u"未开始"
		else:
			cache_key = 'apps_lottery_%s_html' % id
			#从redis缓存获取静态页面
			cache_data = GET_CACHE(cache_key)
			if cache_data:
				print 'redis---return'
				return HttpResponse(cache_data)

			try:
				record = app_models.lottery.objects.get(id=id)
			except:
				c = RequestContext(request,{
					'is_deleted_data': True
				})
				return render_to_response('lottery/templates/webapp/m_lottery.html', c)

			expend = record.expend
			share_page_desc = record.name
			activity_status, record = update_lottery_status(record)
			project_id = 'new_app:lottery:%s' % record.related_page_id

		request.GET._mutable = True
		request.GET.update({"project_id": project_id})
		request.GET._mutable = False
		html = pagecreater.create_page(request, return_html_snippet=True)
		c = RequestContext(request, {
			'expend_integral': expend,
			'record_id': id,
			'activity_status': activity_status,
			'page_title': record.name if record else u'微信抽奖',
			'page_html_content': html,
			'app_name': "lottery",
			'resource': "lottery",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': False if member else True,
			'auth_appid_info': auth_appid_info,
			'share_page_desc': share_page_desc,
			'share_img_url': thumbnails_url
		})
		response = render_to_string('lottery/templates/webapp/m_lottery.html', c)
		if member:
			SET_CACHE(cache_key, response)
		return HttpResponse(response)


	def api_get(request):
		"""
		响应GET
		"""
		record_id = request.GET.get('id',None)
		participance_data_count = 0
		has_prize = False
		lottery_status = False
		can_play_count = 0
		member = request.member

		response = create_response(500)

		if not record_id or not member:
			response.errMsg = u'活动信息出错'
			return response.get_response()

		record = app_models.lottery.objects(id=record_id)
		if record.count() <= 0:
			response.errMsg = 'is_deleted'
			return response.get_response()

		record = record.first()
		member_id = member.id
		isMember = member.is_subscribed
		activity_status, record = update_lottery_status(record)

		lottery_participance = app_models.lotteryParticipance.objects(belong_to=record_id, member_id=member_id)
		participance_data_count = lottery_participance.count()
		if participance_data_count != 0 and record.limitation_times != -1:
			lottery_participance = lottery_participance[0]
			total_count = lottery_participance.total_count
			#再次进入抽奖活动页面，根据抽奖规则限制以及当前日期和最近一次抽奖日期，更新can_play_count
			now_date_str = datetime.today().strftime('%Y-%m-%d')
			last_lottery_date_str = lottery_participance.lottery_date.strftime('%Y-%m-%d')
			if record.limitation == 'once_per_user' and total_count > 0:
				lottery_participance.update(set__can_play_count=0)
				can_play_count = 0
			if now_date_str != last_lottery_date_str:
				if record.limitation == 'once_per_day':
					lottery_participance.update(set__can_play_count=1)
					can_play_count = 1
				elif record.limitation == 'twice_per_day':
					lottery_participance.update(set__can_play_count=2)
					can_play_count = 2
			else:
				can_play_count = lottery_participance.can_play_count
			lottery_participance.reload()
		else:
			can_play_count = record.limitation_times
		if can_play_count != 0:
			lottery_status = True

		#会员信息
		member_info = {
			'isMember': isMember,
			'member_id': member_id,
			'remained_integral': member.integral,
			'activity_status': activity_status,
			'lottery_status': lottery_status if activity_status == u'进行中' else False,
			'can_play_count': can_play_count if lottery_status else 0
		}
		#历史中奖记录
		all_prize_type_list = ['integral', 'coupon', 'entity']
		lotteries = app_models.lottoryRecord.objects(belong_to=record_id, member_id=member_id, prize_type__in=all_prize_type_list)

		lottery_history = [{
			'created_at': l.created_at.strftime('%Y-%m-%d'),
			'prize_name': l.prize_name,
			'prize_title': l.prize_title
		} for l in lotteries]

		response = create_response(200)
		response.data = {
			'lottery_history': lottery_history,
			'member_info': member_info
		}
		return response.get_response()

def update_lottery_status(lottery):
	activity_status = lottery.status_text
	now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
	data_start_time = lottery.start_time.strftime('%Y-%m-%d %H:%M')
	data_end_time = lottery.end_time.strftime('%Y-%m-%d %H:%M')
	data_status = lottery.status
	if data_status <= 1:
		if data_start_time <= now_time and now_time < data_end_time:
			lottery.update(set__status=app_models.STATUS_RUNNING)
			activity_status = u'进行中'
		elif now_time >= data_end_time:
			lottery.update(set__status=app_models.STATUS_STOPED)
			activity_status = u'已结束'
		lottery.reload()
	return activity_status, lottery