# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import MySQLdb
import random
import string

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from core.dateutil import get_today

from excel_response import ExcelResponse

from account.models import *
from models import *
from modules.member.models import IntegralStrategySttings
from modules.member import integral

import export


COUNT_PER_PAGE = 20

# Termite GENERATED START: views

FIRST_NAV_NAME = 'webapp'

# MODULE START: productcategory
SHOP_CATEGORY_NAV = 'mall-category'

########################################################################
# list_productcategories: 显示商品分类列表
########################################################################
@login_required
def list_productcategories(request):
	productcategories = ProductCategory.objects.filter(owner=request.user).order_by('display_index')

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SHOP_CATEGORY_NAV,
		'productcategories': productcategories,
	})
	return render_to_response('mall/editor/productcategories.html', c)


########################################################################
# add_productcategory: 添加商品分类
########################################################################
@login_required
def add_productcategory(request):
	if request.POST:
		productcategory = ProductCategory.objects.create(
			owner = request.user,
			name = request.POST.get('name', '').strip(),
			pic_url = request.POST.get('pic_url', '').strip()
		)
		productcategory.display_index = 0-productcategory.id

		product_ids = request.POST.getlist('product_id')
		productcategory.product_count = len(product_ids)

		productcategory.save()

		for product_id in product_ids:
			CategoryHasProduct.objects.create(product_id=product_id, category=productcategory)

		return HttpResponseRedirect('/mall/editor/productcategories/')
	else:
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SHOP_CATEGORY_NAV,
		})
		return render_to_response('mall/editor/edit_productcategory.html', c)


########################################################################
# update_productcategory: 更新商品分类
########################################################################
@login_required
def update_productcategory(request, productcategory_id):
	if request.POST:
		product_ids = request.POST.getlist('product_id')
		ProductCategory.objects.filter(owner=request.user, id=productcategory_id).update(
			name = request.POST.get('name', '').strip(),
			pic_url = request.POST.get('pic_url', '').strip(),
			product_count = len(product_ids)
		)

		CategoryHasProduct.objects.filter(category_id=productcategory_id).delete()

		for product_id in product_ids:
			CategoryHasProduct.objects.create(product_id=product_id,category_id=productcategory_id)

		return HttpResponseRedirect('/mall/editor/productcategories/')
	else:
		productcategory = ProductCategory.objects.get(owner=request.user, id=productcategory_id)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SHOP_CATEGORY_NAV,
			'productcategory': productcategory,
		})
		return render_to_response('mall/editor/edit_productcategory.html', c)


########################################################################
# delete_productcategory: 删除商品分类
########################################################################
@login_required
def delete_productcategory(request, productcategory_id):
	CategoryHasProduct.objects.filter(id=productcategory_id).delete()
	ProductCategory.objects.filter(id=productcategory_id).delete()

	return HttpResponseRedirect('/mall/editor/productcategories/')
# MODULE END: productcategory


# MODULE START: product
SHOP_PRODUCT_NAV = 'mall-product'

########################################################################
# list_products: 显示商品列表
########################################################################
@login_required
def list_products(request):
	products = Product.objects.filter(owner=request.user).order_by('display_index')

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SHOP_PRODUCT_NAV,
		'products': products,
	})

	return render_to_response('mall/editor/products.html', c)

