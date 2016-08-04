# -*- coding: utf-8 -*-
from django.conf import settings
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
from modules.member.module_api import get_member_by_openid



class Mexlottery(resource.Resource):
	app = 'apps/scanlottery'
	resource = 'm_scanlottery'

	def get(request):
		"""
		响应GET
		"""
		id = request.GET['id']
		code = request.GET.get('ex_code', None)
		# expend = 0
		auth_appid_info = None
		share_page_desc = ''
		thumbnails_url = '/static_v2/img/thumbnails_lottery.png'
		cache_key = 'apps_scanlottery_%s_html' % id
		record = None
		member = request.member
		is_pc = False if member else True

		# if not is_pc:
		# 	#从redis缓存获取静态页面
		# 	cache_data = GET_CACHE(cache_key)
		# 	if cache_data:
		# 		print 'redis---return'
		# 		return HttpResponse(cache_data)

		try:
			record = app_models.Scanlottery.objects.get(id=id)
			scanlottery_bg_image = record.scanlottery_bg_image
		except:
			c = RequestContext(request,{
				'is_deleted_data': True
			})
			return render_to_response('exlottery/templates/webapp/m_exlottery.html', c)
		# expend = record.expend
		share_page_desc = record.share_description
		activity_status, record = update_scanlottery_status(record)

		project_id = 'new_app:exlottery:%s' % record.related_page_id

		request.GET._mutable = True
		request.GET.update({"project_id": project_id})
		request.GET._mutable = False
		html = pagecreater.create_page(request, return_html_snippet=True)
		c = RequestContext(request, {
			# 'expend_integral': expend,
			'record_id': id,
			'activity_status': activity_status,
			'page_title': record.name if record else u'幸运码抽奖',
			'page_html_content': html,
			'app_name': "scanlottery",
			'resource': "scanlottery",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': is_pc,
			'auth_appid_info': auth_appid_info,
			'share_page_desc': share_page_desc,
			'share_img_url': scanlottery_bg_image if scanlottery_bg_image else thumbnails_url,
			'code': code
		})
		response = render_to_string('exlottery/templates/webapp/m_exlottery.html', c)
		# if not is_pc:
		# 	SET_CACHE(cache_key, response)
		return HttpResponse(response)


	def api_get(request):
		"""
		响应GET
		"""
		record_id = request.GET.get('id',None)
		scanlottery_status = False

		member = request.member
		code = request.GET.get('ex_code',None)
		response = create_response(500)

		if not record_id or not member:
			response.errMsg = u'活动信息出错'
			return response.get_response()

		record = app_models.Scanlottery.objects(id=record_id)
		if record.count() <= 0:
			response.errMsg = 'is_deleted'
			return response.get_response()

		record = record.first()
		member_id = member.id
		isMember = member.is_subscribed
		activity_status, record = update_scanlottery_status(record)

		can_play_count = 0
		is_member_self = True

		#首先验证抽奖码有没有和本会员绑定
		member_has_code = app_models.ScanlotteryParticipance.objects(code=code, belong_to=record_id,member_id=member_id)
		if member_has_code.count() == 1:
			# 非会员不可参与
			if isMember:
				# 如果绑定，验证抽奖码有没有抽奖
				if member_has_code.first().status == app_models.NOT_USED:
					can_play_count = 1
		#分享处理(如果分享出去，别人访问页面is_member_self为false)
		elif member_has_code.count() == 0:
			is_member_self = False

		if can_play_count != 0:
			scanlottery_status = True

		#会员信息
		member_info = {
			'isMember': isMember,
			'member_id': member_id,
			# 'remained_integral': member.integral,
			'activity_status': activity_status,
			'exlottery_status': scanlottery_status if activity_status == u'进行中' else False,
			'can_play_count': can_play_count if scanlottery_status else 0,
			'is_member_self': is_member_self
		}
		#历史中奖记录
		all_prize_type_list = ['integral', 'coupon', 'entity']
		exlotteries = app_models.ScanlottoryRecord.objects(belong_to=record_id, member_id=member_id, prize_type__in=all_prize_type_list)

		scanlottery_history = [{
			'created_at': l.created_at.strftime('%Y-%m-%d'),
			'prize_name': l.prize_name,
			'prize_title': l.prize_title
		} for l in exlotteries]

		response = create_response(200)
		response.data = {
			'scanlottery_history': scanlottery_history,
			'member_info': member_info
		}
		return response.get_response()

def update_scanlottery_status(lottery):
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