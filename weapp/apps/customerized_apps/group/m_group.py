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
from mall.models import *

class MGroup(resource.Resource):
	app = 'apps/group'
	resource = 'm_group'

	def api_get(request):
		record_id = request.GET.get('id', None)
		group_relation_id = request.GET.get('group_relation_id', None)
		member = request.member
		isMember = False
		timing = 0
		is_group_leader = False
		is_group_unpaid = False #开团成功但未支付成功
		is_helped = False
		self_page = False
		group_status = 0
		group_type = ''
		grouped_number = 0
		# product_original_price = 0
		# product_group_price = 0
		page_owner_name = ''
		page_owner_icon = ''
		page_owner_member_id = 0
		grouped_member_info_list = []

		response = create_response(500)
		if not record_id:
			response.errMsg = u'活动信息出错'
			return response.get_response()
		record = app_models.Group.objects(id=record_id)
		if record.count() <= 0:
			response.errMsg = 'is_deleted'
			return response.get_response()
		record = record.first()
		#获取活动状态
		activity_status = record.status_text
		now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
		data_start_time = record.start_time.strftime('%Y-%m-%d %H:%M')
		data_end_time = record.end_time.strftime('%Y-%m-%d %H:%M')
		if data_start_time <= now_time and now_time < data_end_time:
			record.update(set__status=app_models.STATUS_RUNNING)
			activity_status = u'进行中'
		elif now_time >= data_end_time:
			record.update(set__status=app_models.STATUS_STOPED)
			activity_status = u'已结束'

		if member:
			member_id = member.id
			fid = request.GET.get('fid', member_id)
			isMember =member.is_subscribed
			if u"进行中" == activity_status:
				current_member_group_relation = app_models.GroupRelations.objects(belong_to=record_id,member_id=str(member_id))
				if current_member_group_relation.count() > 0:
					current_member_group_relation = current_member_group_relation.first()
					if current_member_group_relation.group_status == app_models.GROUP_NOT_START: #开团成功但未支付成功
						is_group_unpaid = True
				if group_relation_id:
					# 已经开过团
					group_relation_info = app_models.GroupRelations.objects.get(id=group_relation_id)
					group_status = group_relation_info.group_status
					group_type = group_relation_info.group_type
					grouped_number = group_relation_info.grouped_number
					timing = (group_relation_info.created_at + timedelta(days=int(group_relation_info.group_days)) - datetime.today()).total_seconds()
					if timing <= 0 and group_relation_info.group_status==app_models.GROUP_RUNNING:
						group_relation_info.update(set__group_status=app_models.GROUP_FAILURE)
					#判断分享页是否自己的主页
					if fid is None or str(fid) == str(member_id):
						is_group_leader = True if group_relation_info.member_id == str(member_id) else False
					else:
						is_helped = True if str(member_id) in group_relation_info.grouped_member_ids else False

					# 获取该主页帮助者列表
					helpers = app_models.GroupDetail.objects(relation_belong_to=group_relation_id, owner_id=fid,is_already_paid=True).order_by('-created_at')
					member_ids = [h.grouped_member_id for h in helpers]
					member_id2member = {m.id: m for m in Member.objects.filter(id__in=member_ids)}
					for h in helpers:
						temp_dict = {
							'member_id': h.grouped_member_id,
							'user_icon': member_id2member[h.grouped_member_id].user_icon,
							'username': member_id2member[h.grouped_member_id].username_size_ten
						}
						grouped_member_info_list.append(temp_dict)

				#判断分享页是否自己的主页
				if fid is None or str(fid) == str(member_id):
					page_owner_name = member.username_size_ten
					page_owner_icon = member.user_icon
					page_owner_member_id = member_id
					self_page = True
				else:
					page_owner = Member.objects.get(id=fid)
					page_owner_name = page_owner.username_size_ten
					page_owner_icon = page_owner.user_icon
					page_owner_member_id = fid

		member_info = {
			'isMember': isMember,
			'timing': timing,
			'self_page': self_page,
			'is_helped': is_helped,
			'is_group_leader': is_group_leader,
			'is_group_unpaid': is_group_unpaid,
			'page_owner_name': page_owner_name,
			'page_owner_icon': page_owner_icon,
			'page_owner_member_id': page_owner_member_id,
			'activity_status': activity_status,
			'group_status': group_status, #小团购状态
			'group_type': int(group_type) if group_type !='' else '',
			'grouped_number': int(grouped_number),
			'member_id': member_id if member else ''
			# 'product_original_price': product_original_price,
			# 'product_group_price': product_group_price
		}

		response = create_response(200)
		response.data = {
			'member_info': member_info,
			'helpers_info': grouped_member_info_list
		}
		return response.get_response()

	def get(request):
		"""
		响应GET
		"""
		record_id = request.GET.get('id','id')
		mpUserPreviewName = ''
		activity_status = u"未开始"
		member = request.member
		fid = 0
		group_relation_id = 0
		product_id = None

		if 'new_app:' in record_id:
			project_id = record_id
			record_id = 0
			record = None
		elif member:
			member_id = member.id
			fid = request.GET.get('fid', None)
			group_relation_id = request.GET.get('group_relation_id', None)

			#判断分享页是否自己的主页
			if not fid:
				new_url = url_helper.add_query_part_to_request_url(request.get_full_path(), 'fid', member_id)
				response = HttpResponseRedirect(new_url)
				response.set_cookie('fid', member_id, max_age=60*60*24*365)
				return response

			if not group_relation_id:
				group_relation = app_models.GroupRelations.objects(belong_to=record_id, member_id=str(member_id), group_status=app_models.GROUP_RUNNING)
				if group_relation.count() > 0:
					group_relation = group_relation.first()
					group_relation_id = group_relation.id
					new_url = url_helper.add_query_part_to_request_url(request.get_full_path(), 'group_relation_id', group_relation_id)
					response = HttpResponseRedirect(new_url)
					response.set_cookie('group_relation_id', group_relation_id, max_age=60*60*24*365)
					return response

			# cache_key = 'apps_group_%s_html' % record_id
			# # 从redis缓存获取静态页面
			# cache_data = GET_CACHE(cache_key)
			# if cache_data:
			# 	print 'redis---return'
			# 	return HttpResponse(cache_data)

			record = app_models.Group.objects(id=record_id)
			if record.count() > 0:
				record = record.first()
				#获取公众号昵称
				mpUserPreviewName = request.webapp_owner_info.auth_appid_info.nick_name
				#获取活动状态
				activity_status = record.status_text
				product_id = record.product_id

				now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
				data_start_time = record.start_time.strftime('%Y-%m-%d %H:%M')
				data_end_time = record.end_time.strftime('%Y-%m-%d %H:%M')
				if data_start_time <= now_time and now_time < data_end_time:
					record.update(set__status=app_models.STATUS_RUNNING)
					activity_status = u'进行中'
				elif now_time >= data_end_time:
					record.update(set__status=app_models.STATUS_STOPED)
					activity_status = u'已结束'

				project_id = 'new_app:group:%s' % record.related_page_id
			else:
				c = RequestContext(request, {
					'is_deleted_data': True
				})
				return render_to_response('group/templates/webapp/m_group.html', c)

		else:
			record = app_models.Group.objects(id=record_id)
			if record.count() >0:
				record = record.first()

				#获取活动状态
				activity_status = record.status_text

				now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
				data_start_time = record.start_time.strftime('%Y-%m-%d %H:%M')
				data_end_time = record.end_time.strftime('%Y-%m-%d %H:%M')
				if data_start_time <= now_time and now_time < data_end_time:
					record.update(set__status=app_models.STATUS_RUNNING)
					activity_status = u'进行中'
				elif now_time >= data_end_time:
					record.update(set__status=app_models.STATUS_STOPED)
					activity_status = u'已结束'

				project_id = 'new_app:group:%s' % record.related_page_id
			else:
				c = RequestContext(request, {
					'is_deleted_data': True
				})
				return render_to_response('group/templates/webapp/m_group.html', c)

		request.GET._mutable = True
		request.GET.update({"project_id": project_id})
		request.GET._mutable = False
		html = pagecreater.create_page(request, return_html_snippet=True)

		c = RequestContext(request, {
			'record_id': record_id,
			'group_relation_id': group_relation_id, #小团购id，如不存在则为None
			'product_id': product_id, #产品id，如不存在则为None
			'activity_status': activity_status,
			'page_title': record.name if record else u"团购",
			'page_html_content': html,
			'app_name': "group",
			'resource': "group",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': False if request.member else True,
			'share_page_title': mpUserPreviewName,
			'share_img_url': record.material_image if record else '',
			'share_page_desc': record.name if record else u"团购",
			'share_to_timeline_use_desc': True  #分享到朋友圈的时候信息变成分享给朋友的描述
		})
		response = render_to_string('group/templates/webapp/m_group.html', c)
		# if request.member:
		# 	SET_CACHE(cache_key, response)
		return HttpResponse(response)