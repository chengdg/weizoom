# -*- coding: utf-8 -*-

import json
from core import dateutil
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from stats import export
from core import resource
from core.jsonresponse import create_response
from core.charts_apis import create_bar_chart_response
import stats.util as stats_util
from django.conf import settings

FIRST_NAV = export.STATS_HOME_FIRST_NAV


class ProductSummary(resource.Resource):
	"""
	商品概况
	"""
	app = 'stats'
	resource = 'product_summary'
	
	@login_required
	def get(request):
		"""
		显示商品概况页面
		"""

		#默认显示最近7天的日期
		end_date = dateutil.get_today()
		start_date = dateutil.get_previous_date(end_date, 6) #获取7天前日期
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
	        'app_name': 'stats',
			'second_navs': export.get_stats_second_navs(request),
			'second_nav_name': export.STATS_SALES_SECOND_NAV,
			'third_nav_name': export.PRODUCT_SUMMARY_NAV,
			'start_date': start_date,
			'end_date': end_date,
		})
		
		return render_to_response('sales/product_summary.html', c)

	@login_required
	def api_get(request):
		"""
		商品概况数据
		"""
		# 时间区间
		low_date, high_date, date_range = stats_util.get_date_range(request)
		webapp_id = request.user_profile.webapp_id
		# owner_id = request.user_profile.user_id

		#购买总人数
		buyer_count = stats_util.get_buyer_count(webapp_id, low_date, high_date)
		#下单单量
		order_count = stats_util.get_order_count(webapp_id, low_date, high_date)
		#总成交件数
		deal_product_count = stats_util.get_deal_product_count(webapp_id, low_date, high_date)

		item = {
			'buyer_count': buyer_count,
			'order_count': order_count,
			'deal_product_count': deal_product_count
		}
		response = create_response(200)
		response.data = {
			'item': item,
			'items': [],
			'sortAttr': ''
		}

		return response.get_response()

class DealOrderRankBarChart(resource.Resource):
	app = 'stats'
	resource = 'deal_order_rank_bar_chart'

	@login_required
	def api_get(request):
		"""
		下单单量排行top10柱状图
		"""
		# 时间区间
		low_date, high_date, date_range = stats_util.get_date_range(request)
		webapp_id = request.user_profile.webapp_id

		top10_product_list = stats_util.get_top10_product(webapp_id, low_date, high_date)

		x_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		y_values = []

		for item in top10_product_list:
			# x_values.append(item['rank'])
			y_values.append(item['num'])
			
		if len(y_values) == 0:
			y_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		y_values_list = [{
			"name": "下单次数",
			"values" : y_values,
			"tooltip" : {
				"trigger" : "item",
				"formatter" : u"次数:{c}"
			},
			"barWidth": 20
		}]

		try:
			return create_bar_chart_response(x_values, y_values_list)
		except:
			if settings.DEBUG:
				raise
			else:
				response = create_response(500)
				response.innerErrMsg = unicode_full_stack()
				return response.get_response()

class DealOrderRank(resource.Resource):
	app = 'stats'
	resource = 'deal_order_rank'

	@login_required
	def api_get(request):
		"""
		下单单量排行top10
		"""
		# 时间区间
		low_date, high_date, date_range = stats_util.get_date_range(request)
		webapp_id = request.user_profile.webapp_id

		top10_product_list = stats_util.get_top10_product(webapp_id, low_date, high_date)

		response = create_response(200)
		response.data = {
			'items': top10_product_list,
			'sortAttr': ''
		}

		return response.get_response()