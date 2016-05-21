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
		print '========type:',_type
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
		获取禁用商品
		"""
		owner = request.manager
		#获取当前页数
		cur_page = int(request.GET.get('page', '1'))
		#获取每页个数
		count_per_page = int(request.GET.get('count_per_page', 10))

		name = request.GET.get('name', '')
		bar_code = request.GET.get('barCode', '')
		promotion_status = int(request.GET.get('promotionStatus', -1))
		start_date = request.GET.get('startDate', '')
		end_date = request.GET.get('endDate', '')

		args = {
			'owner': owner
		}
		if promotion_status > 0:
			args['status'] = promotion_status
		else:
			args['status__in'] = (promotion_models.FORBIDDEN_STATUS_NOT_START, promotion_models.FORBIDDEN_STATUS_STARTED)
		if start_date and end_date:
			args['start_date__gte'] = start_date
			args['end_date__lte'] = end_date
		if name:
			args['product__name__contains'] = name
		if bar_code:
			args['product__bar_code'] = bar_code

		forbidden_coupon_products = promotion_models.ForbiddenCouponProduct.objects.filter(**args).order_by('-id')

		items = []
		for product in forbidden_coupon_products:
			if not product.is_overdue:
				items.append(product.to_dict())

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
		products = request.POST.get('products', '')
		start_date = request.POST.get('start_date', '2000-01-01')
		end_date = request.POST.get('end_date', '2000-01-01')
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