########################################################################
# add_product: 添加商品
########################################################################
@login_required
def add_product(request):
	if request.POST:
		product = Product.objects.create(
			owner = request.user,
			name = request.POST.get('name', '').strip(),
			physical_unit = request.POST.get('physical_unit', ''),
			price = request.POST.get('price', ''),
			introduction = request.POST.get('introduction', '').strip(),
			weight = request.POST.get('weight', '0.0').strip(),
			thumbnails_url = request.POST.get('thumbnails_url', '').strip(),
			pic_url = request.POST.get('pic_url', '').strip(),
			detail = request.POST.get('detail', '').strip(),
			remark = request.POST.get('remark', ''),
		
			putaway_type = int(request.POST.get('putaway_type', 0)),
			putaway_start_time = request.POST.get('startTime', ''),
			putaway_end_time = request.POST.get('endTime', ''),

			stock_type = request.POST.get('stock_type', PRODUCT_STOCK_TYPE_UNLIMIT),
			stocks = request.POST.get('stocks', '0').strip(),
		)
		product.display_index = product.id
		product.save()

		product_category_id = int(request.POST.get('product_category', -1))
		if product_category_id != -1:
			CategoryHasProduct.objects.create(category_id=product_category_id, product=product)
			ProductCategory.objects.filter(id=product_category_id).update(product_count = F('product_count') + 1)
			'''
			category = ProductCategory.objects.get(id=product_category_id)
			category.product_count = category.product_count + 1
			category.save()
			'''

		return HttpResponseRedirect('/mall/editor/products/')
	else:
		categories = ProductCategory.objects.filter(owner=request.user)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SHOP_PRODUCT_NAV,
			'categories': categories
		})
		return render_to_response('mall/editor/edit_product.html', c)


########################################################################
# update_product: 更新商品
########################################################################
@login_required
def update_product(request, product_id):
	if request.POST:
		#减少原category的product_count
		if CategoryHasProduct.objects.filter(product_id=product_id).count() > 0:
			old_category_id = CategoryHasProduct.objects.get(product_id=product_id).category_id
			ProductCategory.objects.filter(id=old_category_id).update(product_count = F('product_count') - 1)
			CategoryHasProduct.objects.filter(product_id=product_id).delete()

		#更新product
		Product.objects.filter(owner=request.user, id=product_id).update(
			name = request.POST.get('name', '').strip(),
			physical_unit = request.POST.get('physical_unit', '').strip(),
			price = request.POST.get('price', '').strip(),
			introduction = request.POST.get('introduction', '').strip(),
			weight = request.POST.get('weight', '0.0').strip(),
			thumbnails_url = request.POST.get('thumbnails_url', '').strip(),
			pic_url = request.POST.get('pic_url', '').strip(),
			detail = request.POST.get('detail', '').strip(),
			remark = request.POST.get('remark', '').strip(),
		
			putaway_type = int(request.POST.get('putaway_type', 0)),
			putaway_start_time = request.POST.get('startTime', ''),
			putaway_end_time = request.POST.get('endTime', ''),

			stock_type = request.POST.get('store_type', PRODUCT_STOCK_TYPE_UNLIMIT),
			stocks = request.POST.get('store_sum', '0').strip(),
		)

		product_category_id = int(request.POST.get('product_category', -1))
		if product_category_id != -1:
			CategoryHasProduct.objects.create(category_id=product_category_id, product_id=product_id)
			ProductCategory.objects.filter(id=product_category_id).update(product_count = F('product_count') + 1)

		return HttpResponseRedirect('/mall/editor/products/')
	else:
		product = Product.objects.get(owner=request.user, id=product_id)

		target_category = None
		product_related_categories = CategoryHasProduct.objects.filter(product=product)
		if product_related_categories.count() > 0:
			target_category = product_related_categories[0].category

		categories = ProductCategory.objects.filter(owner=request.user)
		if target_category:
			for category in categories:
				if category.id == target_category.id:
					category.selected = 1

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SHOP_PRODUCT_NAV,
			'product': product,
			'categories': categories
		})
		return render_to_response('mall/editor/edit_product.html', c)

########################################################################
# delete_product: 删除商品
########################################################################
@login_required
def delete_product(request, product_id):
	#减少category的product_count
	if CategoryHasProduct.objects.filter(product_id=product_id).count() > 0:
		old_category_id = CategoryHasProduct.objects.get(product_id=product_id).category_id
		ProductCategory.objects.filter(id=old_category_id).update(product_count = F('product_count') - 1)
		CategoryHasProduct.objects.filter(product_id=product_id).delete()

	Product.objects.filter(id=product_id).delete()

	return  HttpResponseRedirect('/mall/editor/products/')
# MODULE END: product


MALL_SETTINGS_NAV = 'mall-settings'
SHOP_SETTINGS_NAV = 'mall-settings'

