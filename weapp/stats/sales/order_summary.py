# -*- coding: utf-8 -*-

import json
from datetime import datetime
from core import dateutil
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
import time

from stats import export
from core.charts_apis import *
from core import resource
from mall.models import Order, belong_to
from mall import models
from modules.member.models import Member, WebAppUser, SOURCE_SELF_SUB, SOURCE_MEMBER_QRCODE, SOURCE_BY_URL
from core.jsonresponse import create_response
from core.charts_apis import create_bar_chart_response
import stats.util as stats_util

import pandas as pd

FIRST_NAV = export.STATS_HOME_FIRST_NAV


class OrderSummary(resource.Resource):
	"""
	订单概况
	"""
	app = 'stats'
	resource = 'order_summary'
	
	@login_required
	def get(request):
		"""
		显示订单概况
		"""
		#默认显示最近7天的日期
		#默认显示最近7天的日期
		end_date = dateutil.get_today()
		start_date = dateutil.get_previous_date(end_date, 6) #获取7天前日期

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'app_name': 'stats',
			'second_navs': export.get_stats_second_navs(request),
			'second_nav_name': export.STATS_SALES_SECOND_NAV,
			'third_nav_name': export.SALES_ORDER_SUMMARY_NAV,
			'start_date': start_date,
			'end_date': end_date,
		})
		
		return render_to_response('sales/order_summary.html', c)

	@login_required
	def api_get(request):
		"""
		获取订单概况数据	
		"""
		# 时间区间
		low_date, high_date, date_range = stats_util.get_date_range(request)
		start_time = low_date
		end_time = high_date

		webapp_id = request.user_profile.webapp_id
		total_orders = belong_to(webapp_id)
		qualified_orders = total_orders.prefetch_related('orderhasproduct_set').filter(
			#created_at__gte=start_time, created_at__lt=end_time,
			created_at__range=(start_time, end_time),
			status__in=[models.ORDER_STATUS_PAYED_NOT_SHIP, models.ORDER_STATUS_PAYED_SHIPED, models.ORDER_STATUS_SUCCESSED]
			)

		order_num = qualified_orders.count()
		# 【成交金额】=∑订单.实付金额
		paid_amount = 0.0
		# 【成交商品】=∑订单.商品件数
		product_num = 0
		# 【优惠抵扣】=∑订单.积分抵扣金额 + +∑订单.优惠券抵扣金额
		discount_amount = 0.0

		for order in qualified_orders:
		# debug
		# order_id_str += order.order_id + "\n"
			if order.origin_order_id > 0:
				#商户从微众自营商城同步的子订单需要计算采购价
				tmp_paid_amount = order.total_purchase_price
			else:
				tmp_paid_amount = order.final_price + order.weizoom_card_money
			paid_amount += tmp_paid_amount

			for r in order.orderhasproduct_set.all():
				product_num += r.number
			
			discount_amount += float(order.integral_money) + float(order.coupon_money)
			#postage_amount += float(order.postage)

		item = {
			# 【成交订单】=∑订单.个数
			'order_num': order_num,
			# 【成交金额】=∑订单.实付金额
			'paid_amount': paid_amount,
			# 【成交商品】=∑订单.商品件数
			'product_num': product_num,
			# 【优惠抵扣】=∑订单.积分抵扣金额 + +∑订单.优惠券抵扣金额
			'discount_amount': discount_amount
		}

		
		if start_time and end_time:
			response = create_response(200)
			response.data = {
				'items': item,
				'sortAttr': ''
			}
			return response.get_response()
		else:
			response = create_response(500)
			response.errMsg = u'未指定查询时间段'
			return response.get_response()

