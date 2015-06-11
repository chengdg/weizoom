# -*- coding: utf-8 -*-
# """
# """

# import time
# from datetime import timedelta, datetime, date
# import util as mall_util
# import signals
# import urllib, urllib2
# import os
# import json
# import copy
# import shutil
# import random
# import math

# #from itertools import chain

# from django.http import HttpResponseRedirect, HttpResponse
# from django.template import Context, RequestContext
# from django.contrib.auth.decorators import login_required, permission_required
# from django.conf import settings
# #from django.shortcuts import render_to_response
# from django.contrib.auth.models import User, Group, Permission
# #from django.contrib import auth
# from django.db.models import Q, F

# from tools.regional import views as regional_util
# from core.jsonresponse import JsonResponse, create_response
# from core.exceptionutil import unicode_full_stack
# from core import dateutil
# from tools.express import util as express_util

# from account.models import UserProfile
# from modules.member.models import Member, IntegralStrategySttings
# from modules.member import integral
# from models import *
# from core import paginator
# #from market_tools.tools.delivery_plan.models import DeliveryPlan
# #from market_tools.tools.weizoom_card import module_api as weizoom_card_api
# from market_tools.tools.template_message import models as template_message_model
# from market_tools.tools.template_message import module_api as template_message_api
# from mall.promotion import models as promotion_models

# from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_alert, watchdog_warning, watchdog_debug
# from webapp.modules.mall import signals as mall_signals

# random.seed(time.time())

# ########################################################################
# # get_shopping_cart_product_nums: 获得购物车中商品数量
# ########################################################################
# def get_shopping_cart_product_nums(webapp_user):
# 	return ShoppingCart.objects.filter(webapp_user_id=webapp_user.id).count()


# #############################################################################
# # get_products: 获得product集合
# #   options可用参数：
# #	 1. search_info: 搜索
# #############################################################################
# def get_products_in_webapp(webapp_id, is_access_weizoom_mall, webapp_owner_id, category_id, options=dict()):
# 	#获得category和product集合
# 	category = None
# 	products = None
# 	if category_id == 0:
# 		if not is_access_weizoom_mall:
# 			product_ids_in_weizoom_mall = get_product_ids_in_weizoom_mall(webapp_id)
# 			products = Product.objects.filter(owner_id=webapp_owner_id, shelve_type=PRODUCT_SHELVE_TYPE_ON, is_deleted = False).filter(~Q(id__in=product_ids_in_weizoom_mall)).exclude(type = PRODUCT_DELIVERY_PLAN_TYPE).order_by('-display_index')
# 			category = ProductCategory()
# 			category.name = u'全部'
# 		else:
# 			other_mall_products, other_mall_product_ids = get_verified_weizoom_mall_partner_products_and_ids(webapp_id)
# 			products = Product.objects.filter(owner_id=webapp_owner_id, shelve_type=PRODUCT_SHELVE_TYPE_ON, is_deleted = False).exclude(type = PRODUCT_DELIVERY_PLAN_TYPE).order_by('-display_index')
# 			if other_mall_products:
# 				products = list(products) + list(other_mall_products)
# 			category = ProductCategory()
# 			category.name = u'全部'
# 	else:
# 		try:
# 			if WeizoomMall.is_weizoom_mall(webapp_id) is False:
# 				product_ids_in_weizoom_mall = get_product_ids_in_weizoom_mall(webapp_id)
# 				other_mall_product_ids_not_checked = []
# 			else:
# 				product_ids_in_weizoom_mall = []
# 				_, other_mall_product_ids_not_checked = get_not_verified_weizoom_mall_partner_products_and_ids(webapp_id)

# 			category = ProductCategory.objects.get(id=category_id)
# 			category_has_products = CategoryHasProduct.objects.filter(category=category)
# 			products = []
# 			for category_has_product in category_has_products:
# 				if category_has_product.product.shelve_type == PRODUCT_SHELVE_TYPE_ON:
# 					product = category_has_product.product
# 					#过滤已删除商品和套餐商品
# 					if product.is_deleted or product.type == PRODUCT_DELIVERY_PLAN_TYPE or product.id in product_ids_in_weizoom_mall or product.id in other_mall_product_ids_not_checked or product.shelve_type != PRODUCT_SHELVE_TYPE_ON:
# 						continue
# 					products.append(category_has_product.product)
# 			products.sort(lambda x,y: cmp(y.display_index, x.display_index))
# 		except:
# 			products = []
# 			category = ProductCategory()
# 			category.is_deleted = True
# 			category.name = u'全部'

# 	#处理search信息
# 	if 'search_info' in options:
# 		query = options['search_info']['query']
# 		if query:
# 			conditions = {}
# 			conditions['name__contains'] = query
# 			products = products.filter(**conditions)
			
# 	return category, products


# #############################################################################
# # get_products: 获得product集合
# #   options可用参数：
# #	 1. search_info: 搜索
# #############################################################################
# #add args webapp_id by bert at 17.0
# def get_products(webapp_id, is_access_weizoom_mall, webapp_owner_id, webapp_user, category_id, options=dict()):
# 	category, products = get_products_in_webapp(webapp_id, is_access_weizoom_mall, webapp_owner_id, category_id, options)

# 	for product in products:
# 		#added by chuter
# 		if not isinstance(product, Product):
# 			continue
# 		product.original_price = product.price
# 		product.price, _ = webapp_user.get_discounted_money(product.price, product_type=product.type)
			
# 	return category, products


# #############################################################################
# # get_product: 获得product信息
# #############################################################################
# def get_product_by_id(product_id):
# 	if not product_id:
# 		return Product()

# 	try:
# 		return Product.objects.get(id=product_id)
# 	except:
# 		return Product()


# #############################################################################
# # get_products: 获得product集合
# #   options可用参数：
# #	 1. search_info: 搜索
# #############################################################################
# def get_product_detail_for_cache(webapp_owner_id, product_id):
# 	def inner_func():
# 		try:
# 			#获取product及其model
# 			product = Product.objects.get(id=product_id)
# 			product.fill_model()
			
# 			#获取轮播图
# 			product.swipe_images = []
# 			for swipe_image in ProductSwipeImage.objects.filter(product_id=product_id):
# 				product.swipe_images.append({
# 					'url': swipe_image.url
# 				})
# 			product.swipe_images_json = json.dumps(product.swipe_images)

# 			#获取库存
# 			is_sellout = True
# 			for product_model in product.models:	
# 				# 判断是否有库存，只有有一个商品库存时，is_sellout=False
# 				# 当库存为无限时 or 有限并且库存大于0 时， 并且 is_sellout 还没有被设置为False时
# 				if product_model['stock_type'] == PRODUCT_STOCK_TYPE_UNLIMIT:
# 					is_sellout = False
# 				else:
# 					if product_model['stocks'] > 0:
# 						is_sellout = False
# 			product.is_sellout = is_sellout

# 			promotions = promotion_models.ProductHasPromotion.objects.filter(product=product)
# 			if promotions.count() > 0:
# 				promotion = promotions[0].promotion
# 				promotion_models.Promotion.fill_concrete_info_detail(webapp_owner_id, [promotion])
# 				promotion.end_date = promotion.end_date.strftime('%Y-%m-%d %H:%M:%S')
# 				promotion.created_at = promotion.created_at.strftime('%Y-%m-%d %H:%M:%S')
# 				promotion.start_date = promotion.start_date.strftime('%Y-%m-%d %H:%M:%S')
# 				if promotion.promotion_title:
# 					product.promotion_title = promotion.promotion_title
# 				if promotion.type == promotion_models.PROMOTION_TYPE_PRICE_CUT:
# 					promotion.promotion_title = '满%s减%s' % (promotion.detail['price_threshold'], promotion.detail['cut_money'])
# 				elif promotion.type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
# 					promotion.promotion_title = '%s * %s' % (promotion.detail['premium_products'][0]['name'], promotion.detail['count'])
# 				elif promotion.type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
# 					promotion.promotion_title = '活动截止:%s' % (promotion.end_date)
# 				else:
# 					promotion.promotion_title = ''
# 				product.promotion = promotion.to_dict('detail', 'type_name')
# 			Product.fill_property_detail(webapp_owner_id, [product], '')
# 		except:
# 			if settings.DEBUG:
# 				raise
# 			else:
# 				#记录日志
# 				alert_message = u"获取商品记录失败,商品id: {} cause:\n{}".format(product_id, unicode_full_stack())
# 				watchdog_alert(alert_message, type='WEB')
# 				#返回"被删除"商品
# 				product = Product()
# 				product.is_deleted = True

