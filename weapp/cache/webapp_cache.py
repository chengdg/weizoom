# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

from django.conf import settings

from account.models import UserProfile
from mall.models import WeizoomMall
from utils import cache_util
import cache
from mall import module_api as mall_api
from mall import models as mall_models
from mall.promotion import models as promotion_models
from mall.promotion.models import PROMOTION_TYPE_FLASH_SALE

from django.dispatch.dispatcher import receiver
from django.db.models import signals
from weapp.hack_django import post_update_signal, post_delete_signal

local_cache = {}

def get_product_display_price(product, webapp_owner_id):
	"""
	根据促销类型返回商品价格
	"""
	if webapp_owner_id != product.owner_id and product.weshop_sync == 2:
		return round(product.display_price * 1.1, 2)
	elif (hasattr(product, 'promotion') and
	      		(product.promotion is not None) and
	     		product.promotion['type'] == PROMOTION_TYPE_FLASH_SALE):
		return product.promotion['detail']['promotion_price']
	else:
		return product.display_price


def get_webapp_products_from_db(webapp_owner_user_profile, is_access_weizoom_mall):

	def inner_func():
		webapp_id = webapp_owner_user_profile.webapp_id
		webapp_owner_id = webapp_owner_user_profile.user_id

		_, products = mall_api.get_products_in_webapp(webapp_id, is_access_weizoom_mall, webapp_owner_id, 0)

		categories = mall_models.ProductCategory.objects.filter(owner_id=webapp_owner_id)

		product_ids = [product.id for product in products]
		category_has_products = mall_models.CategoryHasProduct.objects.filter(product_id__in=product_ids)
		product2categories = dict()
		for relation in category_has_products:
			product2categories.setdefault(relation.product_id, set()).add(relation.category_id)


		try:
			categories = [{"id":category.id, "name":category.name} for category in categories]
			product_dicts = []

			# Fill detail
			new_products = []
			for product in products:
				new_product = get_webapp_product_detail(webapp_owner_id, product.id)
				new_products.append(new_product)

			mall_models.Product.fill_display_price(new_products)

			for product in new_products:
				product_dict = product.to_dict()
				product_dict['display_price'] = get_product_display_price(product, webapp_owner_id)
				product_dict['categories'] = product2categories.get(product.id, set())
				product_dicts.append(product_dict)
			return {
				'value': {
					"products": product_dicts,
					"categories": categories
				}
			}
		except:
			if settings.DEBUG:
				raise
			else:
				return None
	return inner_func


def get_webapp_products(webapp_owner_user_profile, is_access_weizoom_mall, category_id):
	key = 'webapp_products_categories_{wo:%s}' % webapp_owner_user_profile.user_id
	webapp_owner_id = webapp_owner_user_profile.user_id
	if key in local_cache:
		data = local_cache[key]
	else:
		data = cache_util.get_from_cache(key, get_webapp_products_from_db(webapp_owner_user_profile, is_access_weizoom_mall))
		local_cache[key] = data

	if category_id == 0:
		category = mall_models.ProductCategory()
		category.name = u'全部'
	else:
		id2category = dict([(c["id"], c) for c in data['categories']])
		if category_id in id2category:
			category_dict = id2category[category_id]
			category = mall_models.ProductCategory()
			category.id = category_dict['id']
			category.name = category_dict['name']
		else:
			category = mall_models.ProductCategory()
			category.is_deleted = True
			category.name = u'已删除分类'

	products = mall_models.Product.from_list(data['products'])
	if category_id != 0:
		products = [product for product in products if category_id in product.categories]

	return category, products


def get_webapp_product_categories(webapp_owner_user_profile, is_access_weizoom_mall):
	key = 'webapp_products_categories_{wo:%s}' % webapp_owner_user_profile.user_id
	if key in local_cache:
		data = local_cache[key]
	else:
		data = cache_util.get_from_cache(key, get_webapp_products_from_db(webapp_owner_user_profile, is_access_weizoom_mall))
		local_cache[key] = data

	return mall_models.ProductCategory.from_list(data['categories'])


def update_webapp_product_cache(**kwargs):
	if hasattr(cache, 'request') and cache.request.user_profile:
		webapp_owner_id = cache.request.user_profile.user_id
		key = 'webapp_products_categories_{wo:%s}' % webapp_owner_id
		cache_util.delete_cache(key)

