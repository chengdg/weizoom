__author__ = 'Administrator'
# -*- coding: utf-8 -*-

from core import api_resource, paginator
from wapi.decorators import param_required

from mall import models as mall_models
from mall import module_api as mall_api


from utils import dateutil as utils_dateutil

class Supplier(api_resource.ApiResource):
	"""
	订单
	"""
	app = 'mall'
	resource = 'supplier'

	@param_required(['supplier_ids', 'is_delete'])
	def get(args):
		"""
		获取商品详情

		@param id 商品ID
		"""
		supplier_ids = args['supplier_ids'].split(',') # list
		is_delete = args['is_delete']
		if is_delete == 'False':
			is_delete=False
		else:
			is_delete=True
		suppliers = mall_models.Supplier.objects.filter(id__in=supplier_ids,is_delete=is_delete)
		items = []
		for supplier in suppliers:
			items.append({
				'woid': supplier.owner_id,
				'id': supplier.id,
				'name': supplier.name,
				'responsible_person': supplier.responsible_person,
				'supplier_tel': supplier.supplier_tel,
				'supplier_address': supplier.supplier_address,
				'remark': supplier.remark

			})
		return items


