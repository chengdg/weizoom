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
from termite import pagestore as pagestore_manager

import models as app_models
from datetime import datetime
from mall import export

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class votes(resource.Resource):
	app = 'apps/vote'
	resource = 'votes'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.vote.objects.count()

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
			'third_nav_name': export.MALL_APPS_VOTE_NAV,
			'has_data': has_data
		});
		
		return render_to_response('vote/templates/editor/votes.html', c)
	
	@staticmethod
	def get_datas(request):
		name = request.GET.get('name', '')
		status = int(request.GET.get('status', -1))
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		prize_type = request.GET.get('prize_type', 'all')

		now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
		params = {'owner_id':request.manager.id}
		datas_datas = app_models.vote.objects(**params)
		for data_data in datas_datas:
			data_start_time = data_data.start_time.strftime('%Y-%m-%d %H:%M')
			data_end_time = data_data.end_time.strftime('%Y-%m-%d %H:%M')
			data_status = data_data.status
			if data_status <= 1:
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
		if prize_type != 'all':
			records = []
			prize_type_ids = []
			records = app_models.vote.objects.filter(owner_id=request.manager.id)
			pagestore = pagestore_manager.get_pagestore('mongo')
			for record in records:
				page = pagestore.get_page(record.related_page_id, 1)
				page_details = page['component']['components'][0]['model']
				page_prize_type = page_details['prize']['type']
				if prize_type == page_prize_type:
					prize_type_ids.append(record.id)
			params['id__in'] = prize_type_ids
		datas = app_models.vote.objects(**params).order_by('-id')	
		
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
		pageinfo, datas = votes.get_datas(request)

		pagestore = pagestore_manager.get_pagestore('mongo')
		p_ids = []
		for data in datas:
			p_ids.append(str(data.related_page_id))
		pages = pagestore.db.page.find({"project_id":{"$in":p_ids}})

		related_page_id2page = {}
		for page in pages:
			related_page_id2page[page['project_id']] = page['component']['components'][0]['model']['prize']['type']

		items = []
		for data in datas:
			prize_type = related_page_id2page[str(data.related_page_id)]
			if prize_type == 'no_prize':
				prize_type = '无奖励'
			elif prize_type == 'integral':
				prize_type = '积分'
			elif prize_type == 'coupon':
				prize_type = '优惠券'
			items.append({
				'id': str(data.id),
				'name': data.name,
				'start_time': data.start_time.strftime('%Y-%m-%d %H:%M'),
				'end_time': data.end_time.strftime('%Y-%m-%d %H:%M'),
				'participant_count': data.participant_count,
				'related_page_id': data.related_page_id,
				'status': data.status_text,
				'prize_type': prize_type,
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