########################################################################
# list_mall_settings: 显示商城配置
########################################################################
@login_required
def list_mall_settings(request):
	'''
	if PostageConfig.objects.filter(owner=request.user).count() == 0:
		#创建默认的“免运费”配置
		PostageConfig.objects.create(
			owner = request.user,
			name = u'免运费',
			is_enable_added_weight = False,
			is_used = True,
			is_system_level_config = True
		)
	'''

	postage_configs = PostageConfig.objects.filter(owner=request.user).order_by('display_index')
	
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': MALL_SETTINGS_NAV,
		'postage_configs': postage_configs,
	})
	return render_to_response('mall/editor/mall_settings.html', c)


########################################################################
# update_mall_settings: 更新商城配置
########################################################################
@login_required
def update_mall_settings(request):
	webapp_id = request.user_profile.webapp_id
	
	if request.POST:
		#处理运费信息
		postage_config_id = request.POST.get('postage_config_id', None)
		if postage_config_id:
			PostageConfig.objects.filter(owner=request.user).update(is_used=False)
			PostageConfig.objects.filter(owner=request.user, id=postage_config_id).update(is_used=True)
	
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


SHOP_ORDERS_NAV = 'mall-orders'
@login_required
def list_orders(request):
	webapp_id = request.user_profile.webapp_id
	orders = Order.objects.filter(webapp_id=webapp_id)

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SHOP_ORDERS_NAV,
		'orders': orders,
		})
	return render_to_response('mall/editor/orders.html', c)

COUNT_PER_PAGE = 20



########################################################################
# detail_order: 显示订单详情
########################################################################
@login_required
def detail_order(request, id):
	order = Order.objects.get(id=id)

	if request.method == 'GET':
		order_has_products = OrderHasProduct.objects.filter(order=order)
		
		number = 0
		for order_has_product in order_has_products:
			number += order_has_product.number
		order.number = number

		coupon =  None

		coupons = OrderHasCoupon.objects.filter(order_id=order.order_id)
		if coupons.count() > 0:
			coupon =  coupons[0]		

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SHOP_ORDERS_NAV,
			'order': order,
			'order_has_products':order_has_products,
			'coupon': coupon,
			'order_operation_logs': _get_order_operation_log(order.order_id),
			'order_status_logs': _get_order_status_log(order.order_id),
		})
		return render_to_response('mall/editor/detail_order.html', c)
	else:
		order_status = request.POST.get('order_status', None)
		bill_type = request.POST.get('bill_type', None)
		postage = request.POST.get('postage', None)
		ship_name = request.POST.get('postage', None)
		ship_tel = request.POST.get('ship_tel', None)
		ship_address = request.POST.get('ship_address', None)
		remark = request.POST.get('remark',None)
		to_ship_product_id_list = request.POST.getlist('product_id')

		shiped_product_id_list = []
		for order_has_product in OrderHasProduct.objects.filter(order_id=id, is_shiped=1):
			shiped_product_id_list.append(str(order_has_product.id))

		if set(to_ship_product_id_list) != set(shiped_product_id_list):
			OrderHasProduct.objects.filter(id__in=to_ship_product_id_list).update(is_shiped=1)
			OrderHasProduct.objects.filter(~Q(id__in=to_ship_product_id_list)).update(is_shiped=0)
			
			if len(to_ship_product_id_list) > 0:
				operate_ship_log = u'发货商品：'
				for order_has_product in OrderHasProduct.objects.filter(id__in=to_ship_product_id_list):
					product_name = order_has_product.product.name
					operate_ship_log += product_name + ','

				_watch_operation_logs(order_id, operate_ship_log, request.user, remark)

		operate_log = ''
		expired_status = order.status
		if order_status:
			if order.status != int(order_status):
				operate_log = u' 修改状态'
				_watch_status_logs(order_id, order.status, order_status, request.user, remark)
				order.status = order_status
				try:
					if expired_status < ORDER_STATUS_SUCCESSED and int(order_status) == ORDER_STATUS_SUCCESSED and expired_status != ORDER_STATUS_CANCEL:
						integral.increase_father_member_integral_by_child_member_buyed(order.webapp_user_id, order.webapp_id)
						if integral.is_integral_detail_used and order.final_price > 0:
							integral.increase_integral_for_integral_detail(order.webapp_user_id, order.webapp_id, order.final_price)
				except:
					notify_message = u"订单状态为已完成时为贡献者增加积分，cause:\n{}".format(unicode_full_stack())
					watchdog_error(notify_message)
			
		if bill_type:
			bill = request.POST.get('bill','')
			if order.bill_type != bill_type and order.bill != bill:
				operator_log = operator_log + u' 修改发票'
				order.bill_type = bill_type
				order.bill = bill
			
		if postage:
			if float(order.postage) != float(postage):
				operator_log = operator_log + u' 修改邮费'
				order.total_price = order.total_price - float(postage)
				order.postage = postage
				
		if ship_name:
			if order.ship_name != ship_name:
				operator_log = operator_log + u' 修改收货人'	
				order.ship_name = ship_name
			
		if ship_tel:
			if order.ship_tel != ship_tel:
				operator_log = operator_log + u' 修改收货人电话号'	
				order.ship_tel = ship_tel
			
		if ship_address:
			if order.ship_address != ship_address:
				operator_log = operator_log + u' 修改收货人地址'	
				order.ship_address = ship_address

		if len(operator_log.strip()) > 0:
			_watch_operation_logs(order_id, operator_log, request.user, remark )

		order.save()		
		return HttpResponseRedirect('/mall/editor/orders/')

