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
		has_related_product_ids = [p.product_id for p in app_models.EvaluatesRelatedProducts.objects(owner_id = owner_id)]
		evaluates = app_models.ProductEvaluates.objects(owner_id = owner_id, product_id__in = has_related_product_ids)

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
			evaluates = evaluates.filter(product_id__in = related_product_ids)
			name = ''
			for id in related_product_ids:
				name = name + ' ' + product_id2name.get(id,'')
			items.append({
				'id': str(re.id),
				'product_name': name,
				'evaluate_count': evaluates.count() if evaluates else 0
			})

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'data': {}
		}
		return response.get_response()

	@login_required
	def api_post(request):
		"""
        处理关联评价
        """
		owner_id = request.manager.id

		product_ids = request.POST.get('id', '[]')
		product_ids = json.loads(product_ids)

		try:
			evaluate_relation = app_models.EvaluatesRelations.objects.create(
				owner_id = owner_id,
				related_product_ids = product_ids,
				created_at = datetime.now()
			)

			for id in product_ids:
				app_models.EvaluatesRelatedProducts.objects.create(
					owner_id = owner_id,
					product_id = id,
					belong_to = str(evaluate_relation.id)
				)
			#商品关联，取消之前的置顶
			app_models.ProductEvaluates.objects(product_id__in = product_ids).update(status = 1, top_time=app_models.DEFAULT_DATETIME)

			response = create_response(200)

		except:
			response = create_response(500)
			response.errMsg  = u'评价关联失败，请稍后重试！'

		return response.get_response()

	@login_required
	def api_delete(request):
		"""
        解除关联评价
        """
		relation_id = request.POST['id']

		try:
			app_models.EvaluatesRelations.objects(id = relation_id).delete()
			app_models.EvaluatesRelatedProducts.objects(belong_to = relation_id).delete()

			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'解除评价关联失败，请稍后重试！'

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
			param['name__icontains'] = product_name
		if bar_code:
			param['bar_code__icontains'] = bar_code

		products = mall_models.Product.objects.exclude(id__in = related_products_ids).filter(**param).order_by('-created_at')
		EvaluatesProducts.fill_display_price(products)

		# 分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		current_page = int(request.GET.get('page', '1'))
		pageinfo, products = paginator.paginate(products, current_page,count_per_page,
																		 query_string=request.META['QUERY_STRING'])

		evaluates = app_models.ProductEvaluates.objects(owner_id=owner_id).order_by("-created_at")
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
				'price': product.display_price,
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

	@staticmethod
	def fill_display_price(products):
		"""根据商品规格，获取商品价格
        """
		# 获取所有models
		product2models = {}
		product_ids = [product.id for product in products]
		for model in mall_models.ProductModel.objects.filter(product_id__in=product_ids):
			if model.is_deleted:
				# model被删除，跳过
				continue

			product_id = model.product_id
			if product_id in product2models:
				models = product2models[product_id]
			else:
				models = {
					'standard_model': None,
					'custom_models': [],
					'is_use_custom_model': False}
				product2models[product_id] = models

			if model.name == 'standard':
				models['standard_model'] = model
			else:
				models['is_use_custom_model'] = True
				models['custom_models'].append(model)
		# 为每个product确定显示价格
		for product in products:
			product_id = product.id
			if product_id in product2models:
				models = product2models[product.id]
				if models['is_use_custom_model']:
					custom_models = models['custom_models']
					if len(custom_models) == 1:
						product.display_price = custom_models[0].price
					else:
						prices = sorted(
							[model.price
							 for model in custom_models])

						product.display_price = '%.2f-%.2f' % (prices[0], prices[-1])
				else:
					product.display_price = '%.2f' % models['standard_model'].price
			else:
				product.display_price = product.price