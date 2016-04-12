# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required

from mall import models as mall_models
from django.db.models import Count
from datetime import datetime
class ProductSupplierStatics(api_resource.ApiResource):
	"""
	商品-供应商
	"""
	app = 'mall'
	resource = 'product_statics'

	def get(args):
		"""
		获取商品和供应商信息

		@param product_id 商品ID
		@param supplier_id 供应商ID
		@param supplier_user_id 同步商品的所属商家ID
		"""
		product_ids = args.get('product_ids', None)
		data = {}
		if product_ids:
			order_has_products =mall_models.OrderHasProduct.objects.filter(product_id__in=product_ids.split(','))
			if order_has_products.count()>0:
				order_dot_ids = [order.order_id for order in order_has_products]
				orders_list = mall_models.Order.objects.filter(id__in=order_dot_ids,status__in=[3,4,5]).values('payment_time').annotate(today_order_num=Count('payment_time'))
				print "zl--------------------------",orders_list
				for order in orders_list:
					order_pay_time = datetime.strftime(order['payment_time'],'%Y-%m-%d')
					if order_pay_time in data:
						data[order_pay_time] += order['today_order_num']
					else:
						data[order_pay_time] = order['today_order_num']

		data= sorted(data.iteritems(), key=lambda d:d[0])
		# data 更改为了list类型
		datalist = []
		vallist = []
		for d in data:
			datalist.append(d[0])
			vallist.append(d[1])

		return {
					'datelist':datalist,
					 'vallist':vallist
				}
