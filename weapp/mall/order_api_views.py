# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import copy
import shutil

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
from django.db.models import Min

from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator

from models import *
from promotion import models as promotion_model
from modules.member.models import *
from modules.member import integral
from market_tools.tools.channel_qrcode.models import *
import module_api as mall_api
# import models
from market_tools.tools.weizoom_card.models import AccountHasWeizoomCardPermissions
from watchdog.utils import watchdog_error, watchdog_warning
from core.exceptionutil import unicode_full_stack
from core.restful_url_route import *

COUNT_PER_PAGE = 20

DEFAULT_CREATE_TIME = '2000-01-01 00:00:00'
def get_order_status_text(status):
	return STATUS2TEXT[status]

def _get_order_items(user, query_dict, sort_attr, query_string, count_per_page=15, cur_page=1, date_interval=None ,is_refund=False):
	orders, pageinfo, order_total_count, order_return_count = mall_api.get_order_list(user, query_dict, sort_attr, query_string, count_per_page, cur_page, date_interval, is_refund=is_refund)
	#构造返回的order数据
	items = []

	for order in orders:
		items.append({
			'id': order.id,
			'order_id': order.order_id,
			'status': order.get_status_text(),
			'total_price': float('%.2f' % order.final_price) if order.pay_interface_type != 9 or order.status == 5 else 0,
			'order_total_price': float('%.2f' % order.get_total_price()),
			'ship_name': order.ship_name,
			'buyer_name': order.buyer_name,
			'pay_interface_name': order.pay_interface_type_text,
			'created_at': datetime.strftime(order.created_at, '%Y-%m-%d %H:%M:%S'),
			'product_count': order.product_count,
			'customer_message': order.customer_message,
			'payment_time': order.payment_time,
			'come': order.come,
			'member_id': order.member_id,
			'type': order.type,
			'webapp_id': order.webapp_id,
			'integral': order.integral,
			'products': mall_api.get_order_products(order),
			'pay_interface_type':order.pay_interface_type,
			'order_status':order.status,
			'express_company_name': order.express_company_name,
			'express_number': order.express_number,
			'leader_name': order.leader_name,
			'remark': order.remark,
			'postage': '%.2f' % order.postage,
			'save_money': float(Order.get_order_has_price_number(order)) + float(order.postage) - float(order.final_price) - float(order.weizoom_card_money),
			'weizoom_card_money': float('%.2f' % order.weizoom_card_money),
			'pay_money': '%.2f' % (order.final_price + order.weizoom_card_money),
			'edit_money': str(order.edit_money).replace('.','').replace('-','') if order.edit_money else False
		})
	return items, pageinfo, order_total_count, order_return_count


########################################################################
# get_orders: 显示订单列表
########################################################################
EXPIRE_DAYS = 10
DELIVERY_DAYS = 2
@api(app='mall', resource='orders', action='get')
@login_required
def get_orders(request):
	return _get_orders_response(request)

########################################################################
# get_refund_orders: 显示退款订单列表
########################################################################
EXPIRE_DAYS = 10
DELIVERY_DAYS = 2
@api(app='mall', resource='refund_orders', action='get')
@login_required
def get_refund_orders(request):
	return _get_orders_response(request, True)

########################################################################
# get_refund_orders: 显示审核订单
########################################################################
EXPIRE_DAYS = 10
DELIVERY_DAYS = 2
@api(app='mall', resource='audit_orders', action='get')
@login_required
def get_audit_orders(request):
	return _get_orders_response(request, True)

