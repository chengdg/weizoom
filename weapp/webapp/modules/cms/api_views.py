# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core import dateutil

from models import *

# Termite GENERATED START: api_views


# MODULE START: productcategory
########################################################################
# update_productcategory_display_index: 修改排列顺序
########################################################################
@login_required
def update_productcategory_display_index(request):
	ids = request.GET['ids'].split('_')
	for index, id in enumerate(ids):
		Productcategory.objects.filter(id=id).update(display_index=index+1)

	response = create_response(200)
	return response.get_response()

# MODULE END: productcategory

@login_required
def check_coupon_name_duplicate(request):
	to_check_name = request.POST['name']

	coupon_pools = CouponPool.objects.filter(name=to_check_name)
	if coupon_pools.count() > 0:
		response = create_response(601)
		response.errMsg = u"已存在名称为'{}'的优惠券".format(to_check_name)
		return response.get_response()
	else:
		response = create_response(200)
		return response.get_response()


# MODULE START: product
########################################################################
# update_product_display_index: 修改排列顺序
########################################################################
@login_required
def update_product_display_index(request):
	ids = request.GET['ids'].split('_')
	for index, id in enumerate(ids):
		Product.objects.filter(id=id).update(display_index=index+1)

	response = create_response(200)
	return response.get_response()

# MODULE END: product
# Termite GENERATED END: api_views
########################################################################
# get_products: 获取product列表
########################################################################
@login_required
def get_products(request):
	query = request.GET.get('query', None)
		
	#处理排序
	sort_attr = request.GET.get('sort_attr', 'created_at');
	products = Product.objects.filter(owner=request.user).order_by(sort_attr)

	#处理搜索
	if query:
		products = products.filter(name__icontains=query)
	products = list(products)

	#获取product关联的category集合
	id2product = dict([(product.id, product) for product in products])
	product_ids = []
	for product in products:
		product.categories = []
		id2product[product.id] = product
		product_ids.append(product.id)

	category_ids = []
	category2products = {}
	for relation in CategoryHasProduct.objects.filter(product_id__in=product_ids):
		category_id = relation.category_id
		product_id = relation.product_id
		category_ids.append(category_id)
		category2products.setdefault(category_id, []).append(product_id)

	for category in ProductCategory.objects.filter(id__in=category_ids):
		for product_id in category2products[category.id]:
			id2product[product_id].categories.append({
				'id': category.id,
				'name': category.name
			})

	# 构造返回数据
	items = []
	for product in products:
		items.append({
			'id': product.id,
			'name': product.name,
			'thumbnails_url': product.thumbnails_url,
			'categories': product.categories,
			'price': product.price,
			'created_at': datetime.strftime(product.created_at, '%Y-%m-%d %H:%M')
		})
	
	response = create_response(200)
	response.data = {
		'items': items,
		'sortAttr': sort_attr
	}
	return response.get_response()


def _get_product_info_json(product, category_id=None):
	product_info = dict()
	product_info['id'] = product.id
	product_info['name'] = product.name
	product_info['created_at'] = datetime.strftime(product.created_at, '%Y-%m-%d %H:%M')
	product_info['physical_unit'] = product.physical_unit
	product_info['thumbnails_url'] = product.thumbnails_url
	product_info['introduction'] = product.introduction
	product_info['price'] = '%.2f' % float(product.price)
	product_info['category_id'] =category_id
	category_has_product = CategoryHasProduct.objects.filter(category_id=category_id, product=product)
	if category_has_product.count() > 0:
		product_info['is_category_pro'] = '1'
	else:
		product_info['is_category_pro'] = '0'

	if category_id is None:
		category_json = []
		product_has_categories = CategoryHasProduct.objects.filter(product=product)
		for product_has_category in product_has_categories:
			category = product_has_category.category
			category_info = _get_product_category_info_json(category, False)
			category_json.append(category_info)
		product_info['categories'] = category_json
	return product_info


