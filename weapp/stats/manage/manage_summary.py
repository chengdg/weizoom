# -*- coding: utf-8 -*-

import json
from core import dateutil
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models.query_utils import Q

from stats import export
from core import resource
from django.conf import settings
#from core import paginator
from core.jsonresponse import create_response
import stats.util as stats_util
from modules.member.models import Member
from mall.models import Order, belong_to, ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED, ORDER_SOURCE_OWN
from .brand_value_utils import get_latest_brand_value
from datetime import timedelta
from core.charts_apis import create_line_chart_response


FIRST_NAV = export.STATS_HOME_FIRST_NAV
DEFAULT_COUNT_PER_PAGE = 20


VALID_FOR_BRAND_VALUE = set([
	"hongjinding",
	"manyuanyuan",
	"hongfan",
	"shoucao ",
	"changjiufangzhi",
	"jingyilixiang",
	"tianmashengwu",
	"benduobao",
	"tianreyifang",
	"heshibaineng",
	"wugutang",
	"wubao",
	"yingguan",
	"fxkj",
	"homebi",
	"boniya",
	"hanjin",
	"aliguo",
	"larhea",
	"ainicoffee",
	"gangshanxigu",
	"aodahang",

	"jobs",
	])

def is_valid_for_brandvalue(username):
	return username in VALID_FOR_BRAND_VALUE


class ManageSummary(resource.Resource):
	"""
	经营概况
	"""
	app = 'stats'
	resource = 'manage_summary'

	#@mp_required
	@login_required
	def get(request):
		"""
		显示经营概况的页面
		"""
		#默认显示最近7天的日期
		end_date = dateutil.get_today()
		start_date = dateutil.get_previous_date(end_date, 6) #获取7天前日期

		webapp_id = request.user_profile.webapp_id
		(today_value, yesterday_value, increase_sign, increase_percent) = get_latest_brand_value(webapp_id)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'app_name': 'stats',
			'second_navs': export.get_stats_second_navs(request),
			'second_nav_name': export.STATS_MANAGEMENT_SECOND_NAV,
			'start_date': start_date,
			'end_date': end_date,

			#'is_valid_for_bv': is_valid_for_brandvalue(request.user.username),
			# TODO: 需要清除html中的代码
			'is_valid_for_bv': True, # 全部开启

			# 当日微品牌价值数据
			'brand_value': format(today_value, ','),
			'value_sign': increase_sign,
			'increase_percent': increase_percent, # 相比昨天增长(下降)百分比
			'bv_diff': abs(today_value-yesterday_value), # 品牌价值差值
		})
		return render_to_response('manage/manage_summary.html', c)


	@login_required
	def api_get(request):
		"""
		经营概况分析API  获取店铺经营概况各项统计数据

		"""
		low_date, high_date, date_range = stats_util.get_date_range(request)
		webapp_id = request.user_profile.webapp_id


		#商品复购率


		#商品推荐指数
		

		#成交金额
		transaction_money, transaction_orders = stats_util.get_transaction_money_order_count(webapp_id,low_date,high_date)
		#成交订单

		#购买总人数
		buyer_count = stats_util.get_buyer_count(webapp_id,low_date,high_date)

		#客单价
		if transaction_orders >0:
			vis_price = transaction_money / transaction_orders
		else:
			vis_price = 0 

		#发起扫码会员和扫码新增会员
		# ori_qrcode_member_count, member_from_qrcode_count = stats_util.get_ori_qrcode_member_count(webapp_id, low_date, high_date)

		#发起分享链接会员
		# share_url_member_count = stats_util.get_share_url_member_count(webapp_id, low_date, high_date)

		#分享链接新增会员
		# member_from_share_url_count = stats_util.get_member_from_share_url_count(webapp_id, low_date, high_date)

		#会员复购率
		# bought_member_count = stats_util.get_bought_member_count(webapp_id, low_date, high_date)
		# repeat_buying_member_count = stats_util.get_repeat_buying_member_count(webapp_id, low_date, high_date)
		# repeat_buying_member_rate = '0.00%'
		# if bought_member_count > 0:
		#	 repeat_buying_member_rate = "%.2f%%" % (repeat_buying_member_count * 100.0 / bought_member_count)

		#会员推荐率
		# member_recommend_rate = '0.00%'
		# total_member_count = stats_util.get_total_member_count(webapp_id,high_date)
		# if total_member_count > 0:
		#	 member_recommend_rate = "%.2f%%" % ((share_url_member_count + ori_qrcode_member_count)*100.0 / total_member_count)
		result = {
			# 'repeat_buying_member_rate': repeat_buying_member_rate,
			# 'member_recommend_rate': member_recommend_rate,
			'transaction_orders': transaction_orders,
			# 'ori_qrcode_member_count': ori_qrcode_member_count,
			# 'member_from_qrcode_count': member_from_qrcode_count,
			# 'share_url_member_count': share_url_member_count,
			# 'member_from_share_url_count': member_from_share_url_count,
			'transaction_money': "%.2f" % transaction_money,
			'vis_price': "%.2f" % vis_price,
			'buyer_count': buyer_count
		}

		response = create_response(200)
		response.data = {
			'items':result,
			'sortAttr': ''
		}

		return response.get_response()