def _get_orders_response(request, is_refund=False):
	is_weizoom_mall_partner = AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(request.manager.id)
	if request.manager.is_weizoom_mall:
		is_weizoom_mall_partner = False

	# 获取查询条件字典和时间筛选条件
	query_dict, date_interval = mall_api.get_select_params(request)

	# 处理排序
	sort_attr = request.GET.get('sort_attr', '-id')
	if sort_attr == 'created_at':
		sort_attr = 'id'
	if sort_attr == '-created_at':
		sort_attr = '-id'

	# 分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))

	# 用户
	user = request.manager
	query_string = request.META['QUERY_STRING']


	items, pageinfo, order_total_count, order_return_count = _get_order_items(user, query_dict, sort_attr, query_string, count_per_page, cur_page, date_interval=date_interval,is_refund=is_refund)

	# 获取该用户下的所有支付方式
	existed_pay_interfaces = mall_api.get_pay_interfaces_by_user(user)

	if is_weizoom_mall_partner or request.manager.is_weizoom_mall:
		is_show_source = True
	else:
		is_show_source = False

	response = create_response(200)
	if sort_attr == 'id':
		sort_attr = 'created_at'
	if sort_attr == '-id':
		sort_attr = '-created_at'

	response.data = {
		'items': items,
		'pageinfo': paginator.to_dict(pageinfo),
		'sortAttr': sort_attr,
		'is_show_source': is_show_source,
		'existed_pay_interfaces' : existed_pay_interfaces,
		'order_total_count': order_total_count,
		'order_return_count': order_return_count,
		'current_status_value': query_dict['status'] if query_dict.has_key('status') else '-1',
	}
	return response.get_response()

def _get_status_value(filter_value):
	if filter_value == '-1':
		return -1
	try:
		for item in filter_value.split('|'):
			if item.split(':')[0] == 'status':
				return int(item.split(':')[1])
		return -1
	except:
		return -1

########################################################################
# _get_order_products: 获得订单中的商品列表
########################################################################
def _get_order_products(order_id):
	relations = list(OrderHasProduct.objects.filter(order_id=order_id))
	product_ids = [r.product_id for r in relations]
	id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])

	products = []
	for relation in OrderHasProduct.objects.filter(order_id=order_id):
		product = copy.copy(id2product[relation.product_id])
		product.fill_specific_model(relation.product_model_name)
		products.append({
			'name': product.name,
			'thumbnails_url': product.thumbnails_url,
			'count': relation.number,
			'total_price': '%.2f' % relation.total_price,
			'custom_model_properties': product.custom_model_properties
		})

	return products

########################################################################
# get_order_products: 获得订单中的商品列表
########################################################################
@api(app='mall', resource='order_products', action='get')
@login_required
def get_order_products(request):
	order_id = request.GET['order_id']
	order = Order.objects.get(id=order_id)
	response = create_response(200)
	response.data = {
		'products': mall_api.get_order_products(order),
		'postage': '%.2f' % order.postage,
		'final_price': '%.2f' % order.final_price,
		'ship_name': order.ship_name,
		'ship_tel': order.ship_tel,
		'ship_address': order.ship_address,
		'area_str': order.get_str_area
	}
	return response.get_response()

########################################################################
# get_thanks_card_order_products: 获取感恩贺卡订单类型的商品列表
########################################################################
@login_required
def get_thanks_card_order_products(request):
	order_id = request.GET['order_id']
	response = create_response(200)

	thanks_card_orders = ThanksCardOrder.objects.filter(order_id=order_id)
	products = []
	for thanks_card_order in thanks_card_orders:
		product = {}
		product['thanks_secret'] = thanks_card_order.thanks_secret
		product['card_count'] = thanks_card_order.card_count
		product['listen_count'] = thanks_card_order.listen_count
		products.append(product)
	response.data = {
		'products': products
	}
	return response.get_response()


ORDERED_QUANTITY=1 #日订单量
ORDERED_SHIPED_QUANTITY=2  #日出货量
ORDERED_TOTAL_PRICE=3 #日总金额

