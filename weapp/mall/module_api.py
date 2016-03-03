# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import os
import json
import copy
import random
import math
import operator
import itertools

# from itertools import chain

#from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
#from django.shortcuts import render_to_response
#from django.contrib.auth.models import User, Group, Permission
#from django.contrib import auth
from django.db.models import Q, F
from django.db.utils import IntegrityError
from tools.regional import views as regional_util
from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import unicode_full_stack
from core import dateutil
from tools.express import util as express_util

from account.models import UserProfile
# from modules.member.models import Member, IntegralStrategySttings
# from modules.member import integral

from models import *
import signals
from core import paginator
#from market_tools.tools.delivery_plan.models import DeliveryPlan
from market_tools.tools.template_message import models as template_message_model
from market_tools.tools.template_message import module_api as template_message_api

from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_alert, watchdog_warning
from webapp.modules.mall import util as mall_util
from mall import signals as mall_signals
from mall.promotion import models as promotion_models
from mall import models as mall_models
from modules.member.module_api import get_member_by_id_list
from webapp.models import WebApp
from member.member_grade import auto_update_grade
random.seed(time.time())
from bs4 import BeautifulSoup
# NO_PROMOTION_ID = -1

def __get_promotion_name(product):
	"""判断商品是否促销， 没有返回None, 有返回促销ID与商品的规格名.

	Args:
	  product -

	Return:
	  None - 商品没有促销
	  'int_str' - 商品有促销
	"""
	name = None
	if product.promotion:
		promotion = product.promotion
		now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
		# 已过期或未开始活动的商品，做为 普通商品
		if promotion['start_date'] > now or promotion['end_date'] < now:
			name = '%d_%s' % (promotion['id'], product.model['name'])
		elif promotion['type'] == promotion_models.PROMOTION_TYPE_PRICE_CUT or promotion['type'] == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
			name = promotion['id']
		else:
			name = '%d_%s' % (promotion['id'], product.model['name'])
	elif product.integral_sale:
		return '%d_%s' % (product.integral_sale['id'], product.model['name'])

	return name


def __collect_integral_sale_rules(target_member_grade_id, products):
	"""
	收集product_group积分规则抵扣规则
	"""
	merged_rule = {
		"member_grade_id": target_member_grade_id,
		"product_model_names": []
	}
	for product in products:
		product.active_integral_sale_rule = None
		product_model_name = '%s_%s' % (product.id, product.model['name'])
		#判断积分应用是否不可用
		if hasattr(product,'integral_sale_model'):
			if not product.integral_sale_model:
				continue
			if not product.integral_sale_model.is_active:
				if product.integral_sale['detail']['is_permanant_active']:
					pass
				else:
					continue

			for rule in product.integral_sale['detail']['rules']:
				member_grade_id = int(rule['member_grade_id'])
				if member_grade_id <= 0 or member_grade_id == target_member_grade_id:
					# member_grade_id == -1则为全部会员等级
					merged_rule['product_model_names'].append(product_model_name)
					product.active_integral_sale_rule = rule
					merged_rule['rule'] = rule
			merged_rule['integral_product_info'] = str(product.id) + '-' + product.model_name
	if len(merged_rule['product_model_names']) > 0:
		return merged_rule
	else:
		return None


def __get_group_name(group_products):
	items = []
	for product in group_products:
		items.append('%s_%s' % (product.id, product.model['name']))
	# items.sort()
	return '-'.join(items)


def group_product_by_promotion(request, products):
	"""根据商品促销类型对商品进行分类
	Args:
	  products -

	Return:
	  list - [
				  {'id': ,
				   'uid': ,
				   'products':,
				   'promotion':,
				   'promotion_type': (str),
				   'promotion_result':,
				   'integral_sale_rule':,
				   'can_use_promotion':,
				   'member_grade_id': }
				  ...
			   ]
	"""
	member_grade_id, discount = get_member_discount(request)
	#按照促销对product进行聚类
	# global NO_PROMOTION_ID
	# NO_PROMOTION_ID = -1  # 负数的promotion id表示商品没有promotion
	product_groups = []
	promotion2products = {}
	group_id = 0
	for product in products:
		product.original_price = product.price
		if product.is_member_product:
			product.price = round(product.price * discount / 100, 2)
		#对于满减，同一活动中不同规格的商品不能分开，其他活动，需要分开
		group_id += 1
		default_products = {"group_id": group_id, "products": []}
		promotion_name = __get_promotion_name(product)
		promotion2products.setdefault(promotion_name, default_products)['products'].append(product)
	now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	items = promotion2products.items()
	items.sort(lambda x, y: cmp(x[1]['group_id'], y[1]['group_id']))
	for promotion_id, group_info in items:
		products = group_info['products']
		group_id = group_info['group_id']
		group_unified_id = __get_group_name(products)
		integral_sale_rule = __collect_integral_sale_rules(member_grade_id, products) if member_grade_id != -1 else None

		promotion = products[0].promotion
		# 商品没有参加促销
		if not promotion or promotion_id <= 0:
			product_groups.append({
				"id": group_id,
				"uid": group_unified_id,
				'products': products,
				'promotion': {},
				"promotion_type": '',
				'promotion_result': '',
				'integral_sale_rule': integral_sale_rule,
				'can_use_promotion': False,
				'member_grade_id': member_grade_id
			})
			continue


		# 如果促销对此会员等级的用户不开放
		if not has_promotion(member_grade_id, promotion.get('member_grade_id')):
			product_groups.append({
								  "id": group_id,
								  "uid": group_unified_id,
								  'products': products,
								  'promotion': {},
								  "promotion_type": '',
								  'promotion_result': '',
								  'integral_sale_rule': integral_sale_rule,
								  'can_use_promotion': False,
								  'member_grade_id': member_grade_id
								  })
			continue
		promotion_type = promotion.get('type', 0)
		if promotion_type == 0:
			type_name = 'none'
		else:
			type_name = promotion_models.PROMOTION2TYPE[promotion_type]['name']

		promotion_result = None
		can_use_promotion = False
		# #判断promotion状态
		# 促销活动还未开始，或已结束
		if promotion['start_date'] > now or promotion['end_date'] < now:
			promotion['status'] = promotion_models.PROMOTION_STATUS_NOT_START if promotion['start_date'] > now else promotion_models.PROMOTION_STATUS_FINISHED
		# 限时抢购
		elif promotion_type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
			product = products[0]
			promotion_price = product.promotion['detail'].get('promotion_price', 0)
			product.price = promotion_price
			# 会员价不和限时抢购叠加
			product.member_discount_money = 0
			promotion_result = {
				"saved_money": product.original_price - promotion_price,
				"subtotal": product.purchase_count * product.price
			}

			can_use_promotion = (promotion['status'] == promotion_models.PROMOTION_STATUS_STARTED)
		# 买赠
		elif promotion_type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
			first_product = products[0]
			promotion = first_product.promotion
			promotion_detail = promotion['detail']
			can_use_promotion = (promotion['status'] == promotion_models.PROMOTION_STATUS_STARTED)

			total_purchase_count = 0
			total_product_price = 0.0
			for product in products:
				total_purchase_count += product.purchase_count
				total_product_price += product.price * product.purchase_count

			if total_purchase_count < promotion_detail['count']:
				can_use_promotion = False
			else:
				#如果满足循环满赠，则调整赠品数量
				for product in products:
					product.price = product.original_price
				if promotion_detail['is_enable_cycle_mode']:
					premium_round_count = total_purchase_count / promotion['detail']['count']
					for premium_product in promotion_detail['premium_products']:
						premium_product['original_premium_count'] = premium_product['premium_count']
						premium_product['premium_count'] = premium_product['premium_count'] * premium_round_count
			promotion_result = {
				"subtotal": product.purchase_count * product.price
			}
		# 满减
		elif promotion_type == promotion_models.PROMOTION_TYPE_PRICE_CUT:
			promotion = products[0].promotion
			promotion_detail = promotion['detail']
			total_price = 0.0
			for product in products:
				total_price += product.price * product.purchase_count
			can_use_promotion = (total_price - promotion_detail['price_threshold']) >= 0
			promotion_round_count = 1  # 循环满减执行的次数
			if promotion_detail['is_enable_cycle_mode']:
				promotion_round_count = int(total_price / promotion_detail['price_threshold'])
			if can_use_promotion:
				subtotal = total_price - promotion_detail['cut_money']*promotion_round_count
			else:
				subtotal = total_price
			promotion_result = {
				"subtotal": subtotal,
				"price_threshold": promotion_round_count*promotion_detail['price_threshold']
			}
		product_groups.append({
			"id": group_id,
			"uid": group_unified_id,
			"promotion_type": type_name,
			'products': products,
			'promotion': promotion,
			'promotion_result': promotion_result,
			'integral_sale_rule': integral_sale_rule,
			'can_use_promotion': can_use_promotion,
			'promotion_json': json.dumps(promotion),
			'member_grade_id': member_grade_id
		})
	return product_groups


def get_shopping_cart_product_nums(webapp_user):
	"""
	获得购物车中商品数量
	"""
	return ShoppingCart.objects.filter(webapp_user_id=webapp_user.id).count()


def get_products_in_webapp(webapp_id, is_access_weizoom_mall, webapp_owner_id, category_id, options=dict()):
	"""
		获得商品集合
	"""
	# products = None
	# if category_id == 0:
	# 	products = Product.objects.filter(
	# 		owner_id=webapp_owner_id, shelve_type=PRODUCT_SHELVE_TYPE_ON, is_deleted=False).exclude(
	# 		type=PRODUCT_DELIVERY_PLAN_TYPE).order_by('display_index', '-id')
	# 	if not is_access_weizoom_mall:
	# 		# 非微众商城
	# 		product_ids_in_weizoom_mall = get_product_ids_in_weizoom_mall(webapp_id)
	# 		products.exclude(id__in=product_ids_in_weizoom_mall)
	#
	#
	# else:
	# 	# try:
	# 	if not is_access_weizoom_mall:
	# 		# 非微众商城
	# 		product_ids_in_weizoom_mall = get_product_ids_in_weizoom_mall(webapp_id)
	# 		other_mall_product_ids_not_checked = []
	# 	else:
	# 		product_ids_in_weizoom_mall = []
	# 		_, other_mall_product_ids_not_checked = get_not_verified_weizoom_mall_partner_products_and_ids(webapp_id)
	#
	#
	# 	for category_has_product in category_has_products:
	# 		#微众商城要过滤掉自己的非在售 duhao 20151120
	# 		if is_access_weizoom_mall:
	# 			if category_has_product.product.weshop_status != PRODUCT_SHELVE_TYPE_ON:
	# 				continue
	#
	# 		if category_has_product.product.shelve_type == PRODUCT_SHELVE_TYPE_ON:
	# 			product = category_has_product.product
	# 			#过滤已删除商品和套餐商品
	# 			if(product.is_deleted or product.type == PRODUCT_DELIVERY_PLAN_TYPE or
	# 						product.id in product_ids_in_weizoom_mall or
	# 						product.id in other_mall_product_ids_not_checked or
	# 						product.shelve_type != PRODUCT_SHELVE_TYPE_ON):
	# 				continue

	products = None
	params = {
		'owner_id':webapp_owner_id,
		'shelve_type':PRODUCT_SHELVE_TYPE_ON,
		'is_deleted':False
	}
	if category_id!=0:

		category_has_products = CategoryHasProduct.objects.filter(category_id = category_id)
		product_ids = [p.product_id for p in category_has_products]
		params['id__in'] = product_ids
	# 微众商城代码
	# if is_access_weizoom_mall:
	# 	products = list(Product.objects.filter(**params).exclude(weshop_sync = PRODUCT_SHELVE_TYPE_ON).order_by('-id'))
	# else:
	# 	products = list(Product.objects.filter(**params).order_by('-id'))
	products = list(Product.objects.filter(**params).order_by('-id'))
	return products

# unused zhaolei 2015-11-23
# def get_products(webapp_id, is_access_weizoom_mall, webapp_owner_id, webapp_user, category_id, options=dict()):
# 	"""
# 	get_products: 获得product集合
#
# 	options可用参数：
#
# 	  1. search_info: 搜索
# 	"""
# 	watchdog_alert('过期的方法module_api.get_products', type='mall')
# 	category, products = get_products_in_webapp(webapp_id, is_access_weizoom_mall, webapp_owner_id, category_id, options)
#
# 	for product in products:
# 		#added by chuter
# 		if not isinstance(product, Product):
# 			continue
# 		product.original_price = product.price
# 		# product.price, _ = webapp_user.get_discounted_money(product.price, product_type=product.type)
#
# 	return category, products


def get_product_by_id(product_id):
	"""
	获得product信息
	"""
	if not product_id:
		return Product()

	try:
		return Product.objects.get(id=product_id)
	except:
		return Product()


