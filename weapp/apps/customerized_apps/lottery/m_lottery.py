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

class Mlottery(resource.Resource):
	app = 'apps/lottery'
	resource = 'm_lottery'
	
	def get(request):
		"""
		响应GET
		"""
		id = request.GET['id']
		participance_data_count = 0
		isPC = request.GET.get('isPC', 0)
		has_prize = False
		lottery_status = False
		can_play_count = 0
		expend = 0
		isMember = False
		auth_appid_info = None
		share_page_desc = ''
		thumbnails_url = '/static_v2/img/thumbnails_lottery.png'
		if not isPC:
			isMember = request.member and request.member.is_subscribed
			if not isMember:
				from weixin.user.util import get_component_info_from
				component_info = get_component_info_from(request)
				auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.GET['webapp_owner_id'])[0]
				auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
		if 'new_app:' in id:
			project_id = id
			activity_status = u"未开始"
		else:
			#termite类型数据
			record = app_models.lottery.objects.get(id=id)
			expend = record.expend
			activity_status = record.status_text
			share_page_desc = record.name
			now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
			data_start_time = record.start_time.strftime('%Y-%m-%d %H:%M')
			data_end_time = record.end_time.strftime('%Y-%m-%d %H:%M')
			data_status = record.status
			if data_status <= 1:
				if data_start_time <= now_time and now_time < data_end_time:
					record.update(set__status=app_models.STATUS_RUNNING)
					activity_status = u'进行中'
				elif now_time >= data_end_time:
					record.update(set__status=app_models.STATUS_STOPED)
					activity_status = u'已结束'
				record.reload()
			project_id = 'new_app:lottery:%s' % record.related_page_id
			if request.member:
				lottery_participance = app_models.lotteryParticipance.objects(belong_to=id, member_id=request.member.id)
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
					# if record.limitation in ['once_per_day', 'once_per_user']:
					# 	can_play_count = 1
					# elif record.limitation == 'twice_per_day':
					# 	can_play_count = 2
					# elif record.limitation == 'no_limit':
					# 	can_play_count = -1
					# else:
					# 	can_play_count = 0
					can_play_count = record.limitation_times
		if can_play_count != 0:
			lottery_status = True

		request.GET._mutable = True
		request.GET.update({"project_id": project_id})
		request.GET._mutable = False
		html = pagecreater.create_page(request, return_html_snippet=True)
		c = RequestContext(request, {
			'lottery_status': lottery_status if activity_status == u'进行中' else False,
			'can_play_count': can_play_count if lottery_status else 0,
			'expend_integral': expend,
			'record_id': id,
			'activity_status': activity_status,
			'is_already_participanted': (participance_data_count > 0),
			'page_title': u'微信抽奖',
			'page_html_content': html,
			'app_name': "lottery",
			'resource': "lottery",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': isPC,
			'isMember': isMember,
			'auth_appid_info': auth_appid_info,
			'share_page_desc': share_page_desc,
			'share_img_url': thumbnails_url
		})
		return render_to_response('lottery/templates/webapp/m_lottery.html', c)

