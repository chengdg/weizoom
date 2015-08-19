# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.shortcuts import render_to_response
from webapp.modules.mall import request_util
# from apps.customerized_apps.shihuazhiye.mall import request_util
from mall.models import *
from apps.register import mobile_view_func

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates/webapp' % template_path_items[-1]
TEMPLATE_DIR = 'webapp/mall'


########################################################################
#      PAGE FOR TESTING - 测试用页面
#
# list_coupons: 显示"优惠券"页面
########################################################################
# jz 2015-08-10
# def list_coupons(request):
# 	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
# 	return request_util.list_coupons(request)


########################################################################
# get_productcategory: 显示“商品分类”页面
########################################################################
# jz 2015-08-10
# def get_productcategory(request):
# 	request.template_dir = TEMPLATE_DIR
# 	return request_util.get_productcategory(request)


########################################################################
# list_products: 显示"商品列表"页面
########################################################################
@mobile_view_func(resource='products', action='list')
def list_products(request):
	request.template_dir = TEMPLATE_DIR
	request.is_return_context = True
	context = request_util.list_products(request)
	context.update({
		'page_title': context.get('page_title','商品').replace(u'商品',u'课程')
		})
	return render_to_response('%s/products_original.html' % request.template_dir, context)
	#return request_util.list_products(request)


########################################################################
# get_product: 显示“商品详情”页面
########################################################################
@mobile_view_func(resource='product', action='get')
def get_product(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.get_product(request)

########################################################################
# get_order_list: 获取订单列表
########################################################################
@mobile_view_func(resource='order_list', action='get')
def get_order_list(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.get_order_list(request)
	




########################################################################
# edit_order: 编辑订单
########################################################################
@mobile_view_func(resource='order', action='edit')
def edit_order(request):
	request.template_dir = TEMPLATE_DIR
	# return request_util.edit_order(request)
	request.redirect_url_query_string = _get_redirect_url_query_string(request)
	request.is_return_context = True
	if request.webapp_user.ship_info and request.webapp_user.ship_info.ship_name:
		context = request_util.edit_order(request)
		context.update({
			'page_title': u'编辑个人信息'
			})
		return render_to_response('%s/order_confirm.html' % request.template_dir, context)
	else:
		request.action = 'add'
		context = request_util.edit_address(request)
		context.update({
			'page_title': u'编辑个人信息'
			})
		return render_to_response('%s/order_address.html' % request.template_dir, context)

########################################################################
# edit_address: 编辑收货地址信息
########################################################################
@mobile_view_func(resource='address', action='edit')
def edit_address(request):
	request.template_dir = TEMPLATE_DIR
	request.is_return_context = True
	request.redirect_url_query_string = _get_redirect_url_query_string(request)
	request.action = 'edit'
	context = request_util.edit_address(request)
	ship_info = context.get('ship_info')
	ship_address = ship_info.ship_address.split(',')
	if len(ship_address) == 3:
		ship_info.ship_address = ship_address[0]
		ship_info.post = ship_address[1]
		ship_info.recommend = ship_address[2]
	context.update({
		'ship_info': ship_info,
		'page_title': u'编辑个人信息'
		})
	return render_to_response('%s/order_address.html' % request.template_dir, context)

########################################################################
# list_address: 显示收货地址列表
########################################################################
@mobile_view_func(resource='address', action='list')
def list_address(request):
	request.template_dir = TEMPLATE_DIR
	request.redirect_url_query_string = _get_redirect_url_query_string(request)
	return request_util.list_address(request)


########################################################################
# add_address: 添加收货地址
########################################################################
@mobile_view_func(resource='address', action='add')
def add_address(request):
	request.template_dir = TEMPLATE_DIR
	request.redirect_url_query_string = _get_redirect_url_query_string(request)
	request.action = 'add'
	return request_util.edit_address(request)

########################################################################
# show_coupon: 显示优惠价
########################################################################
def show_coupon(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.show_coupon(request)

def _get_redirect_url_query_string(request):
	# 参数中包含
	redirect_url_query_string = request.GET.get('redirect_url_query_string', None)
	if redirect_url_query_string:
		return redirect_url_query_string

	# 当前页面的参数
	if 'product_ids' in request.REQUEST or 'product_id' in request.REQUEST:
		return request.META.get('QUERY_STRING', '')

	# 前一页的参数
	strs = request.META.get('HTTP_REFERER', '').split('/?')
	if len(strs) > 1:	
		return strs[1]

	return '#'

########################################################################
# pay_order: 支付订单页面
########################################################################
@mobile_view_func(resource='order', action='pay')
def pay_order(request):
	request.template_dir = TEMPLATE_DIR
	request.is_return_context = True
	context = request_util.pay_order(request)
	_update_status(context)
	return render_to_response('%s/order_payment.html' % request.template_dir, context)


def _update_status(context):
	try:
		order = context.get('order')
		if order.status == ORDER_STATUS_PAYED_NOT_SHIP:
			db_order = Order.objects.get(order_id=order.order_id)
			db_order.status = ORDER_STATUS_SUCCESSED
			order.status = ORDER_STATUS_SUCCESSED
			db_order.save()

		ship_address = order.ship_address.split(',')
		order.ship_address = ship_address[0]
		order.post = ship_address[1]
		order.recommend = ship_address[2]
		context.update({
			'order' : order,
			'order_status_info': STATUS2TEXT[order.status]
		})
	except:
		pass

########################################################################
# get_pay_result: 支付结果，在支付宝完成支付后支付宝访问
# 携带的参数中主要使用：
# out_trade_no 订单号
########################################################################
@mobile_view_func(resource='pay_result', action='get')
def get_pay_result(request):
	request.template_dir = TEMPLATE_DIR
	request.is_return_context = True
	context = request_util.get_pay_result(request)
	_update_status(context)
	return render_to_response('%s/order_payment.html' % request.template_dir, context)



########################################################################
# get_pay_notify_result : 支付宝异步 回调接口
########################################################################
@mobile_view_func(resource='pay_notify_result', action='get')
def get_pay_notify_result(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.get_pay_notify_result(request)


########################################################################
# show_shopping_cart: 显示购物车详情
########################################################################
@mobile_view_func(resource='shopping_cart', action='show')
def show_shopping_cart(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.show_shopping_cart(request)


########################################################################
# edit_shopping_cart_order: 编辑从购物车产生的订单
########################################################################
@mobile_view_func(resource='shopping_cart_order', action='edit')
def edit_shopping_cart_order(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.edit_shopping_cart_order(request)

@mobile_view_func(resource='weizoompay_order', action='pay')
def pay_weizoompay_order(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.pay_weizoompay_order(request)

@mobile_view_func(resource='weizoompay_confirm', action='pay')
def get_weizoompay_confirm(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.get_weizoompay_confirm(request)
	
@mobile_view_func(resource='weizoomcard_change_intr', action='pay')
def get_weizoomcard_change_intr(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.get_weizoomcard_change_intr(request)