# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required
from wapi.wapi_utils import create_json_response

class Promotions(api_resource.ApiResource):
	"""
	商品
	"""
	app = 'mall.promotion'
	resource = 'promotions'

	def get(args):
		"""
		获取商品详情

		@param id 商品ID
		"""
		promotions = [{
			"id": 1,
			"name": "promotion 1"
		}, {
			"id": 2,
			"name": "promotion 2"
		}]
		return promotions
