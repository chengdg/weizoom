# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response

import models as app_models
from mall import export as mall_export

FIRST_NAV = mall_export.PRODUCT_FIRST_NAV

class Evaluate(resource.Resource):
	app = 'apps/evaluate'
	resource = 'evaluate'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		evaluate = None
		select_type = 'ordinary'
		is_create_new_data = True
		project_id = 'new_app:evaluate:0'
		try:
			evaluate = app_models.EvaluateTemplateSetting.objects.get(owner_id=request.manager.id)
			select_type = evaluate.template_type
			related_page_id = evaluate.related_page_id
			project_id = 'new_app:evaluate:%s' % related_page_id
			is_create_new_data = False
		except:
			pass

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_mall_product_second_navs(request),
			'second_nav_name': mall_export.PRODUCT_REVIEW_NAV,
			'evaluate': evaluate,
			'is_create_new_data': is_create_new_data,
			'project_id': project_id,
			'select_type': select_type
		})
		
		return render_to_response('evaluate/templates/editor/workbench.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应PUT
		"""
		evaluate = app_models.EvaluateTemplateSetting(
			owner_id = request.manager.id,
			template_type = request.POST['template_type'],
			related_page_id = request.POST['related_page_id']
		)
		evaluate.save()

		response = create_response(200)
		return response.get_response()
	
	@login_required
	def api_post(request):
		"""
		响应POST
		"""
		app_models.EvaluateTemplateSetting.objects(owner_id=request.manager.id).update(set__template_type=request.POST.get('template_type', 'ordinary'))
		response = create_response(200)
		return response.get_response()

