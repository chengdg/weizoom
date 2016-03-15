# -*- coding: utf-8 -*-

import json
from datetime import datetime

from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
from apps import request_util
from termite import pagestore as pagestore_manager
from mall.order.util import update_order_status_by_group_status

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
		webapp_owner_id = request.webapp_owner_id
		record = app_models.Group.objects(product_id=pid,status=app_models.STATUS_RUNNING)
		if record.count() > 0:
			is_in_group_buy = True
			activity_url = '/m/apps/group/m_group/?webapp_owner_id='+str(webapp_owner_id)+'&id='+str(record.first().id)
		response = create_response(200)
		response.data = {
			'is_in_group_buy': is_in_group_buy,
			'activity_url': activity_url
		}
		return response.get_response()

class GroupBuyProducts(resource.Resource):
	app = 'apps/group'
	resource = 'group_buy_products'

	def api_get(request):
		"""
		批量获得商品是否在团购活动中
		"""
		pid2is_in_group_buy = []
		pids = request.GET.get('pids')
		pids = pids.split('_')
		pids = [int(pid) for pid in pids]
		records = app_models.Group.objects(product_id__in=pids,status=app_models.STATUS_RUNNING)
		pid_in_group_buy = [record.product_id for record in records]
		for pid in pids:
			if pid in pid_in_group_buy:
				pid2is_in_group_buy.append({
					'pid': pid,
					'is_in_group_buy': True
				})
			else:
				pid2is_in_group_buy.append({
					'pid': pid,
					'is_in_group_buy': False
				})
		response = create_response(200)
		response.data = {
			'pid2is_in_group_buy': pid2is_in_group_buy
		}
		return response.get_response()

class GroupBuyInfo(resource.Resource):
	app = 'apps/group'
	resource = 'group_buy_info'

	def api_get(request):
		"""
		获取团购商品信息
		"""
		pid = 0
		group_buy_price = 0
		activity_id = ''
		activity_url = ''
		group_id = request.GET.get('group_id')
		webapp_owner_id = request.webapp_owner_id
		group_record = app_models.GroupRelations.objects(id=group_id)
		if group_record.count() > 0:
			group_record = group_record.first()
			pid = group_record.product_id
			group_buy_price = group_record.group_price
			activity_id = group_record.belong_to
			activity_url = '/m/apps/group/m_group/?webapp_owner_id='+str(webapp_owner_id)+'&id='+str(activity_id)
		response = create_response(200)
		response.data = {
			'pid': pid,
			'group_buy_price': group_buy_price,
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
		reason = u''
		group_buy_price = 0

		group_record = app_models.GroupRelations.objects(id=group_id,product_id=int(pid))
		if group_record.count() > 0:
			group_record = group_record.first()
			if group_record.group_status == app_models.GROUP_NOT_START: #团购未生效（团长还未支付成功）
				if member_id == group_record.member_id:
					is_success = True
					reason = u'团长可以进行开团下单操作'
					group_buy_price = group_record.group_price
				else:
					reason = u'团购活动暂未生效，团长还未开团成功'
			elif group_record.group_status == app_models.GROUP_RUNNING:
				if member_id in group_record.grouped_member_ids and (group_record.grouped_number < int(group_record.group_type)):
					is_success = True
					reason = u'可以进行团购下单操作'
					group_buy_price = group_record.group_price
				else:
					reason = u'不可进行团购下单操作'
			else:
				reason = u'该团购已结束'
		else:
			reason = u'该条团购信息不存在'
		response = create_response(200)
		response.data = {
			'is_success': is_success,
			'reason': reason,
			'pid': pid,
			'group_buy_price': group_buy_price,
			'group_id': group_id,
		}
		return response.get_response()

class OrderAction(resource.Resource):
	app = 'apps/group'
	resource = 'order_action'

	def api_put(request):
		"""
		apiserver通知订单支付成功
		"""
		order_id = request.POST['order_id']
		action = request.POST['action']
		group_id = request.POST['group_id']
		member_id = request.POST['member_id']
		group_record = app_models.GroupRelations.objects.get(id=group_id)
		group_detail = app_models.GroupDetail.objects.get(relation_belong_to=group_id,grouped_member_id=member_id)

		if action == 'pay': #参数为'pay'表示支付成功
			if group_record.member_id == member_id:#如果团长支付成功，算开团成功
				group_record.update(set__group_status=app_models.GROUP_RUNNING)
			group_detail.update(set__is_already_paid=True,set__order_id=order_id)
		elif action == 'cancel': #'cancel'(订单已取消)
			if group_record.member_id == member_id:#如果团长订单已取消
				group_record.delete()
			else:
				group_record.update(dec__grouped_number=1,pop__grouped_member_ids=member_id)
			group_detail.delete()

		#如果团购人满，并且全部支付成功，则团购成功
		if int(group_record.group_type) == group_record.grouped_number:
			group_details = app_models.GroupDetail.objects(relation_belong_to=group_id)
			is_already_paid_list = []
			for g in group_details:
				is_already_paid_list.append(g.is_already_paid)
			if 'False' not in is_already_paid_list:
				group_record.update(set__group_status=app_models.GROUP_SUCCESS,set__success_time=datetime.now())
				update_order_status_by_group_status(group_id,'success')
		response = create_response(200)
		return response.get_response()

class GetPidsByWoid(resource.Resource):
	app = 'apps/group'
	resource = 'get_pids_by_woid'

	def api_get(request):
		"""
		获得当前woid处在团购中的Pid_list
		"""
		woid = request.GET.get('woid')
		records = app_models.Group.objects(owner_id=woid,status=app_models.STATUS_RUNNING)
		pids_list = [record.product_id for record in records]
		response = create_response(200)
		response.data = {
			'pids_list': pids_list
		}
		return response.get_response()