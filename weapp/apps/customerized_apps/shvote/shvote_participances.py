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
from mall import export as mall_export
from utils.string_util import byte_to_hex

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class ShvoteParticipances(resource.Resource):
	app = 'apps/shvote'
	resource = 'shvote_participances'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.ShvoteParticipance.objects(belong_to=request.GET['id']).count()
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': "shvotes",
			'has_data': has_data,
			'activity_id': request.GET['id']
		});
		
		return render_to_response('shvote/templates/editor/shvote_participances.html', c)
	
	@staticmethod
	def get_datas(request):
		name = request.GET.get('participant_name', '')
		webapp_id = request.user_profile.webapp_id
		member_ids = []
		# if name:
		# 	hexstr = byte_to_hex(name)
		# 	members = member_models.Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)
		# 	member_ids = [member.id for member in members]
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		
		params = {'belong_to':request.GET['id']}
		if name:
			params['name__icontains'] = name
			# params['webapp_user_id__in'] = member_ids
		if start_time:
			params['created_at__gte'] = start_time
		if end_time:
			params['created_at__lte'] = end_time
		datas = app_models.ShvoteParticipance.objects(**params).order_by('-id')	
		
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
		pageinfo, datas = ShvoteParticipances.get_datas(request)
		
		tmp_member_ids = []
		for data in datas:
			tmp_member_ids.append(data.member_id)
		members = member_models.Member.objects.filter(id__in=tmp_member_ids)
		member_id2member = {member.id: member for member in members}
		
		items = []
		for data in datas:
			items.append({
				'id': str(data.id),
				'participant_icon':data.icon,
				'participant_name':data.name,
				# 'participant_name': member_id2member[data.member_id].username_size_ten if member_id2member.get(data.member_id) else u'未知',
				# 'participant_icon': member_id2member[data.member_id].user_icon if member_id2member.get(data.member_id) else '/static/img/user-1.jpg',
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

