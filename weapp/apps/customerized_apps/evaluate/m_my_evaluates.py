# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from mall import models as mall_models

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
		# app_models.ProductEvaluates.objects().create(
		# 	owner_id = request.webapp_owner_id,
		# 	member_id = 19,
		# 	order_id = '15245',
		# 	product_id = 19,
		# 	score = 5,
		# 	detail = u'asdabsjkdhasuicyzxc,zxnc,m',
		# 	pics = [],
		# 	created_at = datetime.now(),
		# 	status = 1
		# )

		webapp_owner_id = request.webapp_owner_id
		member_id = request.member.id

		product_review_list = app_models.ProductEvaluates.objects.filter(owner_id = webapp_owner_id,
																		 member_id=member_id).order_by('-id')

		# 构造所需商品信息
		product_id_list = set([review.product_id for review in product_review_list])
		products = mall_models.Product.objects.filter(id__in=product_id_list)
		review_products = {}
		for product in products:
			review_products[product.id] = product

		# 构造商品评价列表
		for product_review in product_review_list:
			product_review.product = review_products.get(product_review.product_id)

		c = RequestContext(request, {
			'page_title': "我的评价",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'reviewed_products': product_review_list,
		})


		return render_to_response('evaluate/templates/webapp/m_my_evaluates.html', c)

