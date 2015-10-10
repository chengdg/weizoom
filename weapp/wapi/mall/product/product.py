# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required
#from wapi.wapi_utils import create_json_response

#from mall import models as mall_models
from mall import module_api as mall_api
from modules.member import models as member_models

from utils import dateutil as utils_dateutil

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
			'introduction': product.introduction,
			'weight': product.weight,
			'thumbnails_url': product.thumbnails_url,
			'pic_url': product.pic_url,
			'detail': product.detail,
			'remark': product.remark,
			'created_at': utils_dateutil.datetime2string(product.created_at),
			'shelve_type': product.shelve_type,

			'purchase_price': product.purchase_price
		}
		if hasattr(product, 'promotion'):
			data['promotion'] = product.promotion
			data['promotion_title'] = product.promotion_title
		if hasattr(product, 'display_price'):
			data['display_price'] = product.display_price
		return data

	@param_required(['id', 'woid', 'member_grade_id', 'wuid'])
	def get(args):
		"""
		获取商品详情

		@param id 商品ID
		"""
		product_id = args['id']
		webapp_owner_id = args['woid']
		member_grade_id = args['member_grade_id']
		webapp_user = member_models.WebAppUser.objects.get(id = args['wuid'])
  
		#product = mall_models.Product.objects.get(id=args['id'])
		product = mall_api.get_product_detail(webapp_owner_id, product_id, webapp_user, member_grade_id)
		return Product.to_dict(product)
