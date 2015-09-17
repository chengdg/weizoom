# -*- coding: utf-8 -*-
"""
商品分类相关
"""

from mall.models import *
from core import api_resource
from wapi.decorators import param_required
from utils import dateutil as utils_dateutil

from mall import models as mall_models


class ProductCategory(api_resource.ApiResource):
	"""
	获取WebAPP ID
	"""
	app = 'mall'
	resource = 'product_category'

	@staticmethod
	def category_to_dict(category):
		return {
			"id": category.id,
			"uid": category.owner_id,
			"name": category.name,
			"product_count": category.product_count,
			"created_at": utils_dateutil.datetime2string(category.created_at)
		}


	@param_required(['id'])
	def get(args):
		"""
		获得分类详情

		@param id 分类ID
		"""
		category = mall_models.ProductCategory.objects.get(id=args['id'])
		return ProductCategory.category_to_dict(category)


	@param_required(['id', 'name'])
	def post(args):
		"""
		修改ProductCategory的名字
		"""
		mall_models.ProductCategory.objects.filter(id=args['id']).update(
				name = args['name']
			)
		return


	@param_required(['uid', 'name'])
	def put(args):
		"""
		创建分类
		"""
		product_category = mall_models.ProductCategory.objects.create(
                owner_id=args['uid'],
                name=args.get('name', '').strip()
            )
		product_category.save()
		return ProductCategory.category_to_dict(product_category)
