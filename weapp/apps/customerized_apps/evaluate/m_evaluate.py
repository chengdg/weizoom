# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
import export
from apps import request_util
from mall.models import Order, OrderHasProduct
from termite2 import pagecreater
from cache import webapp_cache
import weixin.user.models as weixin_models

class MEvaluate(resource.Resource):
	app = 'apps/evaluate'
	resource = 'm_evaluate'
	
	def get(request):
		"""
		渲染评价页面
		"""
		param = request.GET
		owner_id = param.get('woid', request.webapp_owner_id)
		template_type = 'ordinary'

		records = app_models.EvaluateTemplateSetting.objects(owner_id=int(owner_id))
		if records.count() > 0 and 'ordinary' != records.first().template_type:
			project_id = 'new_app:evaluate:%s' % records.first().related_page_id
			request.GET._mutable = True
			request.GET.update({"project_id": project_id})
			request.GET._mutable = False
			html = pagecreater.create_page(request, return_html_snippet=True)
			template_type = 'custom'
		else: #读取组件页面
			component_file = open(os.path.join(settings.PROJECT_HOME, '..', 'termite', 'static', 'termite_js', 'app', 'component', 'appkit', 'evaluatedescription', 'evaluatedescription.html'), 'r')
			html = component_file.read()
			html = html[html.index('<!--R-->')+8:html.rindex('<!--R-->')]
			component_file.close()

		c = RequestContext(request, {
			'page_title': "商品评价",
			'page_html_content': html,
			'app_name': "evaluate",
			'resource': "m_evaluate",
			'is_hide_weixin_option_menu': True,
			'template_type': template_type,
			'order_has_product_id': param.get('order_has_product_id', '1'),
			'order_id': param.get('order_id', '1'),
			'product_id': param.get('product_id', '1'),
			'product_model_name': param.get('product_model_name', 'test')
		})

		return render_to_response('evaluate/templates/webapp/m_evaluate.html', c)

	def api_get(request):
		"""
		获取商品以及评价数据
		"""
		response = create_response(500)
		member = request.member
		if not member:
			response.errMsg = u'会员信息出错'
			return response.get_response()
		param = request.GET
		order_id = param.get('order_id', None)
		product_model_name = param.get('product_model_name', None)
		order_has_product_id = int(param.get('order_has_product_id', None))
		product_id = param.get('product_id', None)

		order_review_count = app_models.OrderEvaluates.objects(
			owner_id=member.id,
			order_id=order_id,
		).count()
		has_order_review = order_review_count > 0

		# 得到商品信息, 如果商品已不存在（下架..）, 返回错误
		try:
			product = webapp_cache.get_webapp_product_detail(request.webapp_owner_id,product_id)
			product = product
			product.fill_specific_model(product_model_name, product.models)
		except:
			response.errMsg = u'商品信息出错'
			return response.get_response()

		created = True
		#检查是否已评价过
		product_review_dict = {}
		try:
			product_review = app_models.ProductEvaluates.objects.get(order_has_product_id=order_has_product_id)
			product_review_dict = {
				'id': product_review.id,
				'product_score': product_review.product_score,
				'review_detail': product_review.review_detail,
				'has_pic': len(product_review.pics) > 0
			}
			created = False
		except:
			pass

		response = create_response(200)
		response.data = {
			'product': {
				'thumbnails_url': product.thumbnails_url,
				'id': product.id,
				'name': product.name,
				'props': ' / '.join([model.property_value for model in product.custom_model_properties]) if product.custom_model_properties else ''
			},
			'product_review': product_review_dict,
			'order_has_product_id': order_has_product_id,
			'has_order_review': has_order_review,
			'order_id': order_id,
			'created': created
		}
		return response.get_response()

def render_deleted_page(request):
	c = RequestContext(request,{
		'is_deleted_data': True
	})
	return render_to_response('workbench/wepage_webapp_page.html', c)
