# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os, re
import json
import MySQLdb
import random
import string
import copy
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count
from django.core.cache import cache

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from core.dateutil import get_today
from tools.regional import views as regional_util
from tools.regional.models import *
from tools.regional.views import get_str_value_by_string_ids

from excel_response import ExcelResponse

from account.models import *
from models import *
from modules.member.models import IntegralStrategySttings,Member
from modules.member import integral

from mall import module_api as mall_api 

import util as mall_util

import export
import module_api as mall_api

from watchdog.utils import watchdog_alert, watchdog_error
from webapp.modules.mall import signals as mall_signals
from tools.express import util as express_util
from mall.promotion.models import Coupon, CouponRule


COUNT_PER_PAGE = 20

# Termite GENERATED START: views

FIRST_NAV_NAME = 'webapp'
SHOP_ORDERS_NAV = 'mall-orders'


########################################################################
# list_orders: 显示订单列表
########################################################################
@login_required
def list_orders(request):
	webapp_id = request.user_profile.webapp_id
	weizoom_mall_order_ids = WeizoomMallHasOtherMallProductOrder.get_order_ids_for(webapp_id)
	#TODO: performance
	has_order = (Order.objects.filter(Q(webapp_id=webapp_id)|Q(order_id__in=weizoom_mall_order_ids)).count() > 0)

	MallCounter.clear_unread_order(webapp_owner_id=request.user.id) #清空未读订单数量

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SHOP_ORDERS_NAV,
		'has_order': has_order,
		'STATUS2TEXT': STATUS2TEXT
	})
	return render_to_response('mall/editor/orders.html', c)


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
			mall_api.record_status_log(order.order_id, order.status, order_status, request.user.username)
			order.status = order_status
		
			try:
				if expired_status < ORDER_STATUS_SUCCESSED and int(order_status) == ORDER_STATUS_SUCCESSED and expired_status != ORDER_STATUS_CANCEL:
					integral.increase_father_member_integral_by_child_member_buyed(order.webapp_user_id, order.webapp_id)
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
		mall_api.record_operation_log(order.order_id, request.user.username, operate_log)

	order.save()		
	
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


########################################################################
# update_order_status: 更新订单状态
########################################################################
@login_required
def update_order_status(request):
	order_id = request.GET['order_id']
	action = request.GET['action']
	order = Order.objects.get(id=order_id)
	
	mall_api.update_order_status(request.user, action, order, request)

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
	mall_api.ship_order(order_id, express_company_name, express_number, request.user.username, leader_name=leader_name, is_update_express=is_update_express)

	# target_status = ORDER_STATUS_PAYED_SHIPED

	#order = Order.objects.get(id=order_id)
	# Order.objects.filter(id=order_id).update(status=target_status, express_company_name=express_company_name, express_number=express_number)
	# operate_log = u' 修改状态'
	# mall_api.record_status_log(order.order_id, request.user, order.status, target_status)			
	
	return HttpResponseRedirect('/mall/editor/order/get/?order_id=%s' %order_id)


########################################################################
# get_order_detail: 显示订单详情
########################################################################
@login_required
def get_order_detail(request):
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
		order.products = mall_api.get_order_products(order.id)

		order.area = regional_util.get_str_value_by_string_ids(order.area)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SHOP_ORDERS_NAV,
			'order': order,
			'is_order_not_payed': (order.status == ORDER_STATUS_NOT),
			'coupon': coupon,
			'order_operation_logs': mall_api.get_order_operation_logs(order.order_id),
			'order_status_logs': mall_api.get_order_status_logs(order.order_id),
			'order_has_delivery_times': OrderHasDeliveryTime.objects.filter(order=order)
		})

		return render_to_response('mall/editor/order_detail.html', c)
	else:		
		return HttpResponseRedirect('/mall/editor/orders/')