MAX_VALUE = 6
#===============================================================================
# get_order_daily_trend : 获得订单图表数据
#===============================================================================
from core import chartutil
@login_required
def get_order_daily_trend(request):
	days = request.GET['days']
	type = int(request.GET['type']) # 1为柱状图，2为k线图

	elements = request.GET.get('element','')
	if elements:
	 	elements = elements.split(',')

	total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
	date_list = dateutil.get_date_range_list(low_date, high_date)

	if low_date == high_date:
		orders = Order.objects.filter(created_at__year=low_date.year, created_at__month=low_date.month, created_at__day=low_date.day)
	else:
		if days.find('-') == -1:
			date_list = date_list[:len(date_list)-1]
		else:
			total_days = total_days + 1
			high_date = high_date + timedelta(days = 1)
		orders = Order.objects.filter(created_at__range=(low_date, high_date))

	date2count = dict([(o, o) for o in range(1,7)])

	trend_ordered_quantity_values = []
	trend_shiped_quantity_values = []
	trend_order_weixin_values = []
	trend_order_shopex_values = []
	trend_listened_record_values = []
	trend_recorded_values = []
	x_labels = []

	max_value = MAX_VALUE
	for loop_date in date_list:
		x = (loop_date - low_date).days
		x_labels.append(str(x))
		for e in elements:
			orders_filter_by_date = orders.filter(created_at__year=loop_date.year, created_at__month=loop_date.month, created_at__day=loop_date.day)
			e = int(e)
			if ORDERED_QUANTITY == e:
				count = orders_filter_by_date.count()
				dot = {'x':x, 'y':count}
				max_value = __get_max_values(count, max_value)
				trend_ordered_quantity_values.append(dot)

			if ORDERED_SHIPED_QUANTITY == e:
				count = 0
				for order in orders_filter_by_date.filter(status__gte=ORDER_STATUS_PAYED_SHIPED):
				 	for order_has_product in OrderHasProduct.objects.filter(order=order):
				 		count = count + order_has_product.number
				dot = {'x':x, 'y':count}
				max_value = __get_max_values(count, max_value)
				trend_shiped_quantity_values.append(dot)

			if ORDERED_TOTAL_PRICE == e:
				total_price = 0
				for order in orders_filter_by_date.filter(status=ORDER_STATUS_SUCCESSED):
					total_price = total_price+order.total_price
				dot = {'x':x, 'y':total_price}

				max_value = __get_max_values(total_price, max_value)
				trend_order_shopex_values.append(dot)

	values = []
	for e in elements:
		e = int(e)
		if ORDERED_QUANTITY == e:

			values.append({'title':u'日订单量', 'values':trend_ordered_quantity_values})

		if ORDERED_SHIPED_QUANTITY == e:
			values.append({'title':u'日出货量', 'values':trend_shiped_quantity_values})

		if ORDERED_TOTAL_PRICE == e:
			values.append({'title':u'日总金额', 'values':trend_order_shopex_values})

	if type == 1:

		infos = {
			'title': '',
			'x_labels': x_labels,
			'bar_title': 'ttt',
			'x_legend_text': u'日期',
			'values': values,
			'max_value': max_value,
			'date_info': {'days':total_days, 'low_date':low_date}
		}
		chart_json = chartutil.create_bar_chart(infos)
	else:
		infos = {
			'title': '',
			'values': values,
			'date_info': {'days':total_days, 'low_date':low_date},
			'max_value': max_value
		}
		chart_json = chartutil.create_wine_line_chart(infos, display_today_data=False)

	return HttpResponse(chart_json, 'application/json')

def __get_max_values(count, max_value):
	if count > max_value:
		#MAX_VALUE = count
		return count
	else:
		return max_value

