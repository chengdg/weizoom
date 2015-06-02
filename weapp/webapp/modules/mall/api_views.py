# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil
import random
from itertools import chain

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
from core import paginator

from models import *
import module_api

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
	src_id = request.REQUEST.get('src_id', None)
	dst_id = request.REQUEST.get('dst_id', None)

	if not src_id or not dst_id:
		response = create_response(500)
		response.errMsg = u'invalid arguments: src_id(%s), dst_id(%s)' % (src_id, dst_id)
		return response.get_response()		

	src_id = int(src_id)
	dst_id = int(dst_id)
	if dst_id == 0:
		#dst_id = 0, 将src_product的display_index设置得比第一个product的display_index大即可
		first_product = Product.objects.filter(owner=request.user).order_by('-display_index')[0]
		if first_product.id != src_id:
			Product.objects.filter(id=src_id).update(display_index=first_product.display_index+1)
	else:
		#dst_id不为0，交换src_product, dst_product的display_index
		id2product = dict([(p.id, p) for p in Product.objects.filter(id__in=[src_id, dst_id])])
		Product.objects.filter(id=src_id).update(display_index=id2product[dst_id].display_index)
		Product.objects.filter(id=dst_id).update(display_index=id2product[src_id].display_index)

	response = create_response(200)
	return response.get_response()

