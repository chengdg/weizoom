# -*- coding: utf-8 -*-
import json
from excel_response import ExcelResponse
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from celery.execute import send_task

from core import resource
from core import paginator
from core.jsonresponse import create_response
from core import search_util

from mall import export
from mall import models as mall_models

from export_job.models import ExportJob

from modules.member.module_api import get_member_by_id_list, get_member_info_by
from modules.member.models import Member, MemberHasTag
from modules.member.integral import increase_member_integral
from modules.member import models as member_models

import models as app_models


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
		c = RequestContext(request,{
		   'first_nav_name': FIRST_NAV_NAME,
		   'second_navs': export.get_mall_product_second_navs(request),
		   'second_nav_name': export.PRODUCT_REVIEW_NAV,
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

			is_common_template = True
			review_detail = review.detail
			if isinstance(review_detail, dict):
				is_common_template = False
				# 组织自定义模板用户评价数据结构
				is_review_dialog = True
				review_detail = get_evaluate_detail(review_detail, is_review_dialog)

			items.append({
				'id': str(review.id),
				'product_user_code': review.product_user_code,
				'product_name': id2product[review.product_id].name,
				'user_name': member_id2member_name.get(review.member_id, '已经跑路'),
				'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				'detail': review_detail,
				'product_id': review.product_id,
				'member_id': review.member_id,
				'product_score': review.score,
				'status': {
					'name': mall_models.PRODUCT_REVIEW_STATUS[int(review.status) + 1][1],  # 返回产品状态
					'value': str(review.status),
				},
				'is_common_template': is_common_template
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
			is_review_dialog = True
			evaluate_detail = get_evaluate_detail(evaluate_detail, is_review_dialog)

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

			if product_review_id:
				review = app_models.ProductEvaluates.objects(owner_id=request.webapp_owner_id, id=product_review_id)
				first_review = review.first()
				if status == '2' or status == '1':
					if review.count() == 1 and int(first_review.status) == 0:
						settings = member_models.IntegralStrategySttings.objects.get(
							webapp_id=request.user_profile.webapp_id)
						if settings.review_increase > 0:
							member = member_models.Member.objects.filter(id=first_review.member_id)
							if len(member):
								increase_member_integral(member[0], settings.review_increase, '商品评价奖励')
								#发送积分变动模版
								send_task('services.weixin_template_service.task.service_template_message', args={
									'user_id': request.webapp_owner_id,
									'reason': u'商品评价奖励',
									'event_type': 7,
									'member_id': member[0].id,
									'url': '',
									'items': {
										'keyword1': member[0].username_hexstr.decode('hex').decode('utf-8'),
										'keyword2': datetime.now().strftime(u'%Y年%m月%d日 %H:%M'),
										'keyword3': settings.review_increase,
										'keyword4': member[0].integral,
										'keyword5': u'商品评价奖励'
									}
								})

				if status == '2':
					try:
						#商品评价关联，则关联的商品最多有三个置顶
						product_id = first_review.product_id
						related_product = app_models.EvaluatesRelatedProducts.objects.get(product_id=product_id)
						related_product_ids = app_models.EvaluatesRelations.objects.get(id=related_product.belong_to).related_product_ids
						top_reviews = app_models.ProductEvaluates.objects.filter(product_id__in=related_product_ids,status=int(status)).order_by("top_time")
					except:
						#商品评价没有关联，单个商品也只能最多有三个置顶
						product_review = app_models.ProductEvaluates.objects.get(id=product_review_id)
						top_reviews = app_models.ProductEvaluates.objects.filter(product_id=product_review.product_id,
																		   status=int(status)).order_by("top_time")
					if top_reviews.count() >= 3:
						ids = [re.id for re in top_reviews[:(top_reviews.count() - 2)]]
						app_models.ProductEvaluates.objects(id__in=ids).update(set__status=app_models.STATUS_PASSED,
																				set__top_time=app_models.DEFAULT_DATETIME)
						app_models.ProductEvaluates.objects(id=product_review_id).update(set__status=int(status),
																							  set__top_time=datetime.now())
					else:
						app_models.ProductEvaluates.objects(id=product_review_id).update(set__status=int(status),
																							  set__top_time=datetime.now())
				else:
					review.update(set__status=int(status), set__top_time=app_models.DEFAULT_DATETIME)
				return create_response(200).get_response()
			else:
				return create_response(500).get_response()
		# 批量修改
		else:
			ids = request.POST.get("ids", '')
			action = request.POST.get("action", '')
			ids = ids.split(',')

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
									#发送积分变动模版
									send_task('services.weixin_template_service.task.service_template_message', args={
										'user_id': request.webapp_owner_id,
										'reason': u'商品评价奖励',
										'event_type': 7,
										'member_id': id2member[review.member_id].id,
										'url': '',
										'items': {
											'keyword1': id2member[review.member_id].username_hexstr.decode('hex').decode('utf-8'),
											'keyword2': datetime.now().strftime(u'%Y年%m月%d日 %H:%M'),
											'keyword3': settings.review_increase,
											'keyword4': id2member[review.member_id].integral,
											'keyword5': u'商品评价奖励'
										}
									})
					reviews.update(set__status=app_models.STATUS_PASSED, set__top_time=app_models.DEFAULT_DATETIME)
					return create_response(200).get_response()
				except:
					return create_response(500).get_response()
			else:
				try:
					app_models.ProductEvaluates.objects(owner_id=request.webapp_owner_id, id__in=ids).update(set__status=app_models.STATUS_DENIED)
					return create_response(200).get_response()
				except:
					return create_response(500).get_response()

class EvaluateReviewShopReply(resource.Resource):
	app = 'apps/evaluate'
	resource = 'evaluate_review_shop_reply'

	@login_required
	def api_post(request):
		"""
		商户给会员评价
		@return:
		"""
		reply = request.POST.get('content', '')
		product_review_id = request.POST.get("product_review_id", None)

		try:
			app_models.ProductEvaluates.objects(id = product_review_id).update(
				set__shop_reply = reply
			)

			response = create_response(200)
			return response.get_response()
		except:
			response = create_response(500)
			return response.get_response()

class EvaluatesExport(resource.Resource):
	app = 'apps/evaluate'
	resource = 'evaluates_export'

	@login_required
	def api_get(request):
		"""
		评价列表导出
		@return:
		"""
		user_code = request.GET.get('userCode', '')

		# 当前用户
		owner = request.manager
		all_reviews = app_models.ProductEvaluates.objects(owner_id=owner.id).order_by("-created_at")

		all_reviews = _filter_reviews(request, all_reviews)

		# 处理商品编码
		product_reviews = []
		if user_code:
			for review in all_reviews:
				product = mall_models.Product.objects.get(id=review.product_id)
				if product.user_code == user_code:
					review.product_user_code = user_code
					product_reviews.append(review)
		else:
			product_reviews = all_reviews

		# 处理商品
		product_ids = [review.product_id for review in product_reviews]
		id2product = dict([(product.id, product) for product in mall_models.Product.objects.filter(id__in=product_ids)])
		# 处理会员
		member_ids = [review.member_id for review in product_reviews]
		members = get_member_by_id_list(member_ids)
		member_id2member = dict([(m.id, m) for m in members])

		members_info = [
			[u'商品名称', u'订单号', u'姓名', u'电话', u'评价时间', u'状态', u'产品评星', u'图片链接', u'评价内容']
		]

		for review in product_reviews:
			member_info = get_member_info_by(review.member_id)
			review_detail = review.detail
			#处理自定义模板评价内容
			if isinstance(review_detail, dict):
				review_detail_list = get_evaluate_detail(review_detail, is_review_dialog=False)
				try:
					member = member_id2member.get(review.member_id, None)
					i=0
					for re in review_detail_list:
						info_list = [
							id2product[review.product_id].name if i == 0 else '',
							review.order_id if i == 0 else '',
							member.username_for_html if i == 0 else '' if member else u'已经跑路',
							member_info.phone_number if i == 0 else '' if member_info else '',
							review.created_at.strftime("%Y-%m-%d %H:%H:%S") if i == 0 else '',
							app_models.EVALUATE_STATUS[review.status] if i == 0 else '',
							review.score if i == 0 else '',
							review.pics if i == 0 else '',
							'【%s】%s' % (re['title'],re['answer'])
						]
						members_info.append(info_list)
						i += 1
				except:
					pass
			else:
				try:
					member = member_id2member.get(review.member_id, None)
					info_list = [
						id2product[review.product_id].name,
						review.order_id,
						member.username_for_html if member else u'已经跑路',
						member_info.phone_number if member_info else '',
						review.created_at.strftime("%Y-%m-%d %H:%H:%S"),
						app_models.EVALUATE_STATUS[review.status],
						review.score,
						review.pics,
						review_detail
					]
					members_info.append(info_list)
				except:
					pass

		filename = u'评价列表'
		return ExcelResponse(members_info, output_name=filename.encode('utf8'), force_csv=False)

def get_evaluate_detail(evaluate_detail, is_review_dialog = False):
	from operator import itemgetter
	#组织自定义模板用户评价数据结构
	evaluate_detail_list = []
	for key, value in evaluate_detail.items():
		keys = key.split('::')
		index = keys[1]
		#参与人信息只展示在后台的审核弹窗里
		if is_review_dialog:
			if 'textlist' in keys:
				for k in value:
					shortcut_name = k
					if k in SHORTCUTS_TEXT:
						shortcut_name = SHORTCUTS_TEXT[k]
					evaluate_detail_list.append({
						'title': shortcut_name,
						'answer': value[k],
						'index': int(index)
					})
		if 'qa' in keys:
			qa_title, qa_answer = value.split('::')
			evaluate_detail_list.append({
				'title': qa_title,
				'answer': qa_answer,
				'index': int(index)
			})
		if 'selection' in keys:
			if isinstance(value, list):
				mul_select_answers = []
				mul_select_title = ''
				for select in value:
					mul_select_title, mul_select_answer, num = select.split('::')
					mul_select_answers.append(mul_select_answer)
				if mul_select_title and mul_select_answers:
					evaluate_detail_list.append({
						'title': mul_select_title,
						'answer': ','.join(mul_select_answers),
						'index': int(index)
					})
			elif isinstance(value, basestring):
				select_title, select_answer, num = value.split('::')
				evaluate_detail_list.append({
					'title': select_title,
					'answer': select_answer,
					'index': int(index)
				})
	evaluate_detail_list = sorted(evaluate_detail_list, key=itemgetter('index'))

	return evaluate_detail_list
