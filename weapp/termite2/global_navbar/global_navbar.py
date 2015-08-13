# -*- coding: utf-8 -*-

import json
import qrcode, os

from core import resource
from core.jsonresponse import create_response, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

import termite2.models as termite_models
from django.conf import settings
from termite2 import export
from termite import pagestore as pagestore_manager


FIRST_NAV = export.WEPAGE_FIRST_NAV
class GlobalNavbar(resource.Resource):
	"""
	导航
	"""
	app = 'termite2'
	resource = 'global_navbar'

	@login_required
	def get(request):
		"""
		导航渲染页面

		project_id的格式为：
		fake:${project_type}:${webapp_owner_id}:${page_id}:${mongodb_id}
		"""
		pagestore = pagestore_manager.get_pagestore_by_type('mongo')
		project_id = 'fake:wepage:%d:navbar' % request.user.id
		page_id = 'navbar'
		
		page = pagestore.get_page(project_id, page_id)
		if page:
			mongodb_id = str(page['_id'])
		else:
			mongodb_id = 'new'
		project_id = '%s:%s' % (project_id, mongodb_id)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_wepage_second_navs(request),
			'second_nav_name': export.WEPAGE_GLOBAL_NAVBAR_NAV,
			'is_new_navbar': True,
			'project_id': project_id
		})
		return render_to_response('termite2/global_navbar_editor.html', c)


	@login_required
	def api_put(request):
		"""
		导航 保存
		"""
		# pagestore = pagestore_manager.get_pagestore('mongo')
		content = request.POST.get('content', '')
		pages = request.POST.get('pages', '')
		user = request.user

		# 修改 content
		global_navbar, created = termite_models.TemplateGlobalNavbar.get_object(user)
		global_navbar.content = content
		global_navbar.save()

		# 修改 应用页面
		if pages is not '':
			pages = pages.split(',')
			for page_type in pages:            
				page = termite_models.PageHasGlobalNavbar.get_object(user, page_type, global_navbar)
				page.is_enable = True
				page.save()

			# 将其它 应用页面 设置为不启用
			termite_models.PageHasGlobalNavbar.objects.filter(owner=user, global_navbar=global_navbar).exclude(page_type__in=pages).update(is_enable=False)

		response = create_response(200)
		return response.get_response()