@api(app='mall', resource='channel_qrcode_payed_orders', action='get')
def get_channel_qrcode_payed_orders(request):
	channel_qrcode_id = request.GET.get('id', None)
	relations = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=channel_qrcode_id)
	setting_id2count = {}
	member_id2setting_id = {}
	member_ids = []
	for r in relations:
		member_ids.append(r.member_id)
		member_id2setting_id[r.member_id] = r.channel_qrcode_id
		if r.channel_qrcode_id in setting_id2count:
			setting_id2count[r.channel_qrcode_id] += 1
		else:
			setting_id2count[r.channel_qrcode_id] = 1

	webapp_users = WebAppUser.objects.filter(member_id__in=member_ids)
	webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
	webapp_user_ids = set(webapp_user_id2member_id.keys())
	orders = Order.objects.filter(webapp_user_id__in=webapp_user_ids, status=ORDER_STATUS_SUCCESSED).order_by('-created_at')
	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

	#获取order对应的会员
	webapp_user_ids = set([order.webapp_user_id for order in orders])
	from modules.member.models import Member
	webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

	#获得order对应的商品数量
	order_ids = [order.id for order in orders]
	order2productcount = {}
	for relation in OrderHasProduct.objects.filter(order_id__in=order_ids):
		order_id = relation.order_id
		if order_id in order2productcount:
			order2productcount[order_id] = order2productcount[order_id] + 1
		else:
			order2productcount[order_id] = 1
	#构造返回的order数据
	items = []
	today = datetime.today()
	for order in  orders:
		#获取order对应的member的显示名
		member = webappuser2member.get(order.webapp_user_id, None)
		if member:
			order.buyer_name = member.username_for_html
		else:
			order.buyer_name = u'未知'



		items.append({
			'id': order.id,
			'order_id': order.order_id,
			'status': get_order_status_text(order.status),
			'total_price': order.final_price,
			'ship_name': order.ship_name,
			'buyer_name': order.buyer_name,
			'pay_interface_name': PAYTYPE2NAME.get(order.pay_interface_type, u''),
			'created_at': datetime.strftime(order.created_at, '%m-%d %H:%M'),
			'product_count': order2productcount.get(order.id, 0),
			# 'products': product_items,
			'customer_message': order.customer_message
		})


	response = create_response(200)
	response.data = {
		'items': items,
		'sortAttr': request.GET.get('sort_attr', '-created_at'),
		'pageinfo': paginator.to_dict(pageinfo),
	}
	return response.get_response()

#===============================================================================
# get_thanks_card_orders : 获得感恩贺卡类型的订单列表
#===============================================================================
def get_thanks_card_orders(request):
	webapp_id = request.manager.get_profile().webapp_id

	orders = None
	secret = request.GET.get('secret')
	if secret:
		filter_ids = []
		thanks_card_orders = ThanksCardOrder.objects.filter(thanks_secret=secret)
		for thanks_card_order in thanks_card_orders:
			filter_ids.append(thanks_card_order.order_id)
		orders = Order.objects.filter(webapp_id=webapp_id, type=THANKS_CARD_ORDER, id__in=filter_ids)
	else:
		orders = Order.objects.filter(webapp_id=webapp_id, type=THANKS_CARD_ORDER)

	#处理搜索
	query = request.GET.get('query', None)
	if query:
		orders = orders.filter(order_id=query)
	#处理过滤
	filter_attr = request.GET.get('filter_attr', None)
	filter_value = int(request.GET.get('filter_value', -1))
	if filter_attr and (filter_value != -1):
		params = {filter_attr: filter_value}
		orders = orders.filter(**params)
	#处理排序
	sort_attr = request.GET.get('sort_attr', 'created_at');
	if sort_attr != 'created_at':
		orders = orders.order_by(sort_attr)

	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

	#构造返回的order数据
	items = []
	today = datetime.today()
	for order in  orders:
		payment_time = None
		if order.payment_time is None:
			payment_time = ''
		elif datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M:%S') == DEFAULT_CREATE_TIME:
			payment_time = ''
		else:
			payment_time = datetime.strftime(order.payment_time, '%m-%d %H:%M')

		#感恩贺卡信息
		thanks_secret_count = 0 	#感恩密码数量
		card_count = 0 	#贺卡生成个数
		listen_count = 0 	#贺卡收听次数
		thanks_card_orders = ThanksCardOrder.objects.filter(order_id=order.id)
		for thanks_card_order in thanks_card_orders:
			if thanks_card_order.thanks_secret is not '':
				thanks_secret_count += 1
			card_count += thanks_card_order.card_count
			listen_count += thanks_card_order.listen_count

		items.append({
			'id': order.id,
			'order_id': order.order_id,
			'status': get_order_status_text(order.status),
			'payment_time': payment_time,
			'thanks_secret_count': thanks_secret_count,
			'card_count': card_count,
			'listen_count': listen_count
		})

	response = create_response(200)
	response.data = {
		'items': items,
		'pageinfo': paginator.to_dict(pageinfo),
		'sortAttr': sort_attr
	}
	return response.get_response()