#############################################################################
# get_products: 获得product集合
#   options可用参数：
#	 1. search_info: 搜索
#############################################################################
def get_product_detail_for_cache(webapp_owner_id, product_id, member_grade_id=None):
	def inner_func():
		try:
			#获取product及其model
			product = Product.objects.get(id=product_id)
			# 微众商城代码
			#防止商品的串号问题,商品没有缓存的情况下，下面不执行，直接返回
			# if product.owner_id != webapp_owner_id and webapp_owner_id!=216:
			# 	product = Product()
			# 	product.is_deleted = True
			# 	# product.mark = str(product.id) + '-' + product.model_name
			# 	data = product.to_dict(
			# 							'min_limit',
			# 							'swipe_images_json',
			# 							'models',
			# 							'_is_use_custom_model',
			# 							'product_model_properties',
			# 							'is_sellout',
			# 							'promotion',
			# 							'integral_sale',
			# 							'properties',
			# 							'product_review',
			# 							'master_promotion_title',
			# 							'integral_sale_promotion_title'
			# 	)
			# 	return {'value': data}
			# 	#直接返回
			# if product.owner_id != webapp_owner_id:
			# 	product.postage_id = -1
			# 	product.unified_postage_money = 0
			# 	product.postage_type = POSTAGE_TYPE_UNIFIED
			product.fill_model()

			#获取轮播图
			product.swipe_images = []
			for swipe_image in ProductSwipeImage.objects.filter(product_id=product_id):
				product.swipe_images.append({
					'url': swipe_image.url
				})
			product.swipe_images_json = json.dumps(product.swipe_images)

			#获取商品的评论
			product_review = ProductReview.objects.filter(
										Q(product_id=product.id) &
										Q(status__in=['1', '2'])
							).order_by('-top_time', '-id')[:2]
			product.product_review = product_review

			if product_review:
				member_ids = [review.member_id for review in product_review]
				members = get_member_by_id_list(member_ids)
				member_id2member = dict([(m.id, m) for m in members])
				for review in product_review:
					if member_id2member.has_key(review.member_id):
						review.member_name = member_id2member[review.member_id].username_for_html
						review.user_icon = member_id2member[review.member_id].user_icon
					else:
						review.member_name = '*'
			#获取促销活动和积分折扣信息
			promotion_ids = map(lambda x: x.promotion_id, promotion_models.ProductHasPromotion.objects.filter(product=product))
			# Todo: 促销已经结束， 但数据库状态未更改
			promotions = promotion_models.Promotion.objects.filter(
				owner_id=webapp_owner_id,
				id__in=promotion_ids,
				status=promotion_models.PROMOTION_STATUS_STARTED
			)
			promotion = None
			integral_sale = None
			for one_promotion in promotions:
				if one_promotion.type == promotion_models.PROMOTION_TYPE_INTEGRAL_SALE:
					integral_sale = one_promotion
				# RFC
				elif one_promotion.type != promotion_models.PROMOTION_TYPE_COUPON:
					promotion = one_promotion
			#填充积分折扣信息
			if integral_sale:
				promotion_models.Promotion.fill_concrete_info_detail(webapp_owner_id, [integral_sale])
				# integral_sale.end_date = integral_sale.end_date.strftime('%Y-%m-%d %H:%M:%S')
				# integral_sale.created_at = integral_sale.created_at.strftime('%Y-%m-%d %H:%M:%S')
				# integral_sale.start_date = integral_sale.start_date.strftime('%Y-%m-%d %H:%M:%S')
				if integral_sale.promotion_title:
					product.integral_sale_promotion_title = integral_sale.promotion_title
				product.integral_sale = integral_sale.to_dict('detail', 'type_name')
			else:
				product.integral_sale = None
			#填充促销活动信息
			if promotion:
				promotion_models.Promotion.fill_concrete_info_detail(webapp_owner_id, [promotion])
				if promotion.promotion_title:
					product.master_promotion_title = promotion.promotion_title
				if promotion.type == promotion_models.PROMOTION_TYPE_PRICE_CUT:
					promotion.promotion_title = '满%s减%s' % (promotion.detail['price_threshold'], promotion.detail['cut_money'])
				elif promotion.type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
					promotion.promotion_title = '%s * %s' % (promotion.detail['premium_products'][0]['name'], promotion.detail['count'])
				elif promotion.type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
					# promotion.promotion_title = '活动截止:%s' % (promotion.end_date)
					gapPrice = product.price - promotion.detail['promotion_price']
					promotion.promotion_title = '已优惠%s元' % gapPrice
				else:
					promotion.promotion_title = ''
				product.promotion = promotion.to_dict('detail', 'type_name')
			else:
				product.promotion = None
			Product.fill_property_detail(webapp_owner_id, [product], '')
		except:
			alert_message = u"获取商品记录失败,商品id: {} cause:\n{}".format(product_id, unicode_full_stack())
			watchdog_alert(alert_message, type='WEB')
			#返回"被删除"商品
			product = Product()
			product.is_deleted = True
			product.promotion = None

		# 商品详情图片lazyload
		soup = BeautifulSoup(product.detail)
		for img in soup.find_all('img'):
			try:
				img['data-url'] = img['src']
				del img['src']
				del img['title']
			except:
				pass
		product.detail = str(soup)

		# product.mark = str(product.id) + '-' + product.model_name
		data = product.to_dict(
								'min_limit',
								'swipe_images_json',
								'models',
								'_is_use_custom_model',
								'product_model_properties',
								'is_sellout',
								'promotion',
								'integral_sale',
								'properties',
								'product_review',
								'master_promotion_title',
								'integral_sale_promotion_title'
		)
		return {'value': data}

	return inner_func


def get_product_model_properties_for_cache(webapp_owner_id):
	def inner_func():
		properties = []
		user_profile = UserProfile.objects.filter(user_id=webapp_owner_id)
		if user_profile.count() == 1 and WeizoomMall.objects.filter(webapp_id=user_profile[0].webapp_id, is_active=True).count() == 1:
			properties = list(ProductModelProperty.objects.filter())
		else:
			properties = list(ProductModelProperty.objects.filter(owner_id=webapp_owner_id))
		id2property = {}
		property_ids = []
		for property in properties:
			id2property[property.id] = {"id":property.id, "name":property.name}
			property_ids.append(property.id)

		id2value = {}
		for property_value in ProductModelPropertyValue.objects.filter(property_id__in=property_ids):
			id2value[property_value.id] = {"id":property_value.id, "property_id":property_value.property_id, "name":property_value.name, "pic_url":property_value.pic_url}

		return {
			'value': {
				'id2property': id2property,
				'id2value': id2value
			}
		}

	return inner_func


#################################################################################
# get_mall_config_for_cache: 获取用于缓存的mall config数据
#################################################################################
def get_mall_config_for_cache(webapp_owner_id):
	def inner_func():
		#update by bert at 20151014  for new account can't vs webapp
		try:
			mall_config = MallConfig.objects.get(owner_id=webapp_owner_id)
		except:
			mall_config = MallConfig.objects.create(owner_id=webapp_owner_id)
		return {
			'value': mall_config.to_dict()
		}

	return inner_func


def fill_realtime_stocks(products):
	models = []
	for product in products:
		if product.is_use_custom_model:
			for model in product.models[1:]:
				model['product_id'] = product.id
				models.append(model)
		else:
			model = product.models[0]
			model['product_id'] = product.id
			models.append(model)

	model_ids = [model['id'] for model in models]
	db_product_models = ProductModel.objects.filter(id__in=model_ids)
	id2productmodels = dict([('%s_%s' % (model.product_id, model.id), model) for model in db_product_models])
	for product in products:
		if product.is_use_custom_model:
			for model in product.models[1:]:
				realtime_model = id2productmodels['%s_%s' % (product.id, model['id'])]
				model['stock_type'] = realtime_model['stock_type']
				model['stocks'] = realtime_model['stocks']
				model['is_deleted'] = realtime_model['is_deleted']
		else:
			model = product.models[0]
			realtime_model = id2productmodels['%s_%s' % (product.id, model['id'])]
			model['stock_type'] = realtime_model['stock_type']
			model['stocks'] = realtime_model['stocks']
			model['is_deleted'] = realtime_model['is_deleted']


def get_product_details_with_model(webapp_owner_id, webapp_user, product_infos):
	"""
	获得指定规格的商品详情
	"""
	from cache import webapp_cache

	products = []
	invalid_products = []
	id2info = dict([('%s_%s' % (info['id'], info['model_name']), info) for info in product_infos])
	for product_info in product_infos:
		product = webapp_cache.get_webapp_product_detail(webapp_owner_id, product_info['id'])
		product = copy.copy(product)
		product.flash_data = {
			"product_model_id": '%s_%s' % (product_info['id'], product_info['model_name'])
		}
		products.append(product)

	#__fill_realtime_stocks(products)
	for product in products:
		product_info = id2info[product.flash_data['product_model_id']]
		product.fill_specific_model(product_info['model_name'], product.models)
		# 微众商城代码
		# if webapp_owner_id != product.owner_id and product.weshop_sync == 2:
		# 	product.price = round(product.price * 1.1, 2)

	#if product.stock_type == PRODUCT_STOCK_TYPE_LIMIT and product.stocks <= 0:
	#		product.is_sellout = True
	return products


# #############################################################################
# # get_product_detail: 获取product详情
# #############################################################################
# def get_product_detail(webapp_owner_id, webapp_user, product_id):
# 	try:
# 		from cache import webapp_cache
# 		product = webapp_cache.get_webapp_product_detail(webapp_owner_id, product_id)
# 		if product.is_deleted:
# 			return product

# 		postage_configs = webapp_user.webapp_owner_info.mall_data['postage_configs']#webapp_cache.get_webapp_postage_configs(webapp_owner_id)
# 		if product.type == PRODUCT_INTEGRAL_TYPE:
# 			postage_config = filter(lambda c: c.is_system_level_config, postage_configs)[0]
# 		else:
# 			postage_config = filter(lambda c: c.is_used, postage_configs)[0]

# 		#记录运费计算因子
# 		product.postage_factor = postage_config.factor

# 		#获取每个model的运费
# 		product.postage_config = mall_util.get_postage_for_all_models(webapp_owner_id, product, postage_config)

# 		for product_model in product.models:
# 			#获取折扣后的价格
# 			product_model['price'], _ = webapp_user.get_discounted_money(product_model['price'], product_type=product.type)

# 		# 商品规格
# 		p_type = product.type

# 		#获取product的price info
# 		if product.is_use_custom_model:
# 			custom_models = product.models[1:]
# 			if len(custom_models) == 1:
# 				#只有一个custom model，显示custom model的价格信息
# 				product_model = custom_models[0]
# 				product.price_info = {
# 					'display_price': str("%.2f" % product_model['price']),
# 					'display_original_price': str("%.2f" % product_model['original_price']),
# 					'display_market_price': str("%.2f" % product_model['market_price']),
# 					'min_price': product_model['price'],
# 					'max_price': product_model['price']
# 				}
# 			else:
# 				#有多个custom model，显示custom model集合组合后的价格信息
# 				prices = []
# 				market_prices = []
# 				for product_model in custom_models:
# 					if product_model['price'] > 0:
# 						prices.append(product_model['price'])
# 					if product_model['market_price'] > 0:
# 						market_prices.append(product_model['market_price'])

# 				if len(market_prices) == 0:
# 					market_prices.append(0.0)

# 				if len(prices) == 0:
# 					prices.append(0.0)

# 				prices.sort()
# 				market_prices.sort()
# 				# 如果最大价格和最小价格相同，价格处显示一个价格。
# 				if prices[0] == prices[-1]:
# 					price_range =  str("%.2f" % prices[0])
# 				else:
# 					price_range = '%s-%s' % (str("%.2f" % prices[0]), str("%.2f" % prices[-1]))

# 				if market_prices[0] == market_prices[-1]:
# 					market_price_range = str("%.2f" % market_prices[0])
# 				else:
# 					market_price_range = '%s-%s' % (str("%.2f" % market_prices[0]), str("%.2f" % market_prices[-1]))

# 				# 最低价
# 				min_price = prices[0]
# 				# 最高价
# 				max_price = prices[-1]

# 				product.price_info = {
# 					'display_price': price_range,
# 					'display_original_price': price_range,
# 					'display_market_price': market_price_range,
# 					'min_price': min_price,
# 					'max_price': max_price
# 				}
# 		else:
# 			standard_model = product.models[0]
# 			product.price_info = {
# 				'display_price': str("%.2f" % standard_model['price']),
# 				'display_original_price': str("%.2f" % standard_model['original_price']),
# 				'display_market_price': str("%.2f" % standard_model['market_price']),
# 				'min_price': standard_model['price'],
# 				'max_price': standard_model['price']
# 			}

# 		#获取product的库存信息
# 		if product.is_use_custom_model:
# 			custom_models = product.models[1:]
# 			custom_model_ids = [custom_model['id'] for custom_model in custom_models]
# 			id2model = dict([(custom_model['id'], custom_model) for custom_model in custom_models])
# 			db_product_models = ProductModel.objects.filter(id__in=custom_model_ids)
# 			for db_product_model in db_product_models:
# 				id2model[db_product_model.id]['stocks'] = db_product_model.stocks
# 		else:
# 			standard_model = product.models[0]
# 			db_product_model = ProductModel.objects.get(id=standard_model['id'])
# 			product.stock_type = db_product_model.stock_type
# 			product.stocks = db_product_model.stocks
# 			if product.stock_type == PRODUCT_STOCK_TYPE_LIMIT and product.stocks <= 0:
# 				product.is_sellout = True

# 	except:
# 		if settings.DEBUG:
# 			raise
# 		else:
# 			#记录日志
# 			alert_message = u"获取商品记录失败,商品id: {} cause:\n{}".format(product_id, unicode_full_stack())
# 			watchdog_alert(alert_message, type='WEB')
# 			#返回"被删除"商品
# 			product = Product()
# 			product.is_deleted = True

# 	return product

def get_products_detail(webapp_owner_id, product_ids, webapp_user=None, member_grade_id=None):
	from cache import webapp_cache
	try:
		products = webapp_cache.get_webapp_products_detail(webapp_owner_id, product_ids, member_grade_id)

		for product in products:
			if product.is_deleted:
				continue

			for product_model in product.models:
				#获取折扣后的价格
				# if webapp_user:
					# product_model['price'], _ = webapp_user.get_discounted_money(product_model['price'], product_type=product.type)
				# 微众商城代码
				# if webapp_owner_id != product.owner_id and product.weshop_sync == 2:
				# 	product_model['price'] = round(product_model['price'] * 1.1, 2)

				# 商品规格
				p_type = product.type

				#获取product的price info
				if product.is_use_custom_model:
					custom_models = product.models[1:]
					if len(custom_models) == 1:
						#只有一个custom model，显示custom model的价格信息
						product_model = custom_models[0]
						product.price_info = {
							'display_price': str("%.2f" % product_model['price']),
							'display_original_price': str("%.2f" % product_model['original_price']),
							'display_market_price': str("%.2f" % product_model['market_price']),
							'min_price': product_model['price'],
							'max_price': product_model['price']
						}
					else:
						#有多个custom model，显示custom model集合组合后的价格信息
						prices = []
						market_prices = []
						for product_model in custom_models:
							if product_model['price'] > 0:
								prices.append(product_model['price'])
							if product_model['market_price'] > 0:
								market_prices.append(product_model['market_price'])

						if len(market_prices) == 0:
							market_prices.append(0.0)

						if len(prices) == 0:
							prices.append(0.0)

						prices.sort()
						market_prices.sort()
						# 如果最大价格和最小价格相同，价格处显示一个价格。
						if prices[0] == prices[-1]:
							price_range =  str("%.2f" % prices[0])
						else:
							price_range = '%s-%s' % (str("%.2f" % prices[0]), str("%.2f" % prices[-1]))

						if market_prices[0] == market_prices[-1]:
							market_price_range = str("%.2f" % market_prices[0])
						else:
							market_price_range = '%s-%s' % (str("%.2f" % market_prices[0]), str("%.2f" % market_prices[-1]))

						# 最低价
						min_price = prices[0]
						# 最高价
						max_price = prices[-1]

						product.price_info = {
							'display_price': price_range,
							'display_original_price': price_range,
							'display_market_price': market_price_range,
							'min_price': min_price,
							'max_price': max_price
						}
				else:
					standard_model = product.models[0]
					product.price_info = {
						'display_price': str("%.2f" % standard_model['price']),
						'display_original_price': str("%.2f" % standard_model['original_price']),
						'display_market_price': str("%.2f" % standard_model['market_price']),
						'min_price': standard_model['price'],
						'max_price': standard_model['price']
					}
	except:
		pass

	return products


