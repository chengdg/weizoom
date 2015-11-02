# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from django.http import HttpResponseRedirect

from webapp.modules.mall import request_util

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates/webapp' % template_path_items[-1]

def get_homepage(request):
	print('home---here')
	return request_util.get_homepage(request)

def list_products(request):
	"""显示"商品列表"页面
	"""
	# 2015-10-20
	# if request.user.is_weizoom_mall:
	# 	# 微众商城跳至微众商城首页
	# 	return __weshop_index(request)
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.list_products(request)


def get_product(request):
	"""显示“商品详情”页面
	"""
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
	'''	显示购物车详情
	'''
	if request.user.is_weizoom_mall:
		# 微众商城跳至微众商城首页
		return __weshop_index(request)
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)

	# product_groups, invalid_products = mall_api.get_shopping_cart_products(request.webapp_user, request.webapp_owner_id)

	# product_groups = utils.sorted_product_groups_by_promotioin(product_groups)
	# request.should_hide_footer = True

	# jsons = [{
	# 	"name": "productGroups",
	# 	"content": utils.format_product_group_price_factor(product_groups)
	# }]

	# c = RequestContext(request, {
	# 	'is_hide_weixin_option_menu': True,
	# 	'page_title': u'购物车',
	# 	'product_groups': product_groups,
	# 	'invalid_products': invalid_products,
	# 	'jsons': jsons
	# })
	return request_util.show_shopping_cart(request)


def edit_shopping_cart_order(request):
	"""编辑从购物车产生的订单
	"""
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	# 如果有收货人信息
	if request.webapp_user.ship_info and request.webapp_user.ship_info.ship_name:
		return request_util.edit_shopping_cart_order(request)
	else:
		return request_util.edit_address(request)

# jz 2015-10-09
# def pay_weizoompay_order(request):
# 	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
# 	return request_util.pay_weizoompay_order(request)

# jz 2015-10-09
# def get_weizoompay_confirm(request):
# 	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
# 	return request_util.get_weizoompay_confirm(request)
# def get_weizoomcard_change_intr(request):
# 	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
# 	return request_util.get_weizoomcard_change_intr(request)

# 功能迁移到js
# def _get_redirect_url_query_string(request):
# 	# 入口是图文
# 	sign = request.GET.get('sign', None)
# 	if sign == 'material_news':
# 		return u'woid={}&module=mall&model=address&action=list&sign=material_news'.format(request.webapp_owner_id)
#
# 	# 参数中包含
# 	redirect_url_query_string = request.GET.get('redirect_url_query_string', None)
# 	if redirect_url_query_string:
# 		if 'user_center' in redirect_url_query_string:
# 			return u'woid={}&module=mall&model=address&action=list&sign=material_news'.format(request.webapp_owner_id)
# 		return redirect_url_query_string
#
# 	# 当前页面的参数
# 	if 'product_ids' in request.REQUEST or 'product_id' in request.REQUEST:
# 		return request.META.get('QUERY_STRING', '')
#
# 	# 前一页的参数
# 	strs = request.META.get('HTTP_REFERER', '').split('/?')
# 	if len(strs) > 1:
# 		return strs[1]
#
# 	return '#'


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
	return request_util.list_address(request)


########################################################################
# add_address: 添加收货地址
########################################################################
def add_address(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.edit_address(request)


########################################################################
# edit_address: 编辑收货地址
########################################################################
def edit_address(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	request.action = 'edit'
	return request_util.edit_address(request)


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


def __weshop_index(request):
	'''跳转至微众商城首页
	'''
	return HttpResponseRedirect('?workspace_id=home_page&webapp_owner_id=216&workspace_id=866&state=123&fmt=%s' % request.GET.get('fmt', ''))