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
from export_job.models import ExportJob

FIRST_NAV_NAME = export.PRODUCT_FIRST_NAV
COUNT_PER_PAGE = 50

class Evaluates(resource.Resource):
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
	
	# @staticmethod
	# def get_datas(request):
	# 	name = request.GET.get('name', '')
	# 	status = int(request.GET.get('status', -1))
	# 	start_time = request.GET.get('start_time', '')
	# 	end_time = request.GET.get('end_time', '')
	#
	# 	now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
	# 	params = {'owner_id':request.manager.id}
	# 	datas_datas = app_models.Evaluate.objects(**params)
	# 	for data_data in datas_datas:
	# 		data_start_time = data_data.start_time.strftime('%Y-%m-%d %H:%M')
	# 		data_end_time = data_data.end_time.strftime('%Y-%m-%d %H:%M')
	# 		if data_start_time <= now_time and now_time < data_end_time:
	# 			data_data.update(set__status=app_models.STATUS_RUNNING)
	# 		elif now_time >= data_end_time:
	# 			data_data.update(set__status=app_models.STATUS_STOPED)
	# 	if name:
	# 		params['name__icontains'] = name
	# 	if status != -1:
	# 		params['status'] = status
	# 	if start_time:
	# 		params['start_time__gte'] = start_time
	# 	if end_time:
	# 		params['end_time__lte'] = end_time
	# 	datas = app_models.Evaluate.objects(**params).order_by('-id')
	#
	# 	#进行分页
	# 	count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	# 	cur_page = int(request.GET.get('page', '1'))
	# 	pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	#
	# 	return pageinfo, datas
	
	@login_required
	def api_get(request):
		"""
		得到属于当前用户的所有评论过的商品的列表
		返回包含产品信息和产品评价的json
		advanced table
		"""
		name = request.GET.get('name', '')
		user_code = request.GET.get('userCode', '')
		review_status = request.GET.get('reviewStatus', 'all')
		start_date = request.GET.get('startDate', '')
		end_date = request.GET.get('endDate', '')
		product_score = request.GET.get('productScore', '-1')

		is_fetch_all_reviews = (not name) and (not user_code) and (not start_date) and (not end_date) and (
			review_status == 'all') and (product_score == 'all')

		# 当前用户
		owner = request.manager
		all_reviews = mall_models.ProductReview.objects.filter(owner_id=owner.id).order_by("-created_at")

		if is_fetch_all_reviews:
			# 分页
			count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
			current_page = int(request.GET.get('page', '1'))
			pageinfo, product_reviews = paginator.paginate(all_reviews, current_page, count_per_page,
														   query_string=request.META['QUERY_STRING'])
		else:
			all_reviews = _filter_reviews(request, all_reviews)

			# 处理商品编码
			product_reviews = []
			if user_code:
				for review in all_reviews:
					from cache import webapp_cache

					review_product = mall_models.OrderHasProduct.objects.get(id=review.order_has_product_id)
					product = webapp_cache.get_webapp_product_detail(request.webapp_owner_id, review.product_id)
					product.fill_specific_model(review_product.product_model_name)
					if product.model.user_code == user_code:
						review.product_user_code = user_code
						product_reviews.append(review)
			else:
				product_reviews = all_reviews

			count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
			current_page = int(request.GET.get('page', '1'))
			pageinfo, product_reviews = paginator.paginate(product_reviews, current_page, count_per_page,
														   query_string=request.META['QUERY_STRING'])

		# 处理商品
		product_ids = [review.product_id for review in product_reviews]
		id2product = dict([(product.id, product) for product in mall_models.Product.objects.filter(id__in=product_ids)])
		# 处理会员
		member_ids = [review.member_id for review in product_reviews]
		members = get_member_by_id_list(member_ids)
		member_id2member_name = dict([(m.id, m.username_for_html) for m in members])

		items = []
		from cache import webapp_cache

		reviewids = [r.order_has_product_id for r in product_reviews]
		orderhasproducts = mall_models.OrderHasProduct.objects.filter(id__in=reviewids)
		review2orderhasproductsmap = dict([(i.id, i) for i in orderhasproducts])

		for review in product_reviews:
			if not hasattr(review, 'product_user_code'):
				review_product = review2orderhasproductsmap[review.order_has_product_id]
				review.product_name = review_product.product_name
				review.product_model_name = review_product.product_model_name
				product = webapp_cache.get_webapp_product_detail(request.webapp_owner_id, review.product_id)
				product.fill_specific_model(review.product_model_name)
				review.product_user_code = product.model.user_code
			items.append({
				'id': review.id,
				'product_user_code': review.product_user_code,
				'product_name': id2product[review.product_id].name,
				'user_name': member_id2member_name.get(review.member_id, '已经跑路'),
				'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				'content': review.review_detail,
				'product_id': review.product_id,
				'member_id': review.member_id,
				'product_score': review.product_score,
				'status': {
					'name': mall_models.PRODUCT_REVIEW_STATUS[int(review.status) + 1][1],  # 返回产品状态
					'value': review.status,
				}
			})

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'data': {}
		}
		return response.get_response()