# 		return {
# 			'value': product.to_dict('swipe_images_json', 'models', '_is_use_custom_model', 'product_model_properties', 'is_sellout', 'promotion', 'properties')
# 		}

# 	return inner_func


# def get_product_model_properties_for_cache(webapp_owner_id):
# 	def inner_func():
# 		properties = []
# 		user_profile = UserProfile.objects.filter(user_id=webapp_owner_id)
# 		if user_profile.count() == 1 and WeizoomMall.objects.filter(webapp_id=user_profile[0].webapp_id, is_active=True).count() == 1:
# 			properties = list(ProductModelProperty.objects.filter())
# 		else:
# 			properties = list(ProductModelProperty.objects.filter(owner_id=webapp_owner_id))
# 		id2property = {}
# 		property_ids = []
# 		for property in properties:
# 			id2property[property.id] = {"id":property.id, "name":property.name}
# 			property_ids.append(property.id)

# 		id2value = {}
# 		for property_value in ProductModelPropertyValue.objects.filter(property_id__in=property_ids):
# 			id2value[property_value.id] = {"id":property_value.id, "property_id":property_value.property_id, "name":property_value.name, "pic_url":property_value.pic_url}

# 		return {
# 			'value': {
# 				'id2property': id2property,
# 				'id2value': id2value
# 			}
# 		}

# 	return inner_func


# #################################################################################
# # get_mall_config_for_cache: 获取用于缓存的mall config数据
# #################################################################################
# def get_mall_config_for_cache(webapp_owner_id):
# 	def inner_func():
# 		mall_config = MallConfig.objects.get(owner_id=webapp_owner_id)
# 		return {
# 			'value': mall_config.to_dict()
# 		}

# 	return inner_func


# #############################################################################
# # get_product_details_with_model: 获得指定规格的商品详情
# #############################################################################
# def get_product_details_with_model(webapp_owner_id, webapp_user, product_infos):
# 	from cache import webapp_cache
# 	products = []
# 	for product_info in product_infos:
# 		product_id = product_info['id']
# 		product_model_name = product_info['model_name']
# 		product = webapp_cache.get_webapp_product_detail(webapp_owner_id, product_id)

# 		if product.is_deleted:
# 			products.append(product)
# 			continue

# 		#填充价格等基础信息
# 		has_found_model = False
# 		for model in product.models:
# 			if model['name'] == product_model_name:
# 				has_found_model = True
# 				product.price = model['price']
# 				product.weight = model['weight']
# 				product.stock_type = model['stock_type']
# 				product.stocks = model['stocks']
# 				product.model_name = product_model_name
# 				product.model = model
# 				product.is_model_deleted = False
# 				product.market_price = model['market_price']
# 				break

# 		if not has_found_model:
# 			product.is_model_deleted = True

# 		#填充规格属性信息
# 		if product.model_name != 'standard':
# 			product_model_properties = webapp_user.webapp_owner_info.mall_data['product_model_properties']
# 			id2property = product_model_properties['id2property']
# 			id2value = product_model_properties['id2value']
# 			#id2property, id2value = webapp_user.webapp_owner_info.mall_data['product_model_properties']#webapp_cache.get_webapp_product_model_properties(webapp_owner_id)
# 			result = {}
# 			property_ids = []
# 			property_value_ids = []

# 			for model_property_info in product.model_name.split('_'):
# 				property_id, property_value_id = model_property_info.split(':')	
# 				property_id = int(property_id)
# 				property_value_id = int(property_value_id)
# 				property_value_ids.append(property_value_id)
# 				#将商品规格中出现的model property放入result
# 				result[property_id] = id2property[property_id]

# 				for property_value_id in property_value_ids:
# 					property_value = id2value[property_value_id]
# 					property_id = property_value['property_id']
# 					result[property_id]['property_value'] = property_value['name']
# 					result[property_id]['property_pic_url'] = property_value['pic_url']
# 			product.custom_model_properties = result.values()
# 			product.custom_model_properties.sort(lambda x,y: cmp(x['id'], y['id']))
# 		else:
# 			product.custom_model_properties = None

# 		products.append(product)

# 	#填充商品库存信息
# 	id2product = dict([(product.id, product) for product in products])
# 	product_model_ids = [product.model['id'] for product in products if hasattr(product, 'model')]
# 	db_product_models = ProductModel.objects.filter(id__in=product_model_ids)
# 	for db_product_model in db_product_models:
# 		id2product[db_product_model.product_id].stocks = db_product_model.stocks

# 	return products


# #############################################################################
# # get_product_detail: 获取product详情
# #############################################################################
# def get_product_detail(webapp_owner_id, webapp_user, product_id):
# 	from cache import webapp_cache
# 	try:
# 		product = webapp_cache.get_webapp_product_detail(webapp_owner_id, product_id)
# 		if product.is_deleted:
# 			return product

# 		postage_configs = webapp_user.webapp_owner_info.mall_data['postage_configs']#webapp_cache.get_webapp_postage_configs(webapp_owner_id)
# 		if product.type != PRODUCT_INTEGRAL_TYPE:
# 			postage_config = filter(lambda c: c.id == product.postage_id, postage_configs)
# 		if product.type == PRODUCT_INTEGRAL_TYPE or len(postage_config) == 0:
# 			postage_config = filter(lambda c: c.is_system_level_config, postage_configs)
		
# 		if len(postage_config) > 0:
# 			postage_config = postage_config[0]
# 		else:
# 			print 'jz----ERROR: 没有运费配置。'
			

# 		#记录运费计算因子
# 		product.postage_factor = postage_config.factor

# 		#获取每个model的运费
# 		# product.postage_config = mall_util.get_postage_for_all_models(webapp_owner_id, product, postage_config)

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
# 					'display_price': _get_price_by_type(p_type, product_model['price']),
# 					'display_original_price': _get_price_by_type(p_type, product_model['original_price']),
# 					'display_market_price': _get_price_by_type(p_type, product_model['market_price']),
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
# 					price_range =  _get_price_by_type(p_type, prices[0])
# 				else:
# 					price_range = '%s-%s' % (_get_price_by_type(p_type, prices[0]), _get_price_by_type(p_type, prices[-1]))

# 				if market_prices[0] == market_prices[-1]:
# 					market_price_range = _get_price_by_type(p_type, market_prices[0])
# 				else:
# 					market_price_range = '%s-%s' % (_get_price_by_type(p_type, market_prices[0]), _get_price_by_type(p_type, market_prices[-1]))					
				
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
# 				'display_price': _get_price_by_type(p_type, standard_model['price']),
# 				'display_original_price': _get_price_by_type(p_type, standard_model['original_price']),
# 				'display_market_price': _get_price_by_type(p_type, standard_model['market_price']),
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
	
# def _get_price_by_type(p_type, price):
# 	if p_type == PRODUCT_INTEGRAL_TYPE:
# 		return int(price)
# 	else:
# 		return str("%.2f" % price)

# def create_order(webapp_owner_id, webapp_user, product):
# 	"""
# 	创建一个order

# 	下订单页面调用
# 	"""
# 	order = Order()
# 	if webapp_user.ship_info:
# 		ship_info = webapp_user.ship_info
# 		order.ship_name = ship_info.ship_name
# 		order.area = ship_info.area
# 		order.ship_address = ship_info.ship_address
# 		order.ship_tel = ship_info.ship_tel
# 		order.ship_id = ship_info.id