########################################################################
# get_category_selectable_products: 获取category可选择的product列表
########################################################################
@login_required
def get_category_selectable_products(request):
	category_id = request.GET['category_id']

	products = Product.objects.filter(owner=request.user)
	query = request.GET.get('query', None)
	
	if query:
		products = products.filter(name__icontains=query)
	
	#获取未分类的product id
	product_ids = set(products.values_list('id', flat=True))
	categorized_product_ids = set([relation.product_id for relation in CategoryHasProduct.objects.filter( ~Q(category_id=category_id) )])
	selectable_product_ids = product_ids - categorized_product_ids

	#获取category下已存在的product id
	category_product_ids = set([relation.product_id for relation in CategoryHasProduct.objects.filter(category_id=category_id)])

	# 构造返回数据
	is_all_product_selected = True
	items = []
	if len(selectable_product_ids) > 0:
		for product in Product.objects.filter(id__in=selectable_product_ids):
			item = {
				'id': product.id,
				'name': product.name,
				'thumbnails_url': product.thumbnails_url,
				'price': product.price,
				'created_at': datetime.strftime(product.created_at, '%Y-%m-%d %H:%M'),
				'is_selected': False
			}
			if product.id in category_product_ids:
				item['is_selected'] = True
			else:
				is_all_product_selected = False
			items.append(item)
	else:
		is_all_product_selected = False
	
	response = create_response(200)
	data = {
		'items': items,
		'category_id': category_id,
		'sortAttr': 'id',
		'isAllProductSelected': is_all_product_selected
	}
	response.data = data
	
	return response.get_response()


########################################################################
# get_categories: 获得分类列表
########################################################################
@login_required
def get_categories(request):
	query = request.GET.get('query', None)
		
	#处理排序
	sort_attr = request.GET.get('sort_attr', 'created_at');
	categories = ProductCategory.objects.filter(owner=request.user).order_by(sort_attr)

	#处理搜索
	if query:
		categories = categories.filter(name__icontains=query)
	
	items = []
	for category in  categories:
		items.append({
			'id': category.id,
			'name': category.name,
			'count': category.product_count,
			'created_at': datetime.strftime(category.created_at, '%Y-%m-%d %H:%M')
		})
	
	response = create_response(200)
	response.data = {
		'items': items,
		'sortAttr': sort_attr
	}
	return response.get_response()


# def _get_product_category_info_json(productcategory, from_categories=True):
# 	category_info = dict()
# 	category_info['id'] = productcategory.id
# 	category_info['name'] = productcategory.name
# 	category_info['created_at'] = datetime.strftime(productcategory.created_at, '%Y-%m-%d %H:%M')
	
# 	category_has_products = CategoryHasProduct.objects.filter(category=productcategory)
# 	category_info['count'] = productcategory.product_count
# 	if from_categories:
# 		category_products = []
# 		for category_has_product in category_has_products:
# 			product = category_has_product.product
# 			category_products.append(_get_product_info_json(product, category_has_product.id))
# 		category_info['products'] = category_products


# 	return category_info

########################################################################
# list_orders: 显示订单列表
########################################################################
# EXPIRE_DAYS = 10
# @login_required
# def get_orders(request):
# 	order_id = request.GET.get('order_id', '')
# 	order_source = request.GET.get('source', '')
# 	order_status = request.GET.get('status', '')
# 	order_price = request.GET.get('total_price', None)
# 	#获取当前页数
# 	cur_page = int(request.GET.get('page', '1'))
# 	#获取每页个数
# 	webapp_id = request.user.get_profile().webapp_id
# 	created_at = request.GET.get('created_at', None)
# 	if created_at:
# 		orders = Order.objects.filter(webapp_id=webapp_id).order_by(created_at)
# 	elif order_price:
# 		orders = Order.objects.filter(webapp_id=webapp_id).order_by(order_price)
# 	else:
# 		orders = Order.objects.filter(webapp_id=webapp_id)
			
