# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from core import chartutil
from core import dateutil

from models import *

#===============================================================================
# get_message_daily_trend : 获得接收消息的每日趋势
#===============================================================================
@login_required
def get_message_daily_trend(request):
	days = request.GET['days']
	total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
	statisticses = MessageDailyStatistics.objects.filter(owner=request.user, data_date__range=(low_date, high_date))

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
		values = [{'title':'消息数', 'values':trend_values}]

	infos = {
		'title': '',
	    'values': values,
	    'date_info': {'days':total_days, 'low_date':low_date}
	}

	line_chart_json = chartutil.create_line_chart(infos, display_today_data=settings.IS_UPDATE_PV_UV_REALTIME)

	return HttpResponse(line_chart_json, 'application/json')
