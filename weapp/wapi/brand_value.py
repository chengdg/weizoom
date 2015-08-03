# -*- coding: utf-8 -*-

#import json
#from datetime import datetime
#from django.http import HttpResponseRedirect
#from django.template import RequestContext
from django.contrib.auth.decorators import login_required
#from django.shortcuts import render_to_response
#from django.db.models import F

from core import resource
#from core import paginator
from core.jsonresponse import create_response
#from core.charts_apis import create_line_chart_response

from mall.models import *
#from utils import dateutil as util_dateutil
import pandas as pd
#from core import dateutil
#from webapp import models as webapp_models
#from webapp import statistics_util as webapp_statistics_util
from core.charts_apis import *
#from django.conf import settings
#import stats.util as stats_util
#from stats.models import BrandValueHistory

#from core.exceptionutil import unicode_full_stack
#from watchdog.utils import watchdog_error, watchdog_warning

from wapi.decorators import wapi_access_required

from stats.manage.brand_value_utils import get_brand_value

from utils import dateutil as utils_dateutil


class BrandValue(resource.Resource):
	"""
	获取微品牌价值的接口
	"""
	app = 'wapi'
	resource = 'brand_value'

	@wapi_access_required
	def api_get(request):
		"""
		获取微品牌价值

		@param wid webapp_id
		@param dates 日期列表，多日期用逗号(,)分隔。默认是当天。
		"""
		webapp_id = request.REQUEST.get('wid')
		print("webapp_id: {}".format(webapp_id))
		dates = request.REQUEST.get('dates')
		if dates is None or len(dates)<1:
			dates = [ utils_dateutil.date2string(utils_dateutil.now()) ]
		else:
			dates = dates.split(',')

		#values = [ {"date":date_str, "bv":get_brand_value(webapp_id, date_str)} for date_str in dates ]
		values = {date_str: get_brand_value(webapp_id, date_str) for date_str in dates}

		response = create_response(200)
		response.data = {
			"values": values
		}
		return response.get_response()


# 显示点的个数
DISPLAY_PERIODS_IN_CHARTS = 20


class BrandValueSeries(resource.Resource):
	"""
	微品牌价值列表

	@retval date:value的map
	"""
	app = 'wapi'
	resource = 'brand_value_series'

	@wapi_access_required
	def api_get(request):
		"""
		返回微品牌价值JSON数据

		"""
		webapp_id = request.GET.get('wid')
		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')
		freq_type = request.GET.get('freq_type', 'W')
		try:
			periods = int(request.GET.get('periods', DISPLAY_PERIODS_IN_CHARTS))
		except:
			periods = DISPLAY_PERIODS_IN_CHARTS

		if freq_type == 'week' or freq_type == 'W':
			freq = 'W'
		elif freq_type == 'month' or freq_type == 'M':
			freq = 'M'
		else:
			freq = 'D'

		if end_date is None:
			end_date = utils_dateutil.now()
		else:
			try:
				end_date = utils_dateutil.parse_date(end_date)
			except:
				notify_msg = u"参数错误, cause:\n{}".format(unicode_full_stack())
				watchdog_warning(notify_msg)
				end_date = utils_dateutil.now()

		#webapp_id = request.user_profile.webapp_id
		if start_date is not None:
			date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
		else:
			# 如果不指定start_date，则以end_date为基准倒推DISPLAY_PERIODS_IN_CHARTS 个日期(点)
			date_range = pd.date_range(end=end_date, periods=periods, freq=freq)
		#date_list = []
		#values = []
		# TODO: 需要优化。可以一次计算完成
		data = {}
		for date in date_range:
			date_str = utils_dateutil.date2string(date.to_datetime())  # 将pd.Timestamp转成datetime
			#date_list.append(date_str)
			value = get_brand_value(webapp_id, date_str)
			#values.append()
			data[date_str] = value

		#print("date_list: {}".format(date_list))

		response = create_response(200)
		response.data = data
		return response.get_response()
