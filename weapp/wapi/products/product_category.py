# -*- coding: utf-8 -*-
"""
商品分类相关
"""

from mall.models import *
from core import resource
from wapi.decorators import wapi_access_required
from wapi.wapi_utils import create_json_response
from utils import dateutil as utils_dateutil

from mall import models as mall_models

from django.contrib.auth.models import User
from account.models import UserProfile


class ProductCategories(resource.Resource):
	"""
	获取商品分组列表
	"""
	app = 'wapi'
	resource = 'product_categories'

	@wapi_access_required(required_params=['uid'])
	def api_get(request):
		"""
		@see 参考 mall/product/category.py
		"""
		uid = request.REQUEST.get('uid')
		categories = mall_models.ProductCategory.objects.filter(owner_id=uid)
		data = [{ \
			'id': category.id, \
			'name': category.name, \
			'product_count': category.product_count, \
			'created_at': utils_dateutil.datetime2string(category.created_at)} for category in categories]
		return create_json_response(200, {
				"categories": data
			})


class ProductCategory(resource.Resource):
	"""
	获取WebAPP ID
	"""
	app = 'wapi'
	resource = 'product_category'

	@wapi_access_required(required_params=['id'])
	def api_get(request):
		"""
		获取WebAPP ID

		@param username 用户名
		"""
		category = mall_models.ProductCategory.objects.get(id=request.GET.get('id'))
		return create_json_response(200, {
				"id": category.id,
				"name": category.name,
				"product_count": category.product_count,
				"created_at": utils_dateutil.datetime2string(category.created_at)
			})


	@wapi_access_required(required_params=['id', 'name'])
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
