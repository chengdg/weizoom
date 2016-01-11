# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

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
from core import chartutil, dateutil
from models import *


#===============================================================================
# get_new_weixin_user_daily_trend : 获得新增用户的每日趋势
#===============================================================================
@login_required
def get_new_weixin_user_daily_trend(request):
	webapp_id = request.user_profile.webapp_id

	days = request.GET['days']
	total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
	statisticses = WeixinUserDailyStatistics.objects.filter(webapp_id=webapp_id, data_date__range=(low_date, high_date))

	date2count = dict([(s.data_date, s.count) for s in statisticses])
	date_list = dateutil.get_date_range_list(low_date, high_date)

	trend_values = []
	for loop_date in date_list:
		count = 0
		if loop_date in date2count:
			count = date2count[loop_date]

		x = (loop_date - low_date).days
		dot = {'x':x, 'y':count}
		trend_values.append(dot)

	if len(trend_values) == 0:
		values = []
	else:
		values = [{'title':'新增用户数', 'values':trend_values}]

	infos = {
		'title': '',
	    'values': values,
	    'date_info': {'days':total_days, 'low_date':low_date}
	}

	line_chart_json = chartutil.create_line_chart(infos, display_today_data=True)

	return HttpResponse(line_chart_json, 'application/json')
