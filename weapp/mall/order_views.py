# -*- coding: utf-8 -*-

#import time
from datetime import timedelta, datetime, date
#import urllib, urllib2
#import os
#import json
#import MySQLdb
#import random
#import string
import re

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
#from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
#from django.contrib import auth
from django.db.models import Q, F
#from django.db.models.aggregates import Sum, Count

from tools.regional import views as regional_util
from tools.regional.models import *
from tools.regional.views import get_str_value_by_string_ids, get_str_value_by_string_ids_new
from tools.express import util as express_util

from excel_response import ExcelResponse

#import models as mall_models
from promotion.models import *
from models import *
import export
from core.restful_url_route import *

import module_api as mall_api
#import export

COUNT_PER_PAGE = 20
FIRST_NAV = export.ORDER_FIRST_NAV

@view(app='mall', resource='orders', action='get')
@login_required
def get_orders(request):
	"""
	get_orders: 显示订单列表

	对应URL: `http://hostname/mall/orders/get/`
	"""
	has_order = _is_has_order(request)

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_orders_second_navs(request),
		'second_nav_name': export.ORDER_ALL,
		'has_order': has_order
	})
	return render_to_response('mall/editor/orders.html', c)


@view(app='mall', resource='refund_orders', action='get')
@login_required
def get_refund_orders(request):
	"""
	list_orders: 显示退款订单列表
	"""
	has_order = _is_has_order(request, True)
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_orders_second_navs(request),
		'second_nav_name': export.ORDER_REFUND,
		'has_order': has_order
	})
	return render_to_response('mall/editor/refund_orders.html', c)

########################################################################
# get_audit_orders: 显示审核订单列表
########################################################################
@view(app='mall', resource='audit_orders', action='get')
@login_required
def get_audit_orders(request):
	has_order = _is_has_order(request, True)
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_orders_second_navs(request),
		'second_nav_name': export.ORDER_AUDIT,
		'has_order': has_order
	})
	return render_to_response('mall/editor/audit_orders.html', c)

def _is_has_order(request, is_refund=False):
	webapp_id = request.user_profile.webapp_id
	weizoom_mall_order_ids = WeizoomMallHasOtherMallProductOrder.get_order_ids_for(webapp_id)
	if is_refund:
		has_order = (Order.objects.filter(Q(webapp_id=webapp_id)|Q(order_id__in=weizoom_mall_order_ids), status__in=[ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED]).count() > 0)
	else:
		has_order = (Order.objects.filter(Q(webapp_id=webapp_id)|Q(order_id__in=weizoom_mall_order_ids)).count() > 0)
	MallCounter.clear_unread_order(webapp_owner_id=request.manager.id) #清空未读订单数量
	return has_order

########################################################################
# edit_expired_time: 订单过期时间
########################################################################
@view(app='mall', resource='expired_time', action='edit')
@login_required
def edit_expired_time(request):
	if request.POST:
		# #处理运费信息
		# postage_config_id = request.POST.get('postage_config_id', None)
		# if postage_config_id:
		# 	PostageConfig.objects.filter(owner=request.manager).update(is_used=False)
		# 	PostageConfig.objects.filter(owner=request.manager, id=postage_config_id).update(is_used=True)
		# 	# 修改商品的邮费
		# 	module_api.update_products_postage(request.manager.id, postage_config_id)

		# #处理是否开发票选项
		# is_enable_bill = (request.POST.get('is_enable_bill', '0') == '1')

		#处理订单失效配置信息

		if not request.POST.get('order_expired_day', 24):
			order_expired_day = 0
		else:
			order_expired_day = int(request.POST.get('order_expired_day', 24))
		if MallConfig.objects.filter(owner=request.manager).count() > 0:
			MallConfig.objects.filter(owner=request.manager).update(order_expired_day=order_expired_day)
		else:
			MallConfig.objects.create(owner=request.use, order_expired_day=24)

		mall_config = MallConfig.objects.filter(owner=request.manager)[0]

	else:
		if MallConfig.objects.filter(owner=request.manager).count() == 0:
			MallConfig.objects.create(owner=request.use, order_expired_day=24)

	mall_config = MallConfig.objects.filter(owner=request.manager)[0]
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_orders_second_navs(request),
		'second_nav_name': export.ORDER_EXPIRED_TIME,
		'mall_config': mall_config,
	})
	return render_to_response('mall/editor/edit_expired_time.html', c)


