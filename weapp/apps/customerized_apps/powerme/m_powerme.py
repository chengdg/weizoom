# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response

import models as app_models
import export
from apps import request_util
from termite2 import pagecreater
import weixin.user.models as weixin_models
from weixin.user.module_api import get_mp_qrcode_img
from modules.member.models import Member

class MPowerMe(resource.Resource):
	app = 'apps/powerme'
	resource = 'm_powerme'
	
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			record_id = request.GET['id']
			isPC = request.GET.get('isPC',0)
			project_id = record_id
			member_id = request.member.id
			isMember = False
			qrcode_url = ''
			timing = 0
			if not isPC:
				isMember =request.member.is_subscribed
				if not isMember:
					qrcode_url = get_mp_qrcode_img(request.user.id)

			record = app_models.PowerMe.objects(id=record_id)
			if 'new_app:' in record_id or record.count() == 0:
				activity_status = u"未开启"
				c = RequestContext(request, {
					'activity_status': activity_status,
					'qrcode_url': qrcode_url,
					'isPC': isPC
				})
				return render_to_response('powerme/templates/webapp/m_powerme.html', c)
			else:
				#获取、更新活动信息
				record = record.first()
				record_id = str(record.id)
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

				#判断分享页是否自己的主页
				self_page = False
				is_powered = False
				is_already_participanted = False
				fid = request.GET.get('fid', None)
				#增加/更新当前member的参与信息
				curr_member_power_info = app_models.PowerMeParticipance.objects(belong_to=record_id, member_id=member_id)
				if curr_member_power_info.count()> 0:
					curr_member_power_info = curr_member_power_info.first()
				else:
					curr_member_power_info = app_models.PowerMeParticipance(
						belong_to = record_id,
						member_id = member_id
					)
					curr_member_power_info.save()
				print '================='
				print fid
				print '================='
				if fid is None or str(fid) == str(member_id):
					self_page = True
					page_owner_name = request.member.username_for_html
					page_owner_member_id = member_id
					curr_member_power_info.update(set__has_join=True)
					curr_member_power_info.reload()
					#调整参与数量
					app_models.PowerMe.objects(id=record_id).update(**{"inc__participant_count":1})

					is_powered = fid in curr_member_power_info.powered_member_id
					is_already_participanted = True
				else:
					page_owner_name = Member.objects.get(id=fid).username_for_html
					page_owner_member_id = fid

				participances = app_models.PowerMeParticipance.objects(belong_to=record_id, has_join=True).order_by('-power')
				total_participant_count = participances.count()
				member_ids = [p.member_id for p in participances]
				member_id2member = {m.id: m for m in Member.objects.filter(id__in=member_ids)}

				#检查是否有当前member的排名信息
				current_member_rank_info = None
				participances_list = []
				rank = 0 #排名

				participances = participances[:100]
				for p in participances:
					rank += 1
					participances_list.append({
						'rank': rank,
						'member_id': p.member_id,
						'user_icon': member_id2member[p.member_id].user_icon,
						'user_name': member_id2member[p.member_id].username_for_html,
						'power': p.power
					})
					if member_id == p.member_id:
						current_member_rank_info = {
							'rank': rank,
							'power': p.power
						}

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
				'page_title': u"签到",
				'page_html_content': html,
				'app_name': "powerme",
				'resource': "powerme",
				'hide_non_member_cover': True, #非会员也可使用该页面
				'isPC': isPC,
				'isMember': isMember,
				'is_powered': is_powered, #是否已为该member助力
				'is_self_page': self_page, #是否自己主页
				'participances_list': json.dumps(participances_list),
				'share_page_title': record.name,
				'share_img_url': record.material_image,
				'share_page_desc': u"微助力",
				'qrcode_url': qrcode_url,
				'timing': timing,
				'current_member_rank_info': current_member_rank_info, #我的排名
				'total_participant_count': total_participant_count, #总参与人数
				'page_owner_name': page_owner_name,
				'page_owner_member_id': page_owner_member_id
			})
		else:
			record = None
			c = RequestContext(request, {
				'is_deleted_data': True
			})
			
		return render_to_response('powerme/templates/webapp/m_powerme.html', c)