# 商品类型
PRODUCT_TYPES = [PRODUCT_DEFAULT_TYPE, PRODUCT_INTEGRAL_TYPE]
# MODULE END: product
# Termite GENERATED END: api_views
########################################################################
# get_products: 获取product列表
########################################################################
@login_required
def get_products(request):
	query = request.GET.get('query', None)
	filter_attr = request.GET.get('filter_attr', None)
	filter_value = request.GET.get('filter_value', None)
		
	#处理排序
	sort_attr = request.GET.get('sort_attr', None);
	if not sort_attr:
		sort_attr = '-display_index'

	products = []
	other_mall_products = []
	product_types = PRODUCT_TYPES
	if filter_attr == 'checked' and filter_value != '-1':
		if filter_value  == '1':
			other_mall_products, other_mall_product_ids = module_api.get_verified_weizoom_mall_partner_products_and_ids(request.user_profile.webapp_id)
		else:
			other_mall_products, other_mall_product_ids = module_api.get_not_verified_weizoom_mall_partner_products_and_ids(request.user_profile.webapp_id)
	elif filter_attr == 'source' and filter_value != '-1':
		if filter_value == '1':
			other_mall_products, other_mall_product_ids = module_api.get_weizoom_mall_partner_products_and_ids(request.user_profile.webapp_id)
		else:
			products = Product.objects.filter(owner=request.user, is_deleted = False, type__in = product_types).order_by(sort_attr)
			other_mall_products = None
			other_mall_product_ids = None
	elif filter_attr == 'type' and filter_value !='-1':
		product_types = [filter_value]		
		products = Product.objects.filter(owner=request.user, is_deleted = False, type__in = product_types).order_by(sort_attr)
		other_mall_products, other_mall_product_ids = module_api.get_weizoom_mall_partner_products_and_ids(request.user_profile.webapp_id)
	else:
		products = Product.objects.filter(owner=request.user, is_deleted = False, type__in = product_types).order_by(sort_attr)
		other_mall_products, other_mall_product_ids = module_api.get_weizoom_mall_partner_products_and_ids(request.user_profile.webapp_id)
	
	is_weizoom_mall = request.user.is_weizoom_mall

	#处理搜索
	if query:
		products = products.filter(name__icontains=query)
		if other_mall_products:
			other_mall_products = other_mall_products.filter(name__icontains=query)
		
	products = list(products)
	if other_mall_products:
		# 未审核置顶
		unapproved_products = list()
		audited_products = list()
		for product in other_mall_products:
			if hasattr(product, 'is_checked') and product.is_checked:
				audited_products.append(product)
			else:
				unapproved_products.append(product)
		unapproved_products.sort()
		audited_products.sort()
		
		products = (list(unapproved_products))+products+(list(audited_products))

	#处理过滤
	if filter_attr:
		if (filter_attr == 'category_id') and (not filter_value == '0'):
			category_product_ids = set([r.product_id for r in CategoryHasProduct.objects.filter(category_id=filter_value)])
			filtered_products = list()
			for product in products:
				if product.id in category_product_ids:
					filtered_products.append(product)
			products = filtered_products

	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, products = paginator.paginate(products, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	
	#获取product关联的category集合
	id2product = dict([(product.id, product) for product in products])
	product_ids = []
	for product in products:
		product.categories = []
		id2product[product.id] = product
		product_ids.append(product.id)


	category_ids = []
	category2products = {}
	current_category_ids = [category.id for category in ProductCategory.objects.filter(owner=request.user)]
	for relation in CategoryHasProduct.objects.filter(category_id__in=current_category_ids, product_id__in=product_ids):
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
			
	#获取商城的所有商品分类
	all_categories = []
	for category in ProductCategory.objects.filter(owner=request.user):
		all_categories.append({
			'id': category.id,
			'name': category.name
		})

	# 构造返回数据
	Product.fill_display_price(products)
	items = []

	# 商城
	weizoom_mall = None
	weizoom_malls = WeizoomMall.objects.filter(webapp_id=request.user_profile.webapp_id)
	if weizoom_malls.count() > 0:
		weizoom_mall = weizoom_malls[0]

	for product in products:
		if other_mall_product_ids and product.id in other_mall_product_ids:
			product.is_from_other_mall = True
			if not hasattr(product, 'is_checked'):
				product.is_checked = WeizoomMallHasOtherMallProduct.objects.get(product_id=product.id, weizoom_mall=weizoom_mall).is_checked
		else:
			product.is_from_other_mall = False
			product.is_checked = '-'

		items.append({
			'id': product.id,
			'name': product.name,
			'type_str': product.get_str_type(),
			'thumbnails_url': product.thumbnails_url,
			'categories': product.categories,
			'display_price': product.display_price,
			'is_checked': product.is_checked,
			'is_from_other_mall': product.is_from_other_mall,
			'created_at': datetime.strftime(product.created_at, '%Y-%m-%d %H:%M')
		})

	data = dict()
	data['is_weizoom_mall'] = is_weizoom_mall
	response = create_response(200)
	response.data = {
		'items': items,
		'pageinfo': paginator.to_dict(pageinfo),
		'categories': all_categories,
		'sortAttr': sort_attr,
		'data': data
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
	
	other_mall_products, other_mall_product_ids = module_api.get_weizoom_mall_partner_products_and_ids(request.user_profile.webapp_id)
	if other_mall_products and other_mall_product_ids:
		products = Product.objects.filter(Q(owner=request.user)|Q(id__in=other_mall_product_ids), is_deleted = False, type__in = PRODUCT_TYPES)
	else:
		products = Product.objects.filter(owner=request.user, is_deleted = False, type__in = PRODUCT_TYPES)
	query = request.GET.get('query', None)
	
	if query:
		products = products.filter(name__icontains=query)
	
	#获取未分类的product id
	product_ids = set(products.values_list('id', flat=True))
	# old::: categorized_product_ids = set([relation.product_id for relation in CategoryHasProduct.objects.filter(~Q(category_id=category_id)])
	#categorized_product_ids = set([relation.product_id for relation in CategoryHasProduct.objects.filter(~Q(category_id=category_id), category__owner_id=request.user.id)])
	selectable_product_ids = product_ids #- categorized_product_ids
	#获取category下已存在的product id
	category_product_ids = set([relation.product_id for relation in CategoryHasProduct.objects.filter(category_id=category_id)])

	# 构造返回数据
	is_all_product_selected = True
	items = []
	if len(selectable_product_ids) > 0:
		display_products = Product.objects.filter(id__in=selectable_product_ids)
		Product.fill_display_price(display_products)
		for product in display_products:
			item = {
				'id': product.id,
				'name': product.name,
				'thumbnails_url': product.thumbnails_url,
				'price': product.display_price,
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

########################################################################
# list_orders: 显示订单列表
########################################################################
EXPIRE_DAYS = 10
@login_required
def get_orders(request):
	order_id = request.GET.get('order_id', '')
	order_source = request.GET.get('source', '')
	order_status = request.GET.get('status', '')
	order_price = request.GET.get('total_price', None)
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	webapp_id = request.user.get_profile().webapp_id
	created_at = request.GET.get('created_at', None)

	weizoom_mall_order_ids = WeizoomMallHasOtherMallProductOrder.get_weizoom_mall_order_id(webapp_id)

	is_weizoom_mall_partner = AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(request.user.id)
	if request.user.is_weizoom_mall:
		is_weizoom_mall_partner = False
	#old 
	# if created_at:
	# 	orders = Order.objects.filter(webapp_id=webapp_id).order_by(created_at)
	# elif order_price:
	# 	orders = Order.objects.filter(webapp_id=webapp_id).order_by(order_price)
	# else:
	# 	orders = Order.objects.filter(webapp_id=webapp_id)

	#add by bert at 17.0
	if created_at:
		orders = Order.objects.belong_to(webapp_id).order_by(created_at)
	elif order_price:
		orders = Order.objects.belong_to(webapp_id).order_by(order_price)
	else:
		orders = Order.objects.belong_to(webapp_id)
			
	count = int(request.GET.get('count', 25))
	
	if order_id and order_id != -1:
		orders = orders.filter(order_id__icontains=order_id)

	if order_status and order_status != '-1':
		orders = orders.filter(status=int(order_status))

	#pageinfo, orders = paginator.paginate(orders, cur_page, count, query_string=request.META['QUERY_STRING'])
	orders_josn = []
	for order in orders:
		#更新订单状态 如果时间超过10天并且已经付款，设置成已完成状态
		if (datetime.now() - order.created_at).days >= EXPIRE_DAYS:
			order.status = ORDER_STATUS_SUCCESSED
			order.save()

		if weizoom_mall_order_ids:
			if request.user.is_weizoom_mall and order.id in weizoom_mall_order_ids:
				order.come = 'other_mall'
			elif order.id in weizoom_mall_order_ids:
				order.come = 'weizoom_mall'
			else:
				order.come = 'mine_mall'	
		else:
			order.come = 'mine_mall'
	
		order_info = __get_order_info_json(order)
		orders_josn.append(order_info)

	response = create_response(200)

	if is_weizoom_mall_partner or request.user.is_weizoom_mall:
		is_show_source = True
	else:
		is_show_source = False

	data = dict()
	response.data.items = orders_josn
	#response.date.is_weizoom_mall_partner = is_weizoom_mall_partner
	response.data.is_show_source = is_show_source
	#response.data.page_info = paginator.to_dict(pageinfo)
	return response.get_response()
	
def __get_order_info_json(order):
	order_info = dict()
	order_info['id'] = order.id
	order_info['order_id'] = order.order_id
	order_info['created_at'] = datetime.strftime(order.created_at, '%Y-%m-%d %H:%M')
	order_info['status'] = order.status
	order_info['total_price'] = order.final_price
	order_info['ship_name'] = order.ship_name
	order_info['buyer_name'] = order.buyer_name
	num = 0
	order_details = []
	for order_product in OrderHasProduct.objects.filter(order=order):
		order_detail = dict()
		order_detail['name'] = order_product.product.name
		order_detail['num'] = order_product.number
		total_price = '%.2f' % order_product.total_price
		order_detail['total_price'] = total_price
		order_detail['is_shiped'] = order_product.is_shiped

		if order_product.is_shiped == 1:
			num = num + order_product.number
		order_details.append(order_detail)
	order_info['order_details'] = order_details
	order_info['num'] = num

	return order_info

########################################################################
# 作废优惠券: destory_coupon
########################################################################
from views import __create_random_order_coupon_id
from account.models import UserProfile
def get_coupons(request ,webapp_id):
	profile = UserProfile.objects.get(webapp_id=webapp_id)
	source = request.GET.get('source', None)
	response = create_response(200)
	if source is None:
		response.errMsg = u'source error'
		return response.get_response()
	

	end_time = request.GET.get('end_time', None)
	if end_time is None:
		response.errMsg = u'end_time error'
		return response.get_response()

	sum = request.GET.get('sum', None)

	if sum is None:
		response.errMsg = u'sum error'
		return response.get_response()
	try:
		sum  = int(sum)
	except:
		response.errMsg = u'sum error'
		return response.get_response()

	money = request.GET.get('money',None)
	if money is None:
		response.errMsg = u'money error'
		return response.get_response()		
	try:
		money = int(money)
	except:
		response.errMsg = u'money error'
		return response.get_response()		
	coupon_pools = CouponPool.objects.filter(source=source, money=money,expired_time=end_time)
	if coupon_pools.count() > 0:
		coupon_pool = coupon_pools[0]
		if coupon_pool.residue_sum == 0:
			response.success = u'pool is null'
			response.coupons = []
			return response.get_response()	
		elif coupon_pool.residue_sum < sum:
			sum = coupon_pool.residue_sum
		
		coupon_ids = []
		coupons = []
		for index in range(sum):
			try:
				coupon_id = __create_random_order_coupon_id(coupon_pool.head, profile.user)
				coupon = Coupon.objects.create(
					source=coupon_pool.source,
					coupon_id=coupon_id,
					provided_time=coupon_pool.provided_time,
					expired_time=coupon_pool.expired_time,
					money=coupon_pool.money,
					coupon_pool_id=coupon_pool.id,
					order_id=''
				)
				coupon_ids.append(coupon_id)
				coupons.append(coupon)
			except:
				continue
		coupon_pool.residue_sum = coupon_pool.residue_sum - sum
		coupon_pool.save()
		if user_profile.webapp_template == 'wine':
			__insert_coupons_into_shpex(list(coupons))
		response.coupons = coupon_ids
		return response.get_response()
	else:
		response.errMsg = u'no pool'
		return response.get_response()

########################################################################
# total_statistics: 统计信息
########################################################################
def total_statistics(request):
	total_statistics = dict()
	orders = Order.objects.all()
	order_count = orders.count()
	ship_count = 0
	for order in orders.filter(status=ORDER_STATUS_SUCCESSED):
		for order_has_product in OrderHasProduct.objects.filter(order=order):
			ship_count= ship_count + order_has_product.number

	order_successed = orders.filter(status=ORDER_STATUS_SUCCESSED).count()
	
	total_statistics['order_count'] = order_count
	total_statistics['ship_count'] = ship_count
	total_statistics['order_successed'] = order_successed
	total_price = 0
	for order in orders.filter(status=ORDER_STATUS_SUCCESSED):
		total_price = total_price + order.total_price
	total_statistics['total_price'] = total_price

	
	days = request.GET.get('days', None)
	date_statistics = dict()
	if days:
		total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
		if low_date == high_date:
			date_orders = Order.objects.filter(created_at__year=low_date.year, created_at__month=low_date.month, created_at__day=low_date.day)

		else:
			if days.find('-') == -1:
				pass
			else:
				#total_days = total_days + 1
				high_date = high_date + timedelta(days = 1)
			date_orders = Order.objects.filter(created_at__range=(low_date, high_date))

		ship_count = 0
		total_price = 0
		for order in date_orders.filter(status__gte=ORDER_STATUS_PAYED_SUCCESSED):
			for order_has_product in OrderHasProduct.objects.filter(order=order):
				ship_count= ship_count + order_has_product.number
			total_price = total_price + order.total_price
		
		date_statistics = dict()
		date_statistics['order_count'] = date_orders.count()
		date_statistics['ship_count'] = ship_count
		#total_price = order.total_price
		date_statistics['total_price'] = total_price
		
	response = create_response(200)
	response.data.total_statistics = total_statistics
	response.data.date_statistics = date_statistics

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
				for order in orders_filter_by_date.filter(status__gte=ORDER_STATUS_PAYED_SUCCESSED):
				 	for order_has_product in OrderHasProduct.objects.filter(order=order):
				 		count = count + order_has_product.number
				dot = {'x':x, 'y':count}
				max_value = __get_max_values(count, max_value)
				trend_shiped_quantity_values.append(dot)

			if ORDERED_TOTAL_PRICE == e:
				total_price = 0
				for order in orders_filter_by_date.filter(status__gte=ORDER_STATUS_PAYED_SUCCESSED):
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

def category_has_product_delete(request, id):
	response = create_response(200)

	category = CategoryHasProduct.objects.get(id = id).category
	category.has_product_counts = category.has_product_counts -1
	category.save()
	CategoryHasProduct.objects.filter(id = id).delete()
	return response.get_response()

#===============================================================================
# support_product_make_thanks_card : 商品是否支持制作感恩贺卡制作
#===============================================================================
def support_product_make_thanks_card(request):
	product_ids = request.GET['product_ids']
	if not product_ids or (product_ids is ''):
		Product.objects.filter(owner=request.user).update(is_support_make_thanks_card=0)
	else:
		ids = product_ids.split(',')
		Product.objects.filter(owner=request.user, id__in=ids).update(is_support_make_thanks_card=1)
		Product.objects.filter(owner=request.user).exclude(id__in=ids).update(is_support_make_thanks_card=0)
	response = create_response(200)
	return response.get_response()

#===============================================================================
# get_thanks_card_products : 获取可以设置感恩贺卡的商品
#===============================================================================
def get_thanks_card_products(request):
	products = Product.objects.filter(owner=request.user, is_deleted = False, is_support_make_thanks_card = 1)
	
	items = []
	for product in products:
		items.append({
			'id': product.id,
			'name': product.name,
			'thumbnails_url': product.thumbnails_url,
		})
	
	response = create_response(200)
	response.data = {
		'items': items,
	}
	return response.get_response()

#===============================================================================
# reset_thanks_secret : 重置感恩密码
#===============================================================================
def reset_thanks_secret(request):
	order_id = request.GET.get('order_id')
	secret = request.GET.get('secret')

	taget_secret = __gen_thanks_card_secret()
	ThanksCardOrder.objects.filter(order_id=order_id, thanks_secret=secret).update(thanks_secret=taget_secret, is_used=False, content='', att_url='', card_count=0, listen_count=0)

	response = create_response(200)
	response.data = {
		'secret': taget_secret
	}
	return response.get_response()
	
########################################################################
# __gen_thanks_card_secret: 生成感恩密码
########################################################################
def __gen_thanks_card_secret():
	secret = random.randint(1000000, 9999999)
	if ThanksCardOrder.objects.filter(thanks_secret=secret).count() > 0:
		return __gen_thanks_card_secret()
	else:
		return secret
