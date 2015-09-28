# -*- coding: utf-8 -*-

import json
from datetime import datetime
from core import dateutil
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
import time

from stats import export
from core import resource
from mall.models import Order, belong_to
from mall import models
from modules.member.models import Member, WebAppUser, SOURCE_SELF_SUB, SOURCE_MEMBER_QRCODE, SOURCE_BY_URL
from core.jsonresponse import create_response

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
		end_date = dateutil.get_today()
		start_date = dateutil.get_previous_date(end_date, 6) #获取7天前日期
		start_time = start_date + ' 00:00:00'
		end_time = end_date + ' 23:59:59'
		stats_data = _get_stats_data(request.user, start_time, end_time)
		jsons = [{
			"name": "stats_data",
			"content": stats_data
		}]
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'app_name': 'stats',
			'second_navs': export.get_stats_second_navs(request),
			'second_nav_name': export.STATS_SALES_SECOND_NAV,
			'third_nav_name': export.SALES_ORDER_SUMMARY_NAV,
			'jsons': jsons
		})
		
		return render_to_response('sales/order_summary.html', c)

	@login_required
	def api_get(request):
		"""
		获取订单概况数据	
		"""
		# 时间区间
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		
		if start_time and end_time:
			response = create_response(200)
			response.data = _get_stats_data(request.user, start_time, end_time)
			return response.get_response()
		else:
			response = create_response(500)
			response.errMsg = u'未指定查询时间段'
			return response.get_response()
		
def _get_test_data(start_time, end_time):
	order_trend_stats = {
		'wait_num': 20,
		'cancel_num': 30,
		'not_shipped_num': 45,
		'shipped_num': 36,
		'succeeded_num': 20,
		'refunding_num': 12,
		'refunded_num': 16
	}
	
	buyer_source_stats = {
		# “直接关注购买”：=∑订单.个数
		'sub_source_num': 60,
		# “推广扫码购买”：=∑订单.个数
		'qrcode_source_num': 30,
		# “分享链接购买”：=∑订单.个数
		'url_source_num': 60,
		# “其他”：=∑订单.个数
		'other_source_num': 50
	}
	
		# 优惠抵扣统计
	discount_stats = {
		# 订单总量：=∑订单.个数
		'discount_order_num': 221,
		# 微众卡支付：=∑订单.个数
		'wezoom_num': 60,
		# 微众卡支付金额：=∑订单.微众卡支付金额
		'wezoom_amount': 50.36,
		# 积分抵扣：=∑订单.个数
		'integral_num': 30,
		# 积分抵扣金额：=∑订单.积分抵扣金额
		'integral_amount': 32.23,
		# 优惠券：=∑订单.个数
		'coupon_num': 26,
		# 优惠券金额：=∑订单.优惠券金额
		'coupon_amount': 60.50,
		# 微众卡+积分：=∑订单.个数
		'wezoom_integral_num': 15,
		# (微众卡+积分)金额：=∑订单.(微众卡+积分)金额
		'wezoom_integral_amount': 85.60,
		# 微众卡+优惠券：=∑订单.个数
		'wezoom_coupon_num': 30,
		# (微众卡+优惠券)金额：=∑订单.(微众卡+优惠券)金额
		'wezoom_coupon_amount': 35.60,
		# 积分+优惠券：=∑订单.个数
		# 'integral_coupon_num': 56,
		# (积分+优惠券)金额：=∑订单.(积分+优惠券)金额
		# 'integral_coupon_amount': 85.96,
		# 微众卡+积分+优惠券：=∑订单.个数
		# 'wezoom_integral_coupon_num': 4,
		# (微众卡+积分+优惠券)金额：=∑订单.(微众卡+积分+优惠券)金额
		# 'wezoom_integral_coupon_amount': 30.88
	}
	
	result = {
		'start_time': start_time,
		'end_time': end_time,
		'order_num': 200,
		'paid_amount': 300.66,
		'product_num': 100,
		'discount_amount': 20.60,
		'postage_amount': 10.78,
		'online_order_num': 108,
		'online_paid_amount': 89.68,
		'cod_order_num': 52,
		'cod_amount': 105.95,
		'alipay_amount': 15.60,
		'weixinpay_amount': 18.20,
		'wezoom_card_amount': 35.96,
		'repeated_num': 80,
		'order_trend_stats': order_trend_stats,
		'buyer_source_stats': buyer_source_stats,
		'discount_stats': discount_stats
	}
	
	return result;

