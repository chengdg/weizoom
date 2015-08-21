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
import export
import re

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

ITEM_FOR_DISPLAY = {
	'phone': u'手机号',
	'name': u'姓名',
	'email': u'邮箱',
	'qq':u'QQ号',
	'job':u'职位',
	'addr':u'地址'
}

class eventParticipances(resource.Resource):
	app = 'apps/event'
	resource = 'event_participances'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.eventParticipance.objects(belong_to=request.GET['id']).count()
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': "events",
			'has_data': has_data,
			'activity_id': request.GET['id']
		});
		
		return render_to_response('event/templates/editor/event_participances.html', c)
	
	@staticmethod
	def get_datas(request):
		name = request.GET.get('participant_name', '')
		if name:
			members = member_models.Member.get_by_username(name)
			member_ids = [member.id for member in members]
			webapp_user_ids = [webapp_user.id for webapp_user in member_models.WebAppUser.objects.filter(member_id__in=member_ids)]
			if not webapp_user_ids:
				webapp_user_ids = [-1]
		else:
			webapp_user_ids = []
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		
		params = {'belong_to':request.GET['id']}
		if webapp_user_ids:
			params['webapp_user_id__in'] = webapp_user_ids
		if start_time:
			params['created_at__gte'] = start_time
		if end_time:
			params['created_at__lte'] = end_time
		datas = app_models.eventParticipance.objects(**params).order_by('-id')	
		
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
		pageinfo, datas = eventParticipances.get_datas(request)
		
		webappuser2datas = {}
		webapp_user_ids = set()
		for data in datas:
			webappuser2datas.setdefault(data.webapp_user_id, []).append(data)
			webapp_user_ids.add(data.webapp_user_id)
			data.participant_name = u'未知'
			data.participant_icon = '/static/img/user-1.jpg'
		
		webappuser2member = member_models.Member.members_from_webapp_user_ids(webapp_user_ids)
		if len(webappuser2member) > 0:
			for webapp_user_id, member in webappuser2member.items():
				for data in webappuser2datas.get(webapp_user_id, ()):
					data.participant_name = member.username_for_html
					data.participant_icon = member.user_icon
		
		items = []
		for data in datas:
			item_data_list = []
			event_participance = app_models.eventParticipance.objects.get(id=data.id)
			termite_data = event_participance.termite_data
			for k, v in termite_data.items():
				pureName = k.split('_')[1]
				item_data = {}
				if pureName in ITEM_FOR_DISPLAY:#判断是否是自定义的填写项
					item_data['item_name'] = ITEM_FOR_DISPLAY[pureName]
				else:
					item_data['item_name'] = pureName
				item_data['item_value'] = v['value']
				item_data_list.append(item_data)
			items.append({
				'id': str(data.id),
				'participant_name': data.participant_name,
				'participant_icon': data.participant_icon,
				'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				'informations': item_data_list
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

