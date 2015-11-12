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
		member = request.member

		if 'new_app:' in record_id:
			project_id = record_id
			record_id = 0
			record = None
		elif member:
			member_id = member.id
			isMember =request.member.is_subscribed
			fid = request.GET.get('fid', None)

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

				#检查所有当前参与用户是否取消关注，清空其助力值同时设置为未参与
				clear_non_member_power_info(record_id)

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

				#判断分享页是否自己的主页
				if fid is None or str(fid) == str(member_id):
					page_owner_name = request.member.username_size_ten
					page_owner_member_id = member_id
					self_page = True
				else:
					page_owner_name = Member.objects.get(id=fid).username_size_ten
					page_owner_member_id = fid
					if curr_member_power_info.powered_member_id:
						is_powered = fid in curr_member_power_info.powered_member_id

				participances = app_models.PowerMeParticipance.objects(belong_to=record_id, has_join=True).order_by('-power', 'created_at')
				total_participant_count = participances.count()

				#遍历log，统计助力值
				power_logs = app_models.PowerLog.objects(belong_to=record_id)
				power_member_ids = [p.power_member_id for p in power_logs]
				member_id2subscribe = {m.id: m.is_subscribed for m in Member.objects.filter(id__in=power_member_ids)}
				power_logs = [p for p in power_logs if member_id2subscribe[p.power_member_id]]
				power_log_ids = [p.id for p in power_logs]
				need_power_member_ids = [p.be_powered_member_id for p in power_logs]
				#计算助力值
				need_power_member_id2power = {}
				for m_id in need_power_member_ids:
					if not need_power_member_id2power.has_key(m_id):
						need_power_member_id2power[m_id] = 1
					else:
						need_power_member_id2power[m_id] += 1
				for m_id in need_power_member_id2power.keys():
					app_models.PowerMeParticipance.objects(belong_to=record_id,member_id=m_id).update(inc__power=need_power_member_id2power[m_id])

				#删除计算过的log
				app_models.PowerLog.objects(id__in=power_log_ids).delete()

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
						'username': member_id2member[p.member_id].username_size_ten,
						'power': p.power
					})
					if member_id == p.member_id:
						current_member_rank_info = {
							'rank': rank,
							'power': p.power
						}
				# 取前100位
				participances_list = participances_list[:100]

			else:
				c = RequestContext(request, {
					'is_deleted_data': True
				})
				return render_to_response('powerme/templates/webapp/m_powerme.html', c)

		else:
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
			'isPC': False if request.member else True,
			'isMember': isMember,
			'is_powered': is_powered, #是否已为该member助力
			'is_self_page': self_page, #是否自己主页
			'participances_list': json.dumps(participances_list),
			'share_page_title': mpUserPreviewName,
			'share_img_url': record.material_image if record else '',
			'share_page_desc': record.name if record else u"微助力",
			'params_qrcode_url': record.qrcode['ticket'] if record.qrcode else False,
			'params_qrcode_name': record.qrcode['name'] if record.qrcode else False,
			'timing': timing,
			'current_member_rank_info': current_member_rank_info, #我的排名
			'total_participant_count': total_participant_count, #总参与人数
			'page_owner_name': page_owner_name,
			'page_owner_member_id': page_owner_member_id,
			'reply_content': record.reply_content if record else '',
			'mpUserPreviewName': mpUserPreviewName,
			'share_to_timeline_use_desc': True  #分享到朋友圈的时候信息变成分享给朋友的描述
		})
		return render_to_response('powerme/templates/webapp/m_powerme.html', c)

def clear_non_member_power_info(record_id):
	"""
	所有取消关注的参与用户，清空其助力值同时设置为未参与
	:param record_id: 活动id
	"""
	record_id = str(record_id)
	all_member_power_info = app_models.PowerMeParticipance.objects(belong_to=record_id, has_join=True)
	all_member_power_info_ids = [p.member_id for p in all_member_power_info]
	need_clear_member_ids = [m.id for m in Member.objects.filter(id__in=all_member_power_info_ids, is_subscribed=False)]
	app_models.PowerMeParticipance.objects(belong_to=record_id, member_id__in=need_clear_member_ids).update(set__power=0, set__has_join=False)

