# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required
#from utils import dateutil as utils_dateutil
from cache import webapp_cache


class ProductHint(api_resource.ApiResource):
	"""
	商品提示
	"""
	app = 'mall'
	resource = 'product_hint'

	@staticmethod
	def is_forbidden_coupon(owner_id, product_id):
		"""
		判断商品是否被禁止使用全场优惠券
		"""
		forbidden_coupon_product_ids = webapp_cache.get_forbidden_coupon_product_ids(owner_id)
		product_id = int(product_id)
		return product_id in forbidden_coupon_product_ids

	@param_required(['woid', 'id'])
	def get(args):
		"""
		获取显示在商品详情页的商品相关的提示信息

		@note duhao与2015-09-08增加 `__get_product_hint(owner_id, product_id)`
		"""
		hint = ''
		owner_id = args['woid']
		product_id = args['id']
		if ProductHint.is_forbidden_coupon(owner_id, product_id):
			hint = u'该商品不参与全场优惠券使用！'
		return {"woid": owner_id, "hint": hint}
