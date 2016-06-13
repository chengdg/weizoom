# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from core import resource

class EvaluatesSucceed(resource.Resource):
	app = 'apps/evaluate'
	resource = 'm_evaluate_success'
	
	def get(request):
		"""
		响应GET
		"""
		c = RequestContext(request, {
			'h5_host': settings.APPS_H5_DOMAIN,
			'page_title': u'评价成功',
			'is_hide_weixin_option_menu': True,
			'has_waiting_review': True
		})


		return render_to_response('evaluate/templates/webapp/m_evaluate_success.html', c)
