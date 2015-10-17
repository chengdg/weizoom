# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required
#from wapi.wapi_utils import create_json_response

#from mall import models as mall_models
from mall import module_api as mall_api
from modules.member import models as member_models

from utils import dateutil as utils_dateutil

class Orders(api_resource.ApiResource):
	"""
	订单列表
	"""
	app = 'mall'
	resource = 'orders'

	@param_required([])
	def get(args):
		"""
		获取订单列表

		"""
		#orders = mall_api.get_orders(request)
		return {}