def get_product_detail_refactor(webapp_owner_id, product_id, member_grade_id=None):
	"""获取商品的详细信息
	"""
	from cache import webapp_cache
	try:
		product = webapp_cache.get_webapp_product_detail(webapp_owner_id, product_id, member_grade_id)
		if product.is_deleted:
			return product
		mall_models.Product.fill_display_price([product])
		product.price_info = {
			"display_price": product.display_price
		}
		return product
	except:
		if settings.DEBUG:
			raise
		else:
			#记录日志
			alert_message = u"获取商品记录失败,商品id: {} cause:\n{}".format(product_id, unicode_full_stack())
			watchdog_alert(alert_message, type='WEB')
			#返回"被删除"商品
			product = Product()
			product.is_deleted = True


def get_product_detail(webapp_owner_id, product_id, webapp_user=None, member_grade_id=None):
	"""
	获取商品的详细信息
	"""

	from cache import webapp_cache
	try:
		product = webapp_cache.get_webapp_product_detail(webapp_owner_id, product_id, member_grade_id)
		if product.is_deleted:
			return product
		# 微众商城代码
		# for product_model in product.models:
		# 	#获取折扣后的价格
		# 	if webapp_owner_id != product.owner_id and product.weshop_sync == 2:
		# 		product_model['price'] = round(product_model['price'] * 1.1, 2)

		# 商品规格

		#获取product的price info
		if product.is_use_custom_model:
			custom_models = product.models[1:]
			if len(custom_models) == 1:
				#只有一个custom model，显示custom model的价格信息
				product_model = custom_models[0]
				product.price_info = {
					'display_price': str("%.2f" % product_model['price']),
					'display_original_price': str("%.2f" % product_model['original_price']),
					'display_market_price': str("%.2f" % product_model['market_price']),
					'min_price': product_model['price'],
					'max_price': product_model['price'],
				}
			else:
				#有多个custom model，显示custom model集合组合后的价格信息
				prices = []
				market_prices = []
				for product_model in custom_models:
					if product_model['price'] > 0:
						prices.append(product_model['price'])
					if product_model['market_price'] > 0:
						market_prices.append(product_model['market_price'])

				if len(market_prices) == 0:
					market_prices.append(0.0)

				if len(prices) == 0:
					prices.append(0.0)

				prices.sort()
				market_prices.sort()
				# 如果最大价格和最小价格相同，价格处显示一个价格。
				if prices[0] == prices[-1]:
					price_range =  str("%.2f" % prices[0])
				else:
					price_range = '%s-%s' % (str("%.2f" % prices[0]), str("%.2f" % prices[-1]))

				if market_prices[0] == market_prices[-1]:
					market_price_range = str("%.2f" % market_prices[0])
				else:
					market_price_range = '%s-%s' % (str("%.2f" % market_prices[0]), str("%.2f" % market_prices[-1]))

				# 最低价
				min_price = prices[0]
				# 最高价
				max_price = prices[-1]

				product.price_info = {
					'display_price': price_range,
					'display_original_price': price_range,
					'display_market_price': market_price_range,
					'min_price': min_price,
					'max_price': max_price,
				}
		else:
			standard_model = product.models[0]
			product.price_info = {
				'display_price': str("%.2f" % standard_model['price']),
				'display_original_price': str("%.2f" % standard_model['original_price']),
				'display_market_price': str("%.2f" % standard_model['market_price']),
				'min_price': standard_model['price'],
				'max_price': standard_model['price'],
			}

	except:
		if settings.DEBUG:
			raise
		else:
			#记录日志
			alert_message = u"获取商品记录失败,商品id: {} cause:\n{}".format(product_id, unicode_full_stack())
			watchdog_alert(alert_message, type='WEB')
			#返回"被删除"商品
			product = Product()
			product.is_deleted = True
	return product


def create_order(webapp_owner_id, webapp_user, product):
	"""
	创建一个order

	下订单页面调用
	"""
	from cache import webapp_cache
	order = Order()
	# if webapp_user.ship_info:
	# 	ship_info = webapp_user.ship_info
	# 	order.ship_name = ship_info.ship_name
	# 	order.area = ship_info.area
	# 	order.ship_address = ship_info.ship_address
	# 	order.ship_tel = ship_info.ship_tel
	# 	order.ship_id = ship_info.id

	# 积分订单
	if product.type == PRODUCT_INTEGRAL_TYPE:
		order.type = PRODUCT_INTEGRAL_TYPE

	#计算折扣
	product.original_price = product.price
	# if product.type==PRODUCT_DEFAULT_TYPE:
	# 	product.price, _ = webapp_user.get_discounted_money(product.price, product_type=product.type)
	order.products = [product]

	order.postage = 0.0 #订单运费由前台计算

	# order.used = {
	# 	'postage_config': postage_config
	# }

	#支付方式
	order.pay_interfaces = __get_products_pay_interfaces(webapp_user, order.products)
	return order


#############################################################################
# update_order_type_test: 修改订单的为测试订单，并且修改价钱
#############################################################################
# def update_order_type_test(type, order):
# 	if type == PRODUCT_TEST_TYPE:
# 		order.type = PRODUCT_TEST_TYPE
# 		order.final_price = 0.01

# 	return order


########################################################################
# __create_random_order_id: 生成订单
########################################################################
def __create_random_order_id():
	order_id = time.strftime("%Y%m%d%H%M%S", time.localtime())
	order_id = '%s%03d' % (order_id, random.randint(1, 999))
	if Order.objects.filter(order_id=order_id).count() > 0:
		return __create_random_order_id()
	else:
		return order_id


def save_order(webapp_id, webapp_owner_id, webapp_user, order_info, request=None):
	"""保存订单
	"""
	grade_id, discount = get_member_discount(request)
	order = Order()
	order.session_data = dict()
	order.session_data['webapp_owner_id'] = webapp_owner_id

	order.ship_name = order_info['ship_name']
	order.ship_address = order_info['ship_address']
	order.ship_tel = order_info['ship_tel']
	order.area = order_info['area']
	order.bill_type = order_info['bill_type']
	order.bill = order_info['bill']
	order.customer_message = order_info['customer_message']
	order.type = order_info['type']
	order.pay_interface_type = order_info['pay_interface']

	order.status = ORDER_STATUS_NOT
	order.webapp_id = webapp_id
	order.webapp_user_id = webapp_user.id
	order.member_grade_id = grade_id
	order.member_grade_discount = discount

	products = order_info['products']
	fake_order = order_info['fake_order']
	product_groups = order_info['product_groups']


	#处理订单中的product总价
	order.product_price = sum([product.price * product.purchase_count for product in products])
	order.final_price = order.product_price
	# order.member_grade_discounted_money = order.product_price - order.final_price
	mall_signals.pre_save_order.send(sender=mall_signals, pre_order=fake_order, order=order, products=products, product_groups=product_groups, owner_id=request.webapp_owner_id)
	order.final_price = round(order.final_price, 2)
	if order.final_price < 0:
		order.final_price = 0

	#处理订单中的促销优惠金额
	promotion_saved_money = 0.0
	for product_group in product_groups:
		promotion_result = product_group['promotion_result']
		if promotion_result:
			saved_money = promotion_result.get('promotion_saved_money', 0.0)
			promotion_saved_money += saved_money
	order.promotion_saved_money = promotion_saved_money

	# 微众商城代码
	# # 订单来自商铺
	# if products[0].owner_id == webapp_owner_id:
	# 	order.webapp_source_id = webapp_id
	order.order_source = ORDER_SOURCE_OWN
	# # 订单来自微众商城
	# else:
	# 	order.webapp_source_id = WebApp.objects.get(owner_id=products[0].owner_id).appid
	# 	order.order_source = ORDER_SOURCE_WEISHOP
	save_retry_count = 0
	while save_retry_count <= 10:
		try:
			order.order_id = __create_random_order_id()
			order.save()
		except IntegrityError:
			save_retry_count += 1
			watchdog_info(u"order.id:%s,order_id:%s,重试次数：%s" % (order.id, order.order_id, save_retry_count),
						type="mall", user_id=int(request.webapp_owner_id))
		else:
			break

	#更新库存
	for product in products:
		product_model = product.model
		if product_model['stock_type'] == PRODUCT_STOCK_TYPE_LIMIT:
			ProductModel.objects.filter(id=product_model['id']).update(stocks = F('stocks') - product.purchase_count)

	#建立<order, product>的关系
	supplierIds = []
	for product in products:
		supplier = product.supplier
		if not supplier in supplierIds:
			supplierIds.append(supplier)

		OrderHasProduct.objects.create(
			order=order,
			product_id=product.id,
			product_model_name=product.model['name'],
			number=product.purchase_count,
			total_price=product.total_price,
			price=product.price,
			promotion_id=product.promotion['id'] if product.promotion else 0,
			promotion_money=product.promotion_money if hasattr(product, 'promotion_money') else 0,
			# 目前product.member_discount_money 只有限时抢购会设置成0，不用乘商品数量
			grade_discounted_money=product.member_discount_money if hasattr(product, 'member_discount_money')\
				else product.total_price - product.price * product.purchase_count,
		)

	if len(supplierIds) > 1:
		# 进行拆单，生成子订单
		order.origin_order_id = -1 # 标记有子订单
		for supplier in supplierIds:
			fack_order = copy.copy(order)
			fack_order.id = None
			fack_order.order_id = '%s^%s' % (order.order_id, supplier)
			fack_order.origin_order_id = order.id
			fack_order.supplier = supplier
			fack_order.save()
	elif supplierIds[0] != 0:
		order.supplier = supplierIds[0]
	order.save()

	# 注意强制提交时这里可能会修改赠品数量，所以要在建立促销结果之前运行
	mall_signals.post_save_order.send(sender=mall_signals, order=order, webapp_user=webapp_user, product_groups=product_groups)

	#建立<order, promotion>的关系
	for product_group in product_groups:
		promotion_result = product_group.get('promotion_result', None)
		if promotion_result or product_group.get('integral_sale_rule', None):
			try:
				promotion_id = product_group['promotion']['id']
				promotion_type = product_group['promotion_type']
			except:
				promotion_id = 0
				promotion_type = 'integral_sale'
			try:
				if not promotion_result:
					promotion_result = dict()
				promotion_result['integral_product_info'] = product_group['integral_sale_rule']['integral_product_info']
			except:
				pass
			integral_money = 0
			integral_count = 0
			if product_group['integral_sale_rule'] and product_group['integral_sale_rule'].get('result'):
				integral_money = product_group['integral_sale_rule']['result']['final_saved_money']
				integral_count = product_group['integral_sale_rule']['result']['use_integral']
			OrderHasPromotion.objects.create(
				order=order,
				webapp_user_id=webapp_user.id,
				promotion_id=promotion_id,
				promotion_type=promotion_type,
				promotion_result_json=json.dumps(promotion_result),
				integral_money=integral_money,
				integral_count=integral_count,
			)

	if order.final_price == 0:
		# 优惠券或积分金额直接可支付完成，直接调用pay_order，完成支付
		pay_order(webapp_id, webapp_user, order.order_id, True, PAY_INTERFACE_PREFERENCE)
		# 支付后的操作
		mall_signals.post_pay_order.send(sender=Order, order=order, request=request)

	return order


########################################################################
# get_order: 获取订单
########################################################################
def get_order(webapp_user, order_id, should_fetch_product=False, is_sub_order=False, is_need_area=True):
	order = Order.objects.get(order_id=order_id)
	try:
		if is_need_area:
			order.area = regional_util.get_str_value_by_string_ids(order.area)
		order.display_express_company_name = express_util.get_name_by_value(order.express_company_name)
	except:
		pass

	if should_fetch_product:
		id = order.id
		if order.origin_order_id > 0:
			id = order.origin_order_id
		relations = list(OrderHasProduct.objects.filter(order_id=id).order_by('id'))
		order_promotion_relations = list(OrderHasPromotion.objects.filter(order_id=id))
		id2promotion = dict([(relation.promotion_id, relation) for relation in order_promotion_relations])

		product_infos = []
		webapp_owner_id = webapp_user.webapp_owner_info.user_profile.user_id
		for relation in relations:
			if is_sub_order: #只获取该子订单下面的数据
				if not relation.product.supplier == order.supplier:
					continue
			product_infos.append({
				"id": relation.product_id,
				'model_name': relation.product_model_name
			})
		products = get_product_details_with_model(webapp_owner_id, webapp_user, product_infos)
		id2product = dict([('%s_%s' % (product.id, product.model['name']), product) for product in products])

		products = []
		temp_premium_products = []
		pricecut_id = None
		processed_promotion_set = set()
		for relation in relations:
			if is_sub_order: #只获取该子订单下面的数据
				if not relation.product.supplier == order.supplier:
					continue
			_product_model_id = '%s_%s' % (relation.product_id, relation.product_model_name)
			product = copy.copy(id2product[_product_model_id])
			#product.fill_specific_model(relation.product_model_name)
			product_info = {
				'id' : relation.product_id,
				'name': product.name,
				'thumbnails_url': product.thumbnails_url,
				'count': relation.number,
				'total_price': '%.2f' % relation.total_price,
				'price': '%.2f' % relation.price,
				'custom_model_properties': product.custom_model_properties,
				'physical_unit': product.physical_unit,
				'is_deleted': product.is_deleted,
				'grade_discounted_money': relation.grade_discounted_money
			}

			promotion_relation = id2promotion.get(relation.promotion_id, None)
			if promotion_relation:
				promotion_result = promotion_relation.promotion_result
				product_info['promotion'] = promotion_result
			else:
				product_info['promotion'] = None

			should_clear_temp_premium_products = False
			if not promotion_relation and len(temp_premium_products) > 0:
				should_clear_temp_premium_products = True
			if promotion_relation and len(temp_premium_products) > 0 and (not promotion_relation.promotion_id in processed_promotion_set):
				should_clear_temp_premium_products = True

			if should_clear_temp_premium_products:
				products.extend(temp_premium_products)
				temp_premium_products = []
			products.append(product_info)

			if promotion_relation and promotion_relation.promotion_type == 'premium_sale':
				if promotion_relation.promotion_id in processed_promotion_set:
					continue

				for premium_product in promotion_relation.promotion_result.get('premium_products', []):
					temp_premium_products.append({
						"id": premium_product['id'],
						"name": premium_product['name'],
						"thumbnails_url": premium_product['thumbnails_url'],
						"count": premium_product['count'],
						"price": 0,
						"promotion": {
							"type": "premium_sale:premium_product"
						}
					})
				processed_promotion_set.add(promotion_relation.promotion_id)
		if len(temp_premium_products) > 0:
			products.extend(temp_premium_products)

		order.products = products
	return order


