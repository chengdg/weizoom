# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

from webapp.modules.mall import request_api_util

########################################################################
#      PAGE FOR TESTING - 测试用API
#
# consume_coupon: 领取优惠券
########################################################################
def consume_coupon(request):
	return request_api_util.consume_coupon(request)


########################################################################
# pay: 订单支付api
########################################################################
def pay_order(request):
	return request_api_util.pay_order(request)


def pay_result_notify(request, webapp_id):
	return request_api_util.pay_result_notify(request, webapp_id)


########################################################################
#save_order: 保存订单
########################################################################
def save_order(request):
	return request_api_util.save_order(request)


########################################################################
# add_shopping_cart: 将商品加入购物车
########################################################################
def add_shopping_cart(request):
	return request_api_util.add_shopping_cart(request)


########################################################################
# get_shopping_cart_product_ids: 获得购物车中商品的id集合
########################################################################
def get_shopping_cart_product_ids(request):
	return request_api_util.get_shopping_cart_product_ids(request)


########################################################################
# delete_shopping_cart: 删除购物车内容
########################################################################
def delete_shopping_cart(request):
	return request_api_util.delete_shopping_cart(request)


########################################################################
# update_shopping_cart: 更新购物车内容
########################################################################
def update_shopping_cart(request):
	return request_api_util.update_shopping_cart(request)


########################################################################
# clear_shopping_cart_invalid_products: 清空购物车中的无效商品
########################################################################
def clear_shopping_cart_invalid_products(request):
	return request_api_util.clear_shopping_cart_invalid_products(request)


########################################################################
# check_weizoom_card: 验证卡号和密码
########################################################################
def check_weizoom_card(request):
	return request_api_util.check_weizoom_card(request)

########################################################################
# pay_weizoom_card:使用微众卡支付订单
########################################################################
def pay_weizoom_card(request):
	return request_api_util.pay_weizoom_card(request)

########################################################################
# change_weizoom_card_to_integral:积分兑换
########################################################################
def change_weizoom_card_to_integral(request):
	return request_api_util.change_weizoom_card_to_integral(request)


########################################################################
# update_order_status: 修改订单状态
########################################################################
def update_order_status(request):
	return request_api_util.update_order_status(request)


########################################################################
# get_openid: 获取openid
########################################################################
def get_openid(request):
	return request_api_util.get_openid(request)

########################################################################
# get_wixin_pay_package: 获取微信支付认证信息
########################################################################
def get_wixin_pay_package(request):
	return request_api_util.get_wixin_pay_package(request)

########################################################################
# get_can_use_coupons: 获取可用优惠劵
########################################################################
# def get_can_use_coupons(request):
# 	return request_api_util.get_can_use_coupons(request)

########################################################################
# is_can_use_coupon: 是否可以使用该优惠券
########################################################################
def is_can_use_coupon(request):
	return request_api_util.is_can_use_coupon(request)

########################################################################
# save_address: 保存地址
########################################################################
def save_address(request):
	return request_api_util.save_address(request)

########################################################################
# select_address: 选择地址
########################################################################
def select_address(request):
	return request_api_util.select_address(request)

########################################################################
# list_address: localStorage获取地址信息
########################################################################
def list_address(request):
	return request_api_util.list_address(request)

########################################################################
# delete_address: 删除收获地址
########################################################################
def delete_address(request):
	return request_api_util.delete_address(request)

########################################################################
# check_shopping_cart_products: 检查购物车商品有效性
########################################################################
def check_shopping_cart_products(request):
	return request_api_util.check_shopping_cart_products(request)

def get_products_stocks(request):
	return request_api_util.products_stocks(request)

def get_product_stocks(request):
	return request_api_util.product_stocks(request)

def update_wishlist_product(request):
	"""
	更新商品收藏
	"""
	return request_api_util.update_wishlist_product(request)

def check_product_in_wishlist(request):
	"""
	检查商品是否在收藏夹
	"""
	return request_api_util.check_product_in_wishlist(request)

# def get_product_detail(request):
# 	"""
# 	获取商品的介绍信息
# 	"""
# 	return request_api_util.get_product_detail(request)


def create_product_review(request):
    return request_api_util.create_product_review(request)

def create_product_review2(request):
    return request_api_util.create_product_review2(request)

def update_product_review_picture(request):
    '''
    为指定商品评论添加晒图
    PreCondition: product_review_id, picture_list
    '''
    return request_api_util.update_product_review_picture(request)


def get_member_product_info(request):
	'''
	获取购物车的数量和检查商品是否已被收藏
	'''
	return request_api_util.get_member_product_info(request)