# 	count = int(request.GET.get('count', 25))
	
# 	if order_id and order_id != -1:
# 		orders = orders.filter(order_id__icontains=order_id)

# 	if order_status and order_status != '-1':
# 		orders = orders.filter(status=int(order_status))

# 	#pageinfo, orders = paginator.paginate(orders, cur_page, count, query_string=request.META['QUERY_STRING'])
# 	orders_josn = []
# 	for order in orders:
# 		#更新订单状态 如果时间超过10天并且已经付款，设置成已完成状态
# 		if (datetime.now() - order.created_at).days >= EXPIRE_DAYS:
# 			order.status = ORDER_STATUS_SUCCESSED
# 			order.save()
	
# 		order_info = __get_order_info_json(order)
# 		orders_josn.append(order_info)

# 	response = create_response(200)
# 	data = dict()
# 	response.data.items = orders_josn
# 	#response.data.page_info = paginator.to_dict(pageinfo)
# 	return response.get_response()
	
# def __get_order_info_json(order):
# 	order_info = dict()
# 	order_info['id'] = order.id
# 	order_info['order_id'] = order.order_id
# 	order_info['created_at'] = datetime.strftime(order.created_at, '%Y-%m-%d %H:%M')
# 	order_info['status'] = order.status
# 	order_info['total_price'] = order.total_price
# 	order_info['ship_name'] = order.ship_name
# 	order_info['buyer_name'] = order.buyer_name
# 	num = 0
# 	order_details = []
# 	for order_product in OrderHasProduct.objects.filter(order=order):
# 		order_detail = dict()
# 		order_detail['name'] = order_product.product.name
# 		order_detail['num'] = order_product.number
# 		total_price = '%.2f' % order_product.total_price
# 		order_detail['total_price'] = total_price
# 		order_detail['is_shiped'] = order_product.is_shiped

# 		if order_product.is_shiped == 1:
# 			num = num + order_product.number
# 		order_details.append(order_detail)
# 	order_info['order_details'] = order_details
# 	order_info['num'] = num

# 	return order_info





# ########################################################################
# # 作废优惠券: destory_coupon
# ########################################################################
# from views import __create_random_order_coupon_id
# from account.models import UserProfile
# def get_coupons(request ,webapp_id):
# 	profile = UserProfile.objects.get(webapp_id=webapp_id)
# 	source = request.GET.get('source', None)
# 	response = create_response(200)
# 	if source is None:
# 		response.errMsg = u'source error'
# 		return response.get_response()
	

# 	end_time = request.GET.get('end_time', None)
# 	if end_time is None:
# 		response.errMsg = u'end_time error'
# 		return response.get_response()

# 	sum = request.GET.get('sum', None)

# 	if sum is None:
# 		response.errMsg = u'sum error'
# 		return response.get_response()
# 	try:
# 		sum  = int(sum)
# 	except:
# 		response.errMsg = u'sum error'
# 		return response.get_response()

# 	money = request.GET.get('money',None)
# 	if money is None:
# 		response.errMsg = u'money error'
# 		return response.get_response()		
# 	try:
# 		money = int(money)
# 	except:
# 		response.errMsg = u'money error'
# 		return response.get_response()		
# 	coupon_pools = CouponPool.objects.filter(source=source, money=money,expired_time=end_time)
# 	if coupon_pools.count() > 0:
# 		coupon_pool = coupon_pools[0]
# 		if coupon_pool.residue_sum == 0:
# 			response.success = u'pool is null'
# 			response.coupons = []
# 			return response.get_response()	
# 		elif coupon_pool.residue_sum < sum:
# 			sum = coupon_pool.residue_sum
		
