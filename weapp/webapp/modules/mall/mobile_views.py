# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from webapp.modules.mall import request_util

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates/webapp' % template_path_items[-1]


########################################################################
#      PAGE FOR TESTING - 测试用页面
#
# list_coupons: 显示"优惠券"页面
########################################################################
def list_coupons(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.list_coupons(request)


########################################################################
# get_productcategory: 显示“商品分类”页面
########################################################################
# def get_productcategory(request):
# 	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
# 	return request_util.get_productcategory(request)


########################################################################
# list_products: 显示"商品列表"页面
########################################################################
def list_products(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.list_products(request)


########################################################################
# get_product: 显示“商品详情”页面
########################################################################
def get_product(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_product(request)

########################################################################
# get_order_list: 获取订单列表
########################################################################
def get_order_list(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_order_list(request)


########################################################################
# edit_order: 编辑订单
########################################################################
def edit_order(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	request.redirect_url_query_string = _get_redirect_url_query_string(request)
	if request.webapp_user.ship_info and request.webapp_user.ship_info.ship_name:
		return request_util.edit_order(request)
	else:
		request.action = 'add'
		return request_util.edit_address(request)


########################################################################
# pay_order: 支付订单页面
########################################################################
def pay_order(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.pay_order(request)


########################################################################
# get_pay_result: 支付结果，在支付宝完成支付后支付宝访问
# 携带的参数中主要使用：
# out_trade_no 订单号
########################################################################
def get_pay_result(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_pay_result(request)


########################################################################
# get_pay_notify_result : 支付宝异步 回调接口
########################################################################
def get_pay_notify_result(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_pay_notify_result(request)


########################################################################
# get_order_pay_result_success : 实付金额为0元时，直接跳转
########################################################################
def get_pay_result_success(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_pay_result_success(request)


########################################################################
# show_shopping_cart: 显示购物车详情
########################################################################
def show_shopping_cart(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.show_shopping_cart(request)


########################################################################
# edit_shopping_cart_order: 编辑从购物车产生的订单
########################################################################
def edit_shopping_cart_order(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	request.redirect_url_query_string = _get_redirect_url_query_string(request)
	if request.webapp_user.ship_info and request.webapp_user.ship_info.ship_name:
		print("*"*20, 'edit_shopping_cart_order', ' : 1')
		return request_util.edit_shopping_cart_order(request)
	else:
		print("*"*20, 'edit_shopping_cart_order', ' : 2')
		request.action = 'add'
		return request_util.edit_address(request)

def pay_weizoompay_order(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.pay_weizoompay_order(request)

def get_weizoompay_confirm(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_weizoompay_confirm(request)

def get_weizoomcard_change_intr(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_weizoomcard_change_intr(request)

def _get_redirect_url_query_string(request):
	# 入口是图文
	sign = request.GET.get('sign', None)
	if sign == 'material_news':
		return u'woid={}&module=mall&model=address&action=list&sign=material_news'.format(request.webapp_owner_id)

	# 参数中包含
	redirect_url_query_string = request.GET.get('redirect_url_query_string', None)
	if redirect_url_query_string:
		if 'user_center' in redirect_url_query_string:
			return u'woid={}&module=mall&model=address&action=list&sign=material_news'.format(request.webapp_owner_id)
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
# show_concern_shop_url: 点击关注店铺
########################################################################
def show_concern_shop_url(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.show_concern_shop_url(request)


########################################################################
# list_address: 收货地址列表
########################################################################
def list_address(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	request.redirect_url_query_string = _get_redirect_url_query_string(request)
	return request_util.list_address(request)


########################################################################
# add_address: 添加收货地址
########################################################################
def add_address(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	request.redirect_url_query_string = _get_redirect_url_query_string(request)
	request.action = 'add'
	return request_util.edit_address(request)


########################################################################
# edit_address: 编辑收货地址
########################################################################
def edit_address(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	request.redirect_url_query_string = _get_redirect_url_query_string(request)
	request.action = 'edit'
	return request_util.edit_address(request)



########################################################################
# delete_address: 删除收获地址
########################################################################
def delete_address(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	request.redirect_url_query_string = _get_redirect_url_query_string(request)
	return request_util.delete_address(request)


########################################################################
# success_alert: 成功提示页
########################################################################
def success_alert(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.success_alert(request)


########################################################################
# success_alert: 成功提示页
########################################################################
def get_express_detail(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_express_detail(request)


########################################################################
# create_goods_review: 创建商品评论
########################################################################
def create_product_review(request):
    request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
    return request_util.create_product_review(request)


########################################################################
# get_product_review_successful_page: 创建商品评论
########################################################################
def get_product_review_successful_page(request):
    request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
    return request_util.get_product_review_successful_page(request)


########################################################################
# get_order_review: 会员订单中未评价订单列表
########################################################################
def get_order_review_list(request):
    request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
    return request_util.get_order_review_list(request)


def get_product_review_list(request):
    request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
    return request_util.get_product_review_list(request)


def update_product_review_picture(request):
    request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
    return request_util.update_product_review_picture(request)


def redirect_product_review(request):
    request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
    return request_util.redirect_product_review(request)


#add by bert 
def edit_refueling_order(request):
    request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
    return request_util.edit_refueling_order(request)	