# -*- coding: utf-8 -*-
"""
商品分类相关
"""

from core import api_resource
from wapi.decorators import param_required

from mall import models as mall_models


class ProductCategories(api_resource.ApiResource):
	"""
	获取商品分类列表
	"""
	app = 'mall'
	resource = 'product_categories'

	@param_required(['uid'])
	def api_get(args):
		"""
		@see 参考 mall/product/category.py
		"""
		uid = args['uid']
		categories = mall_models.ProductCategory.objects.filter(owner_id=uid)
		data = [ mall_models.ProductCategory.category_to_dict(category) for category in categories]
		return data