def get_orders(request):
	"""用户中心 获取webapp_user的订单列表
	"""

	orders = Order.by_webapp_user_id(request.webapp_user.id).order_by('-id')

	orderIds = [order.id for order in orders]
	order2count = {}
	orderId2order = dict([(order.id,order) for order in orders])

	orderHasProducts = OrderHasProduct.objects.filter(order_id__in=orderIds)

	totalProductIds = [orderHasProduct.product_id for orderHasProduct in orderHasProducts]
	orderId2productIds = dict()

	from cache import webapp_cache
	cache_products = webapp_cache.get_webapp_products_detail(request.webapp_owner_id, totalProductIds)
	cache_productId2cache_products = dict([(product.id, product) for product in cache_products])

	for orderHasProduct in orderHasProducts:
		if not orderId2productIds.get(orderHasProduct.order_id):
			orderId2productIds[orderHasProduct.order_id] = []
		orderId2productIds.get(orderHasProduct.order_id).append(orderHasProduct.product_id)
		if not hasattr(orderId2order[orderHasProduct.order_id], 'products'):
			orderId2order[orderHasProduct.order_id].products = []
		product = copy.copy(cache_productId2cache_products[orderHasProduct.product_id])
		product.properties = product.fill_specific_model(orderHasProduct.product_model_name, cache_productId2cache_products[product.id].models)
		orderId2order[orderHasProduct.order_id].products.append(product)

		order_id = orderHasProduct.order_id
		old_count = 0
		if order_id in order2count:
			old_count = order2count[order_id]
		order2count[order_id] = old_count + orderHasProduct.number

	red_envelope = request.webapp_owner_info.red_envelope
	red_envelope_orderIds = []

	order_product_has_review = dict([(str(review.order_id) + "_" + str(review.product_id), True) for review in mall_models.ProductReview.objects.filter(member_id=request.member.id)])

	for order in orders:
		order.product_count = order2count.get(order.id, 0)

		is_finished = True
		for productId in orderId2productIds.get(order.id, []):
			key = "%s_%s" % (order.id, productId)
			is_finished = is_finished & order_product_has_review.get(key, False)
		order.review_is_finished = is_finished

		if order.status == ORDER_STATUS_PAYED_SHIPED and (datetime.today() - order.update_at).days >= 3:
			#订单发货后3天显示确认收货按钮
			if not hasattr(order, 'session_data'):
				order.session_data = dict()
			order.session_data['has_comfire_button'] = '1'
		if promotion_models.RedEnvelopeRule.can_show_red_envelope(order, red_envelope):
			# 订单满足红包条件
			order.red_envelope = True
			red_envelope_orderIds.append(order.id)
		else:
			order.red_envelope = False

	exist_red_envelope_orderIds = [relation.order_id for relation in
		promotion_models.RedEnvelopeToOrder.objects.filter(order_id__in=red_envelope_orderIds)]
	for order in orders:
		if order.red_envelope and order.id in exist_red_envelope_orderIds:
			# 订单已经访问过领取红包页面，不显示红包标识
			order.red_envelope = False

	return orders


########################################################################
# pay_order: 支付订单
########################################################################
def pay_order(webapp_id, webapp_user, order_id, is_success, pay_interface_type):
	try:
		order = get_order(webapp_user, order_id, is_need_area=False)
	except:
		watchdog_fatal(u"本地获取订单信息失败：order_id:{}, cause:\n{}".format(order_id, unicode_full_stack()))
		return None, False

	pay_result = False

	if is_success and order.status == ORDER_STATUS_NOT: #支付成功
		pay_result = True
		if order.origin_order_id < 0:
			Order.objects.filter(origin_order_id=order.id).update(status=ORDER_STATUS_PAYED_NOT_SHIP, pay_interface_type=pay_interface_type, payment_time=datetime.now())

		if Order.objects.filter(webapp_id=order.webapp_id, webapp_user_id=order.webapp_user_id, is_first_order=True).count() == 0:
			order.is_first_order = True

		order.status = ORDER_STATUS_PAYED_NOT_SHIP
		order.pay_interface_type = pay_interface_type
		order.payment_time = datetime.now()
		order.save()

		#记录日志
		record_operation_log(order_id, u'客户', u'支付')
		record_status_log(order_id, u'客户', ORDER_STATUS_NOT, ORDER_STATUS_PAYED_NOT_SHIP)

		#更新webapp_user的has_purchased字段
		webapp_user.set_purchased()
		from webapp.handlers import event_handler_util
		from utils import json_util
		event_data = {'order':json.dumps(order.to_dict(),cls=json_util.DateEncoder)}
		event_handler_util.handle(event_data, 'send_order_email')
		# try:
		# 	mall_util.email_order(order=order)
		# except:
		# 	notify_message = u"订单状态为已付款时发邮件失败，order_id={}, webapp_id={}, cause:\n{}".format(order_id, webapp_id, unicode_full_stack())
		# 	watchdog_alert(notify_message)
		# 重新查询订单
	return order, pay_result


########################################################################
# 进行订单的发货处理：
# 	order_id: 需要处理的订单号
#	express_company_name：快递公司名称
# 	express_number: 货运单号
#   leader_name: 负责人
#   is_update_express: 为True时，只修改物流信息，不改变订单状态
#
# 处理操作流程：
# 1. 修改订单的状态为“已发货”
# 2. 修改订单记录，添加运单号和快递公司信息
# 3. 增加订单操作记录信息
# 4. 增加状态更改记录信息
#
# 如果对应订单不存在，或者操作失败直接返回False
# 整个操作过程中如果其中有一个步骤失败则继续之后的操作
# 但是会进行预警处理，以便人工进行相应操作
#
# 如果订单id、快递公司名称或运单号任一为None，直接返回False
########################################################################
def ship_order(order_id, express_company_name,
	express_number, operator_name=u'我', leader_name=u'', is_update_express=False, is_100 = True):
	"""
	进行订单的发货处理：
		order_id: 需要处理的订单号
		express_company_name：快递公司名称
		express_number: 货运单号
		leader_name: 负责人
		is_update_express: 为True时，只修改物流信息，不改变订单状态

	处理操作流程：
	1. 修改订单的状态为“已发货”
	2. 修改订单记录，添加运单号和快递公司信息
	3. 增加订单操作记录信息
	4. 增加状态更改记录信息

	如果对应订单不存在，或者操作失败直接返回False
	整个操作过程中如果其中有一个步骤失败则继续之后的操作
	但是会进行预警处理，以便人工进行相应操作

	如果订单id、快递公司名称或运单号任一为None，直接返回False

	如果订单id、快递公司名称或运单号任一长度为0返回False

	已知引用：
	mobile_app/order_api_views.py
	"""
	# if (len(str(order_id)) == 0) or (len(express_company_name) == 0) or (len(express_number) == 0):
	# 	return False
	if (len(str(order_id)) == 0):
		return False
	target_status = ORDER_STATUS_PAYED_SHIPED

	try:
		# 需要修改的基本参数
		# 只修改物流信息，不修改状态
		order_params = dict()
		order_params['express_company_name'] = express_company_name
		order_params['express_number'] = express_number
		order_params['leader_name'] = leader_name
		order_params['status'] = target_status
		order_params['is_100'] = is_100
		order = Order.objects.get(id=order_id)
		Order.objects.filter(id=order_id).update(**order_params)
		try:
			if express_company_name and express_number:
				order.express_company_name = express_company_name
				order.express_number = express_number
				order.leader_name = leader_name

				template_message_api.send_order_template_message(order.webapp_id, order.id, template_message_model.PAY_DELIVER_NOTIFY)
		except:
			alert_message = u"ship_order 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
			watchdog_warning(alert_message)
		#order.final_price = current_final_price
	except:
		error_msg = u"更改订单({})状态信息失败，cause:\n{}".format(order_id, unicode_full_stack())
		watchdog_error(error_msg)

		return False

	# 记录log信息
	if is_update_express:
		action = u'修改发货信息'
	else:
		action = u'订单发货'
		record_status_log(order.order_id, operator_name, order.status, target_status)

		if order.origin_order_id > 0:
			# 修改子订单状态，上面只修改物流信息
			user = UserProfile.objects.get(webapp_id=order.webapp_id).user
			set_origin_order_status(order, user, 'ship')

	record_operation_log(order.order_id, operator_name, action, order)

	#send post_ship_send_request_to_kuaidi signal
	# 是快递100的才进行发送
	if is_100:
		mall_signals.post_ship_send_request_to_kuaidi.send(sender=Order, order=order)
	from webapp.handlers import event_handler_util
	from utils import json_util
	event_data = {'order':json.dumps(Order.objects.get(id=order_id).to_dict(),cls=json_util.DateEncoder)}
	event_handler_util.handle(event_data, 'send_order_email')
	# try:
	# 	mall_util.email_order(order=Order.objects.get(id=order_id))
	# except:
	# 	notify_message = u"订单状态为已发货时发邮件失败，order_id:{}，cause:\n{}".format(order_id, unicode_full_stack())
	# 	watchdog_alert(notify_message)
	return True


def __get_supplier_name(supplier_id):
	try:
		return Supplier.objects.get(id=supplier_id).name
	except:
		error_msg = u"获取供应商({})名称失败, cause:\n{}".format(supplier_id, unicode_full_stack())
		watchdog_error(error_msg)

def __get_store_name(supplier_user_id):
	try:
		return UserProfile.objects.get(user_id=supplier_user_id).store_name
	except:
		error_msg = u"获取供应商({})名称失败, cause:\n{}".format(supplier_user_id, unicode_full_stack())
		watchdog_error(error_msg)


########################################################################
# add_product_to_shopping_cart: 向购物车中添加商品
######################################################################## c
def add_product_to_shopping_cart(webapp_user, product_id, product_model_name, count):
	try:
		shopping_cart_item = ShoppingCart.objects.get(
			webapp_user_id = webapp_user.id,
			product_id = product_id,
			product_model_name = product_model_name
		)
		shopping_cart_item.count = shopping_cart_item.count + count
		shopping_cart_item.save()
	except:
		shopping_cart_item = ShoppingCart.objects.create(
			webapp_user_id = webapp_user.id,
			product_id = product_id,
			product_model_name = product_model_name,
			count = count
		)


########################################################################
# get_shopping_cart_product_ids: 获取购物车中商品id集合
########################################################################
def get_shopping_cart_product_ids(webapp_user):
	product_ids = [item.product_id for item in ShoppingCart.objects.filter(webapp_user_id=webapp_user.id)]
	return product_ids


########################################################################
# remove_product_from_shopping_cart: 从购物车中删除商品
########################################################################
def remove_product_from_shopping_cart(webapp_user, product_id, product_model_name='standard'):
	ShoppingCart.objects.filter(product_id=product_id, webapp_user_id=webapp_user.id, product_model_name=product_model_name).delete()


########################################################################
# remove_shopping_cart_items: 从购物车中删除商品
########################################################################
def remove_shopping_cart_items(webapp_user, shopping_cart_item_ids):
	ShoppingCart.objects.filter(id__in=shopping_cart_item_ids).delete()


########################################################################
# update_shopping_cart: 更新购物车
########################################################################
def update_shopping_cart(webapp_user, update_info):
	for item_id, count in update_info.items():
		ShoppingCart.objects.filter(id=item_id).update(count=count)


########################################################################
# clear_shopping_cart_invalid_products: 清空购物车中的无效商品
########################################################################
def clear_shopping_cart_invalid_products(webapp_user, shopping_cart_item_ids):
	ShoppingCart.objects.filter(id__in=shopping_cart_item_ids).delete()


########################################################################
# remove_product_from_all_shopping_cart: 从所有购物车中删除商品
########################################################################
def remove_product_from_all_shopping_cart(product_id):
	ShoppingCart.objects.filter(product_id=product_id).delete()


########################################################################
# get_shopping_cart_products: 获取购物车中的product集合
########################################################################
def get_shopping_cart_products(request):
	"""
	获取购物车中的product集合

	@todo 直接使用已在缓存中的model数据来改进fill_specific_model的性能
	"""
	webapp_user = request.webapp_user
	webapp_owner_id = request.webapp_owner_id
	shopping_cart_items = list(ShoppingCart.objects.filter(webapp_user_id=webapp_user.id))

	#product_ids = []
	product_infos = []
	productmodel2shoppingcartitem = dict()
	for shopping_cart_item in shopping_cart_items:
		#product_ids.append(shopping_cart_item.product_id)
		product_infos.append({"id": shopping_cart_item.product_id, "model_name": shopping_cart_item.product_model_name})
		product_model_id = '%s_%s' % (shopping_cart_item.product_id, shopping_cart_item.product_model_name)
		productmodel2shoppingcartitem[product_model_id] = shopping_cart_item

	products = get_product_details_with_model(webapp_owner_id, webapp_user, product_infos)

	#id2product = dict()
	#for product_id in product_ids:
	#	id2product[product_id] = webapp_cache.get_webapp_product_detail(webapp_owner_id, product_id)

	valid_products = []
	invalid_products = []
	for product in products:
		product_model_id = '%s_%s' % (product.id, product.model['name'])
		shopping_cart_item = productmodel2shoppingcartitem[product_model_id]

		product.count = shopping_cart_item.count
		product.purchase_count = shopping_cart_item.count
		product.shopping_cart_id = shopping_cart_item.id
		# product.original_price = product.price

		if product.shelve_type == PRODUCT_SHELVE_TYPE_OFF or \
			product.shelve_type == PRODUCT_SHELVE_TYPE_RECYCLED or\
			product.is_deleted or \
			(product.stock_type == PRODUCT_STOCK_TYPE_LIMIT and product.stocks == 0) or\
			product.is_model_deleted or\
			(shopping_cart_item.product_model_name == 'standard' and product.is_use_custom_model):
			invalid_products.append(product)
		else:
			valid_products.append(product)

	# for shopping_cart_item in shopping_cart_items:
	# 	product = copy.copy(id2product[shopping_cart_item.product_id])
	# 	product.fill_specific_model(shopping_cart_item.product_model_name)
	# 	product.count = shopping_cart_item.count
	# 	product.purchase_count = shopping_cart_item.count
	# 	product.shopping_cart_id = shopping_cart_item.id
	# 	product.original_price = product.price

	# 	if product.shelve_type == PRODUCT_SHELVE_TYPE_OFF or \
	# 		product.shelve_type == PRODUCT_SHELVE_TYPE_RECYCLED or\
	# 		product.is_deleted or \
	# 		(product.stock_type == PRODUCT_STOCK_TYPE_LIMIT and product.stocks == 0) or\
	# 		product.is_model_deleted or\
	# 		(shopping_cart_item.product_model_name == 'standard' and product.is_use_custom_model):
	# 		invalid_products.append(product)
	# 	else:
	# 		product.price, _ = webapp_user.get_discounted_money(product.price)
	# 		products.append(product)

	product_groups = group_product_by_promotion(request, valid_products)

	invalid_products.sort(lambda x, y: cmp(x.shopping_cart_id, y.shopping_cart_id))

	return product_groups, invalid_products