########################################################################
# update_order: 更新订单信息
########################################################################
@login_required
def update_order(request):
	order_id = request.POST['order_id']
	order_status = request.POST.get('order_status', None)
	bill_type = int(request.POST.get('bill_type', ORDER_BILL_TYPE_NONE))
	postage = request.POST.get('postage', None)
	final_price = request.POST.get('final_price', None)
	ship_name = request.POST.get('ship_name', None)
	ship_tel = request.POST.get('ship_tel', None)
	ship_address = request.POST.get('ship_address', None)
	remark = request.POST.get('remark', '').strip()

	operate_log = ''
	order = Order.objects.get(id=order_id)
	expired_status = order.status
	if order_status:
		if order.status != int(order_status):
			operate_log = u' 修改状态'
			mall_api.record_status_log(order.order_id, order.status, order_status, request.manager.username)
			order.status = order_status
			try:
				if expired_status < ORDER_STATUS_SUCCESSED and int(order_status) == ORDER_STATUS_SUCCESSED and expired_status != ORDER_STATUS_CANCEL:
					integral.increase_father_member_integral_by_child_member_buyed(order, order.webapp_id)
					integral.increase_detail_integral(order.webapp_user_id, order.webapp_id, order.final_price)
			except:
				notify_message = u"订单状态为已完成时为贡献者增加积分，cause:\n{}".format(unicode_full_stack())
				watchdog_error(notify_message)

	if bill_type:
		bill = request.POST.get('bill', '')
		# 允许发票信息随意修改
		#if order.bill_type != bill_type:
		operate_log = operate_log + u' 修改发票'
		order.bill_type = bill_type
		order.bill = bill

	if postage:
		if float(order.postage) != float(postage):
			operate_log = operate_log + u' 修改邮费'
			order.final_price = order.final_price - order.postage + float(postage) #更新最终价格
			order.postage = postage

	if ship_name:
		if order.ship_name != ship_name:
			operate_log = operate_log + u' 修改收货人'
			order.ship_name = ship_name

	if ship_tel:
		if order.ship_tel != ship_tel:
			operate_log = operate_log + u' 修改收货人电话号'
			order.ship_tel = ship_tel

	if ship_address:
		if order.ship_address != ship_address:
			operate_log = operate_log + u' 修改收货人地址'
			order.ship_address = ship_address

	if remark:
		if order.remark != remark:
			operate_log = operate_log + u' 修改订单备注'
			order.remark = remark

	if final_price is not None:
		if float(order.final_price) != float(final_price):
			operate_log = operate_log + u' 修改订单金额'
			order.final_price = float(final_price)


	if len(operate_log.strip()) > 0:
		mall_api.record_operation_log(order.order_id, request.manager.username, operate_log)

	order.save()

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


########################################################################
# update_order_status: 更新订单状态 取消订单
########################################################################
@view(app='mall', resource='order', action='update')
@login_required
def update_order(request):
	order_id = request.GET['order_id']
	action = request.GET['action']
	order = Order.objects.get(id=order_id)

	mall_api.update_order_status(request.manager, action, order, request)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


########################################################################
# add_express_info: 增加物流信息
########################################################################
@login_required
def add_express_info(request):
	order_id = request.GET['order_id']
	express_company_name = request.GET['express_company_name']
	express_number = request.GET['express_number']
	leader_name = request.GET['leader_name']
	is_update_express = request.GET['is_update_express']
	is_update_express = True if is_update_express == 'true' else False
	mall_api.ship_order(order_id, express_company_name, express_number, request.manager.username, leader_name=leader_name, is_update_express=is_update_express)

	return HttpResponseRedirect('/mall/editor/order/get/?order_id=%s' %order_id)


########################################################################
# get_order_detail: 显示订单详情
########################################################################
@view(app='mall', resource='order_detail', action='get')
@login_required
def get_order_detail(request):
	return _get_detail_response(request)

