# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json, os, xlrd
import logging
from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource, paginator
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from mall import export
from mall.promotion import models as promotion_models
from mall import models as mall_models

from watchdog.utils import watchdog_alert

import utils
from django.conf import settings

class VirtualProducts(resource.Resource):
	app = 'mall2'
	resource = 'virtual_products'

	@login_required
	def get(request):
		"""
		浏览虚拟商品（福利卡券）列表
		"""
		c = RequestContext(request, {
			'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
			'third_nav_name': export.MALL_PROMOTION_VIRTUAL_PRODUCTS_NAV
		})

		return render_to_response('mall/editor/promotion/virtual_products.html', c)


	@login_required
	def api_get(request):
		"""
		获取虚拟卡券活动列表
		"""
		owner = request.manager
		#获取当前页数
		cur_page = int(request.GET.get('page', '1'))
		#获取每页个数
		count_per_page = int(request.GET.get('count_per_page', 10))

		name = request.GET.get('name', '').strip()
		product_name = request.GET.get('product_name', '').strip()
		bar_code = request.GET.get('barCode', '').strip()
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')

		params = {
			'owner': request.manager
		}
		if name:
			params['name__contains'] = name
		if product_name:
			params['product__name__contains'] = product_name
		if bar_code:
			params['product__bar_code'] = bar_code
		if start_time and end_time:
			params['created_at__range'] = [start_time, end_time]

		virtual_products = promotion_models.VirtualProduct.objects.filter(**params).order_by('-id')
		pageinfo, virtual_products = paginator.paginate(virtual_products, cur_page, count_per_page, None)

		virtual_product_ids = [v.id for v in virtual_products]
		virtual_product_has_codes = promotion_models.VirtualProductHasCode.objects.filter(
				virtual_product_id__in=virtual_product_ids, 
				# status__in=[promotion_models.CODE_STATUS_GET, promotion_models.CODE_STATUS_NOT_GET]
			)

		virtual_product_id2total_stock = {}  #总库存
		virtual_product_id2code_stock = {}  #可用库存
		virtual_product_id2sell_num = {}  #已经售出
		virtual_product_id2overdue_num = {}  #已过期
		virtual_product_id2expired_num = {}  #已失效

		for r in virtual_product_has_codes:
			#总库存
			if virtual_product_id2total_stock.has_key(r.virtual_product_id):
				virtual_product_id2total_stock[r.virtual_product_id] += 1
			else:
				virtual_product_id2total_stock[r.virtual_product_id] = 1

			if r.can_not_use:  #r.can_not_use会检查码是否过期
				#已过期
				if r.status == promotion_models.CODE_STATUS_OVERDUE:
					if virtual_product_id2overdue_num.has_key(r.virtual_product_id):
						virtual_product_id2overdue_num[r.virtual_product_id] += 1
					else:
						virtual_product_id2overdue_num[r.virtual_product_id] = 1

				if r.status == promotion_models.CODE_STATUS_EXPIRED:
					if virtual_product_id2expired_num.has_key(r.virtual_product_id):
						virtual_product_id2expired_num[r.virtual_product_id] += 1
					else:
						virtual_product_id2expired_num[r.virtual_product_id] = 1
			else:
				#可用库存
				if r.status == promotion_models.CODE_STATUS_NOT_GET:
					if virtual_product_id2code_stock.has_key(r.virtual_product_id):
						virtual_product_id2code_stock[r.virtual_product_id] += 1
					else:
						virtual_product_id2code_stock[r.virtual_product_id] = 1
				#已经售出
				elif r.status == promotion_models.CODE_STATUS_GET:
					if virtual_product_id2sell_num.has_key(r.virtual_product_id):
						virtual_product_id2sell_num[r.virtual_product_id] += 1
					else:
						virtual_product_id2sell_num[r.virtual_product_id] = 1

		items = []
		for virtual_product in virtual_products:
			items.append({
				'id': virtual_product.id,
				'name': virtual_product.name,
				'product': {
					'id': virtual_product.product.id,
					'name': virtual_product.product.name,
					'thumbnails_url': virtual_product.product.thumbnails_url,
					'bar_code': virtual_product.product.bar_code,
					'detail_link': '/mall2/product/?id=%d&source=onshelf' % virtual_product.product.id,
				},
				'total_stock': virtual_product_id2total_stock.get(virtual_product.id, 0),  #总库存
				'code_stock': virtual_product_id2code_stock.get(virtual_product.id, 0),  #可用库存
				'sell_num': virtual_product_id2sell_num.get(virtual_product.id, 0),  #已售出数量
				'overdue_num': virtual_product_id2overdue_num.get(virtual_product.id, 0),  #已过期数量
				'expired_num': virtual_product_id2expired_num.get(virtual_product.id, 0),  #已失效数量
				'created_at': virtual_product.created_at.strftime('%Y:%m:%d %H:%M:%S'),
				'is_finished': virtual_product.is_finished
			})

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': ''
		}
		return response.get_response()
