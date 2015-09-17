# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required
from wapi.wapi_utils import create_json_response

from mall import models as mall_models

class Product(api_resource.ApiResource):
	"""
	商品
	"""
	app = 'mall'
	resource = 'product'

	@staticmethod
	def to_dict(product):
		data = {
			'id': product.id,
			'owner_id': product.owner_id,
			'name': product.name,
			'physical_unit': product.physical_unit,
			'price': product.price,	
		}
		return data

	@param_required(['id'])
	def get(args):
		"""
		获取商品详情

		@param id 商品ID
		"""
		product = mall_models.Product.objects.get(id=args['id'])
		return Product.to_dict(product)