#===============================================================================
# save_order_filter : 保存订单的筛选条件
#===============================================================================
@login_required
def save_order_filter(request):
	filter_value = request.GET.get('filter_value', '')
	filter_name = request.GET.get('filter_name', '')

	filter = UserHasOrderFilter.create(request.manager, filter_name, filter_value)

	response = create_response(200)
	response.data = {
		'filter_id': filter.id
	}
	return response.get_response()

#===============================================================================
# delete_order_filter : 删除订单的筛选条件
#===============================================================================
@login_required
def delete_order_filter(request):
	filter_id = request.GET.get('id', '')
	try:
		UserHasOrderFilter.objects.get(id=filter_id).delete()
		response = create_response(200)
	except:
		response = create_response(500)
		response.errMsg = u'删除订单的筛选条件失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()

	return response.get_response()


########################################################################
# get_order_filters: 获得订单的所有筛选标签
########################################################################
@login_required
def get_order_filters(request):
	response = create_response(200)
	response.data = {
		'filters': mall_api.get_order_fitlers_by_user(request.manager)
	}
	return response.get_response()

########################################################################
# get_order_filter_params: 获得订单的所有筛选条件
########################################################################
@api(app='mall', resource='order_filter_params', action='get')
@login_required
def get_order_filter_params(request):
	response = create_response(200)
	# 类型
	type = [{'name': u'普通订单', 'value': PRODUCT_DEFAULT_TYPE},
			{'name': u'测试订单', 'value': PRODUCT_TEST_TYPE},
			{'name': u'积分商品', 'value': PRODUCT_INTEGRAL_TYPE}]
	# 状态
	# status = [{'name': u'待支付', 'value': ORDER_STATUS_NOT},
	# 		{'name': u'已取消', 'value': ORDER_STATUS_CANCEL},
	# 		{'name': u'待发货', 'value': ORDER_STATUS_PAYED_NOT_SHIP},
	# 		{'name': u'已发货', 'value': ORDER_STATUS_PAYED_SHIPED},
	# 		{'name': u'已完成', 'value': ORDER_STATUS_SUCCESSED}]
	status_type = request.POST.get('status', None)

	status = []
	status_dict = {}
	if status_type == 'audit':
		status_dict = AUDIT_STATUS2TEXT
	elif status_type == 'refund':
		status_dict = REFUND_STATUS2TEXT
	else:
		current_status_dict =  copy.copy(STATUS2TEXT)
		#del current_status_dict[ORDER_STATUS_REFUNDED]
		status_dict = current_status_dict

	for key, value in status_dict.items():
		if key != ORDER_STATUS_PAYED_SUCCESSED:
			status.append({'name': value, 'value':key})

	# 来源
	source = [{'name': u'本店', 'value': 0},
			{'name': u'商城', 'value': 1}]

	is_weizoom_mall_partner = AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(request.manager.id)
	if not is_weizoom_mall_partner and not request.manager.is_weizoom_mall:
		source = []

	# 支付方式
	pay_interface_type = mall_api.get_pay_interfaces_by_user(request.manager)
	#pay_interface_type.append({'pay_name':u'优惠抵扣','data_value':PAY_INTERFACE_PREFERENCE})

	# 有该营销工具才会显示此选项
	# user_market_tool_modules = request.manager.market_tool_modules
	# if 'delivery_plan' in user_market_tool_modules:
	# 	type.append({'name': u'套餐订单', 'value': PRODUCT_DELIVERY_PLAN_TYPE})
	# if 'thanks_card' in user_market_tool_modules:
	# 	type.append({'name': u'贺卡订单', 'value': THANKS_CARD_ORDER})

	response.data = {
		'type': type,
		'status': status,
		'pay_interface_type': pay_interface_type,
		'source': source
	}
	return response.get_response()


########################################################################
# update_order_delivery: 发货
########################################################################
@api(app='mall', resource='order_delivery', action='update')
@login_required
def update_order_delivery(request):
	order_id = request.GET.get('order_id', None)
	express_company_name = request.GET.get('express_company_name')
	express_number = request.GET.get('express_number')
	leader_name = request.GET.get('leader_name')
	is_update_express = request.GET.get('is_update_express')
	is_update_express = True if is_update_express == 'true' else False
	is_success = mall_api.ship_order(order_id, express_company_name, express_number, request.manager.username, leader_name=leader_name, is_update_express=is_update_express)

	if is_success:
		response = create_response(200)
	else:
		response = create_response(500)
	return response.get_response()


