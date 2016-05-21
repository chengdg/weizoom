# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
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

class VirtualProducts(resource.Resource):
	app = 'mall2'
	resource = 'virtual_products'

	@login_required
	def get(request):
		"""
		浏览虚拟商品（福利卡券）列表
		创建福利卡券活动
		"""
		_type = request.GET.get('type')
		tmpl = 'mall/editor/promotion/virtual_products.html'
		if _type and _type == 'create':
			tmpl = 'mall/editor/promotion/create_virtual_product.html'

		c = RequestContext(request, {
			'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
            'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
			'third_nav_name': export.MALL_PROMOTION_VIRTUAL_PRODUCTS_NAV
		})

		return render_to_response(tmpl, c)


	@login_required
	def api_get(request):
		"""
		获取虚拟商品和微众卡商品
		"""
		owner = request.manager
		#获取当前页数
		cur_page = int(request.GET.get('page', '1'))
		#获取每页个数
		count_per_page = int(request.GET.get('count_per_page', 10))

		name = request.GET.get('name', '')
		bar_code = request.GET.get('barCode', '')

		activities = promotion_models.VirtualProduct.objects.filter(owner=request.manager, is_finished=False)
		active_product_ids = [activity.product_id for activity in activities]
		#获取没有参加正在进行中的福利卡券活动的虚拟商品列表
		products = mall_models.Product.objects.filter(
					owner=request.manager, 
					type__in=[mall_models.PRODUCT_VIRTUAL_TYPE, mall_models.PRODUCT_WZCARD_TYPE],
					shelve_type = mall_models.PRODUCT_SHELVE_TYPE_ON
				)

		items = []
		for product in products:
			_product = product.to_dict()
			if _product['id'] in active_product_ids:
				_product['can_use'] = False
			else:
				_product['can_use'] = True

		pageinfo, items = paginator.paginate(items, cur_page, count_per_page, None)
		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': ''
		}
		return response.get_response()

	@login_required
	def api_put(request):
		"""
		添加禁用商品
		"""
		owner = request.manager
		product_id = request.POST.get('product_id')
		start_time = request.POST.get('start_time')
		end_time = request.POST.get('end_time')
		is_permanant_active = int(request.POST.get('is_permanant_active', '0'))
		product_ids = []
		for product in json.loads(products):
			product_ids.append(product['id'])
		try:
			for product_id in product_ids:
				promotion_models.ForbiddenCouponProduct.objects.create(
					owner=owner,
					product_id=product_id,
					start_date=start_date,
					end_date=end_date,
					is_permanant_active=is_permanant_active
				)
			response = create_response(200)
			try:
				webapp_owner_id = owner.id
				key = 'forbidden_coupon_products_%s' % webapp_owner_id
				utils.cache_util.delete_cache(key)
				logging.info(u"'del forbidden_coupon_products cache,key:{}".format(key))
			except:
				watchdog_alert(u'del forbidden_coupon_products cache error:{}'.format(unicode_full_stack()))

		except:
			response = create_response(500)

		return response.get_response()

	@login_required
	def api_post(request):
		"""
		结束禁用商品
		"""
		owner = request.manager
		ids = request.POST.get('id', '')
		try:
			for id in json.loads(ids):
				promotion_models.ForbiddenCouponProduct.objects.filter(owner=owner, id=id).update(status=promotion_models.FORBIDDEN_STATUS_FINISHED)
			response = create_response(200)
		except Exception ,e:
			print 'finish forbidden_coupon_products exception:',e
			response = create_response(500)
		
		return response.get_response()