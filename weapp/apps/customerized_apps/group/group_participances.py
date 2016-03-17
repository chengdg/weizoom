# -*- coding: utf-8 -*-
import json
import datetime
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
COUNT_PER_PAGE = 12

class GroupParticipances(resource.Resource):
	app = 'apps/group'
	resource = 'group_participances'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.GroupRelations.objects(belong_to=request.GET['id']).count()

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': "groups",
			'has_data': has_data,
			'activity_id': request.GET['id']
		});

		return render_to_response('group/templates/editor/group_participances.html', c)

	@staticmethod
	def get_datas(request):
		group_leader_name = request.GET.get('group_leader_name', '')
		# group_status = int(request.GET.get('status', -1))
		# start_time = request.GET.get('start_time', '')
		# end_time = request.GET.get('end_time', '')
		# now_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')

		params = {'belong_to':request.GET['id']}
		datas_datas = app_models.GroupRelations.objects(**params)

		if group_leader_name:
			params['group_leader_name__icontains'] = group_leader_name
		# if group_status != -1:
		# 	params['group_status'] = group_status
		# if start_time:
		# 	params['created_at__gte'] = start_time
		# if end_time:
		# 	params['created_at__lte'] = end_time
		datas = app_models.GroupRelations.objects(**params).order_by('group_days')

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
		pageinfo, datas = GroupParticipances.get_datas(request)

		tmp_member_ids = []
		for data in datas:
			tmp_member_ids.append(data.member_id)
		members = member_models.Member.objects.filter(id__in=tmp_member_ids)
		member_id2member = {member.id: member for member in members}

		items = []
		for data in datas:
			success_time = data.success_time
			created_at = data.created_at
			group_days = data.group_days
			rest_days = 0


			if data.status_text == u'团购成功' and data.success_time:
				start_time_date = data.created_at.strftime('%Y/%m/%d')
				start_time_time = data.created_at.strftime('%H:%M')
				end_time_date = data.success_time.strftime('%Y/%m/%d')
				end_time_time = data.success_time.strftime('%H:%M')
				rest_days = (success_time - created_at).days

			else:
				start_time_date = data.created_at.strftime('%Y/%m/%d')
				start_time_time = data.created_at.strftime('%H:%M')

				group_end_time = data.created_at+datetime.timedelta(days=int(group_days))
				end_time_date = group_end_time.strftime('%Y/%m/%d')
				end_time_time = group_end_time.strftime('%H:%M')

				rest_days = int(group_days)

			items.append({
				'id': str(data.id),
				'group_leader':data.group_leader_name,
				'rest_days':rest_days,
				'start_time_date': start_time_date,
				'start_time_time': start_time_time,
				'end_time_date': end_time_date,
				'end_time_time': end_time_time,
				'status':data.status_text,
				'members_count':'%d/%s'%(int(len(data.grouped_member_ids))+1,data.group_type)
			})


		#排序
		items.sort(key=lambda item:item['rest_days'])
		status_ing = []
		status_fail = []
		status_success = []

		for item in items:
			if item['status'] == u'团购未生效' or u'团购进行中':
				status_ing.append(item)
			elif item['status'] == u'团购成功':
				status_success.append(item)
			else:
				status_fail.append(item)
		items = status_ing+status_fail+status_success


		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()




class GroupParticipancesDialog(resource.Resource):
	app = 'apps/group'
	resource = 'group_participances_dialog'

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		relation_id = request.GET['id']
		# relation_name = app_models.GroupRelations.objects(id=relation_id)

		members = app_models.GroupDetail.objects(relation_belong_to = relation_id)
		member_ids = [unicode(member.id) for member in members]
		# member_id2member = {unicode(member.id):member for member in members}

		items = []
		for member in members:
			items.append({
				'id':unicode(member.id),
				'name':member.grouped_member_name,
				'money':0.00,
				'points':'未写',
				'from':'未写',
				'created_at':member.created_at.strftime("%Y-%m-%d %H:%M:%S")
				})

		#进行分页
		count_per_page = int(request.GET.get('count_per_page', 1))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, items = paginator.paginate(items, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()