# 		coupon_ids = []
# 		coupons = []
# 		for index in range(sum):
# 			try:
# 				coupon_id = __create_random_order_coupon_id(coupon_pool.head, profile.user)
# 				coupon = Coupon.objects.create(
# 					source=coupon_pool.source,
# 					coupon_id=coupon_id,
# 					provided_time=coupon_pool.provided_time,
# 					expired_time=coupon_pool.expired_time,
# 					money=coupon_pool.money,
# 					coupon_pool_id=coupon_pool.id,
# 					order_id=''
# 				)
# 				coupon_ids.append(coupon_id)
# 				coupons.append(coupon)
# 			except:
# 				continue
# 		coupon_pool.residue_sum = coupon_pool.residue_sum - sum
# 		coupon_pool.save()
# 		if user_profile.webapp_template == 'wine':
# 			__insert_coupons_into_shpex(list(coupons))
# 		response.coupons = coupon_ids
# 		return response.get_response()
# 	else:
# 		response.errMsg = u'no pool'
# 		return response.get_response()

# ########################################################################
# # total_statistics: 统计信息
# ########################################################################
# def total_statistics(request):
# 	total_statistics = dict()
# 	orders = Order.objects.all()
# 	order_count = orders.count()
# 	ship_count = 0
# 	for order in orders.filter(status=ORDER_STATUS_SUCCESSED):
# 		for order_has_product in OrderHasProduct.objects.filter(order=order):
# 			ship_count= ship_count + order_has_product.number

# 	order_successed = orders.filter(status=ORDER_STATUS_SUCCESSED).count()
	
# 	total_statistics['order_count'] = order_count
# 	total_statistics['ship_count'] = ship_count
# 	total_statistics['order_successed'] = order_successed
# 	total_price = 0
# 	for order in orders.filter(status=ORDER_STATUS_SUCCESSED):
# 		total_price = total_price + order.total_price
# 	total_statistics['total_price'] = total_price

	
# 	days = request.GET.get('days', None)
# 	date_statistics = dict()
# 	if days:
# 		total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
# 		if low_date == high_date:
# 			date_orders = Order.objects.filter(created_at__year=low_date.year, created_at__month=low_date.month, created_at__day=low_date.day)

# 		else:
# 			if days.find('-') == -1:
# 				pass
# 			else:
# 				#total_days = total_days + 1
# 				high_date = high_date + timedelta(days = 1)
# 			date_orders = Order.objects.filter(created_at__range=(low_date, high_date))

# 		ship_count = 0
# 		total_price = 0
# 		for order in date_orders.filter(status__gte=ORDER_STATUS_PAYED_SUCCESSED):
# 			for order_has_product in OrderHasProduct.objects.filter(order=order):
# 				ship_count= ship_count + order_has_product.number
# 			total_price = total_price + order.total_price
		
# 		date_statistics = dict()
# 		date_statistics['order_count'] = date_orders.count()
# 		date_statistics['ship_count'] = ship_count
# 		#total_price = order.total_price
# 		date_statistics['total_price'] = total_price
		
# 	response = create_response(200)
# 	response.data.total_statistics = total_statistics
# 	response.data.date_statistics = date_statistics

# 	return response.get_response()

# ORDERED_QUANTITY=1 #日订单量
# ORDERED_SHIPED_QUANTITY=2  #日出货量
# ORDERED_TOTAL_PRICE=3 #日总金额

# MAX_VALUE = 6
# #===============================================================================
# # get_order_daily_trend : 获得订单图表数据
# #===============================================================================
# from core import chartutil
# @login_required
# def get_order_daily_trend(request):
# 	days = request.GET['days']
# 	type = int(request.GET['type']) # 1为柱状图，2为k线图

# 	elements = request.GET.get('element','')
# 	if elements:
# 	 	elements = elements.split(',')

# 	total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
# 	date_list = dateutil.get_date_range_list(low_date, high_date)