########################################################################
# get_refund_order_detail: 显示退款订单详情
########################################################################
@view(app='mall', resource='refund_order_detail', action='get')
@login_required
def get_refund_order_detail(request):
	return _get_detail_response(request, 'refund')

########################################################################
# get_audit_order_detail: 显示审计订单详情
########################################################################
@view(app='mall', resource='audit_order_detail', action='get')
@login_required
def get_audit_order_detail(request):
	return _get_detail_response(request, 'audit')

def _get_detail_response(request, belong='all'):
	order = Order.objects.get(id=request.GET['order_id'])
	#如果定单是微众卡支付显示微众卡号
	try:
		order.used_weizoom_card_id, order.used_weizoom_card_number = order.get_used_weizoom_card_id()
	except:
		order.used_weizoom_card_id = None
		order.used_weizoom_card_number = None

	if request.method == 'GET':
		order_has_products = OrderHasProduct.objects.filter(order=order)

		number = 0
		for order_has_product in order_has_products:
			number += order_has_product.number
		order.number = number

		#处理订单关联的优惠券
		coupon =  order.get_coupon()
		if coupon:
			coupon_rule = CouponRule.objects.get(id=coupon.coupon_rule_id)
			promotion = Promotion.objects.get(detail_id=coupon_rule.id, type=PROMOTION_TYPE_COUPON)
			relation = ProductHasPromotion.objects.filter(promotion_id=promotion.id)
			if len(relation) > 0:
				coupon.product_id = relation[0].product_id
		'''
		coupons = OrderHasCoupon.objects.filter(order_id=order.order_id)
		if coupons.count() > 0:
			coupon =  coupons[0]
		'''
		if order.status in [ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED]:
			order_has_delivery_times = OrderHasDeliveryTime.objects.filter(order=order,status=UNSHIPED)
			if order_has_delivery_times.count() > 0:
				tmp_time = order_has_delivery_times[0].delivery_date
				for order_has_delivery_time in order_has_delivery_times:
					if order_has_delivery_time.delivery_date <= tmp_time:
						tmp_time = order_has_delivery_time.delivery_date

				#距离配送日期达到两天之内修改订单状态为代发货
				if (tmp_time - date.today()).days <= 2:
					order.status = ORDER_STATUS_PAYED_NOT_SHIP
					order.save()
		# #获得订单关联的商品集合
		# product_ids = []
		# product_infos = []
		# order_product_relations = list(OrderHasProduct.objects.filter(order_id=order.id))
		# for relation in order_product_relations:
		# 	product_ids.append(relation.product_id)
		# 	product_infos.append({
		# 		'count': relation.number, #商品数量
		# 		'id': relation.product_id, #商品id
		# 		'total_price': relation.total_price #商品总价
		# 	})
		# id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])

		# product_items = []
		# for product_info in product_infos:
		# 	product_id = product_info['id']
		# 	product_count = product_info['count']
		# 	product = id2product[product_id]
		# 	product_items.append({
		# 		'name': product.name,
		# 		'thumbnails_url': product.thumbnails_url,
		# 		'count': product_info['count'],
		# 		'total_price': '%.2f' % product_info['total_price']
		# 	})
		order.products = mall_api.get_order_products(order)

		order.area = regional_util.get_str_value_by_string_ids(order.area)
		order.belong = belong
		order.pay_interface_name = PAYTYPE2NAME.get(order.pay_interface_type, u'')
		order.total_price = Order.get_order_has_price_number(order)
		order.save_money = float(Order.get_order_has_price_number(order)) + float(order.postage) - float(order.final_price) - float(order.weizoom_card_money)
		order.pay_money = order.final_price + order.weizoom_card_money

		if order.order_source:
			order.source = u'商城'
			order.come = 'weizoom_mall'
		else:
			order.source = u'本店'
			order.come = 'mine_mall'

		if belong == 'audit':
			second_nav_name = export.ORDER_AUDIT
		elif belong == 'refund':
			second_nav_name = export.ORDER_REFUND
		else:
			second_nav_name = export.ORDER_ALL
		show_first = True if OrderStatusLog.objects.filter(order_id=order.order_id, to_status=ORDER_STATUS_PAYED_NOT_SHIP, operator=u'客户').count() > 0 else False

		order_status_logs = mall_api.get_order_status_logs(order)
		log_count = len(order_status_logs)

		# 微众卡信息
		if order.weizoom_card_money:
			from market_tools.tools.weizoom_card import models as weizoom_card_model
			cardOrders = weizoom_card_model.WeizoomCardHasOrder.objects.filter(order_id=order.order_id)
			cardIds = [card.card_id for card in cardOrders]
			cards = weizoom_card_model.WeizoomCard.objects.filter(id__in=cardIds)
			order.weizoom_cards = ['钱包ID:%s<br>卡号:%s' % (card.weizoom_card_rule_id, card.weizoom_card_id) for card in cards]

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_orders_second_navs(request),
			'second_nav_name': second_nav_name,
			'order': order,
			'is_order_not_payed': (order.status == ORDER_STATUS_NOT),
			'coupon': coupon,
			'order_operation_logs': mall_api.get_order_operation_logs(order.order_id),
			'order_status_logs': order_status_logs,
			'log_count': log_count,
			'order_has_delivery_times': OrderHasDeliveryTime.objects.filter(order=order),
			'show_first':show_first
		})

		return render_to_response('mall/editor/order_detail.html', c)
	else:
		return HttpResponseRedirect('/mall/orders/get/')


