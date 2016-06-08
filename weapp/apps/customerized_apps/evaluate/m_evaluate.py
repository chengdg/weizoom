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
			'order_has_product_id': param.get('order_has_product_id', ''),
			'order_id': param.get('order_id', ''),
			'product_id': param.get('product_id', ''),
			'product_model_name': param.get('product_model_name', '')
		})

		return render_to_response('evaluate/templates/webapp/m_evaluate.html', c)

	def api_get(request):
		"""
		获取商品以及评价数据
		@return:
		"""
		param = request.GET
		order_has_product_id = param.get('order_has_product_id', ''),
		order_id = param.get('order_id', ''),
		product_id = param.get('product_id', ''),
		product_model_name = param.get('product_model_name', '')

		order = Order.objects.get(order_id=order_id)
		order_has_products = OrderHasProduct.objects.filter(order=order, origin_order_id=0)

def render_deleted_page(request):
	c = RequestContext(request,{
		'is_deleted_data': True
	})
	return render_to_response('workbench/wepage_webapp_page.html', c)