# 	# 积分订单
# 	if product.type == PRODUCT_INTEGRAL_TYPE:
# 		order.type = PRODUCT_INTEGRAL_TYPE

# 	#计算折扣
# 	product.original_price = product.price
# 	if product.type==PRODUCT_DEFAULT_TYPE:
# 		product.price, _ = webapp_user.get_discounted_money(product.price, product_type=product.type)
# 	order.products = [product]

# 	# 获取postage config
# 	postage_configs = webapp_user.webapp_owner_info.mall_data['postage_configs']
# 	if product.type == PRODUCT_INTEGRAL_TYPE:
# 		postage_config = filter(lambda c: c.is_system_level_config, postage_configs)[0]
# 	else:
# 		postage_config = filter(lambda c: c.is_used, postage_configs)[0]
# 	#获取重量，计算运费
# 	total_weight = (product.weight * product.purchase_count)	
# 	_, order.postage = mall_util.get_postage_for_weight(total_weight, postage_config)

# 	order.used = {
# 		'postage_config': postage_config
# 	}

# 	#支付方式
# 	order.pay_interfaces = __get_products_pay_interfaces(webapp_owner_id, order.products)
# 	return order


# #############################################################################
# # update_order_type_test: 修改订单的为测试订单，并且修改价钱
# #############################################################################
# def update_order_type_test(type, order):	
# 	if type == PRODUCT_TEST_TYPE:
# 		order.type = PRODUCT_TEST_TYPE
# 		order.final_price = 0.01
		
# 	return order


# ########################################################################
# # __create_random_order_id: 生成订单
# ########################################################################
# def __create_random_order_id():
# 	order_id = time.strftime("%Y%m%d%H%M%S", time.localtime())
# 	order_id = '%s%03d' % (order_id, random.randint(1, 999))
# 	if Order.objects.filter(order_id=order_id).count() > 0:
# 		return __create_random_order_id()
# 	else:
# 		return order_id

# ########################################################################
# # _get_province_id_by_area: 根据area：2_2_22 , 来获取省份id
# ########################################################################
# def _get_province_id_by_area(area):
# 	if area and len(area.split('_')):
# 		return area.split('_')[0]
# 	return 0

# def save_order(webapp_id, webapp_owner_id, webapp_user, order_info, request=None):
# 	"""
# 	保存订单
# 	"""
# 	order = Order()
# 	order.order_id = __create_random_order_id()
	
# 	order.buyer_name = order_info['buyer_name']
# 	order.buyer_tel = order_info['buyer_tel']
# 	order.ship_name = order_info['ship_name']
#  	order.ship_address = order_info['ship_address']
#  	order.ship_tel = order_info['ship_tel']
#  	order.status = ORDER_STATUS_NOT
# 	order.area = order_info['area']
#  	order.integral = order_info['integral']
#  	order.bill_type = order_info['bill_type']
#  	order.bill = order_info['bill']
#  	order.customer_message = order_info['customer_message']
#  	order.weizoom_card_money = order_info['weizoom_card_money']
#  	order.webapp_id = webapp_id
#  	order.webapp_user_id = webapp_user.id
#  	# liupeiyu by 21.0 测试订单
#  	order.type = order_info['type']

#  	products = order_info['products']

# 	#处理订单中的product总价
# 	order.product_price = sum([product.total_price for product in products])
# 	order.promotion_money = sum([product.promotion_money for product in products])

# 	# TODO 处理促销

# 	#计算会员等级折扣价
# 	order.member_grade_discounted_money, _ = webapp_user.get_discounted_money(order.product_price, product_type=order.type)
	
# 	#计算运费
# 	province_id = _get_province_id_by_area(order.area)
# 	order.postage = mall_util.get_postage_for_products(webapp_owner_id,
# 		webapp_user.webapp_owner_info.mall_data['postage_configs'], products, province_id)
# 	# postage 小于0是免运费 by liupeiyu
# 	if order.postage < 0:
# 		order.postage = 0
# 	postage = order.postage
	
# 	#
# 	#处理订单中的优惠券 
# 	# TODO: 将优惠券的判断放入request_api_util.py中
# 	#
# 	order.coupon_money = 0.0
# 	is_use_coupon = (request.POST.get('is_use_coupon', 'false') == 'true')
# 	if is_use_coupon:
# 		coupon_id = int(request.POST.get('coupon_id', 0))
# 		#TODO: 将这段代码改为更好理解
# 		if coupon_id == -1:
# 			coupon_id = 0
# 		coupon_coupon_id = request.POST.get('coupon_coupon_id', 0)
# 		#计算机商品和运费总和
# 		product_postage_total_price = order.member_grade_discounted_money + order.postage
# 		if coupon_id:
# 			coupon = webapp_user.use_coupon(coupon_id, product_postage_total_price)
# 		else:
# 			if request.member:
# 				member_id = request.member.id
# 			else:
# 				member_id = 0
# 			coupon = webapp_user.use_coupon_by_coupon_id(member_id, coupon_coupon_id, product_postage_total_price, request.webapp_owner_id)
		
# 		order.coupon_money = coupon.money
# 		order.coupon_id = coupon.id

# 	#计算订单总价
#  	order.integral_money = webapp_user.use_integral(order.integral)
#  	#add by bert at weizoom accounts 
#  	# if integral:
#  	if False:
#  		integral_strategy_settings = webapp_user.webapp_owner_info.integral_strategy_settings
#  		integral_each_yuan = integral_strategy_settings.integral_each_yuan
#  		if integral_each_yuan is None:
#  			integral_each_yuan = -1

# 	# liupeiyu by 21.0 测试订单修改金额
#  	elif order.type == PRODUCT_TEST_TYPE:
# 		order.final_price = float('%.2f' % (0.01 - order.coupon_money))
#  	else:
# 		order.final_price = float('%.2f' % (order.member_grade_discounted_money \
# 			+ order.postage - order.coupon_money - order.weizoom_card_money - order.promotion_money))
	
# 	if order.final_price < 0:
# 		#调整总价
# 		order.final_price = 0

# 	#待支付的积分商品，将final_price更改为0
# 	if order.type == PRODUCT_INTEGRAL_TYPE and order.status == ORDER_STATUS_NOT:
# 		order.final_price = 0

# 	#更新订单的各种价格信息
# 	order.save()

# 	#更新库存
# 	for product in products:
# 		product_model = product.model
# 		if product_model['stock_type'] == PRODUCT_STOCK_TYPE_LIMIT:
# 			ProductModel.objects.filter(id=product_model['id']).update(stocks = F('stocks') - product.purchase_count)

# 	#建立<order, product>的关系
# 	for product in products:
# 		product_discounted_money, _ = webapp_user.get_discounted_money(product.price, product_type=order.type)
# 		OrderHasProduct.objects.create(
# 			order = order, 
# 			product_id = product.id,
# 			product_model_name = product.model['name'],
# 			number = product.purchase_count, 
# 			total_price = product.total_price,
# 			price = product_discounted_money,
# 			promotion_id = product.promotion['id'] if hasattr(product, 'promotion') else 0,
# 			promotion_money = product.promotion_money,
# 		)
# 		#add by bert at 17.0
# 		WeizoomMallHasOtherMallProductOrder.create(webapp_id, product, order)


# 	if order.final_price == 0:
# 		# 优惠券或积分金额直接可支付完成，直接调用pay_order，完成支付
# 		pay_order(webapp_id, webapp_user, order.order_id, True, PAY_INTERFACE_PREFERENCE)
# 		# 支付后的操作
# 		mall_signals.post_pay_order.send(sender=Order, order=order, request=request)

# 	return order


# # 处理积分商品
# # def _integral_order_handle(order):
# # 	if order.type == PRODUCT_INTEGRAL_TYPE and order.status == ORDER_STATUS_NOT:
# # 		order.final_price = 0
# # 		order.save()
# # 	return order

