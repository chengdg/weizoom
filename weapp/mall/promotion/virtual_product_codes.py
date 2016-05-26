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
from modules.member import models as member_models

from watchdog.utils import watchdog_alert

from utils.string_util import byte_to_hex
from django.conf import settings

class VirtualProductCodes(resource.Resource):
	app = 'mall2'
	resource = 'virtual_product_codes'

	@login_required
	def get(request):
		"""
		创建福利卡券活动
		"""
		virtual_product_id = int(request.GET.get('id', 0))
		virtual_product = None
		if virtual_product_id:
			_virtual_product = promotion_models.VirtualProduct.objects.get(id=virtual_product_id)

			virtual_product = {
				'id': _virtual_product.id,
				'name': _virtual_product.name,
				'created_at': _virtual_product.created_at.strftime('%Y-%m-%d %H:%M')
			}

		c = RequestContext(request, {
			'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
            'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
			'third_nav_name': export.MALL_PROMOTION_VIRTUAL_PRODUCTS_NAV,
			'virtual_product': virtual_product
		})

		return render_to_response('mall/editor/promotion/virtual_product_codes.html', c)


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

		virtual_product_id = int(request.GET.get('virtual_product_id', '-1'))
		code = request.GET.get('code', '')
		member_name = request.GET.get('member_name', '')
		valid_time_start = request.GET.get('valid_time_start', '')
		valid_time_end = request.GET.get('valid_time_end', '')
		get_time_start = request.GET.get('get_time_start', '')
		get_time_end = request.GET.get('get_time_end', '')
		status = int(request.GET.get('status', '-1'))
		order_id = request.GET.get('order_id', '')

		params = {
			'owner': request.manager, 
			'virtual_product_id': virtual_product_id
		}
		if code:
			params['code'] = code
		if member_name:
			query_hex = byte_to_hex(member_name)
			members = member_models.Member.objects.filter(username_hexstr__contains=query_hex)
			member_ids = [m.id for m in members]
			params['member_id__in'] = member_ids
		if valid_time_start and valid_time_end:
			params['start_time__lte'] = valid_time_end
			params['end_time__gte'] = valid_time_start
		if get_time_start and get_time_end:
			params['get_time__lte'] = get_time_end
			params['get_time__gte'] = get_time_start
		if status >= 0:
			params['status'] = status
		if order_id:
			params['order_id'] = order_id

		codes = promotion_models.VirtualProductHasCode.objects.filter(**params).order_by('id')
		pageinfo, codes = paginator.paginate(codes, cur_page, count_per_page, None)

		member_ids = []
		for code in codes:
			if code.member_id:
				member_ids.append(code.member_id)
		members = member_models.Member.objects.filter(id__in=member_ids)
		member_id2nick_name = {}
		for member in members:
			nick_name = member.username
			try:
				nick_name = nick_name.decode('utf8')
			except:
				nick_name = member.username_hexstr
			member_id2nick_name[str(member.id)] = nick_name

		items = []
		for code in codes:
			items.append({
				'id': code.id,
				'code': code.code,
				'created_at': code.created_at.strftime('%Y-%m-%d %H:%M'),
				'start_time': code.start_time.strftime('%Y-%m-%d %H:%M:%S'),
				'end_time': code.end_time.strftime('%Y-%m-%d %H:%M:%S'),
				'status': promotion_models.CODE2TEXT[code.status],
				'get_time': code.get_time.strftime('%Y-%m-%d %H:%M') if code.get_time else u'',
				'member_id': code.member_id,
				'member_name': member_id2nick_name.get(code.member_id, ''),
				'oid': code.oid,
				'order_id': code.order_id
			})

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': ''
		}
		return response.get_response()