def _get_stats_data(user, start_time, end_time):
	# return _get_test_data(start_time, end_time)
	webapp_id = user.get_profile().webapp_id
	total_orders = belong_to(webapp_id)
	qualified_orders = total_orders.prefetch_related('orderhasproduct_set').filter(
		#created_at__gte=start_time, created_at__lt=end_time,
		created_at__range=(start_time, end_time),
		status__in=[models.ORDER_STATUS_PAYED_NOT_SHIP, models.ORDER_STATUS_PAYED_SHIPED, models.ORDER_STATUS_SUCCESSED]
		)
	# time_qualified_orders = total_orders.filter(created_at__gte=start_time, created_at__lt=end_time)
	status_qualified_orders = total_orders.filter(status__in=[models.ORDER_STATUS_PAYED_NOT_SHIP, models.ORDER_STATUS_PAYED_SHIPED, models.ORDER_STATUS_SUCCESSED])
	pre_status_qualified_orders = status_qualified_orders.filter(created_at__lt=start_time)
	past_status_qualified_orders = status_qualified_orders.filter(created_at__lt=end_time)
	
	# print "stats debug: start_time = %s." % start_time
	# print "stats debug: end_time = %s." % end_time
	# print "stats debug: total orders count = %d." % total_orders.count()
	# print "stats debug: time qualified orders count = %d." % time_qualified_orders.count()
	# print "stats debug: status qualified orders count = %d." % status_qualified_orders.count()
	# print "stats debug: qualified orders count = %d." % qualified_orders.count()
	
	# member_t0 = time.clock()
	# member_t1 = time.time()
	webapp_user_ids = set([order.webapp_user_id for order in past_status_qualified_orders])
	webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)
	# __report_performance(member_t0, member_t1, "get member set")
	
	# 【成交订单】=∑订单.个数
	order_num = qualified_orders.count()
	# 【成交金额】=∑订单.实付金额
	paid_amount = 0.0
	# 【成交商品】=∑订单.商品件数
	product_num = 0
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
	
	# 获取订单趋势数据
	order_trend_stats = _get_order_trend_stats(qualified_orders)
	
	# 买家来源统计
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

	# debug
	# order_id_str = ""
	# repeated_order_id_str = ""
	
	# 用于检查复购订单的辅助List
	
	wuid_dict = { 'pos': 0 }
	# loop_t0 = time.clock()
	# loop_t1 = time.time()
	for order in qualified_orders:
		# debug
		# order_id_str += order.order_id + "\n"
		tmp_paid_amount = float(order.final_price) + float(order.weizoom_card_money)
		paid_amount += tmp_paid_amount

		for r in order.orderhasproduct_set.all():
			product_num += r.number
		
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
			elif order.pay_interface_type == models.PAY_INTERFACE_WEIXIN_PAY:
				weixinpay_amount += float(order.final_price)

		wezoom_card_amount += float(order.weizoom_card_money)
		
		
		# t0 = time.clock()
		# t1 = time.time()
		tmp_member = webappuser2member.get(order.webapp_user_id, None)
		# __report_performance(t0, t1, "get member")
		
		# 检查复购订单
		# t0 = time.clock()
		# t1 = time.time()
		repeated_num += _get_repeated_num_increment(order.webapp_user_id, wuid_dict, tmp_member, webappuser2member, pre_status_qualified_orders)
		# __report_performance(t0, t1, "repeat counter")
		
		# 统计不同买家来源的订单数
		_do_buyer_source_stats(buyer_source_stats, tmp_member)
		# 统计优惠抵扣数据
		_do_discount_stats(discount_stats, order)
		
	# __report_performance(loop_t0, loop_t1, "whole loop")
	# debug
	# print "qualified orders:\n %s" % order_id_str
	# print "repeated orders:\n %s" % repeated_order_id_str 
	
	discount_stats['discount_order_num'] = discount_stats['wezoom_num'] + discount_stats['coupon_num'] + discount_stats['integral_num'] + discount_stats['wezoom_coupon_num'] + discount_stats['wezoom_integral_num']
	
	#在线付款需求修改时添加
	online_order_num = order_num - cod_order_num
	online_paid_amount = paid_amount - cod_amount
	
	result = {
		'start_time': start_time,
		'end_time': end_time,
		'order_num': order_num,
		'paid_amount': paid_amount,
		'product_num': product_num,
		'discount_amount': discount_amount,
		'postage_amount': postage_amount,
		'online_order_num': online_order_num,
		'online_paid_amount': online_paid_amount,
		'cod_order_num': cod_order_num,
		'cod_amount': cod_amount,
		'alipay_amount': alipay_amount,
		'weixinpay_amount': weixinpay_amount,
		'wezoom_card_amount': wezoom_card_amount,
		'repeated_num': repeated_num,
		'order_trend_stats': order_trend_stats,
		'buyer_source_stats': buyer_source_stats,
		'discount_stats': discount_stats
	}

	return result

