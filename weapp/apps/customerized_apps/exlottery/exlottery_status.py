# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
from mall import export
from apps import request_util
from termite import pagestore as pagestore_manager

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class ExlotteryStatus(resource.Resource):
	app = 'apps/exlottery'
	resource = 'exlottery_status'

	@login_required
	def get(request):
		"""
        响应GET
        """
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
			'third_nav_name': export.MALL_APPS_EXLOTTERY_NAV,
			# 'has_data': has_data,
			'activity_id': request.GET['id']
		})

		return render_to_response('exlottery/templates/editor/exlottery_status.html', c)
	@login_required
	def api_get(request):
		"""
		响应PGET
		"""
		id = request.GET.get('id',None)
		owner_id = request.manager.id

		exlottery_codes = app_models.ExlotteryCode.objects(owner_id = owner_id, belong_to = id)
		#分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, exlottery_codes = paginator.paginate(exlottery_codes, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		items = []

		for code in exlottery_codes:
			items.append({
				'code': code.code,
				'grade': code.prize_grade,
				'name': code.prize_name,
				'member': code.member_id,
				'time': code.created_at.strftime('%Y-%m-%d %H:%M')
			})

		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()




