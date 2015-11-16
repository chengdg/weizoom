# -*- coding: utf-8 -*-

#import json

from core import api_resource
from wapi.decorators import param_required
from wapi import wapi_utils
#from wapi.wapi_utils import create_json_response

#from mall import models as mall_models

from product import Product
from cache import webapp_cache

from dummy_utils import DummyUserProfile
#from utils import dateutil as utils_dateutil


class ProductsByCategory(api_resource.ApiResource):
	"""
	按类别获取商品列表

	举例：`http://dev.weapp.com/wapi/mall/products_by_category/?webapp_id=3211&category_id=7&uid=33&is_access_weizoom_mall=false`
	"""
	app = 'mall'
	resource = 'products_by_category'

	@staticmethod
	def to_dict(products):
		data = []
		for product in products:
			data.append(Product.to_dict(product))
		return data

	@staticmethod
	def cached_to_dict(products):
		"""
		将cache数据结构转成dict
		"""
		"""
		data = []
		for product in products:
			product['update_time'] = utils_dateutil.date2string(product['update_time'])
			product['created_at'] = utils_dateutil.datetime2string(product['created_at'])
			product['categories'] = ';'.join([str(x) for x in product['categories'] ])
			data.append(product)
		return data
		"""
		data = [Product.to_dict(product) for product in products]
		return data

	@param_required(['oid', 'category_id', 'wid'])
	def get(args):
		"""
		获取商品详情

		@param category_id 类别ID(id=0表示全部分类)
		"""
		#webapp_id = args['webapp_id']
		owner_id = args['oid']
		category_id = args['category_id']
		webapp_id = args['wid']
		#webapp_id = wapi_utils.get_webapp_id_via_oid(owner_id)
		is_access_weizoom_mall = args.get('is_access_weizoom_mall', False)
		print("args: {}".format(args))

		# 伪造一个UserProfile，便于传递参数
		user_profile = DummyUserProfile(webapp_id, owner_id)

		#product = mall_models.Product.objects.get(id=args['id'])

		# 通过缓存获取数据
		category, products = webapp_cache.get_webapp_products_new(user_profile, is_access_weizoom_mall, category_id)
		#print("products: {}".format(products))
		#func = webapp_cache.get_webapp_products_from_db(user_profile, is_access_weizoom_mall)
		#result = func()
		#print("result from get_webapp_products_from_db: {}".format(result))
		#products = result['value']['products']
		#categories = result['value']['categories']
		return ProductsByCategory.cached_to_dict(products)
