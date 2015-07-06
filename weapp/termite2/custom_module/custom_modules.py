# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F

from termite2 import export
import termite2.models as termite_models
from core import resource
from core import paginator
from core.jsonresponse import create_response
from weixin.mp_decorators import mp_required

COUNT_PER_PAGE = 20
FIRST_NAV = export.WEPAGE_FIRST_NAV

class CustomModules(resource.Resource):
	"""
	自定义模块列表
	"""
	app = 'termite2'
	resource = 'custom_modules'

	@login_required
	@mp_required
	def get(request):
		"""
		获取自定义模块
		"""
		custom_module_count = termite_models.TemplateCustomModule.objects.filter(owner=request.manager, is_deleted=False).count()
		if custom_module_count > 0:
			has_custom_module = True
		else:
			has_custom_module = False

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_wepage_second_navs(request),
			'second_nav_name': export.WEPAGE_MODULES_NAV,
			'has_custom_module': has_custom_module
		})

		return render_to_response('termite2/custom_modules.html', c)
	
	def api_get(request):
		"""
		获取自定义模块的json表示
		"""
		selected_custom_module_id = int(request.GET.get('selected_custom_module_id', 0))
		name = request.GET.get('query', None)

		custom_modules = termite_models.TemplateCustomModule.objects.filter(owner=request.manager, is_deleted=False)
		if name and len(name) > 0:
			custom_modules = custom_modules.filter(name__contains=name)
		
		order_by = request.GET.get('sort_attr', '-updated_at')
		custom_modules = custom_modules.order_by(order_by)
		
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, custom_modules = paginator.paginate(custom_modules, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		items = []
		for custom_module in custom_modules:
			items.append({
				"id": custom_module.id,
				"name": custom_module.name,
				"created_at": custom_module.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				"isChecked": True if custom_module.id == selected_custom_module_id else False
			})

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': order_by,
			'data': {}
		}
		return response.get_response()
