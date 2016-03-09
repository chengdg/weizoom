# -*- coding: utf-8 -*-

import json
from datetime import datetime

from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
from apps import request_util
from termite import pagestore as pagestore_manager

class GroupBuyProduct(resource.Resource):
	app = 'apps/group'
	resource = 'group_buy_product'

	def api_get(request):
		"""
		获得商品是否在团购活动中
		"""
		activity_url = ''
		is_in_group_buy = False
		pid = request.GET.get('pid')
		webapp_owner_id = request.webapp_owner_info.auth_appid_info.appid
		record = app_models.Group.objects(product_id=pid,status=app_models.STATUS_RUNNING)
		if record.count() > 0:
			is_in_group_buy = True
			activity_url = '/m/apps/group/m_group/?webapp_owner_id='+webapp_owner_id+'&id='+record.first().id
		response = create_response(200)
		response.data = {
			'is_in_group_buy': is_in_group_buy,
			'activity_url': activity_url
		}
		return response.get_response()

class GroupBuyInfo(resource.Resource):
	app = 'apps/group'
	resource = 'group_buy_info'

	def api_get(request):
		"""
		获取团购商品信息
		"""
		group_id = request.GET.get('group_id')
		webapp_owner_id = request.webapp_owner_info.auth_appid_info.appid
		group_record = app_models.GroupRelations.objects.get(id=group_id)
		activity_id = group_record.belong_to
		activity_url = '/m/apps/group/m_group/?webapp_owner_id='+webapp_owner_id+'&id='+activity_id
		response = create_response(200)
		response.data = {
			'pid': group_record.product_id,
			'group_buy_price': group_record.group_price,
			'group_id': group_id,
			'activity_id': activity_id,
			'activity_url': activity_url,
		}
		return response.get_response()

class CheckGroupBuy(resource.Resource):
	app = 'apps/group'
	resource = 'check_group_buy'

	def api_get(request):
		"""
		下单中的检测
		"""
		member_id = request.GET.get('member_id')
		group_id = request.GET.get('group_id')
		pid = request.GET.get('pid')
		is_success = False
		reason = 'check_group_buy_fail'
		group_record = app_models.GroupRelations.objects.get(id=group_id)
		if member_id in group_record.grouped_member_ids:
			is_success = True
			reason = 'check_group_buy_success'
		response = create_response(200)
		response.data = {
			'is_success': is_success,
			'reason': reason,
			'pid': pid,
			'group_buy_price': group_record.group_price,
			'group_id': group_id,
		}
		return response.get_response()
