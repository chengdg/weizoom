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
import export
from apps import request_util
from termite import pagestore as pagestore_manager
from mall.order.util import update_order_status_by_group_status
from apps.customerized_apps.group.group_participance import send_group_template_message

class GroupStatus(resource.Resource):
	app = 'apps/group'
	resource = 'group_status'

	@login_required
	def api_post(request):
		"""
		响应POST
		"""
		target_status = request.POST['target']
		is_test = request.POST.get('is_test', False)

		if target_status == 'stoped':
			target_status = app_models.STATUS_STOPED
			now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
			record = app_models.Group.objects(id=request.POST['id'])
			record.update(set__end_time=now_time)
			pagestore = pagestore_manager.get_pagestore('mongo')
			datas = app_models.Group.objects(id=request.POST['id'])
			for data in datas:
				related_page_id = data.related_page_id
			page = pagestore.get_page(related_page_id, 1)
			page['component']['components'][0]['model']['end_time'] = now_time
			pagestore.save_page(related_page_id, 1, page['component'])

			#手动关闭活动之后对于小团的处理：
			#活动已结束，所有进行中的小团置为失败
			running_group_relations = app_models.GroupRelations.objects(belong_to=request.POST['id'],group_status=app_models.GROUP_RUNNING)
			for group_relation in running_group_relations:
				group_relation.update(group_status=app_models.GROUP_FAILURE)
				group_relation_id = group_relation.id
				update_order_status_by_group_status(group_relation_id,'failure', is_test=is_test)
				#发送拼团失败模板消息
				try:
					group_details = app_models.GroupDetail.objects(relation_belong_to=str(group_relation_id))
					owner_id = record.owner_id
					product_name = record.product_name
					miss = int(group_relation.group_type)-group_details.count()
					activity_info = {
						"owner_id": str(owner_id),
						"record_id": str(request.POST['id']),
						"group_id": str(group_relation_id),
						"fid": str(group_relation.member_id),
						"price": '%.2f' % group_relation.group_price,
						"product_name": product_name,
						"status" : 'fail',
						"miss": str(miss)
					}
					member_info_list = [{"member_id": group_detail.grouped_member_id, "order_id": group_detail.order_id} for group_detail in group_details]
					send_group_template_message(activity_info, member_info_list)
				except Exception, e:
					print(u'发送拼团失败模板消息失败')
					print 'template----------------------------------'
					print e
					print 'template----------------------------------'

		elif target_status == 'running':
			#说明手动点击开启了
			groups = app_models.Group.objects(id=request.POST['id'])
			groups.update(set__handle_status=1)
			group = groups[0]
			start_time = group.start_time.strftime('%Y-%m-%d %H:%M')
			end_time = group.end_time.strftime('%Y-%m-%d %H:%M')
			now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
			if start_time <= now_time and now_time < end_time:
				target_status = app_models.STATUS_RUNNING
			elif now_time >= end_time:
				target_status = app_models.STATUS_STOPED
			else:
				target_status = app_models.STATUS_NOT_START

		elif target_status == 'not_start':
			target_status = app_models.STATUS_NOT_START

		app_models.Group.objects(id=request.POST['id']).update(set__status=target_status)

		response = create_response(200)
		return response.get_response()
