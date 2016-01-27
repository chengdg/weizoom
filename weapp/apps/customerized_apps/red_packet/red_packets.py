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

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class RedPackets(resource.Resource):
	app = 'apps/red_packet'
	resource = 'red_packets'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.RedPacket.objects.count()
		cert_ready = False
		cert_setting = app_models.RedPacketCertSettings.objects(owner_id=str(request.webapp_owner_id))
		if cert_setting.count() > 0:
			print '================'
			cert_setting = cert_setting.first()
			if '' != cert_setting.cert_path and '' != cert_setting.key_path:
				cert_ready = True

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
            'third_nav_name': export.MALL_APPS_REDPACKET_NAV,
			'has_data': has_data,
			'cert_ready': cert_ready
		})
		
		return render_to_response('red_packet/templates/editor/red_packets.html', c)
	
	@staticmethod
	def get_datas(request):
		name = request.GET.get('name', '')
		status = int(request.GET.get('status', -1))
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		red_packet_type = request.GET.get('red_packet_type','all')
		
		now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
		params = {'owner_id':request.manager.id}
		datas_datas = app_models.RedPacket.objects(**params)
		for data_data in datas_datas:
			data_start_time = data_data.start_time.strftime('%Y-%m-%d %H:%M')
			data_end_time = data_data.end_time.strftime('%Y-%m-%d %H:%M')
			if data_start_time <= now_time and now_time < data_end_time:
				data_data.update(set__status=app_models.STATUS_RUNNING)
			elif now_time >= data_end_time:
				data_data.update(set__status=app_models.STATUS_STOPED)
		if name:
			params['name__icontains'] = name
		if status != -1:
			params['status'] = status
		if start_time:
			params['start_time__gte'] = start_time
		if end_time:
			params['end_time__lte'] = end_time
		if red_packet_type != 'all':
			params['type'] = red_packet_type
		datas = app_models.RedPacket.objects(**params).order_by('-id')

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
		pageinfo, datas = RedPackets.get_datas(request)

		red_packet_ids = [str(p.id) for p in datas]

		#取消关注的参与者也算在列表中，但是一个人只算一次参与，所以取有效参与人的id与无效参与人（可能有多次）的id的并集
		all_unvalid_participances = app_models.RedPacketParticipance.objects(belong_to__in=red_packet_ids, is_valid=False)
		all_unvalid_participance_ids = [un_p.member_id for un_p in all_unvalid_participances]
		print('all_unvalid_participance_ids')
		print(all_unvalid_participance_ids)
		all_valid_participances = app_models.RedPacketParticipance.objects(belong_to__in=red_packet_ids, has_join=True, is_valid=True)
		all_valid_participance_ids = [un_p.member_id for un_p in all_valid_participances]
		print('all_valid_participance_ids',all_valid_participance_ids)
		member_ids = list(set(all_valid_participance_ids).union(set(all_unvalid_participance_ids)))
		print('member_ids!')
		print(member_ids)
		all_participances = app_models.RedPacketParticipance.objects(belong_to__in=red_packet_ids, member_id__in=member_ids)

		red_packet_id2info = {}
		for p in all_participances:
			if not p.belong_to in red_packet_id2info:
				red_packet_id2info[p.belong_to] = {
					"participant_count": 1,
					"already_paid_money": p.current_money if (p.red_packet_status and p.is_already_paid) else 0
				}
			else:
				red_packet_id2info[p.belong_to]["participant_count"] += 1
				red_packet_id2info[p.belong_to]["already_paid_money"] += p.current_money if (p.red_packet_status and p.is_already_paid) else 0

		items = []
		for data in datas:
			str_id = str(data.id)
			items.append({
				'id': str_id,
				'owner_id': data.owner_id,
				'name': data.name,
				'start_time': data.start_time.strftime('%Y-%m-%d %H:%M'),
				'end_time': data.end_time.strftime('%Y-%m-%d %H:%M'),
                'type': u'拼手气' if data.type == 'random' else u'普通',
				'participant_count': red_packet_id2info[str_id]["participant_count"] if red_packet_id2info.get(str_id, None) else 0,
				'total_money' : '%0.2f' %float(data.random_total_money) if data.type == 'random' else '%0.2f' %(float(data.regular_packets_number)*float(data.regular_per_money)),
				'already_paid_money' : '%0.2f' %float(red_packet_id2info[str_id]["already_paid_money"] if red_packet_id2info.get(str_id, None) else 0),
				'related_page_id': data.related_page_id,
				'status': data.status_text,
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

