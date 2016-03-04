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
		member = request.member
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

		isMember = False
		timing = 0
		is_already_participanted = False
		is_helped = False
		self_page = False
		group_status = False
		page_owner_name = ''
		page_owner_icon = ''
		page_owner_member_id = 0
		grouped_member_info_list = []

		if member:
			member_id = member.id
			fid = request.GET.get('fid', member_id)
			isMember =member.is_subscribed
			if u"进行中" == activity_status:
				timing = (record.end_time - datetime.today()).total_seconds()
				curr_member_group_info = app_models.GroupParticipance.objects(belong_to=record_id, member_id=member_id)
				if curr_member_group_info.count()> 0:
					curr_member_group_info = curr_member_group_info.first()
				else:
					curr_member_group_info = app_models.GroupParticipance(
						belong_to = record_id,
						member_id = member_id,
						created_at = datetime.now()
					)
					curr_member_group_info.save()
				curr_member_order = Order.objects.filter(webapp_user_id=member_id,is_group_order=True,group_record_id=record_id)
				print('curr_member_order!!!!!!!!!')
				print(curr_member_order)
				if curr_member_order.count()> 0:
					curr_member_group_info.update(set__is_already_paid=True,set__is_group_leader=True)
				if curr_member_group_info.is_valid:
					is_already_participanted = curr_member_group_info.is_already_paid
				else:
					is_already_participanted = False

				#判断分享页是否自己的主页
				if fid is None or str(fid) == str(member_id):
					page_owner_name = member.username_size_ten
					page_owner_icon = member.user_icon
					page_owner_member_id = member_id
					self_page = True
					group_status = curr_member_group_info.group_status
				else:
					page_owner = Member.objects.get(id=fid)
					page_owner_name = page_owner.username_size_ten
					page_owner_icon = page_owner.user_icon
					page_owner_member_id = fid
					page_owner_member_info = app_models.GroupParticipance.objects.get(belong_to=record_id, member_id=page_owner_member_id)
					group_status = page_owner_member_info.group_status
					is_helped = app_models.GroupRelations.objects(belong_to=record_id, member_id=str(member_id), grouped_member_id=fid).count()>0

				# 获取该主页帮助者列表
				helpers = app_models.GroupedDetail.objects(belong_to=record_id, owner_id=fid,is_already_paid=True).order_by('-created_at')
				member_ids = [h.helper_member_id for h in helpers]
				member_id2member = {m.id: m for m in Member.objects.filter(id__in=member_ids)}
				for h in helpers:
					temp_dict = {
						'member_id': h.helper_member_id,
						'user_icon': member_id2member[h.helper_member_id].user_icon,
						'username': member_id2member[h.helper_member_id].username_size_ten
					}
					grouped_member_info_list.append(temp_dict)

		member_info = {
			'isMember': isMember,
			'timing': timing,
			'is_already_participanted': is_already_participanted,
			'is_helped': is_helped,
			'self_page': self_page,
			'page_owner_name': page_owner_name,
			'page_owner_icon': page_owner_icon,
			'page_owner_member_id': page_owner_member_id,
			'activity_status': activity_status,
			'group_status': group_status
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

		if 'new_app:' in record_id:
			project_id = record_id
			record_id = 0
			record = None
		elif member:
			member_id = member.id
			fid = request.GET.get('fid', None)
			if not fid:
				new_url = url_helper.add_query_part_to_request_url(request.get_full_path(), 'fid', member_id)
				response = HttpResponseRedirect(new_url)
				response.set_cookie('fid', member_id, max_age=60*60*24*365)
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

		params_qrcode_url = False
		params_qrcode_name = False

		try:
			params_qrcode_url = record.qrcode['ticket']
			params_qrcode_name = record.qrcode['name']
		except:
			pass

		c = RequestContext(request, {
			'record_id': record_id,
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
			'params_qrcode_url': params_qrcode_url,
			'params_qrcode_name': params_qrcode_name,
			'share_to_timeline_use_desc': True  #分享到朋友圈的时候信息变成分享给朋友的描述
		})
		response = render_to_string('group/templates/webapp/m_group.html', c)
		# if request.member:
		# 	SET_CACHE(cache_key, response)
		return HttpResponse(response)