class OrderTrends(resource.Resource):
	"""
	订单趋势
	"""
	app = 'stats'
	resource = 'order_trends'

	@login_required
	def api_get(request):

		# 时间区间
		low_date, high_date, date_range = stats_util.get_date_range(request)
		start_time = low_date
		end_time = high_date

		webapp_id = request.user_profile.webapp_id
		total_orders = belong_to(webapp_id)
		qualified_orders = total_orders.prefetch_related('orderhasproduct_set').filter(
			#created_at__gte=start_time, created_at__lt=end_time,
			created_at__range=(start_time, end_time),
			status__in=[models.ORDER_STATUS_PAYED_NOT_SHIP, models.ORDER_STATUS_PAYED_SHIPED, models.ORDER_STATUS_SUCCESSED]
			)

		orders = qualified_orders

		# 待发货：已付款，未发货
		order_count = orders.count()
		if order_count>0:
			data = [(order.id, order.status) for order in orders]
			df = pd.DataFrame(data, columns=['id', 'status'])
			counts = df['status'].value_counts()  # 按status的值统计频度

			#not_shipped_num = orders.filter(status=models.ORDER_STATUS_PAYED_NOT_SHIP).count()
			not_shipped_num = int(counts.get(models.ORDER_STATUS_PAYED_NOT_SHIP, 0))
			# 已发货：已付款，已发货
			#shipped_num = orders.filter(status=models.ORDER_STATUS_PAYED_SHIPED).count()
			shipped_num = int(counts.get(models.ORDER_STATUS_PAYED_SHIPED, 0))
			# 已完成：自下单10日后自动置为已完成状态
			#succeeded_num = orders.filter(status=models.ORDER_STATUS_SUCCESSED).count()
			succeeded_num = int(counts.get(models.ORDER_STATUS_SUCCESSED, 0))
		else:
			not_shipped_num = 0
			# 已发货：已付款，已发货
			shipped_num = 0
			# 已完成：自下单10日后自动置为已完成状态
			succeeded_num = 0
		
		# 系统封装的饼图方法，由于数据次序不统一，故舍弃使用
		# return create_pie_chart_response('',
		# 		{
		# 			"待发货":not_shipped_num, 
		# 		 	"已发货":shipped_num, 
		# 		 	"已完成":succeeded_num
		# 		}
		# 	)
	
		response = create_response(200)
		response.data = {
			"not_shipped_num": not_shipped_num,
			"shipped_num": shipped_num,
			"succeeded_num": succeeded_num
		}

		return response.get_response()

class RepeatPurchaseRate(resource.Resource):
	"""
	复购率
	"""
	app = 'stats'
	resource = 'repeat_purchase_rate'

	@login_required
	def api_get(request):

		# 时间区间
		low_date, high_date, date_range = stats_util.get_date_range(request)
		start_time = low_date
		end_time = high_date

		# 用于检查复购订单的辅助List
		wuid_dict = { 'pos': 0 }

		webapp_id = request.user_profile.webapp_id
		total_orders = belong_to(webapp_id)
		qualified_orders = total_orders.prefetch_related('orderhasproduct_set').filter(
			# created_at__gte=start_time, created_at__lt=end_time,
			created_at__range=(start_time, end_time),
			status__in=[models.ORDER_STATUS_PAYED_NOT_SHIP, models.ORDER_STATUS_PAYED_SHIPED, models.ORDER_STATUS_SUCCESSED]
			)

		status_qualified_orders = total_orders.filter(status__in=[models.ORDER_STATUS_PAYED_NOT_SHIP, models.ORDER_STATUS_PAYED_SHIPED, models.ORDER_STATUS_SUCCESSED])
		pre_status_qualified_orders = status_qualified_orders.filter(created_at__lt=start_time)
		past_status_qualified_orders = status_qualified_orders.filter(created_at__lt=end_time)

		# 订单总量
		order_num = qualified_orders.count()
		# 重复购买
		repeated_num = 0;

		webapp_user_ids = set([order.webapp_user_id for order in past_status_qualified_orders])
		webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

		for order in qualified_orders:
			tmp_member_two = webappuser2member.get(order.webapp_user_id, None)

			# t0 = time.clock()
			# t1 = time.time()
			# print ">>>>>"
			repeated_num += _get_repeated_num_increment(order.webapp_user_id, wuid_dict, tmp_member_two, webappuser2member, pre_status_qualified_orders)
			# __report_performance(t0, t1, "repeat counter")

		# 初次购买
		first_buy = order_num - repeated_num

		# 系统封装的饼图方法，由于数据次序不统一，故舍弃使用
		# return create_pie_chart_response('',
		# 		{
		# 			"重复购买":repeated_num, 
		# 		 	"初次购买":first_buy
		# 		}
		# 	)

		response = create_response(200)
		response.data = {
			"first_buy": first_buy,
			"repeated_num": repeated_num
		}

		return response.get_response()
	
