# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F

from weixin2 import export
import weixin2.models as weixin_models
from core import resource
from core import paginator
from core.jsonresponse import create_response
from weixin.mp_decorators import mp_required

COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class Materials(resource.Resource):
	"""
	图文资源
	"""
	app = 'new_weixin'
	resource = 'materials'

	@login_required
	@mp_required
	def get(request):
		"""
		获取图文列表页面
		"""
		material_count = weixin_models.Material.objects.filter(owner=request.manager, is_deleted=False).count()
		if material_count > 0:
			has_material = True
		else:
			has_material = False

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_weixin_second_navs(request),
			'second_nav_name': export.WEIXIN_ADVANCE_SECOND_NAV,
			'third_nav_name': export.ADVANCE_MANAGE_MATERIAL_NAV,
			'has_material': has_material
		})

		return render_to_response('weixin/advance_manage/materials.html', c)
	
	@login_required
	@mp_required
	def api_get(request):
		"""
		获取素材集合的json表示
		"""
		selected_material_id = int(request.GET.get('selected_material_id', 0))
		title = request.GET.get('query', None)
		if title and len(title) > 0:
			material_ids = weixin_models.Material.objects.filter(owner=request.manager, is_deleted=False).values_list('id', flat=True)
			target_material_ids = [news.material_id for news in weixin_models.News.objects.filter(material_id__in=material_ids, title__contains=title)]
			materials = weixin_models.Material.objects.filter(owner=request.manager, is_deleted=False, id__in=target_material_ids)
		else:
			materials = weixin_models.Material.objects.filter(owner=request.manager, is_deleted=False)
		
		order_by = request.GET.get('sort_attr', '-id')
		materials = materials.order_by(order_by)
		
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, materials = paginator.paginate(materials, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		material_ids = []
		id2material = {}
		for material in materials:
			material_ids.append(material.id)
			material.newses = []
			id2material[material.id] = material
		
		for news in weixin_models.News.objects.filter(material_id__in=material_ids):
			id2material[news.material_id].newses.append({
				"id": news.id,
				"title": news.title
			})

		items = []
		for material in materials:
			items.append({
				"id": material.id,
				"created_at": material.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				"type": 'single' if material.type == weixin_models.SINGLE_NEWS_TYPE else 'multi',
				"newses": material.newses,
				"isChecked": True if material.id == selected_material_id else False
			})

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': order_by,
			'data': {}
		}
		return response.get_response()