# def update_display_price(request, product_groups):
# 	"""根据用户会员等级促销类型， 更新商品价格
# 	"""
# 	user_member_grade_id = get_user_member_grade_id(request)
# 	user_member_grade_discount = get_user_member_discount(requset)
# 	for product_group in product_groups:
# 		pass



#############################################################################
# create_shopping_cart_order: 创建一个基于购物车的order
#############################################################################
def create_shopping_cart_order(webapp_owner_id, webapp_user, products):
	order = Order()

	#在购物车页面，可能更改了商品数量，这里更新购物车中商品的数量
	for product in products:
		ShoppingCart.objects.filter(webapp_user_id=webapp_user.id, product_id=product.id, product_model_name=product.model['name']).update(count=product.purchase_count)

	#计算订单商品总重量的运费
	total_weight = 0.0;
	for product in products:
		# product.original_price = product.price
		# product.price, _ = webapp_user.get_discounted_money(product.price)
		# 有运费商品
		if product.postage_id > 0:
			total_weight += float(product.purchase_count) * float(product.weight)
	'''
	# 运费临时使用，测试
	'''
	# postage_config, order.postage = None, 0
	# postage_config, order.postage = mall_util.get_postage_for_weight(webapp_owner_id, total_weight)
	order.products = products

	# 支付方式
	order.pay_interfaces = __get_products_pay_interfaces(webapp_user, order.products)

	return order


########################################################################
# get_order_operation_logs: 获得订单的操作日志
########################################################################
def get_order_operation_logs(order_id):
	# return OrderOperationLog.objects.filter(order_id=order_id)
	#为了把子订单的操作日志也筛选出来
	return OrderOperationLog.objects.filter(order_id__contains=order_id)


########################################################################
# record_operation_log: 记录订单的操作日志
########################################################################
def record_operation_log(order_id, operator_name, action, order=None):
	try:
		if order and order.origin_order_id > 0:
			if order.supplier > 0:  #add by duhao 如果是子订单，则加入供应商信息
				action = '%s - %s' % (action, __get_supplier_name(order.supplier))
			if order.supplier_user_id > 0:
				action = '%s - %s' % (action, __get_store_name(order.supplier_user_id))
		OrderOperationLog.objects.create(order_id=order_id, action=action, operator=operator_name)
	except:
		error_msg = u"增加订单({})发货操作记录失败, cause:\n{}".format(order_id, unicode_full_stack())
		watchdog_error(error_msg)

########################################################################
# get_order_status_logs: 获得订单的状态日志
########################################################################
def get_order_status_logs(order):
	logs = []
	if order.status == ORDER_STATUS_NOT:
		log = {}
		log['status'] = u'已下单'
		log['created_at'] = order.created_at
		log['is_current'] = 0
		logs.append(log)

		log = {}
		log['status'] = u'待支付'
		log['created_at']  = order.created_at
		log['is_current'] = 1
		logs.append(log)

		log = {}
		log['status'] = u'已发货'
		log['created_at']  = ''
		log['is_current'] = 2
		logs.append(log)

		log = {}
		log['status'] = u'交易完成'
		log['created_at']  = ''
		log['is_current'] = 2
		logs.append(log)
	elif order.status in [ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED]:
		log = {}
		log['status'] = u'已下单'
		log['created_at'] = order.created_at
		log['is_current'] = 0
		logs.append(log)

		is_current = []
		if order.status == ORDER_STATUS_PAYED_NOT_SHIP:
			is_current = [1,2,2]

		if order.status == ORDER_STATUS_PAYED_SHIPED:
			is_current = [0,1,2]

		if order.status == ORDER_STATUS_SUCCESSED:
			is_current = [0,0,1]

		log = {}
		log['status'] = u'待发货'
		log['created_at']  = order.payment_time
		log['is_current'] = is_current[0]
		logs.append(log)

		log = {}
		log['status'] = u'已发货'
		log['created_at'] = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_SHIPED)[0].created_at if OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_SHIPED).count()>0 else ''
		log['is_current'] = is_current[1]
		logs.append(log)

		log = {}
		log['status'] = u'交易完成'
		log['created_at'] = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_SUCCESSED)[0].created_at if OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_SUCCESSED).count()>0 else ''
		log['is_current'] = is_current[2]
		logs.append(log)

	elif order.status == ORDER_STATUS_REFUNDING:
		log = {}
		log['status'] = u'已下单'
		log['created_at'] = order.created_at
		log['is_current'] = 0
		logs.append(log)

		if OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_SUCCESSED).count() > 0:
			log = {}
			log['status'] = u'交易完成'
			log['created_at']  = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_SUCCESSED)[0].created_at
			log['is_current'] = 0
			logs.append(log)
		elif OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_SHIPED).count() > 0:
			log = {}
			log['status'] = u'已发货'
			log['created_at']  = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_SHIPED)[0].created_at
			log['is_current'] = 0
			logs.append(log)
		elif OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_NOT_SHIP).count() > 0:
			log = {}
			log['status'] = u'待发货'
			log['created_at'] = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_NOT_SHIP)[0].created_at
			log['is_current'] = 0
			logs.append(log)

		log = {}
		log['status'] = u'退款中'
		log['created_at']  = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_REFUNDING)[0].created_at if OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_REFUNDING).count()>0 else ''
		log['is_current'] = 1
		logs.append(log)

		log = {}
		log['status'] = u'退款成功'
		log['created_at']  = ''
		log['is_current'] = 2
		logs.append(log)

	elif order.status == ORDER_STATUS_REFUNDED:
		log = {}
		log['status'] = u'已下单'
		log['created_at'] = order.created_at
		log['is_current'] = 0
		logs.append(log)

		if OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_SUCCESSED).count() > 0:
			log = {}
			log['status'] = u'交易完成'
			log['created_at']  = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_SUCCESSED)[0].created_at
			log['is_current'] = 0
			logs.append(log)
		elif OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_SHIPED).count() > 0:
			log = {}
			log['status'] = u'已发货'
			log['created_at'] = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_SHIPED)[0].created_at
			log['is_current'] = 0
			logs.append(log)
		elif OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_NOT_SHIP).count() > 0:
			log = {}
			log['status'] = u'待发货'
			log['created_at'] = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_NOT_SHIP)[0].created_at
			log['is_current'] = 0
			logs.append(log)

		log = {}
		log['status'] = u'退款中'
		log['created_at']  = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_REFUNDING)[0].created_at if OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_REFUNDING).count()>0 else ''
		log['is_current'] = 0
		logs.append(log)

		log = {}
		log['status'] = u'退款成功'
		log['created_at']  = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_REFUNDED)[0].created_at if OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_REFUNDED).count()>0 else ''
		log['is_current'] = 1
		logs.append(log)
	elif order.status == ORDER_STATUS_CANCEL:
		log = {}
		log['status'] = u'已下单'
		log['created_at'] = order.created_at
		log['is_current'] = 0
		logs.append(log)

		if OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_SUCCESSED).count() > 0:
			# if OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_NOT_SHIP).count() > 0:
			# 	log = {}
			# 	log['status'] = u'待发货'
			# 	log['created_at'] = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_NOT_SHIP)[0].created_at
			# 	log['is_current'] = 0
			# 	logs.append(log)
			log = {}
			log['status'] = u'交易完成'
			log['created_at']  = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_SUCCESSED)[0].created_at
			log['is_current'] = 0
			logs.append(log)

		elif OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_NOT_SHIP).count() > 0:
			log = {}
			log['status'] = u'待发货'
			log['created_at'] = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_NOT_SHIP)[0].created_at
			log['is_current'] = 0
			logs.append(log)
			if OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_SHIPED).count() > 0:
				log = {}
				log['status'] = u'已发货'
				log['created_at'] = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_SHIPED)[0].created_at
				log['is_current'] = 0
				logs.append(log)

		log = {}
		log['status'] = u'交易取消'
		log['created_at']  = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_CANCEL)[0].created_at if OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_CANCEL).count()>0 else ''
		log['is_current'] = 1
		logs.append(log)

	return logs

########################################################################
# record_status_log: 记录订单的状态日志
# TODO delete
########################################################################
def record_status_log(order_id, operator_name, from_status, to_status):
	try:
		OrderStatusLog.objects.create(
			order_id = order_id,
			from_status = from_status,
			to_status = to_status,
			operator = operator_name
		)
	except:
		error_msg = u"增加订单({})状态更改记录失败, cause:\n{}".format(order_id, unicode_full_stack())
		watchdog_error(error_msg)


########################################################################
# get_unread_order_count: 获得未读订单数量
########################################################################
def get_unread_order_count(webapp_owner_id):
	counter = MallCounter.objects.filter(owner_id=webapp_owner_id)
	if len(counter) == 1:
		return counter[0].unread_order_count
	else:
		return 0


########################################################################
# get_order_usable_integral: 获得订单中用户可以使用的积分
########################################################################
def get_order_usable_integral(order, integral_info):
	user_integral = 0
	order_integral = 0
	total_money = sum([product.price*product.purchase_count for product in order.products])
	user_integral = integral_info['count']
	usable_integral_percentage_in_order = integral_info['usable_integral_percentage_in_order']
	count_per_yuan = integral_info['count_per_yuan']
	if usable_integral_percentage_in_order:
		pass
	else:
		usable_integral_percentage_in_order = 0
	if count_per_yuan:
		pass
	else:
		count_per_yuan = 0

	# 加上运费的价格 by liupeiyu
	if hasattr(order, 'postage'):
		total_money = total_money + order.postage

	order_integral = math.ceil(total_money*usable_integral_percentage_in_order*count_per_yuan/100.0)

	if user_integral > order_integral:
		return int(order_integral)
	else:
		return int(user_integral)

def get_order_products(order):
	"""
	user参数由duhao在20151023添加，为了使客户演示账号的订单商品不露馅

	获得订单中的商品集合

	返回dict对象
	{
		id:
		name:
		thumbnails_url:
		count:
		total_price:
		price:
		custom_model_properties:
		product_model_name:
		physical_unit:
		is_deleted:
		noline: 后台订单详情页使用,商品不需要上边框时值1
		rowspan: 后台订单详情页使用,商品信息需要跨行组合时,值为rowspan行数
		promotion: 促销详情 dict 对象
		grade_discounted_money: 会员折扣金额
	}

	已知引用：
	mobile_app/order_api_views.py
	"""
	order.session_data = dict()
	order_id = order.id
	relations = list(OrderHasProduct.objects.filter(order_id=order_id).order_by('id'))

	product_ids = [r.product_id for r in relations]
	#products = mall_api.get_product_details_with_model(request.webapp_owner_id, request.webapp_user, product_infos)
	id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])

	order_promotion_relations = list(OrderHasPromotion.objects.filter(order_id=order_id))
	id2promotion = dict([(promotion.promotion_id, promotion) for promotion in order_promotion_relations])
	product2integral = dict([(promotion.promotion_result.get('integral_product_info'), promotion) for promotion in order_promotion_relations])


	products = []
	pricecut_id = None
	# 当前促销id
	current_promotion_id = None
	# 当前促销第一个主商品
	promotion_first_product = None
	# 当前促销买赠商品
	temp_premium_products = []
	# processed_promotion_set = set()
	suppliers = []
	supplier_user_ids = []
	for relation in relations:
		product = copy.copy(id2product[relation.product_id])
		product.fill_specific_model(relation.product_model_name)
		product_info = {
			'id' : relation.product_id,
			'name': product.name,
			'thumbnails_url': product.thumbnails_url,
			'count': relation.number,
			'total_price': '%.2f' % relation.total_price,
			'price': '%.2f' % (relation.total_price / relation.number),
			'custom_model_properties': product.custom_model_properties,
			'product_model_name': relation.product_model_name,
			'physical_unit': product.physical_unit,
			'is_deleted': product.is_deleted,
			'grade_discounted_money': relation.grade_discounted_money,
			'supplier': product.supplier,
			'supplier_user_id': product.supplier_user_id,
			'user_code':product.user_code,
			'purchase_price': relation.purchase_price
		}

		# 更换商品名称为供货商的商品名称
		if UserProfile.objects.get(user_id=product.owner_id).webapp_type == 0 and WeizoomHasMallProductRelation.objects.filter(
							owner_id=product.owner_id,
							weizoom_product_id=relation.product_id
							).count() > 0:
			mall_product_id = WeizoomHasMallProductRelation.objects.get(
										owner=product.owner,
										weizoom_product_id=relation.product_id
									).mall_product_id
			product_info['name'] = Product.objects.get(id=mall_product_id).name

		try:
			integral_product_info = str(product.id) + '-' + product.model_name
			product_info['integral_money'] = product2integral[integral_product_info].integral_money
			product_info['integral_count'] = product2integral[integral_product_info].integral_count
		except:
			product_info['integral_money'] = 0
			product_info['integral_count'] = 0

		suppliers.append(product.supplier)
		supplier_user_ids.append(product.supplier_user_id)

		try:
			product_info['supplier_name'] = Supplier.objects.get(id=product.supplier).name
		except:
			product_info['supplier_name'] = ""
		try:
			product_info['supplier_store_name'] = UserProfile.objects.get(user_id=product.supplier_user_id).store_name
		except:
			product_info['supplier_store_name'] = ""

		promotion_relation = id2promotion.get(relation.promotion_id, None)
		if promotion_relation:
			# 有促销信息
			promotion_result = promotion_relation.promotion_result
			product_info['promotion'] = promotion_result


			# 处理订单详情页跨行的问题
			if current_promotion_id != relation.promotion_id:
				# 当前促销中第一个主商品
				# 设定当前促销变量
				current_promotion_id = relation.promotion_id
				promotion_first_product = product_info

				if len(temp_premium_products) > 0:
					# 上一个促销有赠品
					products.extend(temp_premium_products)
					temp_premium_products = []
				# 初始跨行值为1
				product_info['rowspan'] = 1
				if promotion_result['type'] == 'premium_sale':
					# 买赠商品主商品跨行数+赠品数
					if promotion_result.has_key('premium_products'):
						product_info['rowspan'] += len(promotion_result['premium_products'])

						# 当前促销第一个主商品处理赠品信息
						for premium_product in promotion_relation.promotion_result['premium_products']:
							temp_premium_products.append({
								"id": premium_product['id'],
								"name": premium_product['name'],
								"thumbnails_url": premium_product['thumbnails_url'],
								"count": premium_product['count'],
								"price": '%.2f' % premium_product['price'],
								"total_price": '0.0',
								'product_model_name': "standard",
								"promotion": {
									"type": "premium_sale:premium_product"
								},
								'noline': 1,
								'supplier': product.supplier,
								'supplier_user_id': product.supplier_user_id,
								'supplier_name': product_info.get('supplier_name', ''),
								'supplier_store_name': product_info.get('supplier_store_name', ''),
								'user_code':product.user_code
							})
							suppliers.append(product.supplier)
							supplier_user_ids.append(product.supplier_user_id)
			else:
				# 当前促销中其余商品 不显示上边框,给主商品跨行+1
				product_info['noline'] = 1
				promotion_first_product['rowspan'] += 1
		else:
			# 没有促销的商品
			if len(temp_premium_products) > 0:
				# 上一个促销有赠品
				products.extend(temp_premium_products)
				temp_premium_products = []
			product_info['promotion'] = None

		products.append(product_info)
	if len(temp_premium_products) > 0:
		# 最后一个促销有赠品
		products.extend(temp_premium_products)

	for product in products:
		product['supplier_length'] = suppliers.count(product['supplier'])
		product['supplier_user_length'] = supplier_user_ids.count(product['supplier_user_id'])

	def __sorted_by_supplier(s):
		return (s['supplier'], s['supplier_user_length'])
	sorted(products, key=__sorted_by_supplier)  # 相同supplier排到一起

	return products