class BuyerSources(resource.Resource):
	"""
	买家来源
	"""
	app = 'stats'
	resource = 'buyer_sources'

	@login_required
	def api_get(request):

		# 时间区间
		low_date, high_date, date_range = stats_util.get_date_range(request)
		start_time = low_date
		end_time = high_date

		webapp_id = request.user_profile.webapp_id
		total_orders = belong_to(webapp_id)
		qualified_orders = total_orders.prefetch_related('orderhasproduct_set').filter(
			# created_at__gte=start_time, created_at__lt=end_time,
			created_at__range=(start_time, end_time),
			status__in=[models.ORDER_STATUS_PAYED_NOT_SHIP, models.ORDER_STATUS_PAYED_SHIPED, models.ORDER_STATUS_SUCCESSED]
			)

		status_qualified_orders = total_orders.filter(status__in=[models.ORDER_STATUS_PAYED_NOT_SHIP, models.ORDER_STATUS_PAYED_SHIPED, models.ORDER_STATUS_SUCCESSED])
		pre_status_qualified_orders = status_qualified_orders.filter(created_at__lt=start_time)
		past_status_qualified_orders = status_qualified_orders.filter(created_at__lt=end_time)

		#买家来源
		buyer_source_stats = {
			# “直接关注购买”：=∑订单.个数
			'sub_source_num': 0,
			# “推广扫码购买”：=∑订单.个数
			'qrcode_source_num': 0,
			# “分享链接购买”：=∑订单.个数
			'url_source_num': 0,
			# “其他”：=∑订单.个数
			'other_source_num': 0
		}

		webapp_user_ids = set([order.webapp_user_id for order in past_status_qualified_orders])
		webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)
		for order in qualified_orders:
			tmp_member = webappuser2member.get(order.webapp_user_id, None)
			if tmp_member:
				if tmp_member.source == SOURCE_SELF_SUB:
					buyer_source_stats['sub_source_num'] += 1
				elif tmp_member.source == SOURCE_MEMBER_QRCODE:
					buyer_source_stats['qrcode_source_num'] += 1
				elif tmp_member.source == SOURCE_BY_URL:
					buyer_source_stats['url_source_num'] += 1
				else:
					buyer_source_stats['other_source_num'] += 1
			else:
				buyer_source_stats['other_source_num'] += 1

		# 系统封装的饼图方法，由于数据次序不统一，故舍弃使用
		# return create_pie_chart_response('',
		# 		{
		# 			"直接关注购买":buyer_source_stats['sub_source_num'], 
		# 		 	"推广扫码购买":buyer_source_stats['qrcode_source_num'],
		# 		 	"分享链接购买":buyer_source_stats['url_source_num'], 
		# 		 	"其他":buyer_source_stats['other_source_num']
		# 		}
		# 	)

		response = create_response(200)
		response.data = {
			"sub_source_num": buyer_source_stats['sub_source_num'],
			"qrcode_source_num": buyer_source_stats['qrcode_source_num'],
			"url_source_num": buyer_source_stats['url_source_num'],
			"other_source_num": buyer_source_stats['other_source_num']
		}

		return response.get_response()

