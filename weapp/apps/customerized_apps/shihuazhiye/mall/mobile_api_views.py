# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

from apps.customerized_apps.shihuazhiye.mall import request_api_util as shihuazhiye_api_util
from webapp.modules.mall import request_util

from apps.register import mobile_api

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
@mobile_api(resource='order', action='pay')
def pay_order(request):
	return shihuazhiye_api_util.pay_order(request)

@mobile_api(resource='result_notify', action='pay')
def pay_result_notify(request, webapp_id):
	return request_api_util.pay_result_notify(request, webapp_id)


########################################################################
#save_order: 保存订单
########################################################################
@mobile_api(resource='order', action='save')
def save_order(request):
	return shihuazhiye_api_util.save_order(request)


########################################################################
# save_address: 保存订单详情
########################################################################
@mobile_api(resource='address', action='save')
def save_address(request):
	return request_api_util.save_address(request)


########################################################################
# add_shopping_cart: 将商品加入购物车
########################################################################
@mobile_api(resource='shopping_cart', action='add')
def add_shopping_cart(request):
	return request_api_util.add_shopping_cart(request)


########################################################################
# delete_shopping_cart: 删除购物车内容
########################################################################
@mobile_api(resource='shopping_cart', action='delete')
def delete_shopping_cart(request):
	return request_api_util.delete_shopping_cart(request)


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
# save_address: 保存地址
########################################################################
def save_address(request):
	return request_api_util.save_address(request)

########################################################################
# select_address: 选择地址
########################################################################
def select_address(request):
	return request_api_util.select_address(request)
