# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from webapp.modules.mall import request_util
from mall import module_api as mall_api
from account.models import UserProfile, OperationSettings
from cache import webapp_cache
from . import utils

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


def list_products(request):
	"""显示"商品列表"页面
	"""
	template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	category_id = int(request.GET.get('category_id', 0))
	category, products = webapp_cache.get_webapp_products(
		request.user_profile, request.is_access_weizoom_mall,
		category_id)
	products = utils.get_processed_products(request, products)
	product_categories = webapp_cache.get_webapp_product_categories(request.user_profile, request.is_access_weizoom_mall)
	has_category = False
	if len(product_categories) > 0:
		has_category = True
	c = RequestContext(request, {
		'page_title': u'商品列表(%s)' % (category.name if hasattr(category, 'name') else category['name']),
		'products': products,
		'category': category,
		'is_deleted_data': category.is_deleted if hasattr(category, 'is_deleted') else False,
		#'shopping_cart_product_nums': mall_api.get_shopping_cart_product_nums(request.webapp_user),
		'product_categories': product_categories,
		'has_category': has_category,
		'hide_non_member_cover': True
	})
	if hasattr(request, 'is_return_context'):
		return c
	if request.user.is_weizoom_mall:
		return render_to_response('%s/products.html' % template_dir, c)
	else:
		return render_to_response('%s/products_original.html' % template_dir, c)


def get_product(request):
	"""显示“商品详情”页面
	"""
	discount = utils.get_vip_discount(request)
	member_grade_id = utils.get_user_member_grade_id(request)
	template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	product_id = request.GET['rid']
	member_grade_id = request.member.grade_id if request.member else None
	product = mall_api.get_product_detail_refactor(request.webapp_owner_id, product_id, member_grade_id)
	product = utils.get_display_price(discount, member_grade_id, product)
	#product.fill_model()

	if product.is_deleted:
		c = RequestContext(request, {
			'is_deleted_data': True
		})
		return render_to_response('%s/product_detail.html' % request.template_dir, c)

	if product.promotion:
		product.promotion['is_active'] = product.promotion_model.is_active
		product.promotion['detail']['cut_price'] = product.price_info['display_price'] - product.display_price
	jsons = [{
		"name": "models",
		"content": product.models
	}, {
		'name': 'priceInfo',
		'content': product.price_info
	}, {
		'name': 'promotion',
		'content': product.promotion
	}]
	#获得运费计算因子
	#postage_factor = mall_util.get_postage_factor(request.webapp_owner_id, product=product)

	###################################################
	non_member_followurl = None
	if request.user.is_weizoom_mall:
		product.is_can_buy_by_product(request)
		otherProfile = UserProfile.objects.get(user_id=product.owner_id)
		otherSettings = OperationSettings.objects.get(owner=otherProfile.user)
		if otherSettings.weshop_followurl.startswith('http://mp.weixin.qq.com'):
			non_member_followurl = otherSettings.weshop_followurl

			# liupeiyu 记录点击关注信息
			non_member_followurl = './?woid={}&module=mall&model=concern_shop_url&action=show&product_id={}&other_owner_id={}'.format(request.webapp_owner_id, product.id, product.owner.id)

	request.should_hide_footer = True

	usable_integral = request.member.integral if request.member else 0
	use_integral = request.member.integral if request.member else 0

	is_non_member = True if request.member else False

	c = RequestContext(request, {
		'page_title': product.name,
		'product': product,
		'jsons': jsons,
		'is_deleted_data': product.is_deleted if hasattr(product, 'is_deleted') else False,
		'is_enable_get_coupons': settings.IS_IN_TESTING,
		'model_property_size': len(product.product_model_properties),
		# 'postage_factor': json.dumps(product.postage_factor),
		'hide_non_member_cover': True,
		'non_member_followurl': non_member_followurl,
		'price_info': product.price_info,
		'usable_integral': usable_integral,
		'use_integral': use_integral,
		'is_non_member': is_non_member,
		'per_yuan': request.webapp_owner_info.integral_strategy_settings.integral_each_yuan,
		#add by bert 增加分享时显示信息
		'share_page_desc': product.name,
		'share_img_url': product.thumbnails_url
	})

	if hasattr(request, 'is_return_context'):
		return c, product
	else:
		return render_to_response('%s/product_detail.html' % template_dir, c)


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
