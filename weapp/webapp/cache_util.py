# -*- coding: utf-8 -*-

__author__ = 'bert'

from django.core.cache import cache
from models import *
from utils import cache_util
from mall.models import ProductModel
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error

def get_webapp_by_appid(appid):
	key = 'webapp_appid_%s' % appid
	return cache_util.get_from_cache(key, get_webapp_from_db(appid=appid))

def get_webapp_from_db(**kwargs):
	def inner_func():
		try:
			webapp = WebApp.objects.get(**kwargs)
			return {
				'keys': [
					'webapp_appid_%s' % webapp.appid
				],
				'value': webapp
			}
		except:
			return None
	return inner_func



def get_product_stocks_from_cache(id_str, is_model_ids = False):
	"""
	获取商品库存信息 duhao
	"""
	key = 'mall_product_model_product_id_%s' % id_str
	if is_model_ids:
		key = 'mall_product_model_ids_%s' % id_str

	return cache_util.get_from_cache(key, get_product_stocks(id_str, is_model_ids))

def get_product_stocks(id_str, is_model_ids):
	
	def inner_func():
		try:
			key = 'mall_product_model_product_id_%s' % id_str
			if is_model_ids:
				product_models = ProductModel.objects.filter(id__in=id_str.split(","))
				key = 'mall_product_model_ids_%s' % id_str
			else:
				product_models = ProductModel.objects.filter(product_id=id_str)
			model_dict = {}
			for model in product_models:
				model_dict[model.id] = {
					'stocks': model.stocks, 
					'stock_type': model.stock_type
				}
			return {
				'keys': [
					key
				],
				'value': model_dict
			}
		except:
			error_msg = u"获取商品库存缓存数据失败，{}, {}, cause:\n{}".format(id_str, is_model_ids, unicode_full_stack())
			print error_message
			watchdog_error(error_msg)
			return None
	return inner_func


from django.dispatch.dispatcher import receiver
from django.db.models import signals
from weapp.hack_django import post_update_signal

def update_mall_product_model_cache(**kwargs):
	model = kwargs.get('instance', None)
	if model:
		model_id = model[0].id
		product_id = model[0].product_id

		key_product_id = 'mall_product_model_product_id_%s' % (product_id)
		key_model_ids = 'mall_product_model_ids_*%s*' % (model_id)
		cache_util.delete_cache(key_product_id)
		cache_util.delete_pattern(key_model_ids)

		if model[0].stocks < 1:
			model = model[0]
			key = 'webapp_product_detail_{wo:%s}_{pid:%s}' % (
				model.owner_id, model.product_id)
			cache_util.delete_cache(key)

			if model.owner_id != 216:
				key = 'webapp_product_detail_{wo:216}_{pid:%s}' % (
					model.product_id)
				cache_util.delete_cache(key)

post_update_signal.connect(update_mall_product_model_cache, sender=ProductModel, dispatch_uid = "product_model.update")
signals.post_save.connect(update_mall_product_model_cache, sender=ProductModel, dispatch_uid = "product_model.save")
signals.post_delete.connect(update_mall_product_model_cache, sender=ProductModel, dispatch_uid = "product_model.delete")