########################################################################
# bulk_shipments: 批量发货
########################################################################
@api(app='mall', resource='bulk_shipments', action='update')
@login_required
def update_bulk_shipments(request):
	response = create_response(200)
	file_url = request.POST.get('file_url', '')
	# 读取文件
	json_data, error_rows = _read_file(file_url[1:])

	# 批量处理订单
	success_data, error_items = mall_api.batch_handle_order(json_data, request.manager)
	# print '------------------'
	# print json_data
	# print u'成功处理订单'
	# print success_data
	# print u'失败处理订单'
	# print 'error_rows'
	# print error_rows
	# print 'error_items'
	# print error_items

	# __clean_file(file_url[1:])
	response.data = {
		'success_count': len(success_data),
		'error_count': len(error_rows) + len(error_items),
		'error_items': error_items
	}
	return response.get_response()


def _read_file(file_url):
	data = []
	error_rows = []

	import csv
	file_path = os.path.join(settings.PROJECT_HOME, '..', file_url)

	with open(file_path) as csvfile:
		reader = csv.reader(csvfile, delimiter=':', quotechar='|')
		for row in reader:
			try:
				if len(row) > 0:
					item = dict()
					row = row[0].split(',')
					if not (len(row[0]) or len(row[1]) or len(row[2])) or not row[0].isdigit():
						continue
					item['order_id'] = row[0]
					item['express_company_name'] = row[1].decode('gbk')
					item['express_number'] = row[2]
					data.append(item)
			except:
				error_rows.append(', '.join(row))
			# print(', '.join(row))

		csvfile.close()

	if len(error_rows) > 0:
		alert_message = u"bulk_shipments批量发货 读取文件错误的行, error_rows:{}".format(error_rows)
		watchdog_warning(alert_message)

	return data, error_rows

def __clean_file(file_url):
	import os
	try:
		file_path = os.path.join(settings.PROJECT_HOME, '..', file_url)
		os.remove(file_path)
	except:
		alert_message = u"__clean_file cause:\n{}".format(unicode_full_stack())
		watchdog_warning(alert_message)

########################################################################
# get_orders: 显示订单列表
########################################################################
EXPIRE_DAYS = 10
DELIVERY_DAYS = 2
@api(app='mall', resource='order_remark', action='update')
@login_required
def update_remark_order(request):
	order_id = request.POST.get('order_id', None)
	remark = request.POST.get('remark', None)

	Order.objects.filter(id=order_id).update(remark=remark)

	response = create_response(200)
	return response.get_response()



########################################################################
# update_order_info: 更新订单信息
########################################################################
@api(app='mall', resource='order_info', action='update')
@login_required
def update_order_info(request):
	order_id = request.POST['order_id']
	order_status = request.POST.get('order_status', None)
	bill_type = int(request.POST.get('bill_type', ORDER_BILL_TYPE_NONE))
	# postage = request.POST.get('postage', None)
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
					#integral.increase_for_self_buy(order.webapp_user_id, order.webapp_id, order.final_price)
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

	# if postage:
	# 	if float(order.postage) != float(postage):
	# 		operate_log = operate_log + u' 修改邮费'
	# 		order.final_price = order.final_price - order.postage + float(postage) #更新最终价格
	# 		order.postage = postage

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
			order.edit_money = (order.product_price + order.postage) - (order.coupon_money + order.integral_money + order.weizoom_card_money + order.promotion_saved_money) - order.final_price
			# TODO 临时解决方案，需要数据清理
			promotions = OrderHasPromotion.objects.filter(order_id=order.id)
			for promotion in promotions:
				if promotion.promotion_type == 'flash_sale':
					order.edit_money += json.loads(promotion.promotion_result_json)['promotion_saved_money']


	if len(operate_log.strip()) > 0:
		mall_api.record_operation_log(order.order_id, request.manager.username, operate_log)

	order.save()

	response = create_response(200)
	return response.get_response()