###################################################################################
# get_weizoom_mall_partner_products: 获取该微众商城下的合作商家加入到微众商城的商品
###################################################################################
def get_weizoom_mall_partner_products_and_ids(webapp_id):
	return _get_weizoom_mall_partner_products_and_ids_by(webapp_id)

def get_verified_weizoom_mall_partner_products_and_ids(webapp_id):
	return _get_weizoom_mall_partner_products_and_ids_by(webapp_id, True)

def get_not_verified_weizoom_mall_partner_products_and_ids(webapp_id):
	return _get_weizoom_mall_partner_products_and_ids_by(webapp_id, False)

def _get_weizoom_mall_partner_products_and_ids_by(webapp_id, is_checked=None):
	if WeizoomMall.objects.filter(webapp_id=webapp_id).count() > 0:
		weizoom_mall = WeizoomMall.objects.filter(webapp_id=webapp_id)[0]

		product_ids = []
		product_check_dict = dict()
		other_mall_products = WeizoomMallHasOtherMallProduct.objects.filter(weizoom_mall=weizoom_mall)
		if is_checked != None:
			other_mall_products = other_mall_products.filter(is_checked=is_checked)

		for other_mall_product in other_mall_products:
			product_check_dict[other_mall_product.product_id] = other_mall_product.is_checked
			product_ids.append(other_mall_product.product_id)

		products = Product.objects.filter(id__in=product_ids, shelve_type=PRODUCT_SHELVE_TYPE_ON, is_deleted=False)

		for product in products:
			product.is_checked = product_check_dict[product.id]

		return products, product_ids
	else:
		return None, None

def has_other_mall_product(webapp_id):
	return WeizoomMallHasOtherMallProduct.objects.filter(weizoom_mall__webapp_id=webapp_id).count() > 0

def get_product_ids_in_weizoom_mall(webapp_id):
	return [weizoom_mall_other_mall_product.product_id for weizoom_mall_other_mall_product in WeizoomMallHasOtherMallProduct.objects.filter(webapp_id=webapp_id)]


def set_origin_order_status(child_order, user, action, request=None):
	children_order_status = [order.status for order in Order.objects.filter(origin_order_id=child_order.origin_order_id)]
	origin_order = Order.objects.get(id=child_order.origin_order_id)
	if origin_order.status != min(children_order_status):
		if action == 'ship':
			origin_order.status = min(children_order_status)
			origin_order.save()
			if min(children_order_status) == ORDER_STATUS_PAYED_SHIPED:
				update_order_status(user, action, origin_order, request)
		else:
			update_order_status(user, action, origin_order, request)


def update_order_status(user, action, order, request=None):
	"""
	修改订单状态

	已知引用：
	mobile_app/order_api_views.py
	mall/order.py
	services/cancel_not_pay_order_service/tasks.py

	已知action:
	'action' : 'pay' 支付
	'action' : 'finish' 完成
	'action' : 'cancel' 取消
	'action' : 'return_pay' 退款
	'action' : 'rship' 发货
	"""
	order_id = order.id
	# 快递100签收发送的finsh动作不记录日志，没有user
	if user:
		operation_name = user.username
	else:
		operation_name = None
	action_msg = None
	if action == 'pay':
		action_msg = '支付'
		target_status = ORDER_STATUS_PAYED_NOT_SHIP
		# jz 2015-10-20
		#记录购买统计项
		# PurchaseDailyStatistics.objects.create(
		# 	webapp_id = order.webapp_id,
		# 	webapp_user_id = order.webapp_user_id,
		# 	order_id = order.order_id,
		# 	order_price = order.final_price,
		# 	date = dateutil.get_today()
		# )
		mall_signals.post_pay_order.send(sender=Order, order=order, request=request)
	elif action == 'ship':
		action_msg = '发货'
		target_status = ORDER_STATUS_PAYED_SHIPED
	elif 'finish' in action:
		action_msg = '完成'
		target_status = ORDER_STATUS_SUCCESSED
		actions = action.split('-')
		if operation_name:
			operation_name = u'{} {}'.format(operation_name, (actions[1] if len(actions) > 1 else ''))
		else:
			operation_name = actions[1] if len(actions) > 1 else ''
		#更新红包引入消费金额的数据 by Eugene
		if order.coupon_id and promotion_models.RedEnvelopeParticipences.objects.filter(coupon_id=order.coupon_id, introduced_by__gt=0).count() > 0:
			red_envelope2member = promotion_models.RedEnvelopeParticipences.objects.get(coupon_id=order.coupon_id)
			relation = promotion_models.RedEnvelopeParticipences.objects.filter(
				red_envelope_rule_id=red_envelope2member.red_envelope_rule_id,
				red_envelope_relation_id=red_envelope2member.red_envelope_relation_id,
				member_id=red_envelope2member.introduced_by
			)
			relation.update(introduce_sales_number = F('introduce_sales_number') + order.final_price + order.postage)

	elif action == 'return_pay':
		action_msg = '退款'
		target_status = ORDER_STATUS_REFUNDING
	elif 'cancel' in action or 'return_success' == action:
		actions = action.split('-')
		operation_name = u'{} {}'.format(operation_name, (actions[1] if len(actions) > 1 else ''))
		if 'cancel' in action:
			action_msg = '取消订单'
			target_status = ORDER_STATUS_CANCEL
		else:
			action_msg = '退款完成'
			target_status = ORDER_STATUS_REFUNDED

		try:
			# 返回订单使用的积分
			if order.integral:
				from modules.member.models import WebAppUser
				from modules.member.integral import increase_member_integral
				member = WebAppUser.get_member_by_webapp_user_id(order.webapp_user_id)
				increase_member_integral(member, order.integral, u'取消订单 返还积分')
			# 返回订单使用的优惠劵
			if order.coupon_id:
				from market_tools.tools.coupon.util import restore_coupon
				restore_coupon(order.coupon_id)
			# 返回商品的数量
			__restore_product_stock_by_order(order)
			mall_signals.cancel_order.send(sender=Order, order=order)


		except :
			notify_message = u"取消订单业务处理异常，cause:\n{}".format(unicode_full_stack())
			watchdog_alert(notify_message, "mall")
	else:
		target_status = None
	expired_status = order.status
	if target_status:
		if 'cancel' in action and request:
			Order.objects.filter(id=order_id).update(status=target_status, reason=request.POST.get('reason', ''))

		elif 'pay' == action:
			payment_time = datetime.now()
			Order.objects.filter(id=order_id).update(status=target_status, payment_time=payment_time)
			Order.objects.filter(origin_order_id=order_id).update(status=target_status, payment_time=payment_time)
			# 更新首单信息
			pay_order = Order.objects.get(id=order_id)
			if Order.objects.filter(
					webapp_id=pay_order.webapp_id,
					webapp_user_id=pay_order.webapp_user_id,
					is_first_order=True
					).count() == 0:
				Order.objects.filter(id=order_id).update(is_first_order=True)
			try:
				"""
					增加异步消息：修改会员消费次数和金额,平均客单价
				"""
				from modules.member.tasks import update_member_pay_info
				order.payment_time = payment_time
				update_member_pay_info(order)
			except:
				alert_message = u"update_order 修改会员消费次数和金额,平均客单价, cause:\n{}".format(unicode_full_stack())
				watchdog_error(alert_message)

		else:
			Order.objects.filter(id=order_id).update(status=target_status)
		operate_log = u' 修改状态'
		if operation_name:
			record_status_log(order.order_id, operation_name, order.status, target_status)
			record_operation_log(order.order_id, operation_name, action_msg, order)

	try:
		# TODO 返还用户积分
		from modules.member import integral
		if expired_status < ORDER_STATUS_SUCCESSED and int(target_status) == ORDER_STATUS_SUCCESSED \
				and expired_status != ORDER_STATUS_CANCEL and order.origin_order_id <= 0:
			if MallOrderFromSharedRecord.objects.filter(order_id=order.id).count() > 0:
				order_record = MallOrderFromSharedRecord.objects.filter(order_id=order.id)[0]
				fmt = order_record.fmt
			else:
				order_record = None
				fmt = None
			integral.increase_after_payed_finsh(fmt, order)
			if order_record and order_record.url and order_record.is_updated == False:
				from modules.member.models import MemberSharedUrlInfo, Member
				followed_member = Member.objects.get(token=fmt)
				MemberSharedUrlInfo.objects.filter(shared_url=order_record.url, member_id=followed_member.id).update(leadto_buy_count=F('leadto_buy_count')+1)
				order_record.is_updated = True
				order_record.save()
				#print '>>>>>.aaaaaaaaaaaaaaaaaaaaaaaaffffff>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
	except:
		notify_message = u"订单状态为已完成时为贡献者增加积分，cause:\n{}".format(unicode_full_stack())
		watchdog_error(notify_message)
	from webapp.handlers import event_handler_util
	from utils import json_util
	event_data = {'order':json.dumps(Order.objects.get(id=order_id).to_dict(),cls=json_util.DateEncoder)}
	event_handler_util.handle(event_data, 'send_order_email')
	# try:
	# 	mall_util.email_order(order=Order.objects.get(id=order_id))
	# except :
	# 	notify_message = u"订单状态改变时发邮件失败，cause:\n{}".format(unicode_full_stack())
	# 	watchdog_alert(notify_message)

	if order.origin_order_id > 0 and target_status in [ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED]:
		# 如果更新子订单，更新父订单状态
		set_origin_order_status(order, user, action, request)
	else:
		# 如果更新父订单，更新子订单状态
		#更新会员的消费、消费次数、消费单价
		try:
			update_user_paymoney(order.webapp_user_id)
		except:
			pass
		from mall.order.util import set_children_order_status
		set_children_order_status(order, target_status)
		if target_status in [ORDER_STATUS_SUCCESSED, ORDER_STATUS_REFUNDING, ORDER_STATUS_CANCEL]:
			auto_update_grade(webapp_user_id=order.webapp_user_id)

def __restore_product_stock_by_order(order):
	"""

	返回商品的库存
	包括赠品库存
	和销量

	"""
	products = get_order_products(order)
	for product in products:
		models = ProductModel.objects.filter(product_id=product['id'], name=product['product_model_name'])
		# 该商品有此规格，并且库存是有限，进入修改商品的数量
		if models.count() > 0 and models[0].stock_type == PRODUCT_STOCK_TYPE_LIMIT:
			product_model = models[0]
			product_model.stocks = product_model.stocks + product['count']
			product_model.save()
		# product sales update
		if order.status < mall_models.ORDER_STATUS_PAYED_SUCCESSED or (
			product.get('promotion', None) and product['promotion'].get('type', '').find('premium_product') > 0):
			# 订单未支付或者是赠品商品, 不需要回退销量数据
			continue
		productsales = ProductSales.objects.filter(product_id=product.get('id'))
		if len(productsales):
			ProductSales.objects.filter(
				product_id=product.get('id')
			).update(sales=productsales[0].sales - product['count'])
		else:
			ProductSales.objects.create(
				product_id=product.get('id'),
				sales=0
			)



########################################################################
# get_order_fitlers_by_user: 获取该用户的所有订单筛选
########################################################################
def get_order_fitlers_by_user(user):
	data_filters = UserHasOrderFilter.objects.filter(owner=user).order_by('created_at')
	filters = []
	for data_filter in data_filters:
		filters.append({
			'id' : data_filter.id,
			'name': data_filter.filter_name,
			'value': data_filter.filter_value
		})

	return filters

# mobile_app/order_api_views.py和mall.order使用
def get_pay_interfaces_by_user(user):
	"""
	获取该用户的所有的支付方式
	TODO: 改成从cache获取

	已知引用：
	mobile_app/order_api_views.py
	"""
	existed_pay_interfaces = []
	pay_interfaces = PayInterface.objects.filter(owner=user)
	for pay_interface in pay_interfaces:
		if pay_interface.type == PAY_INTERFACE_ALIPAY:
			existed_pay_interfaces.append({'pay_name':u'支付宝','data_value':PAY_INTERFACE_ALIPAY})
		if pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
			existed_pay_interfaces.append({'pay_name':u'微信支付','data_value':PAY_INTERFACE_WEIXIN_PAY})
		if pay_interface.type == PAY_INTERFACE_COD:
			existed_pay_interfaces.append({'pay_name':u'货到付款','data_value':PAY_INTERFACE_COD})
		if pay_interface.type == PAY_INTERFACE_WEIZOOM_COIN:
			existed_pay_interfaces.append({'pay_name':u'微众卡支付','data_value':PAY_INTERFACE_WEIZOOM_COIN})

	return existed_pay_interfaces


########################################################################
# get_products_by_ids: 根据ids获取product集合
########################################################################
def get_products_by_ids(ids):
	return list(Product.objects.filter(id__in=ids))


def get_order_status_text(status):
	return STATUS2TEXT[status]