# 	if low_date == high_date:
# 		orders = Order.objects.filter(created_at__year=low_date.year, created_at__month=low_date.month, created_at__day=low_date.day)
# 	else:
# 		if days.find('-') == -1:
# 			date_list = date_list[:len(date_list)-1]
# 		else:
# 			total_days = total_days + 1
# 			high_date = high_date + timedelta(days = 1)
# 		orders = Order.objects.filter(created_at__range=(low_date, high_date))

# 	date2count = dict([(o, o) for o in range(1,7)])

# 	trend_ordered_quantity_values = []
# 	trend_shiped_quantity_values = []
# 	trend_order_weixin_values = []
# 	trend_order_shopex_values = []
# 	trend_listened_record_values = []
# 	trend_recorded_values = []
# 	x_labels = []

# 	max_value = MAX_VALUE
# 	for loop_date in date_list:
# 		x = (loop_date - low_date).days
# 		x_labels.append(str(x))
# 		for e in elements:
# 			orders_filter_by_date = orders.filter(created_at__year=loop_date.year, created_at__month=loop_date.month, created_at__day=loop_date.day)
# 			e = int(e)
# 			if ORDERED_QUANTITY == e:
# 				count = orders_filter_by_date.count()
# 				dot = {'x':x, 'y':count}
# 				max_value = __get_max_values(count, max_value)
# 				trend_ordered_quantity_values.append(dot)

# 			if ORDERED_SHIPED_QUANTITY == e:
# 				count = 0
# 				for order in orders_filter_by_date.filter(status__gte=ORDER_STATUS_PAYED_SUCCESSED):
# 				 	for order_has_product in OrderHasProduct.objects.filter(order=order):
# 				 		count = count + order_has_product.number
# 				dot = {'x':x, 'y':count}
# 				max_value = __get_max_values(count, max_value)
# 				trend_shiped_quantity_values.append(dot)

# 			if ORDERED_TOTAL_PRICE == e:
# 				total_price = 0
# 				for order in orders_filter_by_date.filter(status__gte=ORDER_STATUS_PAYED_SUCCESSED):
# 					total_price = total_price+order.total_price
# 				dot = {'x':x, 'y':total_price}

# 				max_value = __get_max_values(total_price, max_value)
# 				trend_order_shopex_values.append(dot)

# 	values = []
# 	for e in elements:
# 		e = int(e)
# 		if ORDERED_QUANTITY == e:
			
# 			values.append({'title':u'日订单量', 'values':trend_ordered_quantity_values})

# 		if ORDERED_SHIPED_QUANTITY == e:
# 			values.append({'title':u'日出货量', 'values':trend_shiped_quantity_values})

# 		if ORDERED_TOTAL_PRICE == e:
# 			values.append({'title':u'日总金额', 'values':trend_order_shopex_values})

# 	if type == 1:

# 		infos = {
# 			'title': '',
# 			'x_labels': x_labels,
# 			'bar_title': 'ttt',
# 			'x_legend_text': u'日期',
# 			'values': values,
# 			'max_value': max_value,
# 			'date_info': {'days':total_days, 'low_date':low_date}
# 		}
# 		chart_json = chartutil.create_bar_chart(infos)
# 	else:
# 		infos = {
# 			'title': '',
# 			'values': values,
# 			'date_info': {'days':total_days, 'low_date':low_date},
# 			'max_value': max_value
# 		}
# 		chart_json = chartutil.create_wine_line_chart(infos, display_today_data=False)

# 	return HttpResponse(chart_json, 'application/json')

# def __get_max_values(count, max_value):
# 	if count > max_value:
# 		#MAX_VALUE = count
# 		return count
# 	else:
# 		return max_value 

# def category_has_product_delete(request, id):
# 	response = create_response(200)

# 	category = CategoryHasProduct.objects.get(id = id).category
# 	category.has_product_counts = category.has_product_counts -1
# 	category.save()
# 	CategoryHasProduct.objects.filter(id = id).delete()
# 	return response.get_response()