def _get_order_operation_log(order_id):
	return OrderOperationLog.objects.filter(order_id=order_id)

def _get_order_status_log(order_id):
	return OrderStatusLog.objects.filter(order_id=order_id)

def _watch_status_logs(order_id, pre_status, cur_status, user, remark):
	try:
		OrderStatusLog.objects.create(order_id=order_id, pre_status=pre_status, cur_status=cur_status, operator=user.username)	
	except:
		pass
def _watch_operation_logs(order_id, action, user, remark):
	try:
		OrderOperationLog.objects.create(order_id=order_id, action=action, operator=user.username)	
	except:
		pass

@login_required
def create_coupon(request):
	if request.method == 'GET':
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SHOP_SETTINGS_NAV,
		})
		return render_to_response('mall/editor/editor_coupon.html', c)
	else:
		today = get_today()
		expired_date = request.POST.get('expired_time','')
		count = int(request.POST.get('sum', 0))
		name = request.POST.get('name')
		money = float(request.POST.get('money', 0))
		source = request.POST.get('source', COUPON_SOURCE_WEIXIN)

		coupon_pool = CouponPool.objects.create(
			name=name,
			source=source,
			sum=count,
			money=money,
			expired_time=expired_date,
			provided_time=today,
			residue_sum=count,
			owner=request.user
			)

		if COUPON_SOURCE_MAN == source:
			for index in xrange(count):
				coupon_id = __create_random_order_coupon_id(source, request.user)
				coupon = Coupon.objects.create(
					coupon_id=coupon_id,
					provided_time=today,
					expired_time=expired_date,
					money=money,
					coupon_pool_id=coupon_pool.id,
					order_id='',
					owner=request.user,
					source=source
				)

			return HttpResponseRedirect('/mall/editor/show/%d/' % coupon_pool.id)
		else:
			return HttpResponseRedirect('/mall/editor/mall_settings/')

########################################################################
# __create_random_coupon_id: 生成优惠券
########################################################################
def __create_random_order_coupon_id(source, user):
	random_args_value = ['1','2','3','4','5','6','7','8','9','0']
	coupon_id = source+string.join(random.sample(random_args_value, 6)).replace(' ','')
	
	if Coupon.objects.filter(coupon_id=coupon_id, owner=user).count() > 0:
		return __create_random_order_coupon_id(source, user)
	else:
		return coupon_id

########################################################################
# show_coupon: 显示优惠券
########################################################################
@login_required
def show_coupon(request, coupon_pool_id):
	webapp_id = request.user.get_profile().webapp_id
	coupon_pool = CouponPool.objects.get(id=coupon_pool_id)
	coupons = Coupon.objects.filter(coupon_pool_id=coupon_pool.id)
	c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SHOP_SETTINGS_NAV,
			'webapp_id': webapp_id,
			'coupon_pool':coupon_pool,
			'coupons': coupons
		})
	return render_to_response('mall/editor/editor_coupon.html', c)