# ########################################################################
# # get_order: 获取订单
# ########################################################################
# def get_order_by_id(order_id):
# 	try:
# 		return Order.objects.get(id=order_id)
# 	except:
# 		return None

# ########################################################################
# # get_order: 获取订单
# ########################################################################
# def get_order(webapp_user, order_id, should_fetch_product=False):
# 	order = Order.objects.get(order_id=order_id)
# 	try:
# 		order.area = regional_util.get_str_value_by_string_ids(order.area)
# 		order.display_express_company_name = express_util.get_name_by_value(order.express_company_name)
# 	except:
# 		pass

# 	if should_fetch_product:
# 		relations = list(OrderHasProduct.objects.filter(order=order))
# 		product_infos = []
# 		webapp_owner_id = webapp_user.webapp_owner_info.user_profile.user_id
# 		for relation in relations:
# 			product_infos.append({
# 				"id": relation.product_id,
# 				'model_name': relation.product_model_name
# 			})

# 		products = get_product_details_with_model(webapp_owner_id, webapp_user, product_infos)

# 		product2relation = dict([(relation.product_id, relation) for relation in relations])
# 		for product in products:
# 			product.ordered_count = relation.number
# 			product.price = relation.price

# 		# product_ids = [relation.product_id for relation in relations]
# 		# id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])

# 		# products = []
# 		# webapp_owner_id = webapp_user.webapp_owner_info.user_profile.user_id
# 		# product_infos = []
# 		# get_product_details_with_model()
# 		# for relation in relations:
# 		# 	product = copy.copy(id2product[relation.product_id])
# 		# 	model_name = relation.product_model_name
# 		# 	if not model_name:
# 		# 		model_name = 'standard'
# 		# 	product.fill_specific_model(model_name)
# 		# 	product.original_price = product.price
# 		# 	product.price = relation.price
# 		# 	product.ordered_count = relation.number
# 		# 	products.append(product)
# 		order.products = products

# 	return order


# ########################################################################
# # get_orders: 获取webapp user的订单列表
# ########################################################################
# def get_orders(webapp_user, type):
# 	if type == 0:
# 		orders = Order.objects.filter(webapp_user_id=webapp_user.id).order_by('-id')
# 	else:
# 		orders = Order.objects.filter(webapp_user_id=webapp_user.id, status=ORDER_STATUS_NOT).order_by('-id')

# 	order_ids = [order.id for order in orders]
# 	order2count = {}
# 	for order_product_relation in OrderHasProduct.objects.filter(order_id__in=order_ids):
# 		order_id = order_product_relation.order_id
# 		old_count = 0
# 		if order_id in order2count:
# 			old_count = order2count[order_id]
# 		order2count[order_id] = old_count + order_product_relation.number

# 	for order in orders:
# 		order.product_count = order2count.get(order.id, 0)

# 	return orders


# ########################################################################
# # pay_order: 支付订单
# ########################################################################
# def pay_order(webapp_id, webapp_user, order_id, is_success, pay_interface_type):
# 	try:
# 		order = get_order(webapp_user, order_id, True)
# 	except:
# 		watchdog_fatal(u"本地获取订单信息失败：order_id:{}, cause:\n{}".format(order_id, unicode_full_stack()))
# 		return None, False
		
# 	pay_result = False
	
# 	if is_success and order.status == ORDER_STATUS_NOT: #支付成功
# 		#order.status = ORDER_STATUS_PAYED_SUCCESSED
# 		order.status = ORDER_STATUS_PAYED_NOT_SHIP
# 		pay_result = True
# 		Order.objects.filter(order_id=order_id).update(status=ORDER_STATUS_PAYED_NOT_SHIP, pay_interface_type=pay_interface_type, payment_time=datetime.now())

# 		#记录日志
# 		record_operation_log(order_id, u'客户', u'支付')
# 		record_status_log(order_id, u'客户', ORDER_STATUS_NOT, ORDER_STATUS_PAYED_NOT_SHIP)

# 		#记录购买统计项
# 		PurchaseDailyStatistics.objects.create(
# 			webapp_id = webapp_id,
# 			webapp_user_id = webapp_user.id,
# 			order_id = order_id,
# 			order_price = order.final_price,
# 			date = dateutil.get_today()
# 		)

# 		#更新webapp_user的has_purchased字段
# 		webapp_user.set_purchased()
	
# 		try:
# 			mall_util.email_order(order=order)
# 		except:
# 			notify_message = u"订单状态为已付款时发邮件失败，order_id={}, webapp_id={}, cause:\n{}".format(order_id, webapp_id, unicode_full_stack())
# 			watchdog_alert(notify_message)
# 		# 重新查询订单
# 		order = get_order(webapp_user, order_id, True)
# 	return order, pay_result


# ########################################################################
# # 进行订单的发货处理：
# # 	order_id: 需要处理的订单号
# #	express_company_name：快递公司名称
# # 	express_number: 货运单号
# #   leader_name: 负责人
# #   is_update_express: 为True时，只修改物流信息，不改变订单状态
# #
# # 处理操作流程：
# # 1. 修改订单的状态为“已发货”
# # 2. 修改订单记录，添加运单号和快递公司信息
# # 3. 增加订单操作记录信息
# # 4. 增加状态更改记录信息
# #
# # 如果对应订单不存在，或者操作失败直接返回False
# # 整个操作过程中如果其中有一个步骤失败则继续之后的操作
# # 但是会进行预警处理，以便人工进行相应操作
# #
# # 如果订单id、快递公司名称或运单号任一为None，直接返回False
# ########################################################################
# def ship_order(order_id, express_company_name, 
# 	express_number, operator_name=u'我', leader_name=u'', is_update_express=False):
# 	if (order_id is None) or (express_company_name is None) or (express_number is None):
# 		return False
# 	target_status = ORDER_STATUS_PAYED_SHIPED

# 	try:
# 		# 需要修改的基本参数
# 		# 只修改物流信息，不修改状态
# 		order_params = dict()
# 		order_params['express_company_name'] = express_company_name
# 		order_params['express_number'] = express_number
# 		order_params['leader_name'] = leader_name

# 		order_has_delivery_params = dict()
# 		order_has_delivery_params['express_company_name'] = express_company_name
# 		order_has_delivery_params['express_number'] = express_number
# 		order_has_delivery_params['leader_name'] = leader_name

# 		order_has_delivery_id = 0
# 		order = Order.objects.get(id=order_id)

# 		# 即修改物流信息，也修改状态, 需要加上状态条件
# 		if not is_update_express:
# 			order_params['status'] = target_status			
# 			if order.type == PRODUCT_DELIVERY_PLAN_TYPE:
# 				order_has_delivery_times = OrderHasDeliveryTime.objects.filter(order=order, status=UNSHIPED).order_by('delivery_date')
# 				if order_has_delivery_times.count() > 0:
# 					order_has_delivery_id = order_has_delivery_times[0].id
# 					order_has_delivery_params['status'] = SHIPED
# 		else:
# 			if order.type == PRODUCT_DELIVERY_PLAN_TYPE:
# 				order_has_delivery_times = OrderHasDeliveryTime.objects.filter(order=order, status=SHIPED).order_by('-delivery_date')
# 				if order_has_delivery_times.count() > 0:
# 					order_has_delivery_id = order_has_delivery_times[0].id
# 					order_has_delivery_params['status'] = order_has_delivery_times[0].status

# 		OrderHasDeliveryTime.objects.filter(id=order_has_delivery_id).update(**order_has_delivery_params)
# 		Order.objects.filter(id=order_id).update(**order_params)

# 		#发送模板消息
# 		# current_final_price = order.final_price
# 		# if order.type == PRODUCT_INTEGRAL_TYPE:
# 		# 	order.final_price = 0
# 		try:
# 			if express_company_name and express_number:
# 				order.express_company_name = express_company_name
# 				order.express_number = express_number
# 				order.leader_name = leader_name
				
