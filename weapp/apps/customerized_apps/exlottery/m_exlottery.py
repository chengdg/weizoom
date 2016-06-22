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



class Mexlottery(resource.Resource):
	app = 'apps/exlottery'
	resource = 'm_exlottery'

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
		cache_key = 'apps_lottery_%s_html' % id
		record = None
		member = request.member
		if 'new_app:' in id:
			project_id = id
			activity_status = u"未开始"
		else:
			if not is_pc:
				#从redis缓存获取静态页面
				cache_data = GET_CACHE(cache_key)
				if cache_data:
					print 'redis---return'
					return HttpResponse(cache_data)

			try:
				record = app_models.Exlottery.objects.get(id=id)
			except:
				c = RequestContext(request,{
					'is_deleted_data': True
				})
				return render_to_response('exlottery/templates/webapp/m_exlottery.html', c)
			expend = record.expend
			share_page_desc = record.share_description
			activity_status, record = update_exlottery_status(record)
			project_id = 'new_app:exlottery:%s' % record.related_page_id

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
			'isPC': True if is_pc else False,
			'auth_appid_info': auth_appid_info,
			'share_page_desc': share_page_desc,
			'share_img_url': thumbnails_url
		})
		response = render_to_string('exlottery/templates/webapp/m_exlottery.html', c)
		if not is_pc:
			SET_CACHE(cache_key, response)
		return HttpResponse(response)


	def api_get(request):
		"""
		响应GET
		"""
		record_id = request.GET.get('id',None)
		exlottery_status = False
		can_play_count = 0
		member = request.member
		response = create_response(500)

		if not record_id or not member:
			response.errMsg = u'活动信息出错'
			return response.get_response()

		record = app_models.Exlottery.objects(id=record_id)
		if record.count() <= 0:
			response.errMsg = 'is_deleted'
			return response.get_response()

		record = record.first()
		member_id = member.id
		isMember = member.is_subscribed
		activity_status, record = update_exlottery_status(record)

		exlottery_participance = app_models.ExlotteryParticipance.objects(belong_to=record_id, member_id=member_id)
		participance_data_count = exlottery_participance.count()
		if participance_data_count != 0 and record.limitation_times != -1:
			exlottery_participance = exlottery_participance[0]
			total_count = exlottery_participance.total_count
			#再次进入抽奖活动页面，根据抽奖规则限制以及当前日期和最近一次抽奖日期，更新can_play_count
			now_date_str = datetime.today().strftime('%Y-%m-%d')
			last_exlottery_date_str = exlottery_participance.exlottery_date.strftime('%Y-%m-%d')
			if record.limitation == 'once_per_user' and total_count > 0:
				exlottery_participance.update(set__can_play_count=0)
				can_play_count = 0
			if now_date_str != last_exlottery_date_str:
				if record.limitation == 'once_per_day':
					exlottery_participance.update(set__can_play_count=1)
					can_play_count = 1
				elif record.limitation == 'twice_per_day':
					exlottery_participance.update(set__can_play_count=2)
					can_play_count = 2
			else:
				can_play_count = exlottery_participance.can_play_count
			exlottery_participance.reload()
		else:
			can_play_count = record.limitation_times
		if can_play_count != 0:
			exlottery_status = True

		#会员信息
		member_info = {
			'isMember': isMember,
			'member_id': member_id,
			'remained_integral': member.integral,
			'activity_status': activity_status,
			'exlottery_status': exlottery_status if activity_status == u'进行中' else False,
			'can_play_count': can_play_count if exlottery_status else 0
		}
		#历史中奖记录
		all_prize_type_list = ['integral', 'coupon', 'entity']
		exlotteries = app_models.ExlottoryRecord.objects(belong_to=record_id, member_id=member_id, prize_type__in=all_prize_type_list)

		exlottery_history = [{
			'created_at': l.created_at.strftime('%Y-%m-%d'),
			'prize_name': l.prize_name,
			'prize_title': l.prize_title
		} for l in exlotteries]

		response = create_response(200)
		response.data = {
			'exlottery_history': exlottery_history,
			'member_info': member_info
		}
		return response.get_response()

def update_exlottery_status(lottery):
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