# -*- coding: utf-8 -*-

import time
# from datetime import timedelta, datetime, date
# import urllib, urllib2
# import os
# import json
# import shutil

# from django.http import HttpResponseRedirect, HttpResponse,Http404
# from django.template import Context, RequestContext
# from django.contrib.auth.decorators import login_required, permission_required
# from django.conf import settings
# from django.shortcuts import render_to_response
# from django.contrib.auth.models import User, Group, Permission
# from django.contrib import auth
# from django.db.models import Q

# from core.jsonresponse import JsonResponse, create_response
# from core import dateutil
# from core import paginator
# from core import chartutil

from core.alipay.alipay_submit import *
# from core import dateutil
# from core import paginator
# from core.exceptionutil import full_stack
# from core.alipay.alipay_notify import AlipayNotify
# from core.alipay.alipay_submit import AlipaySubmit
from account.models import UserProfile
from modules.member.models import *
# from modules.member.util import *
# import httplib
from mall.models import *
from modules.member.models import WebAppUser
from account.models import *
from mall.models import *

from tools.regional.views import get_str_value_by_string_ids
from core.send_order_email_code import *
# from watchdog.utils import watchdog_debug


def get_postage_for_weight(weight, postage_config, special_factor=None):
	"""
	获得指定运费模板、商品重量对应的运费
	"""
	if special_factor:
		# 有特殊运费
		if weight <= postage_config.first_weight:
			return float('%.2f' % special_factor.get('firstWeightPrice'))

		if not postage_config.is_enable_added_weight:
			return float('%.2f' % special_factor.get('firstWeightPrice'))

		price = special_factor.get('firstWeightPrice')
		weight = weight - postage_config.first_weight

		added_weight_count = 1
		added_weight = float(postage_config.added_weight)
		added_weight_price = float(special_factor.get('addedWeightPrice'))
	else:
		if weight <= postage_config.first_weight:
			return float('%.2f' % postage_config.first_weight_price)

		if not postage_config.is_enable_added_weight:
			return float('%.2f' % postage_config.first_weight_price)

		price = postage_config.first_weight_price
		weight = weight - postage_config.first_weight

		added_weight_count = 1
		added_weight = float(postage_config.added_weight)
		added_weight_price = float(postage_config.added_weight_price)

	while True:
		weight = float('%.2f' % weight) - float('%.2f' % added_weight)
		if weight <= 0:
			break
		else:
			added_weight_count += 1
	added_price = added_weight_count * added_weight_price
	return float('%.2f' % (price + added_price))


def get_postage_for_products(postage_configs, products, province_id=0):
	"""
	获得一批商品的运费
	"""
	# 获取postage config
	if len(products) == 1:
		if products[0].type == PRODUCT_INTEGRAL_TYPE:
			postage_config = filter(lambda c: c.is_system_level_config, postage_configs)[0]
		else:
			postage_config = filter(lambda c: c.is_used, postage_configs)[0]
	else:
		postage_config = filter(lambda c: c.is_used, postage_configs)[0]

	total_weight = 0.0
	for product in products:
		if product.postage_id > 0:
			total_weight += float(product.weight) * product.purchase_count

	factor = postage_config.factor
	if province_id > 0:
		special_factor = factor.get('special_factor', None)
		if special_factor:
			province_special_factor = special_factor.get('province_{}'.format(province_id))
			if province_special_factor:
				return get_postage_for_weight(total_weight, postage_config, province_special_factor)

	return get_postage_for_weight(total_weight, postage_config)


def get_postage_for_all_models(webapp_owner_id, product, postage_config=None):
	"""
	获得商品的所有规格的运费
	商品详情页面调用，暂时不用
	"""
	if not postage_config:
		if product.type == PRODUCT_INTEGRAL_TYPE:
			# 1、积分商品 免运费
			postage_configs = PostageConfig.objects.filter(owner_id=webapp_owner_id, is_system_level_config=True)
		else:
			# 2、普通商品
			postage_configs = PostageConfig.objects.filter(owner_id=webapp_owner_id, is_used=True)

		if postage_configs.count() > 0:
			postage_config = postage_configs[0]
		else:
			return None

	for model in product.models:
		if model["price"] == 0:
			model["postage"] = 0.0
		else:
			_, model["postage"] = get_postage_for_weight(webapp_owner_id, model['weight'], postage_config)

	return postage_config


