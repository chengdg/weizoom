# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response

from termite2 import export
from webapp import models as webapp_models

FIRST_NAV = export.WEPAGE_FIRST_NAV
COUNT_PER_PAGE = 20

class Pages(resource.Resource):
	app = 'termite2'
	resource = 'pages'

	@login_required
	def get(request):
		"""
		微页面列表页
		"""
		has_page = webapp_models.Project.objects.filter(owner=request.user, is_enable=True).count() > 0
		pages = []
		if request.user.is_manager:
			pages = webapp_models.Project.objects.filter(owner=request.user, is_enable=True)
			active_page = None
		else:
			active_page = webapp_models.Project.objects.filter(owner=request.user, is_active=True)[0]

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_wepage_second_navs(request),
			'second_nav_name': export.WEPAGE_PAGES_NAV,
			'has_page': has_page,
			'pages': pages,
			'active_page': active_page
		});

		if request.user.is_manager:
			return render_to_response('termite2/manager_pages.html', c)
		else:
			return render_to_response('termite2/pages.html', c)


	@login_required
	def api_get(request):
		"""
		微页面列表页
		"""
		projects = webapp_models.Project.objects.filter(owner=request.user, is_enable=True)

		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, projects = paginator.paginate(projects, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		items = []
		for project in projects:
			item = {
				"id": project.id,
				"index": project.id,
				"siteTitle": project.site_title,
				"createdAt": project.created_at.strftime("%Y-%m-%d %H:%M"),
				"isActive": project.is_active,
				"name": 'project %s' % project.id
			}
			if project.is_active:
				item['index'] = 99999999999

			items.append(item)

		#首页置顶
		items.sort(lambda x,y: cmp(y['index'], x['index']))
		
		data = {
			"items": items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}
		response = create_response(200)
		response.data = data
		return response.get_response()
