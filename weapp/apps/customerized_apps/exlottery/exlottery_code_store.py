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
		has_data = app_models.ExlotteryCode.objects.count()
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
			'third_nav_name': export.MALL_APPS_EXLOTTERY_NAV,
			'has_data': has_data,
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
		# prize_grade = int(request.GET.get('status', -1))
		if not id:
			id = export_id
		params = {
			'owner_id': owner_id,
			'belong_to': id,
		}
		if code:
			params['code'] = code
		# if prize_grade != -1:
		# 	params['prize_grade'] = prize_grade
		# if member:
		# 	hexstr = byte_to_hex(member)
		# 	members = Member.objects.filter(webapp_id=owner_id, username_hexstr=hexstr)
		# 	temp_ids = [member.id for member in members]
		# 	member_ids = temp_ids if temp_ids else [-1]
		# 	params['member_id__in'] = member_ids

		exlottery_codes = app_models.ExlotteryCode.objects(**params).order_by('-use_time', '-created_at')
		count = exlottery_codes.count()

		exlottery = app_models.Exlottery.objects(id=id).first()
		created_at = exlottery.created_at.strftime('%Y-%m-%d %H:%M')
		status = exlottery.status_text

		codes = [code.code for code in exlottery_codes]
		exlottery_records = app_models.ExlottoryRecord.objects(code__in = codes)

		# 构造会员id和会员名映射
		member_ids = []
		code2record = {}
		for re in exlottery_records:
			member_ids.append(re.member_id)
			code2record[re.code] = re

		members = Member.objects.filter(id__in=member_ids)
		member_id2member_name = {m.id: m.username_for_html for m in members}

		if not export_id:
			# 分页
			count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
			cur_page = int(request.GET.get('page', '1'))
			pageinfo, exlottery_codes = paginator.paginate(exlottery_codes, cur_page, count_per_page,
														   query_string=request.META['QUERY_STRING'])

			return pageinfo, exlottery_codes, code2record, member_id2member_name, count, created_at, status
		else:
			return exlottery_codes, code2record, member_id2member_name, count, created_at, status

	@login_required
	def api_get(request):
		"""
		响应PGET
		"""
		pageinfo, exlottery_codes, code2record, member_id2member_name, count, created_at, status = ExlotteryCodeStore.get_datas(request)

		items = []
		used_count = 0
		first_prize = 0
		second_prize = 0
		third_prize = 0
		for code in exlottery_codes:
			code = code.code
			record = code2record.get(code,None)
			grade = ''
			name = ''
			member = ''
			time = ''
			if record:
				used_count += 1
				grade = record.prize_title
				if grade == u'一等奖':
					first_prize += 1
				if grade == u'二等奖':
					second_prize += 1
				if grade == u'三等奖':
					third_prize += 1
				name = record.prize_name
				member_id = record.member_id
				member = member_id2member_name[member_id]
				time = record.created_at.strftime('%Y-%m-%d %H:%M')

			items.append({
				'code': code,
				'grade': grade,
				'name': name,
				'member': member,
				'time': time
			})

		data = {}
		data['count'] = count
		data['has_used'] = used_count
		data['first'] = first_prize
		data['second'] = second_prize
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
		exlottery_codes, code2record, member_id2member_name, count, created_at, status = ExlotteryCodeStore.get_datas(request)

		members_info = [
			[u'抽奖码', u'使用人', u'使用时间', u'获奖等级', u'奖品名称']
		]

		for code in exlottery_codes:
			record = code2record.get(code, None)
			grade = ''
			name = ''
			member = ''
			time = ''
			if record:
				name = record.prize_name
				member_id = record.member_id
				member = member_id2member_name[member_id]
				time = record.created_at.strftime('%Y-%m-%d %H:%M')
			try:
				info_list = [
					code.code,
					member,
					time,
					grade,
					name
				]
				members_info.append(info_list)
			except:
				pass

		filename = u'专项抽奖码库详情'
		return ExcelResponse(members_info, output_name=filename.encode('utf8'), force_csv=False)