# def get_select_params(request):
# 	"""
# 	构造查询条件
# 	"""
# 	query = request.GET.get('query', '').strip()
# 	ship_name = request.GET.get('ship_name', '').strip()
# 	ship_tel = request.GET.get('ship_tel', '').strip()
# 	product_name = request.GET.get('product_name', '').strip()
# 	pay_type = request.GET.get('pay_type', '').strip()
# 	express_number = request.GET.get('express_number', '').strip()
# 	order_source = request.GET.get('order_source', '').strip()
# 	order_status = request.GET.get('order_status', '').strip()
# 	isUseWeizoomCard = int(request.GET.get('isUseWeizoomCard', '0').strip())
#
# 	# 填充query
# 	query_dict = dict()
# 	if len(query):
# 		query_dict['order_id'] = query.strip().split('-')[0]
# 	if len(ship_name):
# 		query_dict['ship_name'] = ship_name
# 	if len(ship_tel):
# 		query_dict['ship_tel'] = ship_tel
# 	if len(express_number):
# 		query_dict['express_number'] = express_number
# 	if len(product_name):
# 		query_dict['product_name'] = product_name
# 	if len(pay_type):
# 		query_dict['pay_interface_type'] = int(pay_type)
# 	if len(order_source):
# 		query_dict['order_source'] = int(order_source)
# 	if len(order_status):
# 		query_dict['status'] = int(order_status)
# 	if isUseWeizoomCard:
# 		query_dict['isUseWeizoomCard'] = isUseWeizoomCard
#
#
# 	# 时间区间
# 	try:
# 		date_interval = request.GET.get('date_interval', '')
# 		if date_interval:
# 			date_interval = date_interval.split('|')
# 			if " " in date_interval[0]:
# 				date_interval[0] = date_interval[0] +':00'
# 			else:
# 				date_interval[0] = date_interval[0] +' 00:00:00'
#
# 			if " " in date_interval[1]:
# 				date_interval[1] = date_interval[1] +':00'
# 			else:
# 				date_interval[1] = date_interval[1] +' 23:59:59'
# 		else:
# 			date_interval = None
# 	except:
# 		date_interval = None
#
# 	return query_dict, date_interval

# def get_orders_by_params(query_dict, date_interval, orders):
# 	"""
# 	按照查询条件筛选符合条件的订单
# 	"""
# 	#商品名称
# 	product_name = ""
# 	if query_dict.has_key("product_name"):
# 		product_name = query_dict["product_name"]
# 		query_dict.pop("product_name")
#
# 	#处理搜索
# 	if len(query_dict):
# 		if query_dict.has_key("isUseWeizoomCard"):
# 			query_dict.pop("isUseWeizoomCard")
# 			orders = orders.exclude(weizoom_card_money=0)
# 		orders = orders.filter(**query_dict)
#
# 	#处理 时间区间筛选
# 	if date_interval:
# 		start_time = date_interval[0]
# 		end_time = date_interval[1]
# 		orders = orders.filter(created_at__gte=start_time, created_at__lt=end_time)
#
# 	# #处理商品名称筛选条件
# 	# if product_name:
# 	# 	filter_orders = []
# 	# 	order2products = {}
# 	# 	for order in orders:
# 	# 		products = get_order_products(order)
# 	# 		for product in products:
# 	# 			if product_name in product['name']:
# 	# 				filter_orders.append(order)
# 	# 				break
# 	# 	orders = filter_orders
#
# 	# #处理商品名称筛选条件
# 	# if product_name:
# 	# 	filter_orders = []
#	 #
# 	# 	order_ids = [order.id for order in orders]
# 	# 	orderHasProducts = OrderHasProduct.objects.filter(order_id__in=order_ids)
#	 #
# 	# 	orderId2orderHasProducts = dict()
# 	# 	for orderHasProduct in orderHasProducts:
# 	# 		if not orderId2orderHasProducts.get(orderHasProduct.order_id):
# 	# 			orderId2orderHasProducts[orderHasProduct.order_id] = []
# 	# 		orderId2orderHasProducts.get(orderHasProduct.order_id).append(orderHasProduct)
#	 #
# 	# 	order_promotion_relations = list(OrderHasPromotion.objects.filter(order_id__in=order_ids))
# 	# 	id2promotion = dict([(relation.promotion_id, relation) for relation in order_promotion_relations])
#	 #
# 	# 	product_ids = [orderHasProduct.product_id for orderHasProduct in orderHasProducts]
# 	# 	products = Product.objects.filter(id__in=product_ids)
# 	# 	id2product = dict([(product.id, product) for product in products])
#	 #
# 	# 	for order in orders:
# 	# 		for orderHasProduct in orderId2orderHasProducts[order.id]:
#	 #
# 	# 			if product_name in id2product.get(orderHasProduct.product_id, None).name:
# 	# 				filter_orders.append(order)
# 	# 				break
#	 #
# 	# 			promotion_relation = id2promotion.get(orderHasProduct.promotion_id, None)
# 	# 			if promotion_relation:
#	 #
# 	# 				promotion_result = promotion_relation.promotion_result
#	 #
# 	# 				if promotion_result.has_key('premium_products'):
# 	# 					for premium_product in promotion_relation.promotion_result['premium_products']:
#	 #
# 	# 						if product_name in premium_product['name']:
# 	# 							filter_orders.append(order)
# 	# 							break
#	 #
# 	# 	orders = filter_orders
#
#
# 	if product_name:
# 		product_list = Product.objects.filter(name__contains=product_name)
# 		product_ids = [product.id for product in product_list]
#
# 		orderHasProduct_list = OrderHasProduct.objects.filter(product_id__in=product_ids)
#
#
# 		order_ids = [orderHasProduct.order_id for orderHasProduct in orderHasProduct_list]
#
# 		orderHasPromotions = OrderHasPromotion.objects.filter(promotion_type="premium_sale")
#
# 		for orderHasPromotion in orderHasPromotions:
# 			for premium_product in orderHasPromotion.promotion_result['premium_products']:
# 				if premium_product['id'] in product_ids and orderHasPromotion.order_id not in order_ids:
#
# 					order_ids.append(orderHasPromotion.order_id)
#
#
# 		orders =orders.filter(id__in=order_ids)
# 	return orders


########################################################################
# get_order_list: 获取订单列表
########################################################################
DEFAULT_CREATE_TIME = '2000-01-01 00:00:00'

DATA_UPDATE_TYPE = "update_time"
DATA_CREATED_TYPE = "created_time"
def get_order_list(user, query_dict, sort_attr, query_string, count_per_page=15, cur_page=1, date_interval=None,
	date_type=None, is_refund=False):
	webapp_id = user.get_profile().webapp_id
	orders = belong_to(webapp_id)

	if is_refund:
		orders = orders.filter(status__in=[ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED])
	# else:
	# 	orders = orders.filter(~Q(status=ORDER_STATUS_REFUNDED))

	# 统计订单总数
	order_total_count = _get_orders_total_count(orders)
	#处理排序
	if sort_attr != 'created_at':
		orders = orders.order_by(sort_attr)

	orders = get_orders_by_params(query_dict, date_interval, orders)

	#返回订单的数目
	order_return_count = len(orders)
	###################################################
	if count_per_page > 0:
		#进行分页
		pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page, query_string=query_string)
	else:
		#全部订单
		pageinfo = {"object_count": len(orders)}

	#获取order对应的会员
	webapp_user_ids = set([order.webapp_user_id for order in orders])
	from modules.member.models import Member
	webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

	#获得order对应的商品数量
	order_ids = [order.id for order in orders]

	order2productcount = {}
	for relation in OrderHasProduct.objects.filter(order_id__in=order_ids):
		order_id = relation.order_id
		if order_id in order2productcount:
			order2productcount[order_id] = order2productcount[order_id] + 1
		else:
			order2productcount[order_id] = 1



	#构造返回的order数据
	items = []
	for order in orders:
		#获取order对应的member的显示名
		member = webappuser2member.get(order.webapp_user_id, None)
		if member:
			order.buyer_name = member.username_for_html
			order.member_id = member.id
		else:
			order.buyer_name = u'未知'
			order.member_id = 0

		payment_time = None

		if order.payment_time is None:
			payment_time = ''
		elif datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M:%S') == DEFAULT_CREATE_TIME:
			payment_time = ''
		else:
			payment_time = datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M:%S')

		if order.order_source:
			order.come = 'weizoom_mall'
		else:
			order.come = 'mine_mall'

		order.status_text = get_order_status_text(order.status)
		order.product_count = order2productcount.get(order.id, 0)
		order.payment_time = payment_time
		if order.pay_interface_type == 3:
			order.pay_interface_type_text = PAYTYPE2NAME.get(10, u'')
		else:
			order.pay_interface_type_text = PAYTYPE2NAME.get(order.pay_interface_type, u'')


		# liupeiyu 该订单中的会员是否可点击
		# 来自本店的订单,会员不可点击
		# 或者改用户是 微众商城，会员都可点击
		if order.come is 'weizoom_mall' and user.is_weizoom_mall is False:
			order.member_id = 0

		#order_id_list.append(order.id)

	return orders, pageinfo, order_total_count, order_return_count


# ########################################################################
# # _get_orders_total_count: 获得订单中的各种总数
# ########################################################################
# def _get_orders_total_count(orders):
# 	count = orders.count()
# 	status_not_count = orders.filter(status=ORDER_STATUS_NOT).count()
# 	status_payed_not_ship_total = orders.filter(status=ORDER_STATUS_PAYED_NOT_SHIP).count()
# 	status_payed_shiped_total = orders.filter(status=ORDER_STATUS_PAYED_SHIPED).count()
# 	status_cancel_count = orders.filter(status=ORDER_STATUS_CANCEL).count()
# 	status_successed_count = orders.filter(status=ORDER_STATUS_SUCCESSED).count()
# 	return {
# 		'total_count': count,
# 		'status_not_count': status_not_count,
# 		'status_payed_not_ship_total': status_payed_not_ship_total,
# 		'status_payed_shiped_total': status_payed_shiped_total,
# 		'status_cancel_count': status_cancel_count,
# 		'status_successed_count': status_successed_count
# 	}


########################################################################
# get_order: 获取订单
########################################################################
def get_order_by_id(order_id):
	try:
		return Order.objects.get(id=order_id)
	except:
		return None

########################################################################
# get_order_by_order_id: 根据订单号获取订单信息
########################################################################
def get_order_by_order_id(order_id):
	try:
		order = Order.objects.get(order_id=order_id)
	except:
		return None

	order_has_products = OrderHasProduct.objects.filter(order=order)

	number = 0
	for order_has_product in order_has_products:
		number += order_has_product.number
	order.number = number

	#处理订单关联的优惠券
	order.coupon =  order.get_coupon()
	order.products = get_order_products(order)

	logs = get_order_operation_logs(order.order_id)

	if logs.count() > 0:
		order.update_at = logs[0].created_at
	else:
		order.update_at = order.created_at

	return order


########################################################################
# update_order_express_info: 更新订单物流信息
########################################################################
def update_order_express_info(order_id, express_company_name, express_id):
	Order.objects.filter(order_id=order_id).update(express_company_name=express_company_name, express_number=express_id)


########################################################################
# update_product_stock: 更新商品库存信息
########################################################################
def update_product_stock(product_id, product_model_id, stock):
	if stock == -1:
		ProductModel.objects.filter(product_id=product_id, id=product_model_id).update(stock_type=PRODUCT_STOCK_TYPE_UNLIMIT, stocks=-1)
	else:
		ProductModel.objects.filter(product_id=product_id, id=product_model_id).update(stock_type=PRODUCT_STOCK_TYPE_LIMIT, stocks=stock)


def batch_handle_order(json_data, user):
	"""
	批量发货

	已知引用:features/steps/mall_order_manager_steps.py
			mall/order/delivery.py
	"""
	error_data = []
	success_data = []
	for item in json_data:
		try:
			order_id = item.get('order_id', '')
			express_company_name = item.get('express_company_name', '')
			express_number = item.get('express_number', '')
			express_company_value = express_util.get_value_by_name(express_company_name)
			# 快递公司 不符
			if express_company_value == express_company_name:
				item["error_info"] = "快递名称错误"
				error_data.append(item)
				continue
			try:
				order_id = order_id.strip()
				if '-' in order_id:
					new_order_id = order_id.split('-')[0]
					order = Order.objects.get(order_id=new_order_id)
					if str(order.edit_money).replace('.', '').replace('-', '') != order_id.split('-')[1]:
						raise
				else:
					order = Order.objects.get(order_id=order_id)
			except:
				item["error_info"] = "订单号错误"
				error_data.append(item)
				continue
			if not express_number:
				raise
			if order.status == ORDER_STATUS_PAYED_NOT_SHIP:
				# 批量发货
				if ship_order(order.id, express_company_value, express_number, user.username, u''):
					success_data.append(item)
				else:
					raise
			else:
				item["error_info"] = "订单状态错误"
				error_data.append(item)
				continue
		except:
			item["error_info"] = "格式不正确"
			error_data.append(item)
			alert_message = u"batch_handle_order批量发货 格式不正确, item:{}, cause:\n{}".format(item, unicode_full_stack())
			watchdog_warning(alert_message)

	return success_data, error_data


########################################################################
# get_default_postage_by_owner_id: 获取默认运费
########################################################################
def get_default_postage_by_owner_id(owner_id):
	try:
		return PostageConfig.objects.get(owner_id=owner_id, is_used=True, is_system_level_config=False)
	except:
		None


########################################################################
# get_order_pay_interfaces: 获取该订单的支付方式
########################################################################
def get_order_pay_interfaces(webapp_owner_id, webapp_user, order_id):
	products = [h.product for h in OrderHasProduct.objects.filter(order_id=order_id)]
	return __get_products_pay_interfaces(webapp_user, products)


########################################################################
# __get_products_pay_interfaces: 获取商品的共同支付方式
########################################################################
from market_tools.tools.weizoom_card.models import AccountHasWeizoomCardPermissions
def __get_products_pay_interfaces(webapp_user, products):
	pay_interfaces = [pay_interface for pay_interface in webapp_user.webapp_owner_info.pay_interfaces if pay_interface.is_active and not pay_interface.type == PAY_INTERFACE_WEIZOOM_COIN]
	#pay_interfaces = PayInterface.objects.filter(owner_id=webapp_owner_id, is_active=True).filter(~Q(type=PAY_INTERFACE_WEIZOOM_COIN))

	types = [p.type for p in pay_interfaces]

	# 如果不包含货到付款，直接返回所有的在线支付
	if PAY_INTERFACE_COD not in types:
		return pay_interfaces

	# 商品中是 货到付款方式
	pay_interface_cod_count = 0
	for product in products:
		if product.is_use_cod_pay_interface:
			pay_interface_cod_count = pay_interface_cod_count + 1

	if pay_interface_cod_count == len(list(products)):
		return pay_interfaces
	else:
		# return pay_interfaces.filter(type__in = ONLINE_PAY_INTERFACE)
		return [pay_interface for pay_interface in pay_interfaces if pay_interface.type in ONLINE_PAY_INTERFACE]


