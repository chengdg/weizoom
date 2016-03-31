# -*- coding: utf-8 -*-

import json
from datetime import datetime
from core import dateutil
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
import time

from stats import export
from core import resource
from mall.models import Order, belong_to
from mall import models
from modules.member.models import Member, WebAppUser, SOURCE_SELF_SUB, SOURCE_MEMBER_QRCODE, SOURCE_BY_URL
from core.jsonresponse import create_response

import pandas as pd

FIRST_NAV = export.STATS_HOME_FIRST_NAV


class RepeatBuyAnalysis(resource.Resource):
	"""
	会员分析-复购分析
	"""
	app = 'stats'
	resource = 'repeat_buy_analysis'
	
	@login_required
	def get(request):
		"""
		显示复购分析页面
		"""
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'app_name': 'stats',
			'second_navs': export.get_stats_second_navs(request),
			'second_nav_name': export.STATS_MEMBER_SECOND_NAV,
			'third_nav_name': export.REPEAT_BUY_ANALISIS_NAV
		})
		
		return render_to_response('member/repeat_buy_analysis.html', c)


	@login_required
	def api_get(request):
		"""
		复购会员分析数据	
		"""

		tooltip = {
					'trigger': 'item',
					'formatter': '{b}</br>人数：{c}</br>占比：{d}%',
					'backgroundColor': '#FFFFFF',
					'textStyle': {'color': '#363636'},
					'borderWidth': 1,
					'borderColor': '#363636'
				}

		return create_pie_chart_response('',
				{
					u"消费金额：0-100": 213,
					u"消费金额：100-200": 76, 
					u"消费金额：200-500": 34, 
					u"其他": 21
				},
				tooltip
			)


class BuyPercent(resource.Resource):
	"""
	会员购买占比
	"""
	app = 'stats'
	resource = 'buy_percent'

	@login_required
	def api_get(request):
		"""
		会员购买占比数据	
		"""

		tooltip = {
					'trigger': 'item',
					'formatter': '{b}</br>人数：{c}</br>占比：{d}%',
					'backgroundColor': '#FFFFFF',
					'textStyle': {'color': '#363636'},
					'borderWidth': 1,
					'borderColor': '#363636'
				}

		return create_pie_chart_response('',
				{
					u"购买1次的会员": 13,
					u"购买2次的会员": 6, 
					u"购买3-5次的会员": 4, 
					u"购买5次以上的会员": 1
				}, 
				tooltip
			)