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
import models as app_models
from mall import export
from datetime import datetime
import export as rebate_export

from modules.member.models import Member

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class Rebates(resource.Resource):
	app = 'apps/rebate'
	resource = 'rebates'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.Rebate.objects.count()

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
            'third_nav_name': export.MALL_APPS_REBATE_NAV,
			'has_data': has_data
		})
		
		return render_to_response('rebate/templates/editor/rebates.html', c)
	
	@staticmethod
	def get_datas(request):
		name = request.GET.get('name', '')
		
		now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
		params = {'owner_id':request.manager.id,'is_deleted': False}
		datas_datas = app_models.Rebate.objects(**params)
		for data_data in datas_datas:
			data_start_time = data_data.start_time.strftime('%Y-%m-%d %H:%M')
			data_end_time = data_data.end_time.strftime('%Y-%m-%d %H:%M')
			if data_start_time <= now_time and now_time < data_end_time:
				data_data.update(set__status=app_models.STATUS_RUNNING)
			elif now_time >= data_end_time:
				data_data.update(set__status=app_models.STATUS_STOPED)
		if name:
			params['name__icontains'] = name
		datas = app_models.Rebate.objects(**params).order_by('-id')

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
		pageinfo, datas = Rebates.get_datas(request)
		items = []
		#TODO 三个数值
		#统计每个活动的扫码关注人数
		record_id2partis = {}
		record_ids = [d.id for d in datas]
		all_member_ids = set()
		all_partis = app_models.RebateParticipance.objects(belong_to__in=record_ids)
		for p in all_partis:
			member_id = p.member_id
			all_member_ids.add(member_id)
		member_id2subscribe = {m.id: m.is_subscribed for m in Member.objects.filter(id__in=all_member_ids)}
		record_own_member_ids = {}
		for p in all_partis:
			belong_to = p.belong_to
			member_id = p.member_id
			if not record_id2partis.has_key(belong_to):
				if member_id2subscribe[member_id]:
					record_id2partis[belong_to] = {member_id}
			else:
				if member_id2subscribe[member_id]:
					record_id2partis[belong_to].add(member_id)

			if not record_own_member_ids.has_key(belong_to):
				record_own_member_ids[belong_to] = {member_id}
			else:
				record_own_member_ids[belong_to].add(member_id)

		#统计扫码后成交金额和首次下单数
		webapp_user_id_belong_to_member_id, id2record, member_id2records, member_id2order_ids, all_orders = rebate_export.get_target_orders(datas)
		id2order = {str(o.id): o for o in all_orders}
		record_id2orders = {}
		for rid in record_ids:
			rid = str(rid)
			member_ids = record_own_member_ids.get(rid, None)
			if not member_ids:
				continue
			for mid in member_ids:
				if not record_id2orders.has_key(rid):
					record_id2orders[rid] = member_id2order_ids[mid]
				else:
					record_id2orders[rid] += member_id2order_ids[mid]
		record_id2cash = {}
		record_id2first_buy_num = {}
		for rid, order_ids in record_id2orders.items():
			record = id2record[rid]
			has_order = False
			for oid in order_ids:
				oid = str(oid)
				if not record_id2cash.has_key(rid):
					record_id2cash[rid] = id2order[oid].final_price
				else:
					record_id2cash[rid] += id2order[oid].final_price
				if not record_id2first_buy_num.has_key(rid):
					if not has_order and (id2order[oid].created_at > record.start_time or id2order[oid].created_at < record.end_time):
						record_id2first_buy_num[rid] = 1
						has_order = True
				else:
					if not has_order and (id2order[oid].created_at > record.start_time or id2order[oid].created_at < record.end_time):
						record_id2first_buy_num[rid] += 1
						has_order = True

		for data in datas:
			str_id = str(data.id)
			items.append({
				'id': str_id,
				'owner_id': data.owner_id,
				'name': data.name,
				'attention_number': len(record_id2partis[str_id]) if record_id2partis.get(str_id, None) else 0,
				'order_money': record_id2cash[str_id] if record_id2cash.get(str_id, None) else 0,
				'first_buy_num': record_id2first_buy_num[str_id] if record_id2cash.get(str_id, None) else 0,
				'start_time': data.start_time.strftime('%Y-%m-%d %H:%M'),
				'end_time': data.end_time.strftime('%Y-%m-%d %H:%M'),
				'status': data.status_text,
				'ticket': data.ticket,
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