# 				template_message_api.send_order_template_message(order.webapp_id, order.id, template_message_model.PAY_DELIVER_NOTIFY)
# 		except:
# 			alert_message = u"ship_order 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
# 			watchdog_warning(alert_message)
# 		#order.final_price = current_final_price
# 	except:
# 		error_msg = u"更改订单({})状态信息失败，cause:\n{}".format(order_id, unicode_full_stack())
# 		watchdog_error(error_msg)

# 		return False	

# 	# 记录log信息
# 	if is_update_express:
# 		action = u'修改发货信息'
# 	else:
# 		action = u'订单发货'
# 		record_status_log(order.order_id, operator_name, order.status, target_status)

# 	record_operation_log(order.order_id, operator_name, action)

# 	#send post_ship_order signal
# 	signals.post_ship_order.send(sender=Order, order=order)

# 	try:
# 		mall_util.email_order(order=Order.objects.get(id=order_id))
# 	except:
# 		notify_message = u"订单状态为已发货时发邮件失败，order_id:{}，cause:\n{}".format(order_id, unicode_full_stack())
# 		watchdog_alert(notify_message)
# 	return True


# ########################################################################
# # add_product_to_shopping_cart: 向购物车中添加商品
# ########################################################################
# def add_product_to_shopping_cart(webapp_user, product_id, product_model_name, count):
# 	try:
# 		shopping_cart_item = ShoppingCart.objects.get(
# 			webapp_user_id = webapp_user.id, 
# 			product_id = product_id,
# 			product_model_name = product_model_name
# 		)
# 		shopping_cart_item.count = shopping_cart_item.count + count
# 		shopping_cart_item.save()
# 	except:
# 		shopping_cart_item = ShoppingCart.objects.create(
# 			webapp_user_id = webapp_user.id,
# 			product_id = product_id,
# 			product_model_name = product_model_name,
# 			count = count
# 		)


# ########################################################################
# # remove_product_from_shopping_cart: 从购物车中删除商品
# ########################################################################
# def remove_product_from_shopping_cart(webapp_user, product_id, product_model_name='standard'):
# 	ShoppingCart.objects.filter(product_id=product_id, webapp_user_id=webapp_user.id, product_model_name=product_model_name).delete()


# ########################################################################
# # remove_shopping_cart_items: 从购物车中删除商品
# ########################################################################
# def remove_shopping_cart_items(webapp_user, shopping_cart_item_ids):
# 	ShoppingCart.objects.filter(id__in=shopping_cart_item_ids).delete()


# ########################################################################
# # update_shopping_cart: 更新购物车
# ########################################################################
# def update_shopping_cart(webapp_user, update_info):
# 	for item_id, count in update_info.items():
# 		ShoppingCart.objects.filter(id=item_id).update(count=count)


# ########################################################################
# # clear_shopping_cart_invalid_products: 清空购物车中的无效商品
# ########################################################################
# def clear_shopping_cart_invalid_products(webapp_user, shopping_cart_item_ids):
# 	ShoppingCart.objects.filter(id__in=shopping_cart_item_ids).delete()


# ########################################################################
# # remove_product_from_all_shopping_cart: 从所有购物车中删除商品
# ########################################################################
# def remove_product_from_all_shopping_cart(product_id):
# 	ShoppingCart.objects.filter(product_id=product_id).delete()


# ########################################################################
# # get_shopping_cart_products: 获取购物车中的product集合
# ########################################################################
# def get_shopping_cart_products(webapp_user, webapp_owner_id):
# 	from cache import webapp_cache
# 	shopping_cart_items = list(ShoppingCart.objects.filter(webapp_user_id=webapp_user.id))

# 	product_ids = [item.product_id for item in shopping_cart_items]
# 	id2product = dict()
# 	for product_id in product_ids:
# 		id2product[product_id] = webapp_cache.get_webapp_product_detail(webapp_owner_id, product_id)
# 	# id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])

# 	products = []
# 	invalid_products = []
# 	for shopping_cart_item in shopping_cart_items:
# 		product = copy.copy(id2product[shopping_cart_item.product_id])
# 		product.fill_specific_model(shopping_cart_item.product_model_name)
# 		product.count = shopping_cart_item.count
# 		product.shopping_cart_id = shopping_cart_item.id
# 		product.original_price = product.price

# 		if product.shelve_type == PRODUCT_SHELVE_TYPE_OFF or \
# 			product.is_deleted or \
# 			(product.stock_type == PRODUCT_STOCK_TYPE_LIMIT and product.stocks == 0) or\
# 			product.is_model_deleted or\
# 			(shopping_cart_item.product_model_name == 'standard' and product.is_use_custom_model):
# 			invalid_products.append(product)
# 		else:
# 			product.price, _ = webapp_user.get_discounted_money(product.price)
# 			products.append(product)

# 	invalid_products.sort(lambda x,y: cmp(x.shopping_cart_id, y.shopping_cart_id))

# 	return products, invalid_products


# #############################################################################
# # create_shopping_cart_order: 创建一个基于购物车的order
# #############################################################################
# def create_shopping_cart_order(webapp_owner_id, webapp_user, products):
# 	order = Order()
# 	#获取收货人信息
# 	if webapp_user.ship_info:
# 		ship_info = webapp_user.ship_info
# 		order.ship_name = ship_info.ship_name
# 		order.area = ship_info.area
# 		order.ship_address = ship_info.ship_address
# 		order.ship_tel = ship_info.ship_tel
# 		order.ship_id = ship_info.id

# 	#在购物车页面，可能更改了商品数量，这里更新购物车中商品的数量	
# 	for product in products:
# 		ShoppingCart.objects.filter(webapp_user_id=webapp_user.id, product_id=product.id).update(count=product.purchase_count)

# 	#计算订单商品总重量的运费
# 	total_weight = 0.0;
# 	for product in products:
# 		product.original_price = product.price
# 		product.price, _ = webapp_user.get_discounted_money(product.price)
# 		# 有运费商品
# 		if product.postage_id > 0:
# 			total_weight += float(product.purchase_count) * float(product.weight)
		
# 	'''
# 	# 运费临时使用，测试
# 	'''
# 	postage_config, order.postage = None, 0
# 	# postage_config, order.postage = mall_util.get_postage_for_weight(webapp_owner_id, total_weight)
# 	order.products = products

# 	# 支付方式
# 	order.pay_interfaces = __get_products_pay_interfaces(webapp_owner_id, order.products)

# 	return order


# ########################################################################
# # get_order_operation_logs: 获得订单的操作日志
# ########################################################################
# def get_order_operation_logs(order_id):
# 	return OrderOperationLog.objects.filter(order_id=order_id)


# ########################################################################
# # record_status_log: 记录订单的操作日志
# ########################################################################
# def record_operation_log(order_id, operator_name, action):
# 	try:
# 		OrderOperationLog.objects.create(order_id=order_id, action=action, operator=operator_name)	
# 	except:
# 		error_msg = u"增加订单({})发货操作记录失败, cause:\n{}".format(order_id, unicode_full_stack())
# 		watchdog_error(error_msg)
# 	# 修改订单修改时间
# 	update_order_time(order_id)

# ########################################################################
# # get_order_status_logs: 获得订单的状态日志
# ########################################################################
# def get_order_status_logs(order_id):
# 	return OrderStatusLog.objects.filter(order_id=order_id)


# ########################################################################
# # record_status_log: 记录订单的状态日志
# ########################################################################
# def record_status_log(order_id, operator_name, from_status, to_status):
# 	try:
# 		OrderStatusLog.objects.create(
# 			order_id = order_id, 
# 			from_status = from_status, 
# 			to_status = to_status, 
# 			operator = operator_name
# 		)	
# 	except:
# 		error_msg = u"增加订单({})状态更改记录失败, cause:\n{}".format(order_id, unicode_full_stack())
# 		watchdog_error(error_msg)