########################################################################
# export_orders:  导出订单列表
########################################################################
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
		'5':u'已完成'
	}

	type = ORDER_TYPE2TEXT

	source_list = {
		'mine_mall': u'本店',
		'weizoom_mall': u'商户'
	}

	orders = [
		[u'下单时间',u'订单号',u'订单金额',u'支付类型',u'支付金额', 
		u'订单状态', u'订单类型',u'商品名称',u'规格',u'商品数', u'购买人',
		u'来源', u'积分', u'优惠券名称', u'优惠券金额',u'收货人',u'联系电话',
		u'收货地址省份',u'收货地址',u'发货人',u'备注',u'物流公司',u'快递单号']
	]

	order_list = None
	# 购买数量
	number = 0

	order_send_count = 0
	webapp_id = request.user_profile.webapp_id
	order_list = Order.objects.belong_to(webapp_id).order_by('-created_at')

	# 搜索
	query = request.GET.get('query', '').strip()
	ship_name = request.GET.get('ship_name', '').strip()
	ship_tel = request.GET.get('ship_tel', '').strip()

	# 填充query
	query_dict = dict()
	if len(query):
		query_dict['order_id'] = query
	if len(ship_name):
		query_dict['ship_name'] = ship_name
	if len(ship_tel):
		query_dict['ship_tel'] = ship_tel

	#处理搜索
	if len(query_dict):
		order_list = order_list.filter(**query_dict)
		
	# 筛选条件
	source = None
	filter_value = request.GET.get('filter_value', '')	
	if filter_value and (filter_value != '-1'):
		params, source_value = UserHasOrderFilter.get_filter_params_by_value(filter_value)
		order_list = order_list.filter(**params)
		if source_value == 1:
			source = 'weizoom_mall'
		elif source_value == 0:
			source = 'mine_mall'

	if request.user.is_weizoom_mall:
		weizoom_mall_order_ids = WeizoomMallHasOtherMallProductOrder.get_orders_weizoom_mall_for_other_mall(webapp_id)
	else:
		weizoom_mall_order_ids = WeizoomMallHasOtherMallProductOrder.get_order_ids_for(webapp_id)
	
	order_id_list = []
	if source:
		for order in order_list:
			if weizoom_mall_order_ids:
				if order.order_id in weizoom_mall_order_ids:
					if request.user.is_weizoom_mall:
						order.come = 'weizoom_mall'
					else:
						order.come = 'weizoom_mall'
				else:
					order.come = 'mine_mall'	
			else:
				order.come = 'mine_mall'
			if source and order.come != source:
				continue
			order_id_list.append(order.id)

	if source:
		order_list = order_list.filter(id__in=order_id_list)

	###################################################
	# 处理 时间区间筛选
	# 时间区间
	try:
		date_interval = request.GET.get('date_interval', '')
		if date_interval:
			date_interval = date_interval.split('|')
		else:
			date_interval = None
	except:
		date_interval = None
	if date_interval:
		start_time = date_interval[0]+' 00:00:00'
		end_time = date_interval[1]+' 23:59:59'
		order_list = order_list.filter(created_at__gte=start_time, created_at__lt=end_time)
		
	#####################################
	# 订单除去 积分订单
	exclude_order_list = order_list.exclude(type=PRODUCT_INTEGRAL_TYPE)
	#####################################
	# 订单总量
	order_count = order_list.count()
	finished_order_count = exclude_order_list.filter(status=ORDER_STATUS_SUCCESSED).count()
	
	# 订单金额
	total_order_money = 0.0
	# 支付金额
	final_total_order_money = 0.0
	# 积分总和
	use_integral_count = 0
	# 优惠劵价值总和
	coupon_money_count = 0
	#####################################

	# print 'begin step 1 order_list - '+str(time.time() - begin_time)
	order_list = list(order_list.all())
	order_ids = []
	coupon_ids = []
	for o in order_list:
		order_ids.append(o.id)
		if o.coupon_id:
			coupon_ids.append(o.coupon_id)

	# print 'begin step 2 relations - '+str(time.time() - begin_time)
	relations = {}
	product_ids = []
	model_value_ids = []
	# print 'begin step 2.5 order_list - '+str(time.time() - begin_time)
	# product_ids = 
	for relation in OrderHasProduct.objects.filter(order__id__in=order_ids):
		# if test_index % pre_page == pre_page - 1:
		# 	print str(test_index) + 's-' +str(time.time() - begin_time)
		# 	print relation.order_id
		# test_index+=1
		key = relation.order_id
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
	for coupon in Coupon.objects.filter(id__in=coupon_ids):
		coupon2role[coupon.id] = coupon.coupon_rule_id
		if role_ids.count(coupon.coupon_rule_id) == 0:
			role_ids.append(coupon.coupon_rule_id)
	role2name = dict([(role.id, role.name) for role in CouponRule.objects.filter(id__in=role_ids)])

	# print 'begin step 5 models - '+str(time.time() - begin_time)
	id2modelname = dict([(str(value.id), value.name) for value in ProductModelPropertyValue.objects.filter(id__in = model_value_ids)])
	# print 'end step 6 coupons - '+str(time.time() - begin_time)
	
	#获取order对应的会员
	webapp_user_ids = set([order.webapp_user_id for order in order_list])
	webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

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
		final_price = order.get_final_price(webapp_id)
		total_price = order.get_total_price()
		use_integral = order.get_use_integral(webapp_id)
		if order.status == ORDER_STATUS_SUCCESSED and order.type != PRODUCT_INTEGRAL_TYPE:
			final_total_order_money += final_price
			total_order_money += total_price
			coupon_money_count += order.coupon_money
			if use_integral:
				use_integral_count += use_integral

		area = get_str_value_by_string_ids(order.area)
		if area:
			addr = '%s %s' % (area, order.ship_address)
		else:
			addr = '%s' % (order.ship_address)
		pay_type = PAYTYPE2NAME.get(order.pay_interface_type, '')

		if weizoom_mall_order_ids:
			if order.order_id in weizoom_mall_order_ids:
				if request.user.is_weizoom_mall:
					order.come = 'weizoom_mall'
				else:
					order.come = 'weizoom_mall'
			else:
				order.come = 'mine_mall'	
		else:
			order.come = 'mine_mall'

		source = source_list.get(order.come, u'本店')
		if webapp_id != order.webapp_id:
			if request.user.is_weizoom_mall:
				source = u'商户'
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
			if order.coupon_id:
				role_id = coupon2role.get(order.coupon_id,None)
				if role_id:
					coupon_name = role2name[role_id]

			if i == 0:
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

				orders.append([
					order.created_at.strftime('%Y-%m-%d %H:%M'),
					order.order_id,
					total_price,
					pay_type,
					final_price,
					status[str(order.status)],
					type_name,
					product.name,
					model_value[1:],
					relation.number,
					order.buyer_name,
					source,
					use_integral,
					coupon_name,
					order.coupon_money,
					order.ship_name,
					order.ship_tel,
					province,
					addr,
					order.leader_name,
					remark,
					express_util.get_name_by_value(order.express_company_name),
					order.express_number
				])
			else:
				orders.append([
					'',
					'',
					'',
					'',
					'',
					'',
					'',
				product.name,
				model_value[1:],
				relation.number,
					'',
					'',
					'',
					'',
					'',
					'',
					'',
					'',
					''
				])
			i = i +  1
		# if test_index % pre_page == pre_page-1:
		# 	print str(test_index)+' - '+str(time.time() - test_begin_time)+'-'+str(time.time() - begin_time)
	orders.append([
		u'总计',
		u'订单量:'+str(order_count),
		u'已完成:'+str(finished_order_count),
		u'订单金额:'+str(total_order_money),
		u'支付金额:'+str(final_total_order_money),
		u'积分总和:'+str(use_integral_count),
		u'优惠劵价值总和:'+str(coupon_money_count)
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