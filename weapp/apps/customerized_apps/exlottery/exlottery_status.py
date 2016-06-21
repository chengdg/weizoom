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
from modules.member.models import Member

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class ExlotteryStatus(resource.Resource):
	app = 'apps/exlottery'
	resource = 'exlottery_status'

	@login_required
	def get(request):
		"""
        码库页面
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
		count = exlottery_codes.count()

		exlottery = app_models.Exlottery.objects(id = id).first()
		created_at = exlottery.created_at.strftime('%Y-%m-%d %H:%M')
		status = exlottery.status_text

		#构造会员id和会员名映射
		member_ids = [code.member_id for code in exlottery_codes]
		members = Member.objects.filter(id__in = member_ids)
		member_id2member_name = {m.id: m.username_for_html for m in members}

		#分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, exlottery_codes = paginator.paginate(exlottery_codes, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		items = []
		used_count = 0
		first_prize = 0
		second_proze = 0
		third_prize = 0
		for code in exlottery_codes:
			grade = code.prize_grade
			if grade != 0:
				if grade == 1:
					first_prize += 1
				elif grade == 2:
					second_proze += 1
				elif grade == 3:
					third_prize += 1
				grade = app_models.EXLOTTERY_PRIZE[grade]
				used_count += 1
			else:
				grade = ''
			member_id = code.member_id
			items.append({
				'code': code.code,
				'grade': grade,
				'name': code.prize_name,
				'member': member_id2member_name[member_id] if member_id != 0 else '',
				'time': code.created_at.strftime('%Y-%m-%d %H:%M')
			})

		data = {}
		data['count'] = count
		data['has_used'] = used_count
		data['first'] = first_prize
		data['second'] = second_proze
		data['third'] = third_prize
		data['create_at'] = created_at
		data['status'] = status

		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'data': data,
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()




