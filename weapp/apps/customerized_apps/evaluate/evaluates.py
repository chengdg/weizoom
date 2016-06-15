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
from core import search_util
from modules.member.module_api import get_member_by_id_list
from modules.member.models import Member, MemberHasTag

FIRST_NAV_NAME = export.PRODUCT_FIRST_NAV
COUNT_PER_PAGE = 50

SHORTCUTS_TEXT={
	'phone': u'手机',
	'name': u'姓名',
	'email': u'邮箱',
	'qq':u'QQ号',
	'job':u'职位',
	'addr':u'地址'
}

REVIEW_FILTERS = {
	'review': [
		{
			'comparator': lambda review, filter_value: (filter_value == 'all') or (filter_value == str(review.status)) or (
				filter_value == '1' and review.status == 2),
			'query_string_field': 'reviewStatus'
		}, {
			'comparator': lambda review, filter_value: (filter_value == 'all') or (filter_value == str(review.score)),
			'query_string_field': 'productScore'
		}, {
			'comparator': lambda review, filter_value: filter_value <= review.created_at.strftime("%Y-%m-%d %H:%M"),
			'query_string_field': 'startDate'
		}, {
			'comparator': lambda review, filter_value: filter_value >= review.created_at.strftime("%Y-%m-%d %H:%M"),
			'query_string_field': 'endDate'
		}
	],
	'product': [
		{
			'comparator': lambda product, filter_value: filter_value in product.name,
			'query_string_field': 'name'
		}
	],
}

def _filter_reviews(request, reviews):
	# 处理商品名称、评论时间、审核状态、商品星级
	has_filter = search_util.init_filters(request, REVIEW_FILTERS)
	if not has_filter:
		# 没有filter，直接返回
		return reviews

	reviews = search_util.filter_objects(reviews, REVIEW_FILTERS['review'])
	product_id2review = dict([(review.product_id, review) for review in reviews])
	product_ids = product_id2review.keys()
	products = mall_models.Product.objects.filter(id__in=product_ids)
	products = search_util.filter_objects(products, REVIEW_FILTERS['product'])
	product_ids = [product.id for product in products]
	filter_reviews = []
	for review in reviews:
		if review.product_id in product_ids:
			filter_reviews.append(review)

	return filter_reviews

