# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required

from mall import models as mall_models

class ProductSupplier(api_resource.ApiResource):
	"""
	商品-供应商
	"""
	app = 'mall'
	resource = 'product_supplier'

	def get(args):
		"""
		获取商品和供应商信息

		@param product_id 商品ID
		@param supplier_id 供应商ID
		"""
		product_id = args.get('product_id', None)
		if product_id:
			try:
				product = mall_models.Product.objects.get(id=product_id)
				return {
					'product_name': product.name,
					'supplier_user_id': product.supplier_user_id,
					'supplier_id': product.supplier
				}
			except Exception, e:
				print u'根据商品id获取商品名失败：', product_id, e
				return {
					'product_name': u'未知商品名：' + product_id
				}

		supplier_id = args.get('supplier_id', None)
		if supplier_id:
			try:
				supplier = mall_models.Supplier.objects.get(id=supplier_id)
				return {
					'supplier_name': supplier.name

				}
			except Exception, e:
				print u'根据供应商id获取供应商名失败：', supplier_id, e
				return {
					'supplier_name': u'未知供应商名：' + supplier_id
				}

		return {}