########################################################################
# export_orders:  导出订单列表
########################################################################
@view(app='mall', resource='orders', action='export')
@login_required
def export_orders(request):
	orders = _export_orders_json(request)
	return ExcelResponse(orders,output_name=u'订单列表'.encode('utf8'),force_csv=False)

def _export_orders_json(request):
	# debug
	# pre_page = 500
	# test_index = 0
	# begin_time = time.time()
	status = {
		'0':u'待支付',
		'1':u'已取消',
		'2':u'已支付',
		'3':u'待发货',
		'4':u'已发货',
		'5':u'已完成',
		'6':u'退款中',
		'7':u'退款完成',
	}

	payment_type = {
		'-1': u'',
		'0': u'支付宝',
		'2': u'微信支付',
		'3': u'微众卡支付',
		'9': u'货到付款',
		'10': u'优惠抵扣'
	}

	type = ORDER_TYPE2TEXT

	source_list = {
		'mine_mall': u'本店',
		'weizoom_mall': u'商户'
	}

	orders = [
		[u'订单号', u'下单时间',u'付款时间', u'商品名称', u'规格',
		u'商品单价', u'商品数量', u'支付方式', u'支付金额',u'现金支付金额',u'微众卡支付金额',
		u'运费', u'积分抵扣金额', u'优惠券金额',u'优惠券名称', u'订单状态', u'购买人',
		u'收货人', u'联系电话', u'收货地址省份', u'收货地址', u'发货人', u'备注', u'来源', u'物流公司', u'快递单号', u'发货时间']
	]

	order_list = None
	# 购买数量
	number = 0

	order_send_count = 0
	webapp_id = request.user_profile.webapp_id
	order_list = Order.objects.belong_to(webapp_id).order_by('-created_at')
	status_type = request.GET.get('status', None)
	if status_type:
		if status_type == 'refund':
			order_list = order_list.filter(status__in=[ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED])
		elif status_type == 'audit':
			order_list = order_list.filter(status__in=[ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED])

	#####################################
	# 订单除去 积分订单
	exclude_order_list = order_list.exclude(type=PRODUCT_INTEGRAL_TYPE)

	# 获取查询条件字典和时间筛选条件
	query_dict, date_interval = mall_api.get_select_params(request)
	product_name = ''
	if query_dict.has_key("product_name"):
		product_name = query_dict["product_name"]

	order_list = mall_api.get_orders_by_params(query_dict, date_interval, order_list)
	if product_name:
		# 订单总量
		order_count = len(order_list)
		finished_order_count = 0
		for order in order_list:
			if order.type != PRODUCT_INTEGRAL_TYPE and order.status == ORDER_STATUS_SUCCESSED:
				finished_order_count += 1
	else:
		order_count = order_list.count()
		finished_order_count = exclude_order_list.filter(status=ORDER_STATUS_SUCCESSED).count()
		order_list = list(order_list.all())


	#商品总额：
	total_product_money = 0.0
	# 订单金额
	total_order_money = 0.0
	# 支付金额
	final_total_order_money = 0.0
	# 微众卡支付金额
	weizoom_card_total_order_money = 0.0
	# 积分总和
	use_integral_count = 0
	# 积分抵扣总金额
	use_integral_money = 0.0
	#赠品总数
	total_premium_product = 0
	# 优惠劵价值总和
	coupon_money_count = 0
	# 直降总金额
	save_money_count = 0
	#
	#####################################

	# print 'begin step 1 order_list - '+str(time.time() - begin_time)
	# order_list = list(order_list.all())
	order_ids = []
	order_order_ids = []
	coupon_ids = []
	for o in order_list:
		order_ids.append(o.id)
		order_order_ids.append(o.order_id)
		if o.coupon_id:
			coupon_ids.append(o.coupon_id)

	# print 'begin step 2 relations - '+str(time.time() - begin_time)
	relations = {}
	product_ids = []
	promotion_ids = []
	model_value_ids = []
	# print 'begin step 2.5 order_list - '+str(time.time() - begin_time)
	# product_ids =
	for relation in OrderHasProduct.objects.filter(order__id__in=order_ids):
		# if test_index % pre_page == pre_page - 1:
		# 	print str(test_index) + 's-' +str(time.time() - begin_time)
		# 	print relation.order_id
		# test_index+=1
		key = relation.order_id
		promotion_ids.append(relation.promotion_id)
		if relations.get(key):
			relations[key].append(relation)
		else:
			relations[key] = [relation]
		if product_ids.count(relation.product_id) == 0:
			product_ids.append(relation.product_id)
		if relation.product_model_name != 'standard':
			for mod in relation.product_model_name.split('_'):
				i = mod.find(':') + 1
				if i > 0 and re.match('',mod[i:]) and model_value_ids.count(mod[i:]) == 0:
					model_value_ids.append(mod[i:])



	# print 'begin step 3 products - '+str(time.time() - begin_time)
	id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])

	# print 'begin step 4 coupons - '+str(time.time() - begin_time)
	coupon2role = {}
	role_ids = []
	from promotion.models import Coupon,CouponRule
	for coupon in Coupon.objects.filter(id__in=coupon_ids):
		coupon2role[coupon.id] = coupon.coupon_rule_id
		if role_ids.count(coupon.coupon_rule_id) == 0:
			role_ids.append(coupon.coupon_rule_id)
	role_id2role = dict([(role.id, role) for role in CouponRule.objects.filter(id__in=role_ids)])

	# print 'begin step 5 models - '+str(time.time() - begin_time)
	id2modelname = dict([(str(value.id), value.name) for value in ProductModelPropertyValue.objects.filter(id__in = model_value_ids)])
	# print 'end step 6 coupons - '+str(time.time() - begin_time)

	#获取order对应的会员
	webapp_user_ids = set([order.webapp_user_id for order in order_list])
	from modules.member.models import Member
	webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

	# print 'end step 6.7 - '+str(time.time() - begin_time)
	#获取order对应的赠品
	order2premium_product = {}
	order2promotion = dict([(order_promotion_relation.order_id, order_promotion_relation.promotion_result)for order_promotion_relation in OrderHasPromotion.objects.filter(order_id__in=order_ids, promotion_id__in=promotion_ids, promotion_type='premium_sale')])
	for order_id in order2promotion:
		temp_premium_products = []
		if order2promotion[order_id].has_key('premium_products'):
			for premium_product in order2promotion[order_id]['premium_products']:
				temp_premium_products.append({
					'name' : premium_product['name'],
					'count' : premium_product['count'],
					'price' : premium_product['price']
				})
		order2premium_product[order_id] = temp_premium_products


	#获取order对应的发货时间
	order2postage_time = dict([(log.order_id, log.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8')) for log in OrderOperationLog.objects.filter(order_id__in=order_order_ids, action="订单发货")])

	# print 'end step 8 order - '+str(time.time() - begin_time)
	#获取order对应的收货地区
	#area = get_str_value_by_string_ids(order.area)
	for order in order_list:
		# if test_index % pre_page == 0:
		# 	test_begin_time = time.time()
		# test_index+=1

		#获取order对应的member的显示名
		member = webappuser2member.get(order.webapp_user_id, None)
		if member:
			order.buyer_name = _handle_member_nickname(member.username_for_html)
			order.member_id = member.id
		else:
			order.buyer_name = u'未知'

		# 计算总和
		final_price = 0.0
		weizoom_card_money = 0.0
		total_price = order.get_total_price()
		use_integral = order.get_use_integral(webapp_id)
		if order.type == PAY_INTERFACE_COD:
			if order.status == ORDER_STATUS_SUCCESSED:
				final_price = order.final_price
				weizoom_card_money = order.weizoom_card_money
				final_total_order_money += order.final_price
				try:
					coupon_money_count += order.coupon_money
					weizoom_card_total_order_money += order.weizoom_card_money
					use_integral_money += order.integral_money
				except:
					pass
		else:
			if order.status in [2,3,4,5]:
				final_price = order.final_price
				weizoom_card_money = order.weizoom_card_money
				final_total_order_money += order.final_price
				try:
					coupon_money_count += order.coupon_money
					weizoom_card_total_order_money += order.weizoom_card_money
					use_integral_money += order.integral_money
				except:
					pass

		area = get_str_value_by_string_ids_new(order.area)
		if area:
			addr = '%s %s' % (area, order.ship_address)
		else:
			addr = '%s' % (order.ship_address)
		pay_type = PAYTYPE2NAME.get(order.pay_interface_type, '')

		if order.order_source:
			order.come = 'weizoom_mall'
		else:
			order.come = 'mine_mall'

		source = source_list.get(order.come, u'本店')
		if webapp_id != order.webapp_id:
			if request.manager.is_weizoom_mall:
				source = request.manager.username
			else:
				source = u'微众商城'

		orderRelations = relations.get(order.id,[])
		product_ids = [r.product_id for r in orderRelations]

		i = 0
		for relation in orderRelations:
			product = id2product[relation.product_id]
			model_value = ''
			for mod in relation.product_model_name.split('_'):
				mod_i = mod.find(':') + 1
				if mod_i > 0:
					model_value += '-' + id2modelname.get(mod[mod_i:], '')
				else:
					model_value = '-'
			models_name = ''
			coupon_name = ''
			coupon_money = ''
			promotion_name = ''
			promotion_type = ''
			#订单发货时间
			postage_time = order2postage_time.get(order.order_id, '')
			#付款时间
			if order.status > ORDER_STATUS_CANCEL and order.payment_time:
				payment_time = order.payment_time.strftime('%Y-%m-%d %H:%M').encode('utf8')
			else:
				payment_time = ''
			total_product_money += relation.price * relation.number
			#save_money_count += relation.total_price - relation.price * relation.number

			# if relation.promotion_id:
			# 	promotion_name = Promotion.objects.get(id=relation.promotion_id).name
			# 	promotion_type = Promotion.objects.get(id=relation.promotion_id).type
			if order.coupon_id:
				role_id = coupon2role.get(order.coupon_id,None)
				if role_id:
					if role_id2role[role_id].limit_product:
						if role_id2role[role_id].limit_product_id == relation.product_id:
							coupon_name = role_id2role[role_id].name+"（单品券）"
					elif i == 0:
						coupon_name = role_id2role[role_id].name+"（通用券）"


			if i == 0:
				if promotion_type == 1 and "(限时抢购)" not in product.name:
					product.name = u"(限时抢购)" + product.name

				if coupon_name:
					coupon_money = order.coupon_money

				type_name = type.get(order.type,'')

				if area:
					province = area.split(' ')[0]
				else:
					province = u''

				temp_leader_names = order.leader_name.split('|')
				remark = ''
				j = 1
				while j < len(temp_leader_names):
					remark += temp_leader_names[j]
					j += 1
				order.leader_name = temp_leader_names[0]
				save_money = str(order.edit_money).replace('.','').replace('-','') if order.edit_money else False
				orders.append([
					'%s%s'.encode('utf8') % (order.order_id, '-%s' % save_money if save_money else ''),
					order.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8'),
					payment_time,
					product.name.encode('utf8'),
					model_value[1:].encode('utf8'),
					relation.price,
					relation.number,
					payment_type[str(int(order.pay_interface_type))],
					final_price + weizoom_card_money,
					final_price,
					weizoom_card_money,
					order.postage,
					order.integral_money,
					coupon_money,
					coupon_name,
					status[str(order.status)].encode('utf8'),
					order.buyer_name.encode('utf8'),
					order.ship_name.encode('utf8'),
					order.ship_tel.encode('utf8'),
					province.encode('utf8'),
					addr.encode('utf8'),
					order.leader_name.encode('utf8'),
					remark.encode('utf8'),
					source.encode('utf8'),
					express_util.get_name_by_value(order.express_company_name).encode('utf8'),
					order.express_number.encode('utf8'),
					postage_time
				])
			else:
				if coupon_name:
					coupon_money = order.coupon_money
				orders.append([
				'%s%s'.encode('utf8') % (order.order_id, '-%s' % save_money if save_money else ''),
				order.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8'),
				payment_time,
				product.name,
				model_value[1:],
				relation.price,
				relation.number,
				payment_type[str(int(order.pay_interface_type))],
					u'',
					u'',
					u'',
					u'',
					u'',
				coupon_money,
				coupon_name,
				status[str(order.status)].encode('utf8'),
				order.buyer_name.encode('utf8'),
				order.ship_name.encode('utf8'),
				order.ship_tel.encode('utf8'),
				province.encode('utf8'),
				addr.encode('utf8'),
				order.leader_name.encode('utf8'),
				remark.encode('utf8'),
				source.encode('utf8'),
				express_util.get_name_by_value(order.express_company_name).encode('utf8'),
				order.express_number.encode('utf8'),
				postage_time
				])
			i = i +  1
			if order.id in order2premium_product:
				total_premium_product += len(order2premium_product[order.id])
				for premium_product in order2premium_product[order.id]:
					orders.append([
					'%s%s'.encode('utf8') % (order.order_id, '-%s' % save_money if save_money else ''),
					order.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8'),
					payment_time,
					u'(赠品)'+premium_product['name'],
						u'',
					premium_product['price'],
					premium_product['count'],
					payment_type[str(int(order.pay_interface_type))],
						u'',
						u'',
						u'',
						u'',
						u'',
						u'',
						u'',
					status[str(order.status)].encode('utf8'),
					order.buyer_name.encode('utf8'),
					order.ship_name.encode('utf8'),
					order.ship_tel.encode('utf8'),
					province.encode('utf8'),
					addr.encode('utf8'),
					order.leader_name.encode('utf8'),
					remark.encode('utf8'),
					source.encode('utf8'),
					express_util.get_name_by_value(order.express_company_name).encode('utf8'),
					order.express_number.encode('utf8'),
					postage_time
					])
				temp_premium_products = []
		# if test_index % pre_page == pre_page-1:
		# 	print str(test_index)+' - '+str(time.time() - test_begin_time)+'-'+str(time.time() - begin_time)
	orders.append([
		u'总计',
		u'订单量:'+str(order_count).encode('utf8'),
		u'已完成:'+str(finished_order_count).encode('utf8'),
		u'商品金额:' + str(total_product_money).encode('utf8'),
		u'支付总额:'+str(final_total_order_money + weizoom_card_total_order_money).encode('utf8'),
		u'现金支付金额:'+str(final_total_order_money).encode('utf8'),
		u'微众卡支付金额:'+str(weizoom_card_total_order_money).encode('utf8'),
		u'赠品总数:'+str(total_premium_product).encode('utf8'),
		u'积分抵扣总金额:'+str(use_integral_money).encode('utf8'),
		u'优惠劵价值总额:'+str(coupon_money_count).encode('utf8'),
		#u'直降金额总额:'+str(save_money_count).encode('utf8'),
	])
	# print 'end - '+str(time.time() - begin_time)

	return orders


def _handle_member_nickname(name):
	try:
		reobj = re.compile(r'\<span.*?\<\/span\>')
		name, number = reobj.subn('口', name)
		return u'{}'.format(name)
	except:
		return u''