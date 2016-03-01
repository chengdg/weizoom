# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from core import resource

import models as app_models
from core.jsonresponse import create_response
from termite2 import pagecreater
from utils import url_helper
from utils.cache_util import GET_CACHE, SET_CACHE
from modules.member.models import Member

class MGroup(resource.Resource):
	app = 'apps/group'
	resource = 'm_group'

	def api_get(request):
		record_id = request.GET.get('id', None)
		#获取webapp_owner_id
		owner_id = request.webapp_owner_id
		if not record_id:
			response = create_response(500)
			response.errMsg = u'活动信息出错'
			return response.get_response()
		group_participances = app_models.GroupParticipance.objects(belong_to=record_id,group_status=False,is_group_leader=True,is_valid=True)
		group_ids = [str(p.belong_to) for p in group_participances]
		groups = app_models.Group.objects(id__in=group_ids,status=app_models.STATUS_RUNNING)
		all_groups_can_join = []
		for group in groups:
			group_dict = json.loads(group.group_dict),
			all_groups_can_join.append({
				'id': str(group.id),
				'name': group.name,
				'product_img': group.product,
				# 'group_dict': group_dict,
				'participant_count': group.participant_count,
				'end_time': group.end_time.strftime('%y-%m-%d'),
				'url': '/m/apps/group/m_group_detail/?webapp_owner_id=%d&id=%s' % (owner_id, str(group.id))
			})
		response = create_response(200)
		response.data = {
			'all_groups_can_join': all_groups_can_join
		}
		return response.get_response()

	def get(request):
		"""
		响应GET
		"""
		all_groups_can_open = []
		#获取webapp_owner_id
		owner_id = request.webapp_owner_id
		#我要开团
		groups = app_models.Group.objects(owner_id=owner_id,status=app_models.STATUS_RUNNING).order_by('-created_at')
		for group in groups:
			try:
				group_dict = json.loads(group.group_dict),
				all_groups_can_open.append({
					'id': str(group.id),
					'name': group.name,
					'product_img': group.product,
					# 'group_dict': group_dict,
					'end_time': group.end_time.strftime('%y-%m-%d'),
					'url': '/m/apps/group/m_group_detail/?webapp_owner_id=%d&id=%s' % (owner_id, str(group.id))
				})
			except:
				pass

		c = RequestContext(request, {
			'page_title': u'团购列表',
			'all_groups_can_open': all_groups_can_open,
			'is_hide_weixin_option_menu':True
		})
		return render_to_response('group/templates/webapp/m_group_list.html', c)