post_update_signal.connect(update_webapp_product_cache, sender=mall_models.Product, dispatch_uid = "product.update")
signals.post_save.connect(update_webapp_product_cache, sender=mall_models.Product, dispatch_uid = "product.save")
signals.post_save.connect(update_webapp_product_cache, sender=mall_models.ProductCategory, dispatch_uid = "product_category.save")
signals.post_save.connect(update_webapp_product_cache, sender=mall_models.CategoryHasProduct, dispatch_uid = "category_has_product.save")
post_delete_signal.connect(update_webapp_product_cache, sender=mall_models.ProductCategory, dispatch_uid = "mall_product_category.delete")
post_delete_signal.connect(update_webapp_product_cache, sender=mall_models.CategoryHasProduct, dispatch_uid = "mall_category_has_product.delete")
signals.post_save.connect(update_webapp_product_cache, sender=promotion_models.Promotion, dispatch_uid = "update_webapp_product_cache_by_promotion.save")
post_update_signal.connect(update_webapp_product_cache, sender=promotion_models.Promotion, dispatch_uid = "update_webapp_product_cache_by_promotion.update")


def get_webapp_products_detail(webapp_owner_id, product_ids, member_grade_id=None):
	"""
	功能同get_webapp_product_detail

	批量获取商品详情的缓存
	"""
	key_infos = []
	for pid in product_ids:
		key_infos.append({
			'key': 'webapp_product_detail_{wo:%s}_{pid:%s}' % (webapp_owner_id, pid),
			'on_miss': mall_api.get_product_detail_for_cache(webapp_owner_id, pid)
		})
	data = cache_util.get_many_from_cache(key_infos)
	products = []

	for key in data:
		product = mall_models.Product.from_dict(data[key])

		if hasattr(product, 'integral_sale') and product.integral_sale \
			and product.integral_sale['detail'].get('rules', None):
			for i in product.integral_sale['detail']['rules']:
				if i['member_grade_id'] == member_grade_id:
					product.integral_sale['detail']['discount'] = str(i['discount'])+"%"
					break

		promotion_data = data[key]['promotion']
		if promotion_data and len(promotion_data) > 0:
			product.promotion_model = promotion_models.Promotion.from_dict(promotion_data)
		else:
			product.promotion_model = dict()

		integral_sale_data = data[key]['integral_sale']
		if integral_sale_data and len(integral_sale_data) > 0:
			product.integral_sale_model = promotion_models.Promotion.from_dict(integral_sale_data)
		else:
			product.integral_sale_model = None

		products.append(product)

	return products

def get_webapp_product_detail(webapp_owner_id, product_id, member_grade_id=None):
	"""
	管理product detail缓存

	获取商品详情的缓存
	"""
	key = 'webapp_product_detail_{wo:%s}_{pid:%s}' % (webapp_owner_id, product_id)
	data = cache_util.get_from_cache(key, mall_api.get_product_detail_for_cache(webapp_owner_id, product_id))
	product = mall_models.Product.from_dict(data)

	# Set member's discount of the product
	if hasattr(product, 'integral_sale') and product.integral_sale \
		and product.integral_sale['detail'].get('rules', None):
		for i in product.integral_sale['detail']['rules']:
			if i['member_grade_id'] == member_grade_id:
				product.integral_sale['detail']['discount'] = str(i['discount'])+"%"
				break

	promotion_data = data['promotion']
	if promotion_data and len(promotion_data) > 0:
		product.promotion_model = promotion_models.Promotion.from_dict(promotion_data)
	else:
		product.promotion_model = dict()

	integral_sale_data = data['integral_sale']
	if integral_sale_data and len(integral_sale_data) > 0:
		product.integral_sale_model = promotion_models.Promotion.from_dict(integral_sale_data)
	else:
		product.integral_sale_model = None

	return product


def update_webapp_product_detail_cache(**kwargs):
	"""
	更新商品详情缓存
	"""
	if hasattr(cache, 'request') and cache.request.user_profile:
		webapp_owner_id = cache.request.user_profile.user_id
		product_ids = None
		cache_args = kwargs.get('cache_args', None)
		if cache_args:
			product_ids = cache_args.get('ids', [])

		if product_ids and len(product_ids) > 0:
			for product_id in product_ids:
				key = 'webapp_product_detail_{wo:%s}_{pid:%s}' % (webapp_owner_id, product_id)
				cache_util.delete_cache(key)
				# 更新微众商城缓存
				# TODO 更好的设计微众商城
				if webapp_owner_id != 216:
					key = 'webapp_product_detail_{wo:%s}_{pid:%s}' % (216, product_id)
					cache_util.delete_cache(key)
			if webapp_owner_id != 216:
				cache_util.delete_cache('webapp_products_categories_{wo:216}')
		else:
			pattern = 'webapp_product_detail_{wo:%s}_*' % webapp_owner_id
			cache_util.delete_pattern(pattern)


