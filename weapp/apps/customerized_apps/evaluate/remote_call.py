# -*- coding: utf-8 -*-
from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack

import models as apps_models
from mall.models import Order
from modules.member.models import Member


def _get_order_id_to_id(evaluates):
	order_ids = [p.order_id for p in evaluates]
	return {o.order_id: o.id for o in Order.objects.filter(order_id__in=order_ids)}

class GetProductEvaluatesStatus(resource.Resource):
	app = 'apps/evaluate'
	resource = 'get_product_evaluates_status'

	def api_get(request):
		"""
		个人中心-待评价订单，获取待评价订单的评价状态
		@params woid, member_id
		@return:{
				  "orders": [
					  {'order_id':6789,
					  'order_is_reviewed':True,
					  'order_product':
						  [{'product_id':3333333,
							'order_has_product_id':5555555,
							'has_reviewed_picture':True,
							'has_reviewed':True
							}]
					  }
					]
				}
		"""

		owner_id = request.GET.get('woid', None)
		member_id = request.GET.get('member_id', None)
		response = create_response(500)
		if not owner_id or not member_id:
			response.errMsg = u'参数错误'
			return response.get_response()
		evaluates = apps_models.ProductEvaluates.objects(owner_id=int(owner_id), member_id=int(member_id))
		order_id2id = _get_order_id_to_id(evaluates)
		order_id2evaluiates = dict()
		for evaluate in evaluates:
			order_id = order_id2id.get(evaluate.order_id, 0)
			has_reviewed = False
			if isinstance(evaluate.detail, dict):
				for k, v in evaluate.detail.items():
					if (k.find('qa') >= 0 and v) or (k.find('selection') >= 0 and v):
						has_reviewed = True
						break
			else:
				has_reviewed = True
			temp_dict = {
				'product_id': evaluate.product_id,
				'order_has_product_id': evaluate.order_has_product_id,
				'has_reviewed_picture': len(evaluate.pics) > 0,
				'has_reviewed': has_reviewed
			}
			if not order_id2evaluiates.has_key(order_id):
				order_id2evaluiates[order_id] = [temp_dict]
			else:
				order_id2evaluiates[order_id].append(temp_dict)
		orders = []
		for k, v in order_id2evaluiates.items():
			orders.append({
				'order_id': k,
				'order_is_reviewed': v['has_reviewed_picture'],
				'order_product': v
			})
		response = create_response(200)
		response.data = {'orders': orders}
		return response.get_response()

class GetProductEvaluates(resource.Resource):
	app = 'apps/evaluate'
	resource = 'get_product_evaluates'

	def api_get(request):
		"""
		商品详情-两条评价信息
		@params woid, product_id
		@return {
			'product_reviews': [{
				'status': 2,
				'member_icon': '',
				'created_at': '2016-06-06 10:32:10',
				'member_id': 1,
				'review_detail': '',
				'member_name': 'bill'
			}],
			'has_more': True
		}
		"""
		owner_id = request.GET.get('woid', None)
		product_id = request.GET.get('product_id', None)
		response = create_response(500)
		if not owner_id or not product_id:
			response.errMsg = u'参数错误'
			return response.get_response()

		#需要考虑到评价相关联的商品
		owner_id=int(owner_id)
		product_id = int(product_id)
		relations = apps_models.EvaluatesRelatedProducts.objects(owner_id=owner_id, product_id=product_id)
		if relations.count() > 0:
			product_ids = apps_models.EvaluatesRelations.objects(id=relations.first().belong_to).first().related_product_ids
		else:
			product_ids = [product_id]

		evaluates = apps_models.ProductEvaluates.objects(owner_id=owner_id, product_id__in=product_ids, status__in=[apps_models.STATUS_PASSED, apps_models.STATUS_TOP]).order_by('-top_time', '-created_at')
		member_ids = [e.member_id for e in evaluates]
		member_id2info = {m.id: {'icon': m.user_icon, 'name': m.username_for_title} for m in Member.objects.filter(id__in=member_ids)}
		result = []
		count = 0
		for evaluate in evaluates:
			count += 0
			member_id = evaluate.member_id
			detail = evaluate.detail
			temp_detail = []
			if isinstance(detail, dict):
				for k, v in detail.items():
					if (k.find('qa') >= 0 and v) or (k.find('selection') >= 0 and v):
						temp_detail.append(v.split('::')[1])
				temp_detail = u'；'.join(temp_detail)
			else:
				temp_detail = detail

			result.append({
				'status': evaluate.status,
				'member_icon': member_id2info[member_id]['icon'],
				'created_at': evaluate.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				'member_id': member_id,
				'review_detail': temp_detail,
				'member_name': member_id2info[member_id]['name']
			})
			if count >= 2:
				break
		response = create_response(200)
		response.data = {
			'product_reviews': result,
			'has_more': evaluates.count() > 2
		}
		return response.get_response()

class GetUnreviewdCount(resource.Resource):
	app = 'apps/evaluate'
	resource = 'get_unreviewd_count'

	def api_get(request):
		"""
		个人中心-待评价(获取待评价的个数) 当前会员所有未晒图的产品
		@param	order_has_product_list_ids
		@return: {
				"reviewed_count": int
			}
		"""
		response = create_response(500)
		order_has_product_list_ids = request.GET.get('order_has_product_list_ids', None)
		if not order_has_product_list_ids:
			response.errMsg = u'缺少参数'
			return response.get_response()
		order_has_product_list_ids = map(lambda x: int(x), order_has_product_list_ids.split('_'))
		try:
			count = apps_models.ProductEvaluates.objects(order_has_product_id__in=order_has_product_list_ids, pics__ne=[]).count()
			response = create_response(200)
			response.data = {
				"reviewed_count": count
			}
			return response.get_response()
		except:
			response.errMsg = u'查询失败'
			return response.get_response()

class GetOrderEvaluatesStatus(resource.Resource):

	app = 'apps/evaluate'
	resource = 'get_order_evaluates'

	def api_get(request):
		"""
		个人中心-全部订单，获取订单的评价状态
		@param woid, member_id
		@return: {
	                  "orders": [
	                      {'order_id':6789,
	                      'order_is_reviewed':True,
	                      }]
	                }
		"""
		owner_id = request.GET.get('woid', None)
		member_id = request.GET.get('member_id', None)
		response = create_response(500)
		if not owner_id or not member_id:
			response.errMsg = u'参数错误'
			return response.get_response()
		order_evas = apps_models.OrderEvaluates.objects(owner_id=int(owner_id), member_id=int(member_id))
		order_id2id = _get_order_id_to_id(order_evas)
		response = create_response(200)
		response.data = {'orders': [{'order_id': order_id2id.get(o.order_id, 0), 'order_is_reviewed': True} for o in order_evas]}
		return response.get_response()