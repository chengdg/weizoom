# -*- coding: utf-8 -*-

import json
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from core import resource
from core import paginator
from core.jsonresponse import create_response
from core.charts_apis import create_line_chart_response

from mall.models import *
from utils import dateutil as util_dateutil
import pandas as pd
from core import dateutil
from core.charts_apis import *
from django.conf import settings

from core.exceptionutil import unicode_full_stack

DEFAULT_COUNT_PER_PAGE = 20

# EChart上显示点的个数
DISPLAY_PERIODS_IN_CHARTS = 20

from .brand_value_utils import get_brand_value, get_latest_brand_value


class BrandValue(resource.Resource):
	"""
	微品牌价值
	"""
	app = 'stats'
	resource = 'brand_value'

	@login_required
	def api_get(request):
		"""
		返回微品牌价值的EChart数据

		"""
		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')
		freq_type = request.GET.get('freq_type')
		try:
			periods = int(request.GET.get('periods', DISPLAY_PERIODS_IN_CHARTS))
		except:
			periods = DISPLAY_PERIODS_IN_CHARTS

		if freq_type == 'week':
			freq = 'W'
		elif freq_type == 'month':
			freq = 'M'
		else:
			freq = 'D'

		if end_date is None:
			end_date = util_dateutil.now()
		else:
			try:
				end_date = util_dateutil.parse_date(end_date)
			except:
				notify_msg = u"参数错误, cause:\n{}".format(unicode_full_stack())
				watchdog_warning(notify_msg)
				end_date = util_dateutil.now()

		webapp_id = request.user_profile.webapp_id
		if start_date is not None:
			date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
		else:
			# 如果不指定start_date，则以end_date为基准倒推DISPLAY_PERIODS_IN_CHARTS 个日期(点)
			date_range = pd.date_range(end=end_date, periods=periods, freq=freq)
		date_list = []
		values = []
		# TODO: 需要优化。可以一次计算完成
		for date in date_range:
			date_str = util_dateutil.date2string(date.to_datetime())  # 将pd.Timestamp转成datetime
			date_list.append(date_str)
			values.append(get_brand_value(webapp_id, date_str))

		print("date_list: {}".format(date_list))

		response = create_line_chart_response(
			"",
			"",
			#['2010-10-10', '2010-10-11', '2010-10-12', '2010-10-13'],
			date_list,
			[{
				"name": "品牌价值",
				"values" : values
			}]
			)
		return response



class LatestBrandValue(resource.Resource):
	"""
	获取最新的微品牌价值、增量百分比

	eg: http://dev.weapp.com/stats/api/latest_brand_value/
	"""
	app = 'stats'
	resource = 'latest_brand_value'

	@login_required
	def api_get(request):
		#date_str = request.GET.get('end_date')
		#if date_str is None:
		webapp_id = request.user_profile.webapp_id
		(today_value, yesterday_value, is_increasing, increase_percent) = get_latest_brand_value(webapp_id)

		response = create_response(200)
		response.data = {
			"brand_value": today_value,
			"yesterday_value": yesterday_value,
			"is_increasing": is_increasing,
			"percent": "%.2f" % increase_percent
		}
		return response.get_response()
