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
import models as app_models
import export
from datetime import datetime
from mall import export as mall_export

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class Shvotes(resource.Resource):
	app = 'apps/shvote'
	resource = 'shvotes'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.Shvote.objects.count()

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': "shvotes",
			'has_data': has_data
		})

		return render_to_response('shvote/templates/editor/shvotes.html', c)

	@staticmethod
	def get_datas(request):
		name = request.GET.get('name', '')
		status = int(request.GET.get('status', -1))
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')

		now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
		params = {'owner_id':request.manager.id}
		datas_datas = app_models.Shvote.objects(**params)
		for data_data in datas_datas:
			data_start_time = data_data.start_time.strftime('%Y-%m-%d %H:%M')
			data_end_time = data_data.end_time.strftime('%Y-%m-%d %H:%M')
			if data_start_time <= now_time and now_time < data_end_time:
				data_data.update(set__status=app_models.STATUS_RUNNING)
			elif now_time >= data_end_time:
				data_data.update(set__status=app_models.STATUS_STOPED)
		if name:
			params['name__icontains'] = name
		if status != -1:
			params['status'] = status
		if start_time:
			params['start_time__gte'] = start_time
		if end_time:
			params['end_time__lte'] = end_time
		datas = app_models.Shvote.objects(**params).order_by('-id')

		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		return pageinfo, datas

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		pageinfo, datas = Shvotes.get_datas(request)

		record_id2memberinfo = {}
		for c in app_models.ShvoteControl.objects():
			belong_to = c.belong_to
			if record_id2memberinfo.has_key(belong_to) and c.member_id not in record_id2memberinfo[belong_to]:
				record_id2memberinfo[belong_to].append(c.member_id)
			else:
				record_id2memberinfo[belong_to] = [c.member_id]

		#后端审核通过，计入参与人数
		ids = [str(data.id) for data in datas]
		participances = app_models.ShvoteParticipance.objects(belong_to__in=ids, is_use=app_models.MEMBER_IS_USE['YES'])

		id2asking_count = id2participant_count = {str(one_id):0 for one_id in ids}
		for participance in participances:
			belong_to = str(participance.belong_to)
			# if record_id2memberinfo.has_key(belong_to):
			# 	record_id2memberinfo[belong_to] += participance.count
			# else:
			# 	record_id2memberinfo[belong_to] = participance.count

			if id2participant_count.has_key(belong_to):
				id2asking_count[belong_to] += 1

		items = []
		for data in datas:
			id_str = str(data.id)
			items.append({
				'id': id_str,
				'owner_id': request.manager.id,
				'name': data.name,
				'start_time': data.start_time.strftime('%Y-%m-%d %H:%M'),
				'end_time': data.end_time.strftime('%Y-%m-%d %H:%M'),
				'total_voted_count': len(record_id2memberinfo.get(id_str, [])),
				'total_participanted_count': id2asking_count[id_str],
				'related_page_id': data.related_page_id,
				'status': data.status_text,
				'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S")
			})
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