post_update_signal.connect(update_webapp_product_detail_cache, sender=mall_models.Product, dispatch_uid = "product_detail.update")
signals.post_save.connect(update_webapp_product_detail_cache, sender=mall_models.Product, dispatch_uid = "product_detail.save")

def update_webapp_product_model_cache(**kwargs):
	model = kwargs.get('instance', None)
	if model and model[0].stocks < 1:
		model = model[0]
		key = 'webapp_product_detail_{wo:%s}_{pid:%s}' % (model.owner_id, model.product_id)
		cache_util.delete_cache(key)

		if model.owner_id != 216:
			key = 'webapp_product_detail_{wo:216}_{pid:%s}' % (model.product_id)
			cache_util.delete_cache(key)

post_update_signal.connect(update_webapp_product_model_cache, sender=mall_models.ProductModel, dispatch_uid = "product_model.update")

def update_webapp_product_detail_by_review_cache(**kwargs):
	if hasattr(cache, 'request'):
		webapp_owner_id = cache.request.user_profile.user_id
		product_id = None
		instance = kwargs.get('instance', None)
		if instance:
			product_id = instance[0].product_id

		if product_id:
			key = 'webapp_product_detail_{wo:%s}_{pid:%s}' % (webapp_owner_id, product_id)
			cache_util.delete_cache(key)

post_update_signal.connect(update_webapp_product_detail_by_review_cache, sender=mall_models.ProductReview, dispatch_uid = "product_review.update")


def update_webapp_product_detail_cache_by_promotion(instance, **kwargs):
	"""
	根据促销信息，更新商品详情
	"""
	if not hasattr(cache, 'request'):
		#不是后台web系统的update，直接返回
		return

	webapp_owner_id = cache.request.user_profile.user_id
	if isinstance(instance, promotion_models.Promotion):
		promotion_ids = [instance.id]
	else:
		promotion_ids = [promotion.id for promotion in instance]
	for p in promotion_models.ProductHasPromotion.objects.filter(promotion_id__in=promotion_ids):
		key = 'webapp_product_detail_{wo:%s}_{pid:%s}' % (webapp_owner_id, p.product_id)
		cache_util.delete_cache(key)


post_update_signal.connect(update_webapp_product_detail_cache_by_promotion, sender=promotion_models.Promotion, dispatch_uid = "product_detail_by_promotion.update")
signals.post_save.connect(update_webapp_product_detail_cache_by_promotion, sender=promotion_models.Promotion, dispatch_uid = "product_detail_by_promotion.save")


def get_webapp_product_model_properties(webapp_owner_id):
	"""
	管理product model缓存
	"""
	key = 'webapp_product_model_properties_{wo:%s}' % webapp_owner_id
	data = cache_util.get_from_cache(key, mall_api.get_product_model_properties_for_cache(webapp_owner_id))

	id2property = data['id2property']
	id2value = data['id2value']
	return id2property, id2value



def update_webapp_product_model_properties_cache(**kwargs):
	"""
	更新product model缓存
	"""
	if cache.request.user_profile:
		webapp_owner_id = cache.request.user_profile.user_id
		key = 'webapp_product_model_properties_{wo:%s}' % webapp_owner_id
		cache_util.delete_cache(key)

		for weizoom_mall in WeizoomMall.objects.filter(is_active=True):
			user_profile = UserProfile.objects.filter(webapp_id = weizoom_mall.webapp_id)
			if user_profile.count() == 1:
				key = 'webapp_product_model_properties_{wo:%s}' % user_profile[0].user_id
				cache_util.delete_cache(key)


post_update_signal.connect(update_webapp_product_model_properties_cache, sender=mall_models.ProductModelProperty, dispatch_uid = "product_model_property.update")
signals.post_save.connect(update_webapp_product_model_properties_cache, sender=mall_models.ProductModelProperty, dispatch_uid = "product_model_property.save")
post_update_signal.connect(update_webapp_product_model_properties_cache, sender=mall_models.ProductModelPropertyValue, dispatch_uid = "product_model_property_value.update")
signals.post_save.connect(update_webapp_product_model_properties_cache, sender=mall_models.ProductModelPropertyValue, dispatch_uid = "product_model_property_value.save")



