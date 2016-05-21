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

		name = request.GET.get('name', '').strip()
		bar_code = request.GET.get('barCode', '').strip()

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
			product.fill_standard_model()
			_product = {
				'id': product.id,
				'name': product.name,
				'bar_code': product.bar_code,
				'price': product.price,
				'stocks': product.stocks,
				'created_at': product.created_at.strftime('%Y-%m-%d %H:%M')
			}
			if product.id in active_product_ids:
				_product['can_use'] = False
			else:
				_product['can_use'] = True
			items.append(_product)

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
		创建福利卡券活动
		"""
		owner = request.manager
		name = request.POST.get('name').strip()
		product_id = request.POST.get('product_id').strip()
		start_time = request.POST.get('start_time').strip()
		end_time = request.POST.get('end_time').strip()
		code_file_path = request.POST.get('code_file_path').strip()
		
		try:
			#先创建福利卡券活动
			virtual_product = promotion_models.VirtualProduct.objects.create(
								owner=owner,
								name=name,
								product_id=product_id
							)
			#再为该福利卡券活动上传卡密
			success_num = upload_codes_for(code_file_path, virtual_product)

			response = create_response(200)
			response.data = {'success_num': success_num}
		except:
			response = create_response(500)

		return response.get_response()


	@login_required
	def api_post(request):
		"""
		修改福利卡券活动，补充上传卡密
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


def upload_codes_for(code_file_path, virtual_product):
	if not code_file_path:
		return 0

	codes_dict = get_codes_from_file(code_file_path)
	existed_codes = promotion_models.VirtualProductHasCode.objects.filter(status__in=[promotion_models.CODE_STATUS_NOT_GET, promotion_models.CODE_STATUS_GET])
	existed_code_ids = {}
	for code in existed_codes:
		if not code.can_not_use:
			existed_code_ids[code.code] = 1

	success_num = 0
	for code in codes_dict:
		code = code.strip()
		#如果库中已存在已领取或者未领取的该码，则不添加这个码
		if not code or existed_code_ids[code]:
			continue

		password = codes_dict[code].strip()
		promotion_models.VirtualProductHasCode.objects.create(
			owner=owner,
			virtual_product=virtual_product,
			code=code,
			password=password,
			start_time=start_time,
			end_time=end_time
		)
		success_num += 1
	logging.info('upload %d codes for virtual_product id %d' % (success_num, virtual_product.id))
	return success_num


def get_codes_from_file(path):
    """
    从文件中读取福利卡券的码库
    """
    pass
    # file = ''
    # if file:
    #     pass
    # else:
    #     return {}


def update_stocks():
	"""
	更新商品的库存
	"""
	pass