class PaymentAmount(resource.Resource):
	"""
	支付金额
	"""
	app = 'stats'
	resource = 'payment_amount'

	@login_required
	def api_get(request):

		# 时间区间
		low_date, high_date, date_range = stats_util.get_date_range(request)
		start_time = low_date
		end_time = high_date

		webapp_id = request.user_profile.webapp_id
		total_orders = belong_to(webapp_id)
		qualified_orders = total_orders.prefetch_related('orderhasproduct_set').filter(
			# created_at__gte=start_time, created_at__lt=end_time,
			created_at__range=(start_time, end_time),
			status__in=[models.ORDER_STATUS_PAYED_NOT_SHIP, models.ORDER_STATUS_PAYED_SHIPED, models.ORDER_STATUS_SUCCESSED]
			)

		# 【优惠抵扣】=∑订单.积分抵扣金额 + +∑订单.优惠券抵扣金额
		discount_amount = 0.0
		# 【总运费】=∑订单.运费金额
		postage_amount = 0.0
		# 【在线付款订单】=∑订单.个数
		online_order_num = 0
		# 【在线付款订单金额】=∑订单.实付金额
		online_paid_amount = 0.0
		# 【货到付款订单】=∑订单.个数
		cod_order_num = 0
		# 【货到付款订单金额】=∑订单.实付金额
		cod_amount = 0.0
		# 支付宝支付金额:=∑订单.支付宝支付金额
		alipay_amount = 0.0
		# 微信支付金额:=∑订单.微信支付金额
		weixinpay_amount = 0.0
		# 微众卡支付金额:=∑订单.微众卡支付金额
		wezoom_card_amount = 0.0
		# 复购订单数
		repeated_num = 0
		bestpay_amount = 0.0  #翼支付金额
		kangou_amount = 0.0  #看购支付金额

		for order in qualified_orders:
			# debug
			# order_id_str += order.order_id + "\n"
			if order.origin_order_id > 0:
				#商户从微众自营商城同步的子订单需要计算采购价
				tmp_paid_amount = order.total_purchase_price
			else:
				tmp_paid_amount = order.final_price + order.weizoom_card_money
			# paid_amount += tmp_paid_amount

			# for r in order.orderhasproduct_set.all():
			# 	product_num += r.number
			
			discount_amount += float(order.integral_money) + float(order.coupon_money)
			postage_amount += float(order.postage)
			
			if order.pay_interface_type == models.PAY_INTERFACE_COD:
				cod_order_num += 1
				cod_amount += float(order.final_price)
			else:
				# 在线付款需求修改时去掉
				# online_order_num += 1
				# online_paid_amount += tmp_paid_amount
				
				if order.pay_interface_type == models.PAY_INTERFACE_ALIPAY:
					alipay_amount += float(order.final_price)
				elif order.pay_interface_type == models.PAY_INTERFACE_BEST_PAY:
					bestpay_amount += float(order.final_price)
				elif order.pay_interface_type == models.PAY_INTERFACE_KANGOU:
					kangou_amount += float(order.final_price)
				elif order.pay_interface_type == models.PAY_INTERFACE_WEIXIN_PAY:
					if order.origin_order_id >0: #判断同步订单
						weixinpay_amount += float(order.total_purchase_price)
					else:
						weixinpay_amount += float(order.final_price)

			wezoom_card_amount += float(order.weizoom_card_money)
			
		#在线付款需求修改时添加
		#online_order_num = order_num - cod_order_num
		#online_paid_amount = paid_amount - cod_amount

		# 系统封装的饼图方法，由于数据次序不统一，故舍弃使用
		# return create_pie_chart_response('',
		# 		{
		# 			# 'discount_amount': discount_amount,
		# 			# 'postage_amount': postage_amount,
		# 			# 'online_order_num': online_order_num,
		# 			# 'online_paid_amount': online_paid_amount,
		# 			# 'cod_order_num': cod_order_num,			
		# 			'支付宝': round(alipay_amount,2),
		# 			'微信支付': round(weixinpay_amount,2),
		# 			'货到付款': round(cod_amount,2),
		# 			'微众卡支付': round(wezoom_card_amount,2),
		# 			'翼支付': round(bestpay_amount,2),
		# 			'看购支付': round(kangou_amount,2)
		# 		}
		# 	)

		response = create_response(200)
		response.data = {
			"alipay_amount": round(alipay_amount,2),
			"weixinpay_amount": round(weixinpay_amount,2),
			"cod_amount": round(cod_amount,2),
			"wezoom_card_amount": round(wezoom_card_amount,2),
			"bestpay_amount": round(bestpay_amount,2),
			"kangou_amount": round(kangou_amount,2)
		}

		return response.get_response()

