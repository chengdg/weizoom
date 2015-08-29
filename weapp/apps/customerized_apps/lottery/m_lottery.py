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

class Mlottery(resource.Resource):
	app = 'apps/lottery'
	resource = 'm_lottery'
	
	def get(request):
		"""
		响应GET
		"""
		id = request.GET['id']
		participance_data_count = 0
		has_prize = False
		lottery_status = False
		can_play_count = 0
		expend = 0
		if 'new_app:' in id:
			project_id = id
			activity_status = u"未开始"
		else:
			#termite类型数据
			record = app_models.lottery.objects.get(id=id)
			expend = record.expend
			activity_status = record.status_text

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

			project_id = 'new_app:lottery:%s' % record.related_page_id
			if request.member:
				lottery_participance = app_models.lotteryParticipance.objects(belong_to=id, member_id=request.member.id)
				participance_data_count = lottery_participance.count()

				if participance_data_count != 0:
					lottery_participance = lottery_participance[0]
					has_prize = lottery_participance.has_prize
					#再次进入抽奖活动页面，根据抽奖规则限制以及当前日期和最近一次抽奖日期，更新can_play_count
					now_date_str = datetime.today().strftime('%Y-%m-%d')
					last_lottery_date_str = lottery_participance.lottery_date.strftime('%Y-%m-%d')
					if now_date_str != last_lottery_date_str:
						if record.limitation == 'once_per_day':
							lottery_participance.update(set__can_play_count=1)
							can_play_count = 1
						elif record.limitation == 'twice_per_day':
							lottery_participance.update(set__can_play_count=2)
							can_play_count = 2
				else:
					can_play_count = 1

				lottery_limitation = record.limitation_times
				print lottery_limitation
				if not lottery_participance or lottery_participance.can_play_count >= lottery_limitation:
					lottery_status = True

		request.GET._mutable = True
		request.GET.update({"project_id": project_id})
		request.GET._mutable = False
		html = pagecreater.create_page(request, return_html_snippet=True)
		c = RequestContext(request, {
			'lottery_status': lottery_status,
			'can_play_count': can_play_count if lottery_status else 0,
			'expend_integral': expend,
			'record_id': id,
			'activity_status': activity_status,
			'is_already_participanted': (participance_data_count > 0),
			'page_title': '用户调研',
			'page_html_content': html,
			'app_name': "lottery",
			'resource': "lottery",
			'hide_non_member_cover': True #非会员也可使用该页面
		})

		return render_to_response('lottery/templates/webapp/m_lottery.html', c)

