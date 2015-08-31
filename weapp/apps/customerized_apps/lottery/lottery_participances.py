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
from modules.member import models as member_models
import models as app_models
from mall import export

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

class lotteryParticipances(resource.Resource):
	app = 'apps/lottery'
	resource = 'lottery_participances'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.lotteryParticipance.objects(belong_to=request.GET['id']).count()
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_customerized_apps(request),
			'second_nav_name': "lotteries",
			'has_data': has_data,
			'activity_id': request.GET['id']
		})
		
		return render_to_response('lottery/templates/editor/lottery_participances.html', c)
	
	@staticmethod
	def get_datas(request):
		name = request.GET.get('participant_name', '')
		print name
		prize_type = request.GET.get('prize_type', '-1')
		status = request.GET.get('status', '-1')
		member_ids = []
		if name:
			members = member_models.Member.get_by_username(name)
			member_ids = [member.id for member in members]

		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		
		params = {'belong_to':request.GET['id'], 'prize_type__ne': 'no_prize'}
		if name:
			params['member_id__in'] = member_ids
		if start_time:
			params['created_at__gte'] = start_time
		if end_time:
			params['created_at__lte'] = end_time
		if prize_type != '-1':
			params['prize_type'] = prize_type
		if status != '-1':
			params['status'] = True if status == '1' else False
		# datas = app_models.lotteryParticipance.objects(**params).order_by('-id')
		datas = app_models.lottoryRecord.objects(**params)
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
		pageinfo, datas = lotteryParticipances.get_datas(request)
		
		memberuser2datas = {}
		member_ids = set()
		for data in datas:
			memberuser2datas.setdefault(data.member_id, []).append(data)
			member_ids.add(data.member_id)
			data.participant_name = u'未知'
			data.participant_icon = '/static/img/user-1.jpg'
		
		member_user2member = {}
		members = member_models.Member.objects.filter(id__in=member_ids)
		for member in members:
			if member.id not in member_user2member:
				member_user2member[member.id] = member
			else:
				member_user2member[member.id] = member

		if len(member_user2member) > 0:
			for member_id, member in member_user2member.items():
				for data in memberuser2datas.get(member_id, ()):
					data.participant_name = member.username_for_html
					data.participant_icon = member.user_icon
					data.created_at = member.created_at
		
		items = []
		for data in datas:
			items.append({
				'id': str(data.id),
				'participant_name': data.participant_name,
				'participant_icon': data.participant_icon,
				'tel': data.tel,
				'prize_title': data.prize_title,
				'prize_name': data.prize_name,
				'status': data.status,
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

