# -*- coding: utf-8 -*-
"""
商品分类相关
"""

from core import api_resource
from wapi.decorators import param_required

from mall import models as mall_models
from product_category import ProductCategory


class ProductCategories(api_resource.ApiResource):
	"""
	获取商品分类列表

	举例：`http://dev.weapp.com/wapi/mall/product_categories/?uid=33`
	"""
	app = 'mall'
	resource = 'product_categories'

	@param_required(['uid'])
	def get(args):
		"""
		@see 参考 mall/product/category.py
		"""
		uid = args['uid']
		#print("uid: {}".format(uid))
		categories = mall_models.ProductCategory.objects.filter(owner_id=uid)
		data = [ ProductCategory.category_to_dict(category) for category in categories]
		#print("data: {}".format(data))
		return data
