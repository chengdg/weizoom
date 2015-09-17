# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required
from wapi.wapi_utils import create_json_response

class Product(api_resource.ApiResource):
	"""
	商品
	"""
	app = 'mall'
	resource = 'product'

	@staticmethod
	def to_dict(product):
		return product

	@param_required(['id'])
	def get(args):
		"""
		获取商品详情

		@param id 商品ID
		"""
		product = {
			"id": args['id'], 
			"owner_id": 2,
			"name": "iphone 6s",
			"plysical_unit": u"个",
			"price": 2.0
		}
		result = Product.to_dict(product)
		return result