#获取来源为“本店”的总订单量
# def get_total_buyer(webapp_id,low_date,high_date):
#	 orders = Order.objects.filter(
#				 webapp_id=webapp_id, 
#				 order_source=ORDER_SOURCE_OWN, 
#				 created_at__range=(low_date, high_date), 
#				 status__in=(ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED)
#			 )
#	 order_dict = {}
#	 webapp_user_ids = set([order.webapp_user_id for order in orders])
#	 webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)
#	 member_count = 0
#	 for order in orders:
#		 tmp_member = webappuser2member.get(order.webapp_user_id, None)
#		 if tmp_member:
#			 if not order_dict.has_key(tmp_member.id):
#				 member_count += 1
#				 order_dict[tmp_member.id] = ""
#		 else:
#			 member_count += 1
# 
#	 return member_count

####################################################################
#经营概况 流量、销量统计
####################################################################

# class FlowsValue(resource.Resource):
#   """
#   流量 统计
#   """
#   app = 'stats'
#   resource = 'flow_value'

#   @login_required
#   def api_get(request):
#	   """
#	   获得每日pv、uv统计
#	   """
#	   low_date, high_date, date_range = stats_util.get_date_range(request)
#	   webapp_id = request.user_profile.webapp_id
#	   #对当天的统计结果进行更新
#	   _update_visit_today_daily_statistics(webapp_id)

#	   statisticses = webapp_models.PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id, url_type=webapp_models.URL_TYPE_ALL, data_date__range=(low_date, high_date))
#	   date_list = [date.strftime("%Y-%m-%d") for date in dateutil.get_date_range_list(low_date, high_date)]

#	   date2pv = dict([(s.data_date.strftime('%Y-%m-%d'), s.pv_count) for s in statisticses])
#	   date2uv = dict([(s.data_date.strftime('%Y-%m-%d'), s.uv_count) for s in statisticses])

#	   pv_trend_values = []
#	   uv_trend_values = []
#	   for date in date_list:
#		   pv_trend_values.append(date2pv.get(date, 0))
#		   uv_trend_values.append(date2uv.get(date, 0))

#	   return create_line_chart_response(
#		   '',
#		   '',
#		   date_list,
#		   [{
#			   "name": "PV",
#			   "values" : pv_trend_values
#		   }, {
#			   "name": "UV",
#			   "values" : uv_trend_values
#		   }]
#	   )

# def _update_visit_today_daily_statistics(webapp_id):
#   """
#   更新今天的pv，uv统计
#   """
#   if not settings.IS_UPDATE_PV_UV_REALTIME:
#	   return

#   #先删除当天的pv,uv统计结果，然后重新进行统计
#   today = dateutil.get_today()
#   webapp_models.PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id, data_date=today).delete()
#   webapp_statistics_util.count_visit_daily_pv_uv(webapp_id, today)


class OrdernumValue(resource.Resource):
	"""
	订单数 统计
	"""
	app = 'stats'
	resource = 'ordernum_value'

	@login_required
	def api_get(request):
		low_date, high_date, date_range = stats_util.get_date_range(request)
		try:
			webapp_id = request.user_profile.webapp_id
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

			#当最后一天是今天时，折线图中不显示最后一天的数据 duhao 2015-08-12
			#当起止日期都是今天时，数据正常显示
			today = dateutil.get_today()
			if len(date_list) > 1 and date_list[-1] == today:
				del date_list[-1]

			for date in date_list:
				count_trend_values.append(date2count.get(date, 0))

			return create_line_chart_response(
					'',
					'',
					date_list,
					[{
						"name": "订单数",
						"values" : count_trend_values
					}]
				)
		except:
			if settings.DEBUG:
				raise
			else:
				response = create_response(500)
				response.innerErrMsg = unicode_full_stack()
				return response.get_response()


class SaleroomValue(resource.Resource):
	"""
	销售额 统计
	"""
	app = 'stats'
	resource = 'saleroom_value'

	@login_required
	def api_get(request):
		low_date, high_date, date_range = stats_util.get_date_range(request)
		try:
			webapp_id = request.user_profile.webapp_id
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

			price_trend_values = []

			#当最后一天是今天时，折线图中不显示最后一天的数据 duhao 2015-08-12
			#当起止日期都是今天时，数据正常显示
			today = dateutil.get_today()
			if len(date_list) > 1 and date_list[-1] == today:
				del date_list[-1]

			for date in date_list:
				price_trend_values.append("%.2f" % (date2price.get(date, 0.0)))

			return create_line_chart_response(
					'',
					'',
					date_list,
					[{
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