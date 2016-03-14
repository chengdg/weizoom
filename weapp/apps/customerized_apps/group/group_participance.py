# -*- coding: utf-8 -*-

import json
from datetime import datetime
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from django.template import RequestContext
from django.shortcuts import render_to_response
from core.exceptionutil import unicode_full_stack

import models as app_models
from modules.member.models import Member

COUNT_PER_PAGE = 20

class GroupParticipance(resource.Resource):
	app = 'apps/group'
	resource = 'group_participance'

	def api_put(request):
		"""
		响应PUT
		"""
		try:
			member_id = request.member.id
			group_relation_id = request.POST['group_relation_id']
			fid = request.POST['fid']
			try:
				fid_member = Member.objects.get(id=fid)
			except:
				response = create_response(500)
				response.errMsg = u'不存在该会员'
				return response.get_response()
			#更新小团购信息
			group_relation = app_models.GroupRelations.objects(id=group_relation_id, member_id=fid).first()
			if group_relation.group_status == app_models.GROUP_RUNNING:
				#更新当前member的参与信息
				total_number = int(group_relation.group_type)
				sync_result = group_relation.modify(
					query={'grouped_number__lt': total_number},
					inc__grouped_number=1,
					push__grouped_member_ids=str(member_id)
				)
				if sync_result:
					try:
						group_detail = app_models.GroupDetail(
							relation_belong_to = group_relation_id,
							owner_id = str(fid),
							grouped_member_id = str(member_id),
							grouped_member_name = request.member.username_for_html,
							created_at = datetime.now()
						)
						group_detail.save()
					except:
						group_relation.update(dec__grouped_number=1,pop__grouped_member_ids=str(member_id))
						response = create_response(500)
						response.errMsg = u'只能参与一次'
						return response.get_response()
				else:
					response = create_response(500)
					response.errMsg = u'团购名额已满'
					return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'参与失败'
			response.inner_errMsg = unicode_full_stack()
			return response.get_response()
		response = create_response(200)
		return response.get_response()

	def api_post(request):
		"""
		我要开团
		"""
		group_record_id = request.POST['group_record_id']
		member_id = request.POST['fid']
		product_id =  request.POST['product_id']
		group_type = request.POST['group_type']
		group_days = request.POST['group_days']
		group_price = request.POST['group_price']
		try:
			group_member_info = app_models.GroupRelations(
				belong_to = group_record_id,
				member_id = member_id,
				group_leader_name = request.member.username_for_html,
				product_id = product_id,
				group_type = group_type,
				group_days = group_days,
				group_price = group_price,
				grouped_number = 1,
				grouped_member_ids = list(member_id),
				created_at = datetime.now()
			)
			group_member_info.save()
			data = json.loads(group_member_info.to_json())
			relation_belong_to = data['_id']['$oid']
			group_detail = app_models.GroupDetail(
				relation_belong_to = relation_belong_to,
				owner_id = member_id,
				grouped_member_id = member_id,
				grouped_member_name = request.member.username_for_html,
				created_at = datetime.now()
			)
			group_detail.save()
			response = create_response(200)
			response.data = {
				'relation_belong_to': relation_belong_to
			}
			return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'只能开团一次'
		return response.get_response()

	# @staticmethod
	# def get_datas(request):
	# 	product_name = request.GET.get('product_name', '')
	# 	group_name = request.GET.get('group_name', '')
	# 	status = int(request.GET.get('status', -1))
	# 	start_time = request.GET.get('start_time', '')
	# 	end_time = request.GET.get('end_time', '')

	# 	now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
	# 	params = {'owner_id':request.manager.id}
	# 	datas_datas = app_models.Group.objects(**params)
	# 	for data_data in datas_datas:
	# 		data_start_time = data_data.start_time.strftime('%Y-%m-%d %H:%M')
	# 		data_end_time = data_data.end_time.strftime('%Y-%m-%d %H:%M')
	# 		if data_start_time <= now_time and now_time < data_end_time:
	# 			data_data.update(set__status=app_models.STATUS_RUNNING)
	# 		elif now_time >= data_end_time:
	# 			data_data.update(set__status=app_models.STATUS_STOPED)

	# 	if group_name:
	# 		params['name__icontains'] = group_name
	# 	if product_name:
	# 		params['product_name__icontains'] = product_name
	# 	if status != -1:
	# 		params['status'] = status
	# 	if start_time:
	# 		params['start_time__gte'] = start_time
	# 	if end_time:
	# 		params['end_time__lte'] = end_time
	# 	datas = app_models.Group.objects(**params).order_by('-created_at')

	# 	#进行分页
	# 	count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	# 	cur_page = int(request.GET.get('page', '1'))
	# 	pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

	# 	return pageinfo, datas

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		relation_id = request.GET['id']
		print 'backend:',77777777777771111111111111110000000000000
		print relation_id

		members = app_models.GroupDetail.objects(relation_belong_to = relation_id)
		# pageinfo, members = paginator.paginate(members, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		print 'GGGGGGGGGGGGG'
		print type(members)
		print members
		items = []
		for member in members:
			items.append({
				'id':unicode(member.id),
				'name':member.grouped_member_name,
				'created_at':member.created_at.strftime("%Y-%m-%d %H:%M:%S")
				})

		# tmp_member_ids = []
		# for data in datas:
		# 	tmp_member_ids.append(data.member_id)
		# members = member_models.Member.objects.filter(id__in=tmp_member_ids)
		# member_id2member = {member.id: member for member in members}

		# items = []
		# for data in datas:
		# 	items.append({
		# 		'id': str(data.id),
		# 		'group_leader':data.group_leader_name,
		# 		'group_days':data.group_days,
		# 		'status':data.status_text,
		# 		'members_count':'%d/%s'%(data.grouped_number,data.group_type)
		# 	})
		response_data = {
			'items': items,
			# 'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()