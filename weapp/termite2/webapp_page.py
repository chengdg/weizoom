# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from webapp import models as webapp_models

from termite2 import pagecreater
from termite.workbench import jqm_views


class WebappPage(resource.Resource):
	app = 'termite2'
	resource = 'webapp_page'

	def get(request):
		"""
		webapp页面（目前是首页）
		"""
		if 'model' in request.GET:
			return jqm_views.show_preview_page(request)

		project_id = request.REQUEST.get('project_id', 0)
		if project_id == 0:
			response = create_response(500)
			response.errMsg = u'没有project_id参数'
			return response.get_response()
		html = pagecreater.create_page(request, return_html_snippet=True)

		c = RequestContext(request, {
			'page_title': u'微站首页',
			'page_html_content': html,
			'hide_non_member_cover': True #非会员也可使用该页面
		})

		return render_to_response('workbench/wepage_webapp_page.html', c)