# ########################################################################
# # update_order_time: 更新订单修改时间
# ########################################################################
# def update_order_time(order_id):
# 	try:
# 		Order.objects.filter(order_id=order_id).update(update_at=datetime.now())	
# 	except:
# 		error_msg = u"更新订单({})修改时间记录失败, cause:\n{}".format(order_id, unicode_full_stack())
# 		watchdog_error(error_msg)


# def get_unread_order_count(webapp_owner_id):
# 	"""
# 	获得未读订单数量

# 	@TODO 与'models.increase_unread_order()'合并到一个程序里面
# 	"""
# 	try:
# 		count = MallCounter.objects.get(owner_id=webapp_owner_id).unread_order_count
# 	except:
# 		watchdog_debug("failed to get MallCounter via owner_id={}".format(webapp_owner_id))
# 		count = 0
# 	return count


# ########################################################################
# # get_order_usable_integral: 获得订单中用户可以使用的积分
# ########################################################################
# def get_order_usable_integral(order, integral_info):
# 	user_integral = 0
# 	order_integral = 0
# 	total_money = sum([product.price*product.purchase_count for product in order.products])
# 	user_integral = integral_info['count']
# 	usable_integral_percentage_in_order = integral_info['usable_integral_percentage_in_order']
# 	count_per_yuan = integral_info['count_per_yuan']
# 	if usable_integral_percentage_in_order:
# 		pass
# 	else:
# 		usable_integral_percentage_in_order = 0
# 	if count_per_yuan:
# 		pass
# 	else:
# 		count_per_yuan = 0

# 	# 加上运费的价格 by liupeiyu
# 	if hasattr(order, 'postage'):
# 		total_money = total_money + order.postage

# 	order_integral = math.ceil(total_money*usable_integral_percentage_in_order*count_per_yuan/100.0)

# 	if user_integral > order_integral:
# 		return int(order_integral)
# 	else:
# 		return int(user_integral)


# ########################################################################
# # get_order_products: 获得订单中的商品集合
# ########################################################################
# def get_order_products(order_id):
# 	relations = list(OrderHasProduct.objects.filter(order_id=order_id))
# 	product_ids = [r.product_id for r in relations]
# 	id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])

# 	products = []
# 	for relation in OrderHasProduct.objects.filter(order_id=order_id):
# 		product = copy.copy(id2product[relation.product_id])
# 		product.fill_specific_model(relation.product_model_name)
# 		products.append({
# 			'id' : relation.product_id,
# 			'name': product.name,
# 			'thumbnails_url': product.thumbnails_url,
# 			'count': relation.number,
# 			'total_price': '%.2f' % relation.total_price,
# 			'price': '%.2f' % relation.price,
# 			'custom_model_properties': product.custom_model_properties,
# 			'is_deleted': product.is_deleted
# 		})

# 	return products

# ###################################################################################
# # get_weizoom_mall_partner_products: 获取该微众商城下的合作商家加入到微众商城的商品
# ###################################################################################
# def get_weizoom_mall_partner_products_and_ids(webapp_id):
# 	return _get_weizoom_mall_partner_products_and_ids_by(webapp_id)

# def get_verified_weizoom_mall_partner_products_and_ids(webapp_id):
# 	return _get_weizoom_mall_partner_products_and_ids_by(webapp_id, True)

# def get_not_verified_weizoom_mall_partner_products_and_ids(webapp_id):
# 	return _get_weizoom_mall_partner_products_and_ids_by(webapp_id, False)

# def _get_weizoom_mall_partner_products_and_ids_by(webapp_id, is_checked=None):
# 	if WeizoomMall.objects.filter(webapp_id=webapp_id).count() > 0:
# 		weizoom_mall = WeizoomMall.objects.filter(webapp_id=webapp_id)[0]

# 		product_ids = []
# 		product_check_dict = dict()
# 		other_mall_products = WeizoomMallHasOtherMallProduct.objects.filter(weizoom_mall=weizoom_mall)
# 		if is_checked != None:
# 			 other_mall_products.filter(is_checked=is_checked)

# 		for other_mall_product in other_mall_products:
# 			product_check_dict[other_mall_product.product_id] = other_mall_product.is_checked
# 			product_ids.append(other_mall_product.product_id)

# 		products = Product.objects.filter(id__in=product_ids, shelve_type=PRODUCT_SHELVE_TYPE_ON, is_deleted=False)

# 		for product in products:
# 			product.is_checked = product_check_dict[product.id]

# 		return products, product_ids
# 	else:
# 		return None, None

# def has_other_mall_product(webapp_id):
# 	return WeizoomMallHasOtherMallProduct.objects.filter(weizoom_mall__webapp_id=webapp_id).count() > 0

# def get_product_ids_in_weizoom_mall(webapp_id):
# 	return [weizoom_mall_other_mall_product.product_id for weizoom_mall_other_mall_product in WeizoomMallHasOtherMallProduct.objects.filter(webapp_id=webapp_id)]

# ########################################################################
# # update_order_status: 修改订单状态
# ########################################################################
# def update_order_status(user, action, order, request=None):	
# 	order_id = order.id
# 	operation_name = user.username
# 	if action == 'pay':
# 		target_status = ORDER_STATUS_PAYED_NOT_SHIP

# 		#记录购买统计项
# 		PurchaseDailyStatistics.objects.create(
# 			webapp_id = order.webapp_id,
# 			webapp_user_id = order.webapp_user_id,
# 			order_id = order.order_id,
# 			order_price = order.final_price,
# 			date = dateutil.get_today()
# 		)
# 	elif action == 'ship':
# 		target_status = ORDER_STATUS_PAYED_SHIPED
# 	elif action == 'finish':
# 		target_status = ORDER_STATUS_SUCCESSED
# 	elif 'cancel' in action:
# 		actions = action.split('-')
# 		operation_name = u'{} {}'.format(operation_name, (actions[1] if len(actions) > 1 else ''))
# 		target_status = ORDER_STATUS_CANCEL
# 		# 返回订单使用的积分
# 		if order.integral:
# 			from modules.member.models import WebAppUser
# 			from modules.member.integral import increase_member_integral
# 			member = WebAppUser.get_member_by_webapp_user_id(order.webapp_user_id)
# 			increase_member_integral(member, order.integral, u'取消订单回收积分')
# 		# 返回订单使用的优惠劵
# 		if order.coupon_id:
# 			from market_tools.tools.coupon.util import restore_coupon
# 			restore_coupon(order.coupon_id)
# 		# 返回商品的数量
# 		restore_product_count_by_order_id(order)
# 		mall_signals.cancel_order.send(sender=Order, order=order)
# 	else:
# 		target_status = None
# 	expired_status = order.status
# 	if target_status:
# 		if 'cancel' in action and request:
# 			Order.objects.filter(id=order_id).update(status=target_status, reason=request.GET.get('reason', ''))
# 		else:
# 			Order.objects.filter(id=order_id).update(status=target_status)
# 		operate_log = u' 修改状态'
# 		record_status_log(order.order_id, operation_name, order.status, target_status)

# 	try:
# 		if expired_status < ORDER_STATUS_SUCCESSED and int(target_status) == ORDER_STATUS_SUCCESSED and expired_status != ORDER_STATUS_CANCEL:
# 			integral.increase_father_member_integral_by_child_member_buyed(order.webapp_user_id, order.webapp_id)
# 			integral.increase_detail_integral(order.webapp_user_id, order.webapp_id, order.final_price)
# 	except:
# 		notify_message = u"订单状态为已完成时为贡献者增加积分，cause:\n{}".format(unicode_full_stack())
# 		watchdog_error(notify_message)
# 	try:
# 		mall_util.email_order(order=Order.objects.get(id=order_id))
# 	except :
# 		notify_message = u"订单状态改变时发邮件失败，cause:\n{}".format(unicode_full_stack())
# 		watchdog_alert(notify_message)


