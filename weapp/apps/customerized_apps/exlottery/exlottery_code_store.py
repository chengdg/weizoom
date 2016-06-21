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

from utils.string_util import byte_to_hex
from excel_response import ExcelResponse

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class ExlotteryCodeStore(resource.Resource):
	app = 'apps/exlottery'
	resource = 'exlottery_code_store'

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

		return render_to_response('exlottery/templates/editor/exlottery_code_store.html', c)

	@staticmethod
	def get_datas(request):
		id = request.GET.get('id', None)
		owner_id = request.manager.id
		export_id = request.GET.get('export_id', None)
		# 过滤
		code = request.GET.get('code', None)
		member = request.GET.get('member', None)
		prize_grade = int(request.GET.get('status', -1))
		if not id:
			id = export_id
		param = {
			'owner_id': owner_id,
			'belong_to': id,
		}
		if code:
			param['code'] = code
		if prize_grade != -1:
			param['prize_grade'] = prize_grade

		exlottery_codes = app_models.ExlotteryCode.objects(**param).order_by('-get_time', '-created_at')
		count = exlottery_codes.count()

		exlottery = app_models.Exlottery.objects(id=id).first()
		created_at = exlottery.created_at.strftime('%Y-%m-%d %H:%M')
		status = exlottery.status_text

		# 构造会员id和会员名映射
		member_ids = [code.member_id for code in exlottery_codes]
		members = Member.objects.filter(id__in=member_ids)
		member_id2member_name = {m.id: m.username_for_html for m in members}

		if not export_id:
			# 分页
			count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
			cur_page = int(request.GET.get('page', '1'))
			pageinfo, exlottery_codes = paginator.paginate(exlottery_codes, cur_page, count_per_page,
														   query_string=request.META['QUERY_STRING'])

			return pageinfo, exlottery_codes, member_id2member_name, count, created_at, status
		else:
			return exlottery_codes, member_id2member_name, count, created_at, status

	@login_required
	def api_get(request):
		"""
		响应PGET
		"""
		pageinfo, exlottery_codes, member_id2member_name, count, created_at, status = ExlotteryCodeStore.get_datas(request)

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
					second_prize += 1
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
				'time': code.get_time.strftime('%Y-%m-%d %H:%M') if grade else ''
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

class ExlotteryCodeExport(resource.Resource):
	app = 'apps/exlottery'
	resource = 'exlottery_code_export'

	@login_required
	def api_get(request):
		"""
		码库导出
		@return:
		"""
		exlottery_codes, member_id2member_name, count, created_at, status = ExlotteryCodeStore.get_datas(request)

		members_info = [
			[u'抽奖码', u'使用人', u'使用时间', u'获奖等级', u'奖品名称']
		]

		for code in exlottery_codes:
			member_id = code.member_id
			grade = code.prize_grade
			if grade != 0:
				grade = app_models.EXLOTTERY_PRIZE[grade]
			else:
				grade = ''
			try:
				info_list = [
					code.code,
					member_id2member_name[member_id] if member_id != 0 else '',
					code.get_time.strftime('%Y-%m-%d %H:%M') if grade else '',
					grade,
					code.prize_name
				]
				members_info.append(info_list)
			except:
				pass

		filename = u'专项抽奖码库详情'
		return ExcelResponse(members_info, output_name=filename.encode('utf8'), force_csv=False)