########################################################################
# get_pay_interface_onlines_by_owner_id: 获取在线支付方式
########################################################################
def get_pay_interface_onlines_by_owner_id(owner_id):
	try:
		return PayInterface.objects.filter(owner_id=owner_id, is_active=True, type__in=ONLINE_PAY_INTERFACE)
	except:
		None


########################################################################
# get_pay_interface_cod_by_owner_id: 获取货到付款支付方式
########################################################################
def get_pay_interface_cod_by_owner_id(owner_id):
	try:
		return PayInterface.objects.get(owner_id=owner_id, is_active=True, type=PAY_INTERFACE_COD)
	except:
		None


########################################################################
# update_products_postage: 修改运费
########################################################################
def update_products_postage(owner_id, postage_id):
	# 该id是否为 免运费
	try:
		is_system_level_config = PostageConfig.objects.get(id=postage_id).is_system_level_config
	except:
		is_system_level_config = True

	# id 大于0 并且 不是免运费
	if postage_id > 0 and is_system_level_config == False:
		# 更换邮费
		Product.objects.filter(owner_id=owner_id).exclude(postage_id=-1).update(postage_id=postage_id)
	else:
		# 修改为免运费
		Product.objects.filter(owner_id=owner_id).update(postage_id=-1)


########################################################################
# update_products_pay_interface_cod: 修改商品不使用货到付款
########################################################################
def update_products_pay_interface_cod(owner_id):
	Product.objects.filter(owner_id=owner_id).update(is_use_cod_pay_interface=False)


#############################################################################
# get_postage_configs_for_cache: 获得用于缓存的postage config数据
#############################################################################
def get_postage_configs_for_cache(webapp_owner_id):
	def inner_func():
		postage_configs = PostageConfig.objects.filter(owner_id=webapp_owner_id)

		values = []
		for postage_config in postage_configs:
			factor = {
				'firstWeight': postage_config.first_weight,
				'firstWeightPrice': postage_config.first_weight_price,
				'isEnableAddedWeight': postage_config.is_enable_added_weight,
			}

			#if postage_config.is_enable_added_weight:
			factor['addedWeight'] = float(postage_config.added_weight)
			if postage_config.added_weight_price:
				factor['addedWeightPrice'] = float(postage_config.added_weight_price)
			else:
				factor['addedWeightPrice'] = 0

			# 特殊运费配置
			special_factor = dict()
			if postage_config.is_enable_special_config:
				for special_config in postage_config.get_special_configs():
					data = {
						'firstWeight': special_config.first_weight,
						'firstWeightPrice': special_config.first_weight_price,
						'addedWeight': float(special_config.added_weight),
						'addedWeightPrice': float(special_config.added_weight_price)
					}
					for province_id in special_config.destination.split(','):
						special_factor['province_{}'.format(province_id)] = data
			factor['special_factor'] = special_factor

			# 免运费配置
			free_factor = dict()
			if postage_config.is_enable_free_config:
				for free_config in postage_config.get_free_configs():
					data = {
						'condition': free_config.condition
					}
					if data['condition'] == 'money':
						data['condition_value'] = float(free_config.condition_value)
					else:
						data['condition_value'] = int(free_config.condition_value)
					for province_id in free_config.destination.split(','):
						free_factor.setdefault('province_{}'.format(province_id), []).append(data)
			factor['free_factor'] = free_factor

			postage_config.factor = factor
			values.append(postage_config.to_dict('factor'))

		return {
			'value': values
		}

	return inner_func


def update_promotion_status_by_member_grade(member_grade_ids):
	"""
	删除会员等级，更新与之相关会员等级的促销活动状态
	"""
	try:
		promotion_models.Promotion.objects.filter(member_grade_id__in=member_grade_ids, status__in=[promotion_models.PROMOTION_STATUS_NOT_START, promotion_models.PROMOTION_STATUS_STARTED]).update(status=promotion_models.PROMOTION_STATUS_FINISHED)
		promotion_models.IntegralSaleRule.objects.filter(member_grade_id__in=member_grade_ids).delete()
	except:
		alert_message = u"update_promotion_status_by_member_grade cause:\n{}".format(unicode_full_stack())
		watchdog_error(alert_message)
		try:
			promotion_models.Promotion.objects.filter(member_grade_id__in=member_grade_ids, status__in=[promotion_models.PROMOTION_STATUS_NOT_START, promotion_models.PROMOTION_STATUS_STARTED]).update(status=promotion_models.PROMOTION_STATUS_FINISHED)
		except:
			pass



def get_products_in_wishlist(webapp_user, owner_id, member_id):
	"""
	获取收藏夹中的商品
	"""
	from operator import attrgetter
	wishlist = MemberProductWishlist.objects.filter(owner_id=owner_id, member_id=member_id, is_collect=True).order_by('-id')
	product_ids = [item.product_id for item in wishlist]
	product_list = get_products_detail(owner_id, product_ids, webapp_user)
	product_list = sorted(product_list, key=attrgetter('id'), reverse=True)
	# for item in wishlist:
	# 	#---TODO:似乎有更好的函数可以调用get_product_detail()---
	# 	product = get_product_detail(owner_id, item.product_id, webapp_user)
	# 	#product = webapp_cache.get_webapp_product_detail(owner_id, item.product_id)
	# 	product_list.append(product)
	return product_list

def update_wishlist_product(request):
	"""
	更新商品收藏
	"""
	try:
		webapp_owner_id = request.webapp_owner_id
		member_id = request.member.id
		product_id = request.POST['product_id']
		is_collect = request.POST['is_collect']

		collect = MemberProductWishlist.objects.filter(owner_id=webapp_owner_id, member_id=member_id, product_id=product_id)
		if collect.count() > 0:
			if is_collect == "true":
				collect.update(is_collect=False)
			else:
				collect.update(is_collect=True, add_time=datetime.now())
		else:
			MemberProductWishlist.objects.create(
				owner_id = webapp_owner_id,
				member_id = member_id,
				product_id = product_id,
				is_collect = True,
			)
	except:
		return create_response(500).get_response()

	return create_response(200).get_response()

def check_product_in_wishlist(request):
	"""
	判断会员是否收藏了此商品
	"""
	response = create_response(200)
	try:
		webapp_owner_id = request.webapp_owner_id
		member_id = request.member.id
		product_id = request.GET['product_id']
		collect = MemberProductWishlist.objects.filter(
			owner_id=webapp_owner_id,
			member_id=member_id,
			product_id=product_id,
			is_collect=True
		)
		if collect.count() > 0:
			response.data = 'true'
		else:
			response.data = 'false'
	except:
		return create_response(500).get_response()

	return response.get_response()


def get_member_product_info_dict(request):
	result_data = dict()
	shopping_cart_count = ShoppingCart.objects.filter(webapp_user_id=request.webapp_user.id).count()
	result_data['count'] = shopping_cart_count
	webapp_owner_id = request.webapp_owner_id
	product_id = request.GET.get('product_id', "")
	if request.member:
		member_id = request.member.id
		if product_id:
			collect = MemberProductWishlist.objects.filter(
				owner_id=webapp_owner_id,
				member_id=member_id,
				product_id=product_id,
				is_collect=True
			)
			if collect.count() > 0:
				result_data['is_collect'] = 'true'
			else:
				result_data['is_collect'] = 'false'
		member_grade_id, discount = get_member_discount(request)
		result_data['member_grade_id'] = member_grade_id
		result_data['discount'] = discount
		result_data['usable_integral'] = request.member.integral
		result_data['is_subscribed'] = request.member.is_subscribed
	else:
		if product_id:
			result_data['is_collect'] = 'false'
		result_data['member_grade_id'] = -1
		result_data['discount'] = 100
		result_data['usable_integral'] = 0
		result_data['is_subscribed'] = False
	return result_data

def get_member_product_info(request):
	'''
	获取购物车的数量和检查商品是否已被收藏
	'''
	response = create_response(200)
	response.data = get_member_product_info_dict(request)
	return response.get_response()


def get_member_discount(request):
	"""获取会员等级ID、折扣
	"""
	if not request or not request.member:
		return -1, 100
	member_grade_id = request.member.grade_id
	member_grade = request.webapp_owner_info.member2grade.get(member_grade_id, '')
	if member_grade:
		return member_grade_id, member_grade.shop_discount
	else:
		return member_grade_id, 100


def wishlist_product_count(webapp_owner_id, member_id):
	"""
	获取会员收藏的商品数
	"""
	return MemberProductWishlist.objects.filter(
		owner_id=webapp_owner_id,
		member_id=member_id,
		is_collect=True
	).count()

OVERDUE_DAYS = 15
def check_product_review_overdue(product_id):
	top_review_list = ProductReview.objects.filter(status=2,product_id=product_id)
	for review in top_review_list:
		after_15_days = review.top_time+timedelta(days=OVERDUE_DAYS)
		now = datetime.now()
		if (after_15_days <= now):
			review.status = 1
			ProductReview.objects.filter(id=review.id).update(status=1,top_time=DEFAULT_DATETIME)



def get_product_review(request):
	"""
	获取商品的评价
	"""
	product_id = request.GET.get('product_id', None)
	# 检查置顶评论是否过期
	check_product_review_overdue(product_id)
	product_review_list = ProductReview.objects.filter(Q(product_id=product_id) & Q(status__in=['1', '2'])).order_by('-top_time', '-id')

	from cache import webapp_cache
	cache_product = webapp_cache.get_webapp_product_detail(request.webapp_owner_id, product_id)

	product_review_ids = []
	member_ids = []
	order_has_product_ids = []
	for review in product_review_list:
		product_review_ids.append(review.id)
		member_ids.append(review.member_id)
		order_has_product_ids.append(review.order_has_product_id)

	product_review_pictures = ProductReviewPicture.objects.filter(product_review_id__in=product_review_ids)
	review_id2pictures = {}
	for picture in product_review_pictures:
		if review_id2pictures.has_key(picture.product_review_id):
			review_id2pictures[picture.product_review_id].append(picture.att_url)
		else:
			review_id2pictures[picture.product_review_id] = [picture.att_url]

	members = get_member_by_id_list(member_ids)
	member_id2member = dict([(m.id, m) for m in members])

	id2order_has_product = dict([(o.id, o) for o in OrderHasProduct.objects.filter(id__in=order_has_product_ids)])

	for review in product_review_list:
		#去OrderHasProduct取对应商品的规格数据product_model_name
		review_product = id2order_has_product[review.order_has_product_id]
		review.product_name = review_product.product_name
		review.product_model_name = review_product.product_model_name
		if review.product_model_name == 'standard':
			review.custom_model_properties = []
		else:
			review.custom_model_properties = review_product.product.fill_specific_model(review_product.product_model_name, cache_product.models)

		if review_id2pictures.has_key(review.id):
			review.pictures = review_id2pictures[review.id]
		else:
			review.pictures = []

		member = member_id2member.get(review.member_id, None)
		if member:
			review.member_name = member.username_for_html
			review.user_icon = member.user_icon
		else:
			review.member_name = '*'

	return product_review_list

import base64
from weapp.celery import celery_logger, celery_task as task
from account.views import __validate_image
from core.upyun_util import upload_image_to_upyun

@task
def save_image_and_update_att_url(request, picture, product_review):
	"""
	异步上传评论图片并将地址保存在数据库中
	"""
	now_time = datetime.now()
	date = time.strftime("%Y%m%d")
	dir_path_suffix = 'weapp/%d_%s' % (request.user_profile.user_id, date)
	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	file_name = '%s.%s' % (datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"), 'png')
	ajax_path = '%s/%s' % (dir_path, file_name)
	ajax_file = picture.split(',')

	image_content = base64.b64decode(ajax_file[1])
	image_file = open(ajax_path, 'wb')
	image_file.write(image_content)
	image_file.close()

	save_image_time = datetime.now() - now_time
	watchdog_info(u"将图片保存在本地所花的时间-%s" % str(save_image_time), type="mall", user_id=int(request.webapp_owner_id))

	if __validate_image(ajax_path):
		try:
			image_path = upload_image_to_upyun(ajax_path, '/upload/%s/%s' % (dir_path_suffix, file_name))
			product_review.att_url = image_path
			product_review.save()
			watchdog_info(u"图片%s上传又拍云成功,所花的时间为-%s" % (file_name, str(datetime.now() - now_time)), type="mall", user_id=int(request.webapp_owner_id))
		except:
			product_review.att_url = '/static/upload/%s/%s' % (dir_path_suffix, file_name)
			product_review.save()
			notify_msg = u"上传图片到又拍云时失败,所花的时间为-{}, cause:\n{}".format(str(datetime.now() - now_time), unicode_full_stack())
			watchdog_error(notify_msg, type="mall", user_id=int(request.webapp_owner_id))
	else:
		product_review.att_url = '/static/upload/%s/%s' % (dir_path_suffix, file_name)
		product_review.save()
		notify_msg = u"上传图片地址错误！"
		watchdog_error(notify_msg, type="mall", user_id=int(request.webapp_owner_id))


def has_promotion(user_member_grade_id=None, promotion_member_grade_id=0):
	"""判断促销是否对用户开放.

	Args:
		user_member_grade_id(int): 用户会员等价
		promotion_member_grade_id(int): 促销制定的会员等级

	Return:
		True - if 促销对用户开放
		False - if 促销不对用户开放
	"""
	if promotion_member_grade_id <= 0:
		return True
	elif promotion_member_grade_id == user_member_grade_id:
		return True
	else:
		return False

def update_user_paymoney(id):
	"""
	add by houtingfei
	reason：取消订单修改会员消息信息
	"""
	#更新会员的消费、消费次数、消费单价
	from modules.member.models import WebAppUser
	member = WebAppUser.get_member_by_webapp_user_id(id)
	user_orders = Order.get_orders_from_webapp_user_ids(member.get_webapp_user_ids)
	pay_money = 0
	pay_times = 0
	for user_order in user_orders:
		user_order.final_price = user_order.final_price + user_order.weizoom_card_money
		if user_order.status > 2:
			pay_money += user_order.final_price
			pay_times += 1

	member.pay_times = pay_times
	member.pay_money = pay_money
	try:
		member.unit_price = pay_money/pay_times
	except:
		member.unit_price = 0
	member.save()

def create_mall_order_from_shared(request,order_id):
	from modules.member.util import get_member, get_followed_member_token_from_cookie
	member = get_member(request)
	followed_member_token = get_followed_member_token_from_cookie(request)
	if (member and member.token == followed_member_token) or not followed_member_token:
		return

	MallOrderFromSharedRecord.objects.create(order_id=order_id, fmt=followed_member_token)
	# try:

	# except Exception, e:
	# 	raise e
