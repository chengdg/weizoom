# -*- coding: utf-8 -*-

import json
from datetime import *

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from core import resource

import models as app_models
from core.jsonresponse import create_response
from termite2 import pagecreater
from modules.member.models import Member

class MGroupList(resource.Resource):
	app = 'apps/group'
	resource = 'm_group_list'

	def api_get(request):
		belong_to = request.GET.get('belong_to', None)
		owner_id = request.webapp_owner_id
		if not belong_to:
			response = create_response(500)
			response.errMsg = u'活动信息出错'
			return response.get_response()
		group_relations = app_models.GroupRelations.objects(belong_to=belong_to,group_status=app_models.GROUP_RUNNING)
		group_ids = [str(p.belong_to) for p in group_relations]
		all_groups = app_models.Group.objects(id__in=group_ids)
		all_groups_can_join = []
		all_groups_can_join_part1 = [] #第一段，拼团人数差1的团。所有拼团人数差1的团以剩余时间正序排列
		all_groups_can_join_part2 = [] #第二段，拼团人数差大于1的团，以时间倒序排列。
		for group_relation in group_relations:
			if group_relation.grouped_number < int(group_relation.group_type): #只显示拼团人数未满的团
				current_group = all_groups.get(id=group_relation.belong_to)
				remain_hours = (group_relation.created_at + timedelta(days=int(group_relation.group_days))-datetime.today()).total_seconds()/(60*60)
				if int(group_relation.group_type)-group_relation.grouped_number == 1:
					all_groups_can_join_part1.append({
						'id': str(group_relation.belong_to),
						'group_relation_id': str(group_relation.id),
						'group_owner_name': group_relation.group_leader_name,
						'group_name': current_group.name,
						'product_img': current_group.product_img,
						'product_name': current_group.product_name,
						'participant_count': str(group_relation.grouped_number)+'/'+group_relation.group_type,
						'remain_hours': '%.0f' % remain_hours,
						'url': '/m/apps/group/m_group/?webapp_owner_id=%d&id=%s&group_relation_id=%s&fid=%s' % (owner_id, str(group_relation.belong_to),str(group_relation.id),str(group_relation.member_id))
					})
				else:
					all_groups_can_join_part2.append({
						'id': str(group_relation.belong_to),
						'group_relation_id': str(group_relation.id),
						'group_owner_name': group_relation.group_leader_name,
						'group_name': current_group.name,
						'product_img': current_group.product_img,
						'product_name': current_group.product_name,
						'participant_count': str(group_relation.grouped_number)+'/'+group_relation.group_type,
						'remain_hours': '%.0f' % remain_hours,
						'url': '/m/apps/group/m_group/?webapp_owner_id=%d&id=%s&group_relation_id=%s&fid=%s' % (owner_id, str(group_relation.belong_to),str(group_relation.id),str(group_relation.member_id))
					})
		all_groups_can_join_part1.sort(key=lambda item:int(item['remain_hours']))
		all_groups_can_join_part2.sort(key=lambda item:int(item['remain_hours']),reverse=True)
		all_groups_can_join_part1.extend(all_groups_can_join_part2)
		all_groups_can_join = all_groups_can_join_part1
		if all_groups_can_join == []:
			response = create_response(500)
			response.errMsg = u'暂无可参与的团购'
			return response.get_response()
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
		owner_id = request.webapp_owner_id
		#我要开团
		groups = app_models.Group.objects(owner_id=owner_id,status=app_models.STATUS_RUNNING).order_by('-end_time')
		for group in groups:
			#获取活动状态
			activity_status = group.status_text
			if activity_status == u'已结束':
				group.update(set__status=app_models.STATUS_STOPED)
			try:
				all_group_dict = []
				group_dict_tuple = json.loads(group.group_dict),
				for group_dict in group_dict_tuple:
					for g in group_dict:
						all_group_dict.append({
							'group_price': '%.2f' % float(group_dict[str(g)]['group_price']),
							'group_type': group_dict[str(g)]['group_type']
						})
				all_groups_can_open.append({
					'id': str(group.id),
					'name': group.name,
					'product_img': group.product_img,
					'all_group_dict': all_group_dict,
					'end_time': group.end_time.strftime('%Y-%m-%d'),
					'url': '/m/apps/group/m_group/?webapp_owner_id=%d&id=%s' % (owner_id, str(group.id))
				})
			except:
				pass
		c = RequestContext(request, {
			'page_title': u'团购列表',
			'all_groups_can_open': all_groups_can_open,
			'is_hide_weixin_option_menu':True,
			'app_name': "group",
			'resource': "group",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': False if request.member else True,
			'share_to_timeline_use_desc': True  #分享到朋友圈的时候信息变成分享给朋友的描述
		})
		return render_to_response('group/templates/webapp/m_group_list.html', c)