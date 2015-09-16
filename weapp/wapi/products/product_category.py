# -*- coding: utf-8 -*-
"""
商品分类相关
"""

from mall.models import *
from core import resource
from wapi.decorators import param_required
from wapi.wapi_utils import create_json_response
from utils import dateutil as utils_dateutil

from mall import models as mall_models

#from django.contrib.auth.models import User
#from account.models import UserProfile



class ProductCategory(resource.Resource):
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


	@param_required(params=['id'])
	def api_get(request):
		"""
		获得分类详情

		@param id 分类ID
		"""
		category = mall_models.ProductCategory.objects.get(id=request.GET.get('id'))
		return create_json_response(200, ProductCategory.category_to_dict(category))


	@param_required(params=['id', 'name'])
	def api_post(request):
		"""
		修改ProductCategory的名字
		"""
		mall_models.ProductCategory.objects.filter(id=request.GET.get('id')).update(
				name = request.REQUEST.get('name')
			)
		#print("size: {}".format(len(category)))
		return create_json_response(200, {
			})

	@param_required(params=['uid', 'name'])
	def api_put(request):
		"""
		创建分类
		"""
		product_category = mall_models.ProductCategory.objects.create(
                owner_id=request.REQUEST.get('uid'),
                name=request.REQUEST.get('name', '').strip()
            )
		product_category.save()
		return create_json_response(200, ProductCategory.category_to_dict(product_category))



class ProductCategories(resource.Resource):
	"""
	获取商品分类列表
	"""
	app = 'mall'
	resource = 'product_categories'

	@param_required(params=['uid'])
	def api_get(request):
		"""
		@see 参考 mall/product/category.py
		"""
		uid = request.REQUEST.get('uid')
		categories = mall_models.ProductCategory.objects.filter(owner_id=uid)
		data = [ ProductCategory.category_to_dict(category) for category in categories]
		return create_json_response(200, {
				"categories": data
			})

