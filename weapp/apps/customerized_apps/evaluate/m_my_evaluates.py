# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from mall import models as mall_models
import mall.module_api as mall_api

from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
import export
from apps import request_util
from termite2 import pagecreater
import weixin.user.models as weixin_models

class MyEvaluates(resource.Resource):
	app = 'apps/evaluate'
	resource = 'm_my_evaluates'
	
	def get(request):
		"""
		响应GET
		"""
		webapp_owner_id = request.webapp_owner_id
		member_id = request.member.id

		product_reviews = app_models.ProductEvaluates.objects.filter(owner_id = webapp_owner_id,
																		 member_id=member_id).order_by('-id')

		# 构造所需商品信息
		product_id_list = set([review.product_id for review in product_reviews])
		products = mall_models.Product.objects.filter(id__in=product_id_list)
		review_products = {product.id:product for product in products}

		#构造订单信息
		order_ids = [review.order_id for review in product_reviews]
		orders = mall_models.Order.objects.filter(order_id__in = order_ids)
		order_id2order = {order.order_id: order for order in orders}

		product_review_list = []
		for review in product_reviews:
			order_id = review.order_id
			order = order_id2order.get(order_id, None)
			# 根据订单获取商品
			products = mall_api.get_order_products(order)
			#根据商品评价的product_id拿到products中的所属商品信息
			product_dic = {}
			product_name = review_products[review.product_id].name
			for product in products:
				if product['name'] == product_name:
					product_dic = product

			product_review_list.append({
				'detail': review.detail,
				'created_at': review.created_at,
				'pics': review.pics,
				'product': product_dic,
				'shop_reply': review.shop_reply
			})

		c = RequestContext(request, {
			'page_title': "我的评价",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'reviewed_products': product_review_list,
		})


		return render_to_response('evaluate/templates/webapp/m_my_evaluates.html', c)