def get_webapp_postage_configs(webapp_owner_id):
	"""
	管理postage config缓存

	获取运费配置的缓存
	"""
	key = 'webapp_postage_configs_{wo:%s}' % webapp_owner_id
	data = cache_util.get_from_cache(key, mall_api.get_postage_configs_for_cache(webapp_owner_id))

	postage_configs = mall_models.PostageConfig.from_list(data)
	return postage_configs


###############################################################################
# update_webapp_postage_configs_cache: 更新postage config缓存
###############################################################################
def update_webapp_postage_configs_cache(**kwargs):
	if hasattr(cache, 'request') and cache.request.user_profile:
		webapp_owner_id = cache.request.user_profile.user_id
		key = 'webapp_postage_configs_{wo:%s}' % webapp_owner_id
		cache_util.delete_cache(key)


post_update_signal.connect(update_webapp_postage_configs_cache, sender=mall_models.PostageConfig, dispatch_uid = "postage_config.update")
signals.post_save.connect(update_webapp_postage_configs_cache, sender=mall_models.PostageConfig, dispatch_uid = "postage_config.save")
# post_update_signal.connect(update_webapp_postage_configs_cache, sender=mall_models.SpecialPostageConfig, dispatch_uid = "special_postage_config.update")
# signals.post_save.connect(update_webapp_postage_configs_cache, sender=mall_models.SpecialPostageConfig, dispatch_uid = "special_postage_config.save")
post_update_signal.connect(update_webapp_postage_configs_cache, sender=mall_models.FreePostageConfig, dispatch_uid = "free_postage_config.update")
signals.post_save.connect(update_webapp_postage_configs_cache, sender=mall_models.FreePostageConfig, dispatch_uid = "free_postage_config.save")





'''
管理mall config缓存
'''
###############################################################################
# get_webapp_mall_config: 获取mall config的缓存
###############################################################################
def get_webapp_mall_config(webapp_owner_id):
	key = 'webapp_mall_config_{wo:%s}' % webapp_owner_id
	data = cache_util.get_from_cache(key, mall_api.get_mall_config_for_cache(webapp_owner_id))

	return mall_models.MallConfig.from_dict(data)


###############################################################################
# update_webapp_product_model_properties_cache: 更新product model缓存
###############################################################################
def update_webapp_mall_config_cache(**kwargs):
	if hasattr(cache, 'request') and cache.request.user_profile:
		webapp_owner_id = cache.request.user_profile.user_id
		key = 'webapp_mall_config_{wo:%s}' % webapp_owner_id
		cache_util.delete_cache(key)


post_update_signal.connect(update_webapp_mall_config_cache, sender=mall_models.MallConfig, dispatch_uid = "mall_config.update")
signals.post_save.connect(update_webapp_mall_config_cache, sender=mall_models.MallConfig, dispatch_uid = "mall_config.save")





###############################################################################
# get_webapp_mall_data: 获取商品规格的缓存
###############################################################################
def get_webapp_mall_data(webapp_owner_id):
	'''
	方便外部使用缓存的接口
	'''
	mall_config_key = 'webapp_mall_config_{wo:%s}' % webapp_owner_id
	postage_configs_key = 'webapp_postage_configs_{wo:%s}' % webapp_owner_id
	product_model_properties_key = 'webapp_product_model_properties_{wo:%s}' % webapp_owner_id
	key_infos = [{
		'key': mall_config_key,
		'on_miss': mall_api.get_mall_config_for_cache(webapp_owner_id)
	}, {
		'key': postage_configs_key,
		'on_miss': mall_api.get_postage_configs_for_cache(webapp_owner_id)
	}, {
		'key': product_model_properties_key,
		'on_miss': mall_api.get_product_model_properties_for_cache(webapp_owner_id)
	}]
	data = cache_util.get_many_from_cache(key_infos)

	result = {
		'postage_configs': mall_models.PostageConfig.from_list(data[postage_configs_key]),
		'product_model_properties': data[product_model_properties_key],
		'mall_config': mall_models.MallConfig.from_dict(data[mall_config_key])
	}

	return result