# ########################################################################
# # restore_product_count_by_order_id: 返回商品的数量
# ########################################################################
# def restore_product_count_by_order_id(order):
# 	order_has_products = OrderHasProduct.objects.filter(order_id=order.id)
# 	for order_has_product in order_has_products:
# 		models = ProductModel.objects.filter(product_id=order_has_product.product.id, name=order_has_product.product_model_name)
# 		# 该商品有此规格，并且库存是有限，进入修改商品的数量
# 		if models.count() > 0 and models[0].stock_type == PRODUCT_STOCK_TYPE_LIMIT:
# 			product_model = models[0]
# 			product_model.stocks = product_model.stocks + order_has_product.number
# 			product_model.save()			


# ########################################################################
# # get_order_fitlers_by_user: 获取该用户的所有订单筛选
# ########################################################################
# def get_order_fitlers_by_user(user):
# 	data_filters = UserHasOrderFilter.objects.filter(owner=user).order_by('created_at')
# 	filters = []
# 	for data_filter in data_filters:
# 		filters.append({
# 			'id' : data_filter.id,
# 			'name': data_filter.filter_name,
# 			'value': data_filter.filter_value
# 		})

# 	return filters


# ########################################################################
# # get_pay_interfaces_by_user: 获取该用户的所有的支付方式
# ########################################################################
# def get_pay_interfaces_by_user(user):
# 	existed_pay_interfaces = []
# 	pay_interfaces = PayInterface.objects.filter(owner=user)
# 	for pay_interface in pay_interfaces:
# 		if pay_interface.type == PAY_INTERFACE_ALIPAY:
# 			existed_pay_interfaces.append({'pay_name':u'支付宝','data_value':PAY_INTERFACE_ALIPAY})
# 		if pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
# 			existed_pay_interfaces.append({'pay_name':u'微信支付','data_value':PAY_INTERFACE_WEIXIN_PAY})
# 		if pay_interface.type == PAY_INTERFACE_COD:
# 			existed_pay_interfaces.append({'pay_name':u'货到付款','data_value':PAY_INTERFACE_COD})
# 		if pay_interface.type == PAY_INTERFACE_WEIZOOM_COIN:
# 			existed_pay_interfaces.append({'pay_name':u'微众卡支付','data_value':PAY_INTERFACE_WEIZOOM_COIN})

# 	return existed_pay_interfaces


# ########################################################################
# # get_products_by_ids: 根据ids获取product集合
# ########################################################################
# def get_products_by_ids(ids):
# 	return list(Product.objects.filter(id__in=ids))


# def get_order_status_text(status):
# 	return STATUS2TEXT[status]


# ########################################################################
# # get_order_list: 获取订单列表
# ########################################################################
# DEFAULT_CREATE_TIME = '2000-01-01 00:00:00'

# DATA_UPDATE_TYPE = "update_time"
# DATA_CREATED_TYPE = "created_time"
# def get_order_list(user, query_dict, filter_value, sort_attr, query_string, count_per_page=15, cur_page=1, date_interval=None,
# 	date_type=None):
# 	webapp_id = user.get_profile().webapp_id	
# 	orders = Order.objects.belong_to(webapp_id)
# 	# 统计订单总数
# 	order_total_count = _get_orders_total_count(orders)
# 	###################################################	
# 	#处理搜索
# 	if len(query_dict):
# 		orders = orders.filter(**query_dict)
# 	###################################################	
# 	# 处理筛选条件
# 	source = None
# 	if filter_value and (filter_value != '-1'):
# 		params, source_value = UserHasOrderFilter.get_filter_params_by_value(filter_value)
# 		orders = orders.filter(**params)
# 		if source_value == 1:
# 			source = 'weizoom_mall'
# 		elif source_value == 0:
# 			source = 'mine_mall'

# 	###################################################
# 	if user.is_weizoom_mall:
# 		weizoom_mall_order_ids = WeizoomMallHasOtherMallProductOrder.get_orders_weizoom_mall_for_other_mall(webapp_id)
# 	else:
# 		weizoom_mall_order_ids = WeizoomMallHasOtherMallProductOrder.get_order_ids_for(webapp_id)
# 	order_id_list = []
# 	if source:
# 		for order in orders:
# 			if weizoom_mall_order_ids:
# 				if order.order_id in weizoom_mall_order_ids:
# 					if user.is_weizoom_mall:
# 						order.come = 'weizoom_mall'
# 					else:
# 						order.come = 'weizoom_mall'
# 				else:
# 					order.come = 'mine_mall'	
# 			else:
# 				order.come = 'mine_mall'
# 			if source and order.come != source:
# 				continue

# 			order_id_list.append(order.id)

# 	if source:
# 		orders = orders.filter(id__in=order_id_list)

# 	###################################################
# 	#处理 时间区间筛选
# 	if date_interval:		
# 		start_time = date_interval[0]
# 		end_time = date_interval[1]
# 		if date_type == "update_at":
# 			orders = orders.filter(update_at__gte=start_time, update_at__lt=end_time)
# 		else:
# 			orders = orders.filter(created_at__gte=start_time, created_at__lt=end_time)
# 	###################################################
# 	#处理排序
# 	if sort_attr != 'created_at':
# 		orders = orders.order_by(sort_attr)	
# 	###################################################
# 	if count_per_page > 0:
# 		#进行分页
# 		pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page, query_string=query_string)
# 	else:
# 		#全部订单
# 		pageinfo = {"object_count": orders.count()}
	
# 	#获取order对应的会员
# 	webapp_user_ids = set([order.webapp_user_id for order in orders])
# 	webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

# 	#获得order对应的商品数量
# 	order_ids = [order.id for order in orders]

# 	order2productcount = {}
# 	for relation in OrderHasProduct.objects.filter(order_id__in=order_ids):
# 		order_id = relation.order_id
# 		if order_id in order2productcount:
# 			order2productcount[order_id] = order2productcount[order_id] + 1
# 		else:
# 			order2productcount[order_id] = 1

# 	#构造返回的order数据
# 	items = []
# 	for order in  orders:
# 		#获取order对应的member的显示名
# 		member = webappuser2member.get(order.webapp_user_id, None)
# 		if member:
# 			order.buyer_name = member.username_for_html
# 			order.member_id = member.id
# 		else:
# 			order.buyer_name = u'未知'
# 			order.member_id = 0

# 		payment_time = None

# 		if order.payment_time is None:
# 			payment_time = ''
# 		elif datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M:%S') == DEFAULT_CREATE_TIME:
# 			payment_time = ''
# 		else:
# 			payment_time = datetime.strftime(order.payment_time, '%m-%d %H:%M')

# 		if weizoom_mall_order_ids:
# 			if order.order_id in weizoom_mall_order_ids:
# 				if user.is_weizoom_mall:
# 					order.come = 'weizoom_mall'
# 				else:
# 					order.come = 'weizoom_mall'
# 			else:
# 				order.come = 'mine_mall'	
# 		else:
# 			order.come = 'mine_mall'

# 		order.status_text = get_order_status_text(order.status)
# 		order.product_count = order2productcount.get(order.id, 0)
# 		order.payment_time = payment_time
# 		order.pay_interface_type_text = PAYTYPE2NAME.get(order.pay_interface_type, u'')

# 		if source and order.come != source:
# 			continue

# 		# liupeiyu 该订单中的会员是否可点击
# 		# 来自本店的订单,会员不可点击
# 		# 或者改用户是 微众商城，会员都可点击
# 		if order.come is 'weizoom_mall' and user.is_weizoom_mall is False:
# 			order.member_id = 0

# 		order_id_list.append(order.id)

# 	return orders, pageinfo, order_total_count


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


# ########################################################################
# # get_order_by_order_id: 根据订单号获取订单信息
# ########################################################################
# def get_order_by_order_id(order_id):
# 	try:
# 		order = Order.objects.get(order_id=order_id)
# 	except:
# 		return None	

# 	order_has_products = OrderHasProduct.objects.filter(order=order)
	
# 	number = 0
# 	for order_has_product in order_has_products:
# 		number += order_has_product.number
# 	order.number = number

# 	#处理订单关联的优惠券
# 	order.coupon =  order.get_coupon()
# 	order.products = get_order_products(order.id)

