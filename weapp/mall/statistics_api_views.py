# -*- coding: utf-8 -*-
"""@package mall.statistics_api_views
统计模块的API的实现文件
"""

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import MySQLdb
import random
import string
import operator

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count

import models as mall_models
from models import *
from core import paginator
import export
from core.restful_url_route import *
from core import dateutil
from core.jsonresponse import create_response
from core import search_util
from core.charts_apis import *
from webapp import models as webapp_models
from webapp import statistics_util as webapp_statistics_util


@api(app='mall', resource='purchase_trend', action='get')
@login_required
def get_purchase_trend(request):
	days = request.GET['days']
	try:
		webapp_id = request.user_profile.webapp_id
		total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
		date_list = [date.strftime("%Y-%m-%d") for date in dateutil.get_date_range_list(low_date, high_date)]

		date2count = dict()
		date2price = dict()

		# 11.20从查询mall_purchase_daily_statistics变更为直接统计订单表，解决mall_purchase_daily_statistics遗漏统计订单与统计时间不一样导致的统计结果不同的问题。
		orders = Order.objects.belong_to(webapp_id).filter(created_at__range=(low_date, (high_date+timedelta(days=1))))
		statuses = set([ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED])
		orders = [order for order in orders if (order.type != 'test') and (order.status in statuses)]
		for order in orders:
			# date = dateutil.normalize_date(order.created_at)
			date = order.created_at.strftime("%Y-%m-%d")
			if order.webapp_id != webapp_id:
				order_price =  Order.get_order_has_price_number(order) + order.postage
			else:
				order_price = order.final_price + order.weizoom_card_money

			if date in date2count:
				old_count = date2count[date]
				date2count[date] = old_count + 1
			else:
				date2count[date] = 1

			if date in date2price:
				old_price = date2price[date]
				date2price[date] = old_price + order_price
			else:
				date2price[date] = order_price

		count_trend_values = []
		price_trend_values = []
		for date in date_list:
			count_trend_values.append(date2count.get(date, 0))
			price_trend_values.append(date2price.get(date, 0.0))

		return create_line_chart_response(
				'',
				'',
				date_list,
				[{
		            "name": "订单数",
		            "values" : count_trend_values
		        }, {
		            "name": "销售额",
		            "values" : price_trend_values
		        }]
			)
	except:
		if settings.DEBUG:
			raise
		else:
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()
			return response.get_response()


def _update_visit_today_daily_statistics(webapp_id):
	"""
	更新今天的pv，uv统计

	如果settings.IS_UPDATE_PV_UV_REALTIME为True，则每次都会删除今天的统计数据，重新进行统计
	"""
	if not settings.IS_UPDATE_PV_UV_REALTIME:
		return

	#先删除当天的pv,uv统计结果，然后重新进行统计
	today = dateutil.get_today()
	webapp_models.PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id, data_date=today).delete()
	webapp_statistics_util.count_visit_daily_pv_uv(webapp_id, today)


@api(app='mall', resource='visit_daily_trend', action="get")
@login_required
def get_visit_daily_trend(request):
	"""
	获得每日pv、uv统计
	"""
	days = request.GET['days']
	webapp_id = request.user_profile.webapp_id

	#对当天的统计结果进行更新
	_update_visit_today_daily_statistics(webapp_id)

	total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
	statisticses = webapp_models.PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id, url_type=webapp_models.URL_TYPE_ALL, data_date__range=(low_date, high_date))
	date_list = [date.strftime("%Y-%m-%d") for date in dateutil.get_date_range_list(low_date, high_date)]

	date2pv = dict([(s.data_date.strftime('%Y-%m-%d'), s.pv_count) for s in statisticses])
	date2uv = dict([(s.data_date.strftime('%Y-%m-%d'), s.uv_count) for s in statisticses])

	pv_trend_values = []
	uv_trend_values = []
	for date in date_list:
		pv_trend_values.append(date2pv.get(date, 0))
		uv_trend_values.append(date2uv.get(date, 0))

	return create_line_chart_response(
		'',
		'',
		date_list,
		[{
            "name": "PV",
            "values" : pv_trend_values
        }, {
            "name": "UV",
            "values" : uv_trend_values
        }]
	)