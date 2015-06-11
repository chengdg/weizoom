# -*- coding: utf-8 -*-

__author__ = 'chuter'

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db import connection
from django.db.models import Count

from core.jsonresponse import JsonResponse
from core import chartutil, dateutil, apiview_util
from models import *

from statistics_util import *
from mall.models import *

def _count_visit_yestoday_daily_pv_uv(webapp_id):
	yestoday = dateutil.get_previous_date('today', 1)
	yestoday_records = PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id, data_date=yestoday)
	if yestoday_records.count() > 0:
		return

	#对昨天的pv和uv进行统计
	count_visit_daily_pv_uv(webapp_id, yestoday)

def _update_visit_today_daily_statistics(webapp_id):
	if not settings.IS_UPDATE_PV_UV_REALTIME:
		return

	#先删除当天的pv,uv统计结果，然后重新进行统计
	today = dateutil.get_today()
	PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id, data_date=today).delete()
	count_visit_daily_pv_uv(webapp_id, today)

#===============================================================================
# get_visit_daily_trend : 获得PV和UV的每日趋势
#===============================================================================
@login_required
def get_visit_daily_trend(request):
	webapp_id = request.user_profile.webapp_id

	#先对昨天的数据进行统计
	#_count_visit_yestoday_daily_pv_uv(webapp_id)
	#对当天的统计结果进行更新
	_update_visit_today_daily_statistics(webapp_id)

	days = request.GET['days']

	total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
	statisticses = PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id, url_type=URL_TYPE_ALL, data_date__range=(low_date, high_date))

	date2pv = dict([(s.data_date.strftime('%Y-%m-%d'), s.pv_count) for s in statisticses])
	date2uv = dict([(s.data_date.strftime('%Y-%m-%d'), s.uv_count) for s in statisticses])

	date_list = dateutil.get_date_range_list(low_date, high_date)

	pv_trend_values = []
	uv_trend_values = []
	for loop_date in date_list:
		date = loop_date.strftime('%Y-%m-%d')
		x = (loop_date - low_date).days

		pv_trend_values.append({
			'x': x,
			'y': date2pv.get(date, 0)
		})
		uv_trend_values.append({
			'x': x,
			'y': date2uv.get(date, 0)
		})

	if len(pv_trend_values) == 0:
		values = []
	else:
		values = [{'title':u'PV数', 'values':pv_trend_values}, {'title':u'UV数', 'values':uv_trend_values}]

	infos = {
		'title': '',
	    'values': values,
	    'date_info': {'days':total_days, 'low_date':low_date}
	}

	line_chart_json = chartutil.create_line_chart(infos, display_today_data=settings.IS_UPDATE_PV_UV_REALTIME)

	return HttpResponse(line_chart_json, 'application/json')


#===============================================================================
# get_buy_trend : 获得购买量趋势
#===============================================================================
def get_buy_trend(request):
	days = request.GET['days']
	webapp_id = request.user_profile.webapp_id
	total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
	date_list = dateutil.get_date_range_list(low_date, high_date)

	date2count = dict()
	date2price = dict()

	# 11.20从查询mall_purchase_daily_statistics变更为直接统计订单表，解决mall_purchase_daily_statistics遗漏统计订单与统计时间不一样导致的统计结果不同的问题。
	orders = Order.objects.belong_to(webapp_id).filter(created_at__range=(low_date, (high_date+timedelta(days=1))), status__gte=2)


	for order in orders:
		date = dateutil.normalize_date(order.created_at)
		date = order.created_at.strftime("%Y-%m-%d")
		if order.webapp_id != webapp_id:
			order_price =  Order.get_order_has_price_number(order) + order.postage
		else:
			order_price = order.final_price

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
	for loop_date in date_list:
		date = loop_date.strftime('%Y-%m-%d')
		x = (loop_date - low_date).days
		count_trend_values.append({
			'x': x,
			'y': date2count.get(date, 0)
		})
		price_trend_values.append({
			'x': x,
			'y': date2price.get(date, 0)
		})

	if len(count_trend_values) == 0:
		values = []
	else:
		values = [{'title':u'订单数', 'values':count_trend_values}, {'title':u'销售额', 'values':price_trend_values}]

	infos = {
		'title': '',
	    'values': values,
	    'date_info': {'days':total_days, 'low_date':low_date}
	}

	line_chart_json = chartutil.create_line_chart(infos, display_today_data=True)

	return HttpResponse(line_chart_json, 'application/json')


#===============================================================================
# call_statistics : 统计函数的入口函数
#===============================================================================
@login_required
def call_statistics(request):
	statistics_function = apiview_util.get_api_function(request, globals())
	return statistics_function(request)

import views as webapp_views