class Evaluates(resource.Resource):
	app = 'apps/evaluate'
	resource = 'evaluates'
	
	@login_required
	def get(request):
		"""
		商品评价列表
		"""
		woid = request.webapp_owner_id

		export_jobs = ExportJob.objects.filter(woid=woid, type=2, is_download=0).order_by("-id")
		if export_jobs:
			export2data = {
				"woid": int(export_jobs[0].woid),  #
				"status": 1 if export_jobs[0].status else 0,
				"is_download": 1 if export_jobs[0].is_download else 0,
				"id": int(export_jobs[0].id),
				# "file_path": export_jobs[0].file_path,
			}
		else:
			export2data = {
				"woid": 0,
				"status": 1,
				"is_download": 1,
				"id": 0,
				"file_path": 0,
			}
		c = RequestContext(request,{
		   'first_nav_name': FIRST_NAV_NAME,
		   'second_navs': export.get_mall_product_second_navs(request),
		   'second_nav_name': export.PRODUCT_REVIEW_NAV,
		   'export2data': export2data,
	   })
		
		return render_to_response('evaluate/templates/editor/evaluates.html', c)

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
		all_reviews = app_models.ProductEvaluates.objects(owner_id=owner.id).order_by("-created_at")

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
					# from cache import webapp_cache

					# review_product = mall_models.OrderHasProduct.objects.get(id=review.order_has_product_id)
					# product = webapp_cache.get_webapp_product_detail(request.webapp_owner_id, review.product_id)
					# product.fill_specific_model(review_product.product_model_name)
					product = mall_models.Product.objects.get(id=review.product_id)
					if product.user_code == user_code:
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
		# from cache import webapp_cache
		#
		# reviewids = [r.order_has_product_id for r in product_reviews]
		# orderhasproducts = mall_models.OrderHasProduct.objects.filter(id__in=reviewids)
		# review2orderhasproductsmap = dict([(i.id, i) for i in orderhasproducts])

		for review in product_reviews:
			if not hasattr(review, 'product_user_code'):
				# review_product = review2orderhasproductsmap[review.order_has_product_id]
				# review.product_name = review_product.product_name
				# review.product_model_name = review_product.product_model_name
				# product = webapp_cache.get_webapp_product_detail(request.webapp_owner_id, review.product_id)
				# product.fill_specific_model(review.product_model_name)
				review.product_user_code = id2product[review.product_id].user_code
			items.append({
				'id': str(review.id),
				'product_user_code': review.product_user_code,
				'product_name': id2product[review.product_id].name,
				'user_name': member_id2member_name.get(review.member_id, '已经跑路'),
				'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				'content': review.detail,
				'product_id': review.product_id,
				'member_id': review.member_id,
				'product_score': review.score,
				'status': {
					'name': mall_models.PRODUCT_REVIEW_STATUS[int(review.status) + 1][1],  # 返回产品状态
					'value': str(review.status),
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

class EvaluateReview(resource.Resource):
	app = 'apps/evaluate'
	resource = 'evaluate_review'

	@login_required
	def api_get(request):
		"""
		审核评价弹窗
		"""

		evaluate_id = request.GET.get('id',None)
		evaluate = app_models.ProductEvaluates.objects(id = evaluate_id)[0]

		member = Member.objects.get(id = evaluate.member_id)
		member_has_tags = MemberHasTag.get_member_has_tags(member)
		tag_list = []
		for tag in member_has_tags:
			tag_list.append({
				'tag_name': tag.member_tag.name,
				'tag_id': tag.member_tag.id
			})

		is_common_template = True
		evaluate_detail = evaluate.detail
		if isinstance(evaluate_detail, dict):
			is_common_template = False
			# 组织自定义模板用户评价数据结构
			evaluate_detail = get_evaluate_detail(evaluate_detail)

		items = {
			'time': evaluate.created_at.strftime('%Y/%m/%d'),
			'score': evaluate.score,
			'detail': evaluate_detail,
			'img': evaluate.pics,
			'product_name': mall_models.Product.objects.get(id = evaluate.product_id).name,
			'order_num': evaluate.order_id, #订单号
			'member_id': member.id,
			'member_name': member.username_for_html,
			'member_grade': member.grade.name,
			'shop_reply': evaluate.shop_reply,
			'member_has_tags': tag_list,
			'order_id': mall_models.Order.objects.get(order_id = evaluate.order_id).id,
			'is_common_template': is_common_template
		}

		response = create_response(200)
		response.data = {
			'items': items,
		}
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		审核评价
		"""
		# 单个修改
		if "product_review_id" in request.POST:
			product_review_id = request.POST.get("product_review_id", None)
			status = request.POST.get("status", None)
			from modules.member.integral import increase_member_integral
			from modules.member import models as member_models

			if product_review_id:
				review = app_models.ProductEvaluates.objects(owner_id=request.webapp_owner_id, id=product_review_id)
				if status == '2' or status == '1':
					if len(review) == 1 and int(review[0].status) == 0:
						settings = member_models.IntegralStrategySttings.objects.get(
							webapp_id=request.user_profile.webapp_id)
						if settings.review_increase > 0:
							member = member_models.Member.objects.filter(id=review[0].member_id)
							if len(member):
								increase_member_integral(member[0], settings.review_increase, '商品评价奖励')

				if status == '2':
					product_review = app_models.ProductEvaluates.objects.get(id=product_review_id)
					top_reviews = app_models.ProductEvaluates.objects.filter(product_id=product_review.product_id,
																		   status=int(status)).order_by("top_time")
					if top_reviews.count() >= 3:
						ids = [review.id for review in top_reviews[:(top_reviews.count() - 2)]]
						app_models.ProductEvaluates.objects(id__in=ids).update(status=1,
																				top_time=app_models.DEFAULT_DATETIME)
						app_models.ProductEvaluates.objects(id=product_review_id).update(status=int(status),
																							  top_time=datetime.now())
					else:
						app_models.ProductEvaluates.objects(id=product_review_id).update(status=int(status),
																							  top_time=datetime.now())
				else:
					review.update(status=int(status), top_time=app_models.DEFAULT_DATETIME)
				return create_response(200).get_response()
			else:
				return create_response(500).get_response()
		# 批量修改
		else:
			ids = request.POST.get("ids", '')
			action = request.POST.get("action", '')
			ids = ids.split(',')

			from modules.member.integral import increase_member_integral
			from modules.member import models as member_models

			if action == 'pass':
				try:
					reviews = app_models.ProductEvaluates.objects(owner_id=request.webapp_owner_id, id__in=ids)

					settings = member_models.IntegralStrategySttings.objects.get(
						webapp_id=request.user_profile.webapp_id)
					if settings.review_increase > 0:
						# 处理增加积分
						increase_integral_member_ids = []
						for review in reviews:
							if int(review.status) == 0:
								increase_integral_member_ids.append(review.member_id)

						if len(increase_integral_member_ids) > 0:
							members = member_models.Member.objects.filter(id__in=increase_integral_member_ids)
							id2member = dict((member.id, member) for member in members)
							for review in reviews:
								if int(review.status) == 0:
									increase_member_integral(id2member[review.member_id], settings.review_increase,
															 '商品评价奖励')
					reviews.update(status=1, top_time=app_models.DEFAULT_DATETIME)
					return create_response(200).get_response()
				except:
					return create_response(500).get_response()
			else:
				try:
					app_models.ProductEvaluates.objects(owner_id=request.webapp_owner_id, id__in=ids).update(status=-1)
					return create_response(200).get_response()
				except:
					return create_response(500).get_response()

class EvaluateReviewShopReply(resource.Resource):
	app = 'apps/evaluate'
	resource = 'evaluate_review_shop_reply'

	@login_required
	def api_post(request):
		"""
		商户给会员评价&修改会员等级
		@return:
		"""
		reply = request.POST.get('content', '')
		tag_ids = request.POST.get('tag_ids', None)
		product_review_id = request.POST.get("product_review_id", None)
		member_id = request.POST.get('member_id', None)
		member = Member.objects.get(id=member_id)

		try:
			app_models.ProductEvaluates.objects(id = product_review_id).update(
				shop_reply = reply
			)

			if tag_ids:
				tag_id_list = json.loads(tag_ids)
				MemberHasTag.delete_tag_member_relation_by_member(member)
				MemberHasTag.add_tag_member_relation(member, tag_id_list)

			response = create_response(200)
			return response.get_response()
		except:
			response = create_response(500)
			return response.get_response()

def get_evaluate_detail(evaluate_detail):
	#组织自定义模板用户评价数据结构
	evaluate_detail_list = []
	for key, value in evaluate_detail.items():
		value = evaluate_detail[key]
		if 'textlist' in key.split('::'):
			for k in value:
				shortcut_name = k
				if k in SHORTCUTS_TEXT:
					shortcut_name = SHORTCUTS_TEXT[k]
				evaluate_detail_list.append({
					'title': shortcut_name,
					'answer': value[k]
				})
		elif 'qa' in key.split('::'):
			qa_title, qa_answer = value.split('::')
			evaluate_detail_list.append({
				'title': qa_title,
				'answer': qa_answer
			})
		elif 'selection' in key.split('::'):
			if isinstance(value, list):
				mul_select_answers = []
				for select in value:
					mul_select_title, mul_select_answer, num = select.split('::')
					mul_select_answers.append(mul_select_answer)
				evaluate_detail_list.append({
					'title': mul_select_title,
					'answer': ','.join(mul_select_answers)
				})
			elif isinstance(value, basestring):
				select_title, select_answer, num = value.split('::')
				evaluate_detail_list.append({
					'title': select_title,
					'answer': select_answer
				})

	return evaluate_detail_list
