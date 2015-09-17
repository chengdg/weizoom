# -*- coding: utf-8 -*-
"""
商品相关
"""

from core import resource
from wapi.decorators import param_required
from wapi.wapi_utils import create_json_response
from utils import dateutil as utils_dateutil

from mall import models as mall_models


class Product(resource.Resource):
	"""
	获取商品详情
	"""
	app = 'wmall'
	resource = 'product'

	@staticmethod
	def product_to_dict(product):
		return {
			'id': product.id,
			'owner_id': product.owner_id,
			'name': product.name,
			'physical_unit': product.physical_unit,
			'price': product.price,
		}

	@param_required(params=['id'])
	def api_get(request):
		"""
		获取商品详情

		@param id 商品ID
		"""
		product = mall_models.Product.objects.get(id=request.GET.get('id'))
		return create_json_response(200, Product.product_to_dict(product))
