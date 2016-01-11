# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db.models import F

from core import resource
from core import paginator
from core.jsonresponse import create_response

from termite2 import export
from webapp import models as webapp_models
from mall import models as mall_models

FIRST_NAV = export.WEPAGE_FIRST_NAV
COUNT_PER_PAGE = 20

class WebappDatas(resource.Resource):
	"""
	webapp链接资源
	"""
	app = 'termite2'
	resource = 'webapp_datas'

	@staticmethod
	def get_datas_for_type(request, type, query, order_by):
		"""
		获取相应的链接
		"""
		user = request.manager
		webapp_owner_id = user.id
		type2info = {
			'product': {
				'class': mall_models.Product, 
				'filter': {'shelve_type': mall_models.PRODUCT_SHELVE_TYPE_ON, "is_deleted": False},
				'query_name': 'name',
				'link_template': './?module=mall&model=product&action=get&rid={}&workspace_id=mall&webapp_owner_id=%d' % webapp_owner_id
			},
			'category': {
				'class': mall_models.ProductCategory, 
				'query_name': 'name',
				'link_template': './?module=mall&model=products&action=list&category_id=1&workspace_id=mall&webapp_owner_id=%d' % webapp_owner_id
			},
		}


		kwargs = {
			'owner': user
		}
		info = type2info[type]
		if query and len(query) > 0:
			kwargs[info['query_name']+'__contains'] = query
		if 'filter' in info:
			kwargs.update(info['filter'])

		objects = info['class'].objects.filter(**kwargs).order_by(order_by)

		return objects, info
	
	
	@login_required
	def api_get(request):
		"""
		获取链接集合的json表示
		"""
		query = request.GET.get('query', None)
		type = request.GET.get('type', None)
		order_by = request.GET.get('sort_attr', '-id')

		objects, type_info = WebappDatas.get_datas_for_type(request, type, query, order_by)
		
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, objects = paginator.paginate(objects, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		# 根据link_target获取已选的id跟type
		selected_id = int(request.GET.get('selected_id', 0))

		items = []
		id2data = {}
		for obj in objects:
			item = {
				"id": obj.id,
				"created_at": obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				"name": obj.name,
				"link": type_info['link_template'].format(obj.id),
				"isChecked": True if selected_id > 0 and obj.id == selected_id else False
			}

			if 'product' == type:
				productData = {
					"price": obj.price,
					"name": obj.name,
					"thumbnails_url": obj.thumbnails_url
				}
				id2data[obj.id] = productData
			items.append(item)

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': order_by,
			'data': id2data
		}
		return response.get_response()
