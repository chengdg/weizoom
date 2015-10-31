# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from core import resource

import models as app_models
from termite2 import pagecreater
from utils import url_helper
from weixin.user.module_api import get_mp_qrcode_img
from modules.member.models import Member

class MPowerMe(resource.Resource):
	app = 'apps/powerme'
	resource = 'm_powerme'
	
	def get(request):
		"""
		响应GET
		"""
		record_id = request.GET.get('id','id')
		isPC = request.GET.get('isPC',0)
		isMember = False
		qrcode_url = ''
		timing = 0
		mpUserPreviewName = ''
		is_already_participanted = False
		is_powered = False
		self_page = False
		fid = None
		current_member_rank_info = None
		participances_list = []
		total_participant_count = 0
		page_owner_name = ''
		page_owner_member_id = 0
		activity_status = u"未开始"

		if 'new_app:' in record_id:
			project_id = record_id
			record_id = 0
			record = None
		elif isPC:
			record = app_models.PowerMe.objects(id=record_id)
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

				project_id = 'new_app:powerme:%s' % record.related_page_id
			else:
				c = RequestContext(request, {
					'is_deleted_data': True
				})
				return render_to_response('powerme/templates/webapp/m_powerme.html', c)
		else:
			member = request.member
			member_id = member.id
			isMember =request.member.is_subscribed
			if hasattr(request, "webapp_owner_info") and request.webapp_owner_info and hasattr(request.webapp_owner_info, "qrcode_img") :
				qrcode_url = request.webapp_owner_info.qrcode_img
			else:
				qrcode_url = get_mp_qrcode_img(request.webapp_owner_id)

			fid = request.GET.get('fid', None)

			qrcode_url = qrcode_url if qrcode_url is not None else ''

			if not fid:
				new_url = url_helper.add_query_part_to_request_url(request.get_full_path(), 'fid', member_id)
				response = HttpResponseRedirect(new_url)
				response.set_cookie('fid', member_id, max_age=60*60*24*365)
				return response
			record = app_models.PowerMe.objects(id=record_id)
			if record.count() >0:
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

				project_id = 'new_app:powerme:%s' % record.related_page_id

				#增加/更新当前member的参与信息
				curr_member_power_info = app_models.PowerMeParticipance.objects(belong_to=record_id, member_id=member_id)
				if curr_member_power_info.count()> 0:
					curr_member_power_info = curr_member_power_info.first()
				else:
					curr_member_power_info = app_models.PowerMeParticipance(
						belong_to = record_id,
						member_id = member_id,
						created_at = datetime.now()
					)
					curr_member_power_info.save()
				is_already_participanted = curr_member_power_info.has_join

				#如果当前member不是会员，则清空其助力值
				if not isMember:
					curr_member_power_info.update(set__power=0)

				#判断分享页是否自己的主页
				if fid is None or str(fid) == str(member_id):
					#调整参与数量(首先检测是否已参与)
					if not is_already_participanted:
						app_models.PowerMe.objects(id=record_id).update(inc__participant_count=1)
						curr_member_power_info.update(set__has_join=True)
						curr_member_power_info.reload()

					page_owner_name = request.member.username_for_html

					page_owner_member_id = member_id

					self_page = True
				else:
					page_owner_name = Member.objects.get(id=fid).username_for_html
					page_owner_member_id = fid
					if curr_member_power_info.powered_member_id:
						is_powered = fid in curr_member_power_info.powered_member_id

				participances = app_models.PowerMeParticipance.objects(belong_to=record_id, has_join=True).order_by('-power', 'created_at')
				total_participant_count = participances.count()
				# 取前100位
				participances = participances[:100]

				member_ids = [p.member_id for p in participances]
				member_id2member = {m.id: m for m in Member.objects.filter(id__in=member_ids)}

				#检查是否有当前member的排名信息
				current_member_rank_info = None
				rank = 0 #排名

				for p in participances:
					rank += 1
					participances_list.append({
						'rank': rank,
						'member_id': p.member_id,
						'user_icon': member_id2member[p.member_id].user_icon,
						'username': member_id2member[p.member_id].username_for_html,
						'power': p.power
					})
					if member_id == p.member_id:
						current_member_rank_info = {
							'rank': rank,
							'power': p.power
						}

			else:
				c = RequestContext(request, {
					'is_deleted_data': True
				})
				return render_to_response('powerme/templates/webapp/m_powerme.html', c)
		request.GET._mutable = True
		request.GET.update({"project_id": project_id})
		request.GET._mutable = False
		html = pagecreater.create_page(request, return_html_snippet=True)

		if u"进行中" == activity_status:
			timing = (record.end_time - datetime.today()).total_seconds()

		c = RequestContext(request, {
			'record_id': record_id,
			'activity_status': activity_status,
			'is_already_participanted': is_already_participanted,
			'page_title': record.name if record else u"微助力",
			'page_html_content': html,
			'app_name': "powerme",
			'resource': "powerme",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': isPC,
			'isMember': isMember,
			'is_powered': is_powered, #是否已为该member助力
			'is_self_page': self_page, #是否自己主页
			'participances_list': json.dumps(participances_list),
			'share_page_title': mpUserPreviewName,
			'share_img_url': record.material_image if record else '',
			'share_page_desc': record.name if record else u"微助力",
			'qrcode_url': qrcode_url,
			'timing': timing,
			'current_member_rank_info': current_member_rank_info, #我的排名
			'total_participant_count': total_participant_count, #总参与人数
			'page_owner_name': page_owner_name,
			'page_owner_member_id': page_owner_member_id,
			'reply_content': record.reply_content if record else '',
			'mpUserPreviewName': mpUserPreviewName
		})
		return render_to_response('powerme/templates/webapp/m_powerme.html', c)
