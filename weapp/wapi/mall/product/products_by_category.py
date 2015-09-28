# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required
#from wapi.wapi_utils import create_json_response

from mall import models as mall_models

from product import Product
from cache import webapp_cache

from utils import dateutil as utils_dateutil

class DummyUserProfile:
	"""
	模拟webapp_owner_user_profile，用于cache调用
	"""
	def __init__(self, webapp_id, user_id):
		self.webapp_id = webapp_id
		self.user_id = user_id



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
		data = []
		for product in products:
			product['update_time'] = utils_dateutil.date2string(product['update_time'])
			product['created_at'] = utils_dateutil.datetime2string(product['created_at'])
			product['categories'] = ';'.join([str(x) for x in product['categories'] ])
			data.append(product)
		return data

	@param_required(['webapp_id', 'category_id', 'uid', 'is_access_weizoom_mall'])
	def get(args):
		"""
		获取商品详情

		@param category_id 类别ID(id=0表示全部分类)
		"""
		webapp_id = args['webapp_id']
		category_id = args['category_id']
		owner_id = args['uid']
		is_access_weizoom_mall = args['is_access_weizoom_mall']
		print("args: {}".format(args))

		user_profile = DummyUserProfile(webapp_id, owner_id)

		#product = mall_models.Product.objects.get(id=args['id'])
		#category, products = webapp_cache.get_webapp_products(user_profile, is_access_weizoom_mall, category_id)

		func = webapp_cache.get_webapp_products_from_db(user_profile, is_access_weizoom_mall)
		result = func()
		print("result from get_webapp_products_from_db: {}".format(result))
		products = result['value']['products']
		categories = result['value']['categories']
		#categories = result['value']['categories']
		#return ProductsByCategory.to_dict(products)
		#return products
		#return {"products": "{}".format(products)}
		return ProductsByCategory.cached_to_dict(products)
