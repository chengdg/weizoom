__author__ = 'Administrator'
# -*- coding: utf-8 -*-

from core import api_resource, paginator
from wapi.decorators import param_required

from mall import models as mall_models
from mall import module_api as mall_api


from utils import dateutil as utils_dateutil

class SupplierProducts(api_resource.ApiResource):
	"""
	订单
	"""
	app = 'mall'
	resource = 'supplier_products'

	@param_required(['category_ids'])
	def get(args):
		"""
		获取商品详情

		@param id 商品ID
		"""
		category_ids = args['category_ids'].split(',') # list

		categoryhascategorys  = mall_models.CategoryHasProduct.objects.filter(category_id__in=category_ids)
		product_ids = [chg.product_id for chg in categoryhascategorys]
		products = mall_models.Product.objects.filter(id__in=product_ids)
		product_ids = [p.id for p in products]
		product_supplier = dict([(p.id,p.supplier)for p in products])
		product_id_product = dict([(p.id,p)for p in products])
		# 获取供应商的商品
		order_has_products = mall_models.OrderHasProduct.objects.filter(product_id__in=product_ids)

		products_orders = {}
		for order_has_product in order_has_products:
			if order_has_product.product_id in products_orders:
				products_orders[order_has_product.product_id].append(order_has_product.order_id)
			else:
				products_orders[order_has_product.product_id] = []
		order_has_product_orderids = [order_has_product.order_id for order_has_product in order_has_products]
		orders = mall_models.Order.objects.filter(id__in=order_has_product_orderids)
		order_id_order = dict([(order.id,order) for order in orders ])

		# 计算商品的金额相关
		supplier_product_info = []
		for product_id,order_ids in products_orders.items():
			supplier_product = {}
			supplier_product[product_id] = {}
			cash = 0
			card = 0
			for order_id in order_ids:
				order = order_id_order[order_id]
				cash +=order.final_price
				card +=order.weizoom_card_money
			supplier_product[product_id]['cash'] = cash
			supplier_product[product_id]['card'] = card
			supplier_product[product_id]['name'] = product_id_product[product_id].name
			supplier_product[product_id]['on_sale_time'] = product_id_product[product_id].created_at.strftime('%Y-%m-%d %H:%M:%S')
			supplier_product[product_id]['order_count'] = len(order_ids)
			supplier_product[product_id]['supplier_id'] = product_supplier[product_id]
			supplier_product[product_id]['owner_id'] = product_id_product[product_id].owner_id
			supplier_product_info.append(supplier_product)


		return supplier_product_info