def __report_performance(clock_t, wall_t, title):
	clock_x = time.clock() - clock_t
	wall_x = time.time() - wall_t
	clock_msg = "seconds process time for " + title
	wall_msg = "seconds wall time for " + title
	print clock_x, clock_msg
	print wall_x, wall_msg
	print "=========================================="

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
			tmp_member = webappuser2member.get(tmp_wuid, None)
			if member and tmp_member:
				if tmp_member.id == member.id:
					wuid_dict['pos'] = index + 1
					return 1

	return result

def _do_discount_stats(discount_stats, order):
	weizoom_used = order.weizoom_card_money > 0
	coupon_used = order.coupon_money > 0
	integral_used = order.integral_money > 0
	
	if (not weizoom_used) and (not coupon_used) and (not integral_used):
		return
	
	# discount_stats['discount_order_num'] += 1
	# if weizoom_used and coupon_used and integral_used:
	#	discount_stats['wezoom_integral_coupon_num'] += 1
	#	discount_stats['wezoom_integral_coupon_amount'] += float(order.weizoom_card_money) + float(order.coupon_money) + float(order.integral_money)
	
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
	
	# if (not weizoom_used) and coupon_used and integral_used:
	#	discount_stats['integral_coupon_num'] += 1
	#	discount_stats['integral_coupon_amount'] += float(order.coupon_money) + float(order.integral_money)

def _do_buyer_source_stats(buyer_source_stats, member):
	if member:
		if member.source == SOURCE_SELF_SUB:
			buyer_source_stats['sub_source_num'] += 1
		elif member.source == SOURCE_MEMBER_QRCODE:
			buyer_source_stats['qrcode_source_num'] += 1
		elif member.source == SOURCE_BY_URL:
			buyer_source_stats['url_source_num'] += 1
		else:
			buyer_source_stats['other_source_num'] += 1
	else:
		buyer_source_stats['other_source_num'] += 1


def _get_order_trend_stats(orders):
	"""
	获取订单趋势的统计数据
	"""
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
	
	# ORDER_STATUS_PAYED_SUCCESSED = 2  # 已支付：已下单，已付款 ?
	result = {
		'not_shipped_num': not_shipped_num,
		'shipped_num': shipped_num,
		'succeeded_num': succeeded_num,
	}
	
	return result