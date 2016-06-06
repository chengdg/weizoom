# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as app_models
# import export
from datetime import datetime
from mall import export
from mall import models as mall_models
from export_job.models import ExportJob

FIRST_NAV_NAME = export.PRODUCT_FIRST_NAV
COUNT_PER_PAGE = 50

class EvaluatesRelations(resource.Resource):
	app = 'apps/evaluate'
	resource = 'evaluate_relations'
	
	@login_required
	def get(request):
		"""
		商品关联页面
		"""

		c = RequestContext(request,{
		   'first_nav_name': FIRST_NAV_NAME,
		   'second_navs': export.get_mall_product_second_navs(request),
		   'second_nav_name': export.PRODUCT_REVIEW_NAV
	   })
		
		return render_to_response('evaluate/templates/editor/evaluate_relations.html', c)

	@login_required
	def api_get(request):
		"""
		得到属于当前用户的关联详情列表
		返回包含产品信息和产品评价的json
		advanced table
		"""
		owner_id  = request.manager.id

		evaluate_relations = app_models.EvaluatesRelations.objects(owner_id = owner_id).order_by('-created_at')

		# 分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		current_page = int(request.GET.get('page', '1'))
		pageinfo, evaluate_relations = paginator.paginate(evaluate_relations, current_page, count_per_page,
													   query_string=request.META['QUERY_STRING'])

		products = mall_models.Product.objects.filter(owner_id = owner_id)
		product_id2name = {p.id: p.name for p in products}

		items = []
		for re in evaluate_relations:
			related_product_ids = re.related_product_ids
			name = ''
			for id in related_product_ids:
				name = name + ' ' + product_id2name.get(id,'')
			items.append({
				'id': str(re.id),
				'product_name': name
			})

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'data': {}
		}
		return response.get_response()

class EvaluatesProducts(resource.Resource):
	app = 'apps/evaluate'
	resource = 'search_products_dialog'

	@login_required
	def api_get(request):
		"""
        查询已上架商品
        """
		product_name = request.GET.get('product_name','')
		bar_code = request.GET.get('bar_code', '')

		owner_id = request.manager.id

		#过滤掉已经关联过的商品
		related_products = app_models.EvaluatesRelatedProducts.objects()
		related_products_ids = [p.product_id for p in related_products]

		#查询
		param = {
			'owner_id': owner_id
		}
		if product_name:
			param['name'] = product_name
		if bar_code:
			param['bar_code'] = bar_code

		products = mall_models.Product.objects.exclude(id__in = related_products_ids).filter(**param).order_by('-created_at')

		# 分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		current_page = int(request.GET.get('page', '1'))
		pageinfo, products = paginator.paginate(products, current_page,count_per_page,
																		 query_string=request.META['QUERY_STRING'])

		evaluates = app_models.Evaluates.objects(owner_id=owner_id).order_by("-created_at")
		#构造商品对应的评价数映射
		product_id2evaluate_count = {}
		for evaluate in evaluates:
			product_id = evaluate.product_id
			if product_id in product_id2evaluate_count:
				product_id2evaluate_count[product_id] += 1
			else:
				product_id2evaluate_count[product_id] = 1

		items = []
		for product in products:
			product_id = product.id
			items.append({
				'id': product_id,
				'bar_code': product.bar_code,
				'product_name': product.name,
				'price': product.price,
				'evaluate_count': product_id2evaluate_count.get(product_id,0)
			})

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'data': {}
		}
		return response.get_response()