########################################################################
# get_postage_factor: 获得运费计算因子
# 1、当该商品为 积分商品时， 免运费
# 2、普通商品 计算运费
########################################################################
def get_postage_factor(webapp_owner_id, product=None):
	if product and (product.type == PRODUCT_INTEGRAL_TYPE or product.postage_id < 0):
		# 1、积分商品 免运费
		postage_configs = PostageConfig.objects.filter(owner_id=webapp_owner_id, is_system_level_config=True)
	else:
		# 2、普通商品
		#_update_default_postage_config(webapp_owner_id)
		postage_configs = PostageConfig.objects.filter(owner_id=webapp_owner_id, is_used=True)

	if postage_configs.count() > 0:
		postage_config = postage_configs[0]
		factor = {
			'firstWeight': postage_config.first_weight,
			'firstWeightPrice': postage_config.first_weight_price,
			'isEnableAddedWeight': postage_config.is_enable_added_weight,
		}

		if postage_config.is_enable_added_weight:
			factor['addedWeight'] = float(postage_config.added_weight)
			if postage_config.added_weight_price:
				factor['addedWeightPrice'] = float(postage_config.added_weight_price)
			else:
				factor['addedWeightPrice'] = 0

		# 特殊运费配置
		special_factor = dict()
		for special_config in postage_config.get_special_configs():
			for has_province in special_config.get_special_has_provinces():
				s_factor = {
					'firstWeight': postage_config.first_weight,
					'firstWeightPrice': special_config.first_weight_price,
					'isEnableAddedWeight': postage_config.is_enable_added_weight,
					'addedWeight': float(postage_config.added_weight),
					'addedWeightPrice': float(special_config.added_weight_price)
				}

				special_factor['province_{}'.format(has_province.province.id)] = s_factor

		factor['special_factor'] = special_factor
		return factor
	else:
		return {}


########################################################################
# _update_default_postage_config: 修改运费默认配置
# 当改owner_id下的运费没有默认使用的
# 将‘免运费’设置为启用
########################################################################
def _update_default_postage_config(webapp_owner_id):
	postages = PostageConfig.objects.filter(owner_id=webapp_owner_id)
	if postages.filter(is_used=True).count() == 0:
		postages.filter(is_system_level_config=True).update(is_used=True)


########################################################################
# email_order: 订单状态改变发送邮件
########################################################################
def email_order(order):

	from account.util import notify_order
	from mall.promotion.models import Coupon

	order_has_products = OrderHasProduct.objects.filter(order=order)
	buy_count = ''
	product_name = ''
	product_pic_list = []
	for order_has_product in order_has_products:
		buy_count = buy_count+str(order_has_product.number)+','
		product_name = product_name+order_has_product.product.name+','
		product_pic_list.append(order_has_product.product.thumbnails_url)
	buy_count = buy_count[:-1]
	product_name = product_name[:-1]

	user = UserProfile.objects.get(webapp_id=order.webapp_id).user

	if order.coupon_id == 0:
		coupon = ''
	else:
		coupon = str(Coupon.objects.get(id=int(order.coupon_id)).coupon_id)+u',￥'+str(order.coupon_money)

	try:
		area = get_str_value_by_string_ids(order.area)
	except:
		area = order.area
	else:
		area = u''

	buyer_address = area+u" "+order.ship_address

	if order.status == 0:
		status = 0
		order_status = u"待支付"
	elif order.status == 3:
		status = 1
		order_status = u"待发货"
	elif order.status == 4:
		status = 2
		order_status = u"已发货"
	elif order.status == 5:
		status = 3
		order_status = u"已完成"
	elif order.status == 1:
		status = 4
		order_status = u"已取消"
	elif order.status == 6:
		status = 5
		order_status = u"退款中"
	elif order.status == 7:
		status = 6
		order_status = u"退款完成"
	else:
		status = -1
		order_status = ''

	try:
		member= WebAppUser.get_member_by_webapp_user_id(order.webapp_user_id)
		if member is not None:
			member_id = member.id
		else:
			member_id = -1
	except :
		member_id = -1

	if order.express_company_name:
		from tools.express.util import  get_name_by_value
		express_company_name = get_name_by_value(order.express_company_name)
	else:
		express_company_name = ""
	if order.express_number:
		express_number = order.express_number
	else:
		express_number = ''

	notify_order(
			user=user,
			member_id=member_id,
			status=status,
			order_id=order.order_id,
			buyed_time=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),
			order_status=order_status,
			buy_count=buy_count,
			total_price=order.final_price,
			bill=order.bill,
			coupon=coupon,
			product_name=product_name,
			integral = order.integral,
			buyer_name=order.ship_name,
			buyer_address=buyer_address,
			buyer_tel=order.ship_tel,
			remark=order.customer_message,
			product_pic_list=product_pic_list,
			postage=order.postage,
			express_company_name=express_company_name,
			express_number=express_number
			)