# 	logs = get_order_operation_logs(order.order_id)

# 	if logs.count() > 0:
# 		order.update_at = logs[0].created_at
# 	else:
# 		order.update_at = order.created_at

# 	return order


# ########################################################################
# # update_order_express_info: 更新订单物流信息
# ########################################################################
# def update_order_express_info(order_id, express_company_name, express_id):
# 	Order.objects.filter(order_id=order_id).update(express_company_name=express_company_name, express_number=express_id)


# ########################################################################
# # update_product_stock: 更新商品库存信息
# ########################################################################
# def update_product_stock(product_id, product_model_id, stock):
# 	if stock == -1:
# 		ProductModel.objects.filter(product_id=product_id, id=product_model_id).update(stock_type=PRODUCT_STOCK_TYPE_UNLIMIT, stocks=-1)
# 	else:
# 		ProductModel.objects.filter(product_id=product_id, id=product_model_id).update(stock_type=PRODUCT_STOCK_TYPE_LIMIT, stocks=stock)


# ########################################################################
# # batch_handle_order: 批量发货
# ########################################################################
# def batch_handle_order(json_data, user):
# 	error_data = []
# 	success_data = []
# 	for item in json_data:
# 		try:
# 			order_id = item.get('order_id', '')
# 			express_company_name = item.get('express_company_name', '')
# 			express_number = item.get('express_number', '')
# 			express_company_value = express_util.get_value_by_name(express_company_name)
# 			# 快递公司 不符
# 			if express_company_value == express_company_name:
# 				error_data.append(item)
# 				continue
# 			order = Order.objects.get(order_id=order_id.strip())
# 			if order.status == ORDER_STATUS_PAYED_NOT_SHIP:
# 				ship_order(order.id, express_company_value, express_number, user.username, u'')
# 				success_data.append(item)
# 		except:
# 			error_data.append(item)			
# 			alert_message = u"batch_handle_order批量发货 格式不正确, item:{}, cause:\n{}".format(item, unicode_full_stack())
# 			watchdog_warning(alert_message)

# 	return success_data, error_data


# ########################################################################
# # get_default_postage_by_owner_id: 获取默认运费
# ########################################################################
# def get_default_postage_by_owner_id(owner_id):
# 	try:
# 		return PostageConfig.objects.get(owner_id=owner_id, is_used=True, is_system_level_config=False)
# 	except:
# 		None


# ########################################################################
# # get_order_pay_interfaces: 获取该订单的支付方式
# ########################################################################
# def get_order_pay_interfaces(webapp_owner_id, order_id):
# 	products = [h.product for h in OrderHasProduct.objects.filter(order_id=order_id)]
# 	return __get_products_pay_interfaces(webapp_owner_id, products)


# ########################################################################
# # __get_products_pay_interfaces: 获取商品的共同支付方式
# ########################################################################
# from market_tools.tools.weizoom_card.models import AccountHasWeizoomCardPermissions
# def __get_products_pay_interfaces(webapp_owner_id, products):
# 	# 没有微众卡权限的，不能使用微众卡支付
# 	is_can_use_weizoom_card = AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(webapp_owner_id)	
# 	if is_can_use_weizoom_card is False:
# 		pay_interfaces = PayInterface.objects.filter(owner_id=webapp_owner_id, is_active=True).filter(~Q(type=PAY_INTERFACE_WEIZOOM_COIN))
# 	else:
# 		pay_interfaces = PayInterface.objects.filter(owner_id=webapp_owner_id, is_active=True)
		
# 	types = [p.type for p in pay_interfaces]

# 	# 如果不包含货到付款，直接返回所有的在线支付
# 	if PAY_INTERFACE_COD not in types:
# 		return pay_interfaces

# 	# 商品中是 货到付款方式 
# 	pay_interface_cod_count = 0
# 	for product in products:
# 		if product.is_use_cod_pay_interface:
# 			pay_interface_cod_count = pay_interface_cod_count + 1

# 	if pay_interface_cod_count == len(list(products)):
# 		return pay_interfaces
# 	else:
# 		return pay_interfaces.filter(type__in = ONLINE_PAY_INTERFACE)


# ########################################################################
# # get_pay_interface_onlines_by_owner_id: 获取在线支付方式
# ########################################################################
# def get_pay_interface_onlines_by_owner_id(owner_id):
# 	try:
# 		return PayInterface.objects.filter(owner_id=owner_id, is_active=True, type__in=ONLINE_PAY_INTERFACE)
# 	except:
# 		None


# ########################################################################
# # get_pay_interface_cod_by_owner_id: 获取货到付款支付方式
# ########################################################################
# def get_pay_interface_cod_by_owner_id(owner_id):
# 	try:
# 		return PayInterface.objects.get(owner_id=owner_id, is_active=True, type=PAY_INTERFACE_COD)
# 	except:
# 		None


# ########################################################################
# # update_products_postage: 修改运费
# ########################################################################
# def update_products_postage(owner_id, postage_id):	
# 	# 该id是否为 免运费
# 	try:
# 		is_system_level_config = PostageConfig.objects.get(id=postage_id).is_system_level_config
# 	except:
# 		is_system_level_config = True
	
# 	# id 大于0 并且 不是免运费
# 	if postage_id > 0 and is_system_level_config == False:
# 		# 更换邮费
# 		Product.objects.filter(owner_id=owner_id).exclude(postage_id=-1).update(postage_id=postage_id)
# 	else:
# 		# 修改为免运费
# 		Product.objects.filter(owner_id=owner_id).update(postage_id=-1)


# ########################################################################
# # update_products_pay_interface_cod: 修改商品不使用货到付款
# ########################################################################
# def update_products_pay_interface_cod(owner_id):
# 	Product.objects.filter(owner_id=owner_id).update(is_use_cod_pay_interface=False)


# #############################################################################
# # get_postage_configs_for_cache: 获得用于缓存的postage config数据
# #############################################################################
# def get_postage_configs_for_cache(webapp_owner_id):
# 	def inner_func():
# 		postage_configs = PostageConfig.objects.filter(owner_id=webapp_owner_id)

# 		values = []
# 		for postage_config in postage_configs:
# 			factor = {
# 				'firstWeight': postage_config.first_weight,
# 				'firstWeightPrice': postage_config.first_weight_price,
# 				'isEnableAddedWeight': postage_config.is_enable_added_weight,
# 			}

# 			if postage_config.is_enable_added_weight:
# 				factor['addedWeight'] = float(postage_config.added_weight)
# 				if postage_config.added_weight_price:
# 					factor['addedWeightPrice'] = float(postage_config.added_weight_price)
# 				else:
# 					factor['addedWeightPrice'] = 0

# 			# 特殊运费配置
# 			special_factor = dict()
# 			for special_config in postage_config.get_special_configs():
# 				s_factor = {
# 					'firstWeight': special_config.first_weight,
# 					'firstWeightPrice': special_config.first_weight_price,
# 					'isEnableAddedWeight': postage_config.is_enable_added_weight,
# 				}
# 				if postage_config.is_enable_added_weight:
# 					s_factor['addedWeight'] = float(special_config.added_weight)
# 					s_factor['addedWeightPrice'] = float(special_config.added_weight_price)

# 				for has_province in special_config.destination.split(','):
# 					special_factor['province_{}'.format(has_province)] = s_factor
# 			factor['special_factor'] = special_factor

# 			# 免运费配置
# 			free_factor = dict()
# 			for free_config in postage_config.get_free_configs():
# 				s_factor = {
# 					'condition': free_config.condition,
# 					'condition_value': free_config.condition_value,
# 				}
# 				for has_province in free_config.destination.split(','):
# 					free_factor['province_{}'.format(has_province)] = s_factor
# 			factor['free_factor'] = free_factor

# 			postage_config.factor = factor
# 			values.append(postage_config.to_dict('factor'))		

# 		return {
# 			'value': values
# 		}

# 	return inner_func