####################################
#  导出优惠劵
####################################
@login_required
def export_coupon(request, coupon_pool_id):
    coupon_list  = [
        [u'优惠券', u'过期时间', u'抵扣金额']
        ]
    coupons = Coupon.objects.filter(coupon_pool = coupon_pool_id)
    for coupon in coupons:
        coupon_list.append([
            coupon.coupon_id,
            coupon.expired_time,
            coupon.money
        ])

    return ExcelResponse(coupon_list, output_name=u'优惠券'.encode('utf8'), force_csv=False)

########################################################################
# list_coupons: 优惠券首页
########################################################################
@login_required
def list_coupons(request):
	webapp_id = request.user.get_profile().webapp_id
	coupon_pools = CouponPool.objects.filter(owner=request.user)
	coupons = Coupon.objects.filter(owner=request.user)
	count = coupons.count()
	destroy_count = Coupon.objects.filter(is_active=0).count()

	#处理有coupon被使用的pool
	for coupon_pool in coupon_pools:
		coupon_pool.can_delete = True

		#更新超时pool
		current_time = int(time.time())
		end_time = int(time.mktime(time.strptime(coupon_pool.expired_time,'%Y-%m-%d')))
		if current_time > end_time:
			coupon_pool.residue_sum = 0
			coupon_pool.save()
			coupon_pool.can_delete = False
			Coupon.objects.filter(coupon_pool_id=coupon_pool.id).update(is_active=0)
	

	destroy_count = Coupon.objects.filter(is_active=0).count()

	if count == destroy_count:
		is_all_destory = 1
	else:
		is_all_destory = 0

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SHOP_SETTINGS_NAV,
		'coupons': coupons,
		'coupon_pools': coupon_pools,
		'count': count,
		'is_all_destory': is_all_destory

	})
	return render_to_response('mall/editor/coupons.html', c)

@login_required
def integral_settings(request):
	integral_settings = IntegralStrategySttings.objects.filter(webapp_id=request.user.get_profile().webapp_id)
	if request.method == 'GET':
		if integral_settings.count() > 0:
			integral_setting = integral_settings[0]
		else:
			integral_setting = None
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SHOP_SETTINGS_NAV,
			'integral_setting': integral_setting,
			})
		return render_to_response('mall/editor/integral_settings.html', c)
	else:
		if integral_settings.count() > 0:
			integral_settings.update(
				be_member_increase_count=int(request.POST.get('be_member_increase_count',0)),
				integral_each_yuan = int(request.POST.get('integral_each_yuan',0)),
				click_shared_url_increase_count_after_buy=int(request.POST.get('click_shared_url_increase_count_after_buy',0)),
				click_shared_url_increase_count_before_buy=int(request.POST.get('click_shared_url_increase_count_before_buy',0)),
				buy_via_shared_url_increase_count_for_buyer=int(request.POST.get('buy_via_shared_url_increase_count_for_buyer',0)),
				buy_via_shared_url_increase_count_for_author=int(request.POST.get('buy_via_shared_url_increase_count_for_author',0)),)
		else:
			integral_setting = IntegralStrategySttings.objects.create(
				webapp_id=request.user.get_profile().webapp_id,
				be_member_increase_count=int(request.POST.get('be_member_increase_count',0)),
				integral_each_yuan = int(request.POST.get('integral_each_yuan',0)),
				click_shared_url_increase_count_after_buy=int(request.POST.get('click_shared_url_increase_count_after_buy',0)),
				click_shared_url_increase_count_before_buy=int(request.POST.get('click_shared_url_increase_count_before_buy',0)),
				buy_via_shared_url_increase_count_for_buyer=int(request.POST.get('buy_via_shared_url_increase_count_for_buyer',0)),
				buy_via_shared_url_increase_count_for_author=int(request.POST.get('buy_via_shared_url_increase_count_for_author',0)),
				)
	
		return HttpResponseRedirect('/mall/editor/postagesettingses/')

