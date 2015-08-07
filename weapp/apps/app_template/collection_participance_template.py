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
__STRIPPER_TAG__
FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20
__STRIPPER_TAG__
class {{resource.class_name}}(resource.Resource):
	app = 'apps/{{app_name}}'
	resource = '{{resource.lower_name}}'

	{% if resource.actions.get %}
	__STRIPPER_TAG__
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.{{resource.item_class_name}}.objects(belong_to=request.GET['id']).count()
		__STRIPPER_TAG__
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': "{{resource.second_nav}}",
			'has_data': has_data,
			'activity_id': request.GET['id']
		});
		__STRIPPER_TAG__
		return render_to_response('{{app_name}}/templates/editor/{{resource.lower_name}}.html', c)
	{% endif %} 

	{% if resource.actions.api_get %}
	__STRIPPER_TAG__
	@staticmethod
	def get_datas(request):
		name = request.GET.get('participant_name', '')
		members = member_models.Member.get_by_username(name)
		member_ids = [member.id for member in members]
		webapp_user_ids = [webapp_user.id for webapp_user in member_models.WebAppUser.objects.filter(member_id__in=member_ids)]

		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		__STRIPPER_TAG__
		params = {'belong_to':request.GET['id']}
		if webapp_user_ids:
			params['webapp_user_id__in'] = webapp_user_ids
		if start_time:
			params['created_at__gte'] = start_time
		if end_time:
			params['created_at__lte'] = end_time
		datas = app_models.{{resource.item_class_name}}.objects(**params).order_by('-id')	
		__STRIPPER_TAG__
		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		__STRIPPER_TAG__
		return pageinfo, datas

	__STRIPPER_TAG__
	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		pageinfo, datas = {{resource.class_name}}.get_datas(request)
		__STRIPPER_TAG__
		webappuser2datas = {}
		webapp_user_ids = set()
		for data in datas:
			webappuser2datas.setdefault(data.webapp_user_id, []).append(data)
			webapp_user_ids.add(data.webapp_user_id)
			data.participant_name = u'未知'
			data.participant_icon = '/static/img/user-1.jpg'
		__STRIPPER_TAG__
		webappuser2member = member_models.Member.members_from_webapp_user_ids(webapp_user_ids)
		if len(webappuser2member) > 0:
			for webapp_user_id, member in webappuser2member.items():
				for data in webappuser2datas.get(webapp_user_id, ()):
					data.participant_name = member.username_for_html
					data.participant_icon = member.user_icon
		__STRIPPER_TAG__
		items = []
		for data in datas:
			items.append({
				'id': str(data.id),
				'participant_name': data.participant_name,
				'participant_icon': data.participant_icon,
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
	{% endif %}