class PreferentialDiscount(resource.Resource):
	"""
	优惠折扣
	"""
	app = 'stats'
	resource = 'preferential_discount'

	@login_required
	def api_get(request):

		# 时间区间
		low_date, high_date, date_range = stats_util.get_date_range(request)
		start_time = low_date
		end_time = high_date

		webapp_id = request.user_profile.webapp_id
		total_orders = belong_to(webapp_id)
		qualified_orders = total_orders.prefetch_related('orderhasproduct_set').filter(
			# created_at__gte=start_time, created_at__lt=end_time,
			created_at__range=(start_time, end_time),
			status__in=[models.ORDER_STATUS_PAYED_NOT_SHIP, models.ORDER_STATUS_PAYED_SHIPED, models.ORDER_STATUS_SUCCESSED]
			)

		# 优惠抵扣统计
		discount_stats = {
			# 订单总量：=∑订单.个数
			'discount_order_num': 0,
			# 微众卡支付：=∑订单.个数
			'wezoom_num': 0,
			# 微众卡支付金额：=∑订单.微众卡支付金额
			'wezoom_amount': 0.0,
			# 积分抵扣：=∑订单.个数
			'integral_num': 0,
			# 积分抵扣金额：=∑订单.积分抵扣金额
			'integral_amount': 0.0,
			# 优惠券：=∑订单.个数
			'coupon_num': 0,
			# 优惠券金额：=∑订单.优惠券金额
			'coupon_amount': 0.0,
			# 微众卡+积分：=∑订单.个数
			'wezoom_integral_num': 0,
			# (微众卡+积分)金额：=∑订单.(微众卡+积分)金额
			'wezoom_integral_amount': 0.0,
			# 微众卡+优惠券：=∑订单.个数
			'wezoom_coupon_num': 0,
			# (微众卡+优惠券)金额：=∑订单.(微众卡+优惠券)金额
			'wezoom_coupon_amount': 0.0,
			# 积分+优惠券：=∑订单.个数
			# 'integral_coupon_num': 0,
			# (积分+优惠券)金额：=∑订单.(积分+优惠券)金额
			# 'integral_coupon_amount': 0.0,
			# 微众卡+积分+优惠券：=∑订单.个数
			#'wezoom_integral_coupon_num': 0,
			# (微众卡+积分+优惠券)金额：=∑订单.(微众卡+积分+优惠券)金额
			#'wezoom_integral_coupon_amount': 0.0
		}
		for order in qualified_orders:
			_do_discount_stats(discount_stats, order)
			discount_stats['discount_order_num'] = discount_stats['wezoom_num'] + discount_stats['coupon_num'] + discount_stats['integral_num'] + discount_stats['wezoom_coupon_num'] + discount_stats['wezoom_integral_num']

		response = create_response(200)
		response.data = {
			'discount_stats': discount_stats,
			'sortAttr': ''
		}

		return response.get_response()

# 以下为类中用到的方法封装

#业绩报告 
def __report_performance(clock_t, wall_t, title):
	clock_x = time.clock() - clock_t
	wall_x = time.time() - wall_t
	clock_msg = "seconds process time for " + title
	wall_msg = "seconds wall time for " + title
	# print clock_x, clock_msg
	# print wall_x, wall_msg
	# print "=========================================="

def _get_repeated_num_increment(wuid, wuid_dict, member, webappuser2member, pre_status_qualified_orders):
	if wuid_dict.has_key(wuid):
		return 1
	
	result = 0
	wuid_dict[wuid] = ""

	if pre_status_qualified_orders:
		for index in range(wuid_dict['pos'], len(pre_status_qualified_orders)):
			tmp_wuid = pre_status_qualified_orders[index].webapp_user_id
			if wuid == tmp_wuid:
				wuid_dict['pos'] = index + 1
				return 1

			wuid_dict[tmp_wuid] = ""
			tmp_member_two = webappuser2member.get(tmp_wuid, None)
			if member and tmp_member_two:
				if tmp_member_two.id == member.id:
					wuid_dict['pos'] = index + 1
					return 1
	# print "+++++++++++++++++++++++++++++++++"
	return result

def _do_discount_stats(discount_stats, order):
	weizoom_used = order.weizoom_card_money > 0
	coupon_used = order.coupon_money > 0
	integral_used = order.integral_money > 0
	
	if (not weizoom_used) and (not coupon_used) and (not integral_used):
		return
	
	if weizoom_used and (not coupon_used) and (not integral_used):
		discount_stats['wezoom_num'] += 1
		discount_stats['wezoom_amount'] += float(order.weizoom_card_money)
	
	if (not weizoom_used) and coupon_used and (not integral_used):
		discount_stats['coupon_num'] += 1
		discount_stats['coupon_amount'] += float(order.coupon_money)
	
	if (not weizoom_used) and (not coupon_used) and integral_used:
		discount_stats['integral_num'] += 1
		discount_stats['integral_amount'] += float(order.integral_money)
	
	if weizoom_used and coupon_used and (not integral_used):
		discount_stats['wezoom_coupon_num'] += 1
		discount_stats['wezoom_coupon_amount'] += float(order.weizoom_card_money) + float(order.coupon_money)
	
	if weizoom_used and (not coupon_used) and integral_used:
		discount_stats['wezoom_integral_num'] += 1
		discount_stats['wezoom_integral_amount'] += float(order.weizoom_card_money) + float(order.integral_money)

# 注：未用到的注释代码部分已删除