###########################################################
#商城面板： list_panel
###########################################################
def list_panel(request):
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SHOP_SETTINGS_NAV,
	})
	return render_to_response('mall/editor/mall_panel.html', c)


########################################################################
# export_order_list:  导出订单列表
########################################################################
@login_required
def export_order_list(request):
    status = {
        '0':u'待支付',
        '1':u'已取消',
        '2':u'已支付',
        '3':u'待发货',
        '4':u'已发货',
        '5':u'已完成'
    }

    orders = [
        [u'下单时间',u'订单号',u'金额',u'订单状态',u'出货数',u'收货人']
    ]

    order_list = None
    #购买数量
    number = 0

    order_send_count = 0

    order_list = Order.objects.all().order_by('-created_at')
    #订单总量
    order_count = order_list.count()
    #总金额
    order_total = order_list.filter(status=5).aggregate(total=Sum('total_price'))
    total = 0
    if order_total:
        if order_total['total']:
           total = order_total['total']
    #已完成
    order_finish_count = order_list.filter(status=5).count()



    for order in order_list:
        number_list = OrderHasProduct.objects.filter(order_id=order.id).aggregate(number=Sum('number'))
        if number_list['number']:
            number = number_list['number']

        #出货
        if order.status == 5:
            order_send_count += number

        orders.append([
            order.created_at.strftime('%Y-%m-%d %H:%M'),
            order.order_id,
            order.total_price,
            status[str(order.status)],
            number,
            order.ship_name
        ])

    orders.append([
        u'总计',
        u'订单量:'+str(order_count),
        u'已完成:'+str(order_finish_count),
        u'出货:'+str(order_send_count),
        u'金额:'+str(total),
        u''
    ])

    return ExcelResponse(orders,output_name=u'订单列表'.encode('utf8'),force_csv=False)


########################################################################
# export_order_csv:  导出订单图表数据
########################################################################
@login_required
def export_order_csv(request):
	
	days = request.GET.get('date_time')
	elements = request.GET.get('types','')
	
	titles = {
        u'1':u'日订单量',
        u'2':u'日出货量',
        u'3':u'日总金额'
    }
	
	title_list = [u'']
	
	
	if elements:
	 	elements = elements.split(',')
	 	
	for el in elements:
	 	title_list.append(titles[el])
	
	orders_data = [title_list,]

	total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
	date_list = dateutil.get_date_range_list(low_date, high_date)
	if low_date == high_date:
		orders = Order.objects.filter(created_at__year=low_date.year, created_at__month=low_date.month, created_at__day=low_date.day)
	else:
		if days != u'7':
		   high_date = high_date + timedelta(days = 1)
		else:
			date_list = date_list[:len(date_list)-1]
           

			
		orders = Order.objects.filter(created_at__range=(low_date, high_date))



	date2count = dict([(o, o) for o in range(1,7)])



	for loop_date in date_list:
		x = (loop_date - low_date).days
		data = [loop_date.strftime('%Y-%m-%d'),]
		for e in elements:
			orders_filter_by_date = orders.filter(created_at__year=loop_date.year, created_at__month=loop_date.month, created_at__day=loop_date.day)
			if u'1' == e:
				count = orders_filter_by_date.count()
				data.append(count)

			if u'2' == e:
				count = 0
				for order in orders_filter_by_date.filter(status__gt=1):
				 	for order_has_product in OrderHasProduct.objects.filter(order=order):
				 		count = count + order_has_product.number
				data.append(count)

			if u'3' == e:
				total_price = 0
				for order in orders_filter_by_date.filter(status__gt=1):
					total_price = total_price+order.total_price

				data.append(total_price)
				
		orders_data.append(data)
				
	

	return ExcelExport(orders_data,output_name=u'图表数据汇总'.encode('utf8'),force_csv=False)


def category_has_product_delete(request, id):
	category_has_product = CategoryHasProduct.objects.get(id = id)
	category = category_has_product.category
	category.product_count = category.product_count - 1
	category.save()
	CategoryHasProduct.objects.filter(id = id).delete()

	return HttpResponseRedirect('/mall/editor/productcategories/')