# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required, ApiParamaterError

from stats.manage.brand_value_utils import get_brand_value
from wapi.wapi_utils import get_webapp_id_via_username

from utils import dateutil as utils_dateutil
import pandas as pd
from core.charts_apis import *

# 显示点的个数
DISPLAY_PERIODS_IN_CHARTS = 20


class BrandValueSeries(api_resource.ApiResource):
	"""
	微品牌价值列表

	@retval date:value的map
	"""
	app = 'stats'
	resource = 'brand_value_series'

	# @param_required(['wid'])
	def get(args):
		"""
		返回微品牌价值JSON数据

		"""
		username = args.get('un', None)
		webapp_id = args.get('wid', None)
		if (not username) and (not webapp_id):
			raise ApiParamaterError('no parameter wid or un!')

		if username:
			webapp_id = get_webapp_id_via_username(username)

		start_date = args.get('start_date', None)
		end_date = args.get('end_date', None)
		freq_type = args.get('freq_type', 'W')
		try:
			periods = int(args.get('periods', DISPLAY_PERIODS_IN_CHARTS))
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

		if start_date is not None:
			date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
		else:
			# 如果不指定start_date，则以end_date为基准倒推DISPLAY_PERIODS_IN_CHARTS 个日期(点)
			date_range = pd.date_range(end=end_date, periods=periods, freq=freq)

		# TODO: 需要优化。可以一次计算完成
		data = {}
		for date in date_range:
			date_str = utils_dateutil.date2string(date.to_datetime())  # 将pd.Timestamp转成datetime
			value = get_brand_value(webapp_id, date_str)
			data[date_str] = value

		return data
