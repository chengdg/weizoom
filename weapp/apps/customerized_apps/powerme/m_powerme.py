# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template.loader import render_to_string

from core import resource

import models as app_models
from core.jsonresponse import create_response
from termite2 import pagecreater
from utils import url_helper
from utils.cache_util import GET_CACHE, SET_CACHE
from weixin.user.module_api import get_mp_qrcode_img
from modules.member.models import Member


class MPowerMe(resource.Resource):
	app = 'apps/powerme'
	resource = 'm_powerme'

	def api_get(request):
		record_id = request.GET.get('id', None)
		member = request.member
		member_id = member.id
		fid = request.GET.get('fid', member_id)

		user_id = request.webapp_owner_info.user_profile.user_id
		username = User.objects.get(id=user_id).username

		response = create_response(500)
		if not record_id or not member_id:
			response.errMsg = u'活动信息出错'
			return response.get_response()
		record = app_models.PowerMe.objects(id=record_id)
		if record.count() <= 0:
			response.errMsg = 'is_deleted'
			return response.get_response()
		# 统计排名信息
		current_member_rank_info = None
		cache_key = 'apps_powerme_%s' % record_id
		cache_data = GET_CACHE(cache_key)
		if username != 'weshop' and cache_data:
			participances_dict = cache_data['participances_dict']
			participances_list = cache_data['participances_list']
			total_participant_count = cache_data['total_participant_count']
			print '================from cache'
		else:
			if username == 'weshop':
				need_del_powerlogs_ids = []
				power_logs = app_models.PowerLog.objects(belong_to=record_id)
				power_member_ids = [p.power_member_id for p in power_logs]
				member_id2subscribe = {m.id: m.is_subscribed for m in Member.objects.filter(id__in=power_member_ids)}

				#统计助力值
				need_power_logs = [p for p in power_logs if member_id2subscribe[p.power_member_id]]
				power_log_ids = [p.id for p in need_power_logs]
				#更新已关注会员的助力详情记录
				detail_power_member_ids = [p.power_member_id for p in need_power_logs]
				detail = app_models.PoweredDetail.objects(belong_to=record_id, power_member_id__in=detail_power_member_ids).order_by('-id').first()
				if detail:
					detail.update(set__has_powered=True)
					#计算助力值
					app_models.PowerMeParticipance.objects(belong_to=record_id,member_id=detail.owner_id).update(inc__power=1)
					need_del_powerlogs_ids += power_log_ids
					#删除计算过的log
					app_models.PowerLog.objects(id__in=need_del_powerlogs_ids).delete()
					app_models.PoweredLimitRelation.objects(belong_to=record_id,powered_member_id=detail.owner_id,member_id=detail.power_member_id).delete()


			# 遍历log，统计助力值
			participances_dict = {}
			participances_list = []
			participances = app_models.PowerMeParticipance.objects(belong_to=record_id, has_join=True).order_by(
				'-power', 'created_at')
			total_participant_count = participances.count()
			member_ids = [p.member_id for p in participances]
			member_id2member = {m.id: m for m in Member.objects.filter(id__in=member_ids)}
			rank = 0  # 排名
			for p in participances:
				rank += 1
				temp_dict = {
					'rank': rank,
					'member_id': p.member_id,
					'user_icon': member_id2member[p.member_id].user_icon,
					'username': member_id2member[p.member_id].username_size_ten,
					'power': p.power
				}
				participances_dict[p.member_id] = temp_dict
				participances_list.append(temp_dict)
			# 取前100位
			participances_list = participances_list[:100]



			SET_CACHE(cache_key, {
				'participances_dict': participances_dict,
				'participances_list': participances_list,
				'total_participant_count': total_participant_count
			})
			print '================set cache'
		current_member_rank_info = participances_dict.get(int(member_id), None)

		isMember = False
		timing = 0
		mpUserPreviewName = ''
		is_already_participanted = False
		is_powered = False
		self_page = False
		page_owner_name = ''
		page_owner_member_id = 0
		activity_status = u"未开始"
		has_power = False

		# fid = request.COOKIES['fid']
		# fid = request.GET.get('fid', member_id)

		if 'new_app:' in record_id:
			project_id = record_id
			record_id = 0
			record = None
		elif member:
			isMember = member.is_subscribed
			record = app_models.PowerMe.objects(id=record_id)
			if record.count() > 0:
				record = record.first()
				# 获取公众号昵称
				mpUserPreviewName = request.webapp_owner_info.auth_appid_info.nick_name
				# 获取活动状态
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

				# 检查所有当前参与用户是否取消关注，清空其助力值同时设置为未参与
				# clear_non_member_power_info(record_id)

				curr_member_power_info = app_models.PowerMeParticipance.objects(belong_to=record_id,
																				member_id=member_id)
				if curr_member_power_info.count() > 0:
					curr_member_power_info = curr_member_power_info.first()
				else:
					curr_member_power_info = app_models.PowerMeParticipance(
						belong_to=record_id,
						member_id=member_id,
						created_at=datetime.now()
					)
					curr_member_power_info.save()
				is_already_participanted = curr_member_power_info.has_join

				# 判断分享页是否自己的主页
				if fid is None or str(fid) == str(member_id):
					page_owner_name = member.username_size_ten
					page_owner_member_id = member_id
					self_page = True
				else:
					user_id = request.webapp_owner_info.user_profile.user_id
					username = User.objects.get(id=user_id).username
					relation = app_models.PoweredLimitRelation.objects(belong_to=record_id,member_id=member_id,powered_member_id=fid)
					has_power = True if username == 'weshop' and relation.count() > 0 else False
					page_owner_name = Member.objects.get(id=fid).username_size_ten
					page_owner_member_id = fid
					# if curr_member_power_info.powered_member_id:
					# 	is_powered = True if fid in curr_member_power_info.powered_member_id and isMember else False
					is_powered = True if app_models.PowerMeRelations.objects(belong_to=record_id,
																			 member_id=str(member_id),
																			 powered_member_id=fid).count() > 0 and isMember else False
			else:
				response.errMsg = u'活动信息出错'
				return response.get_response()
		else:
			record = app_models.PowerMe.objects(id=record_id)
			if record.count() > 0:
				record = record.first()

				# 获取活动状态
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
				response.errMsg = 'is_deleted_data'
				return response.get_response()

		if u"进行中" == activity_status:
			timing = (record.end_time - datetime.today()).total_seconds()

		member_info = {
			'isMember': isMember,
			'timing': timing,
			'mpUserPreviewName': mpUserPreviewName,
			'is_already_participanted': is_already_participanted,
			'is_powered': is_powered,
			'self_page': self_page,
			'member_id': member_id,
			'page_owner_name': page_owner_name,
			'page_owner_member_id': page_owner_member_id,
			'activity_status': activity_status,
			'has_power': has_power
		}


		follow_friend_list = []
		unfollow_friend_list = []
		if username == 'weshop':
			details = app_models.PoweredDetail.objects(belong_to=record_id, owner_id=fid, has_powered=True)
			power_member_ids = [d.power_member_id for d in details]
			power_member_id2member = {m.id: m for m in Member.objects.filter(id__in=power_member_ids)}
			for member_id, member in power_member_id2member.items():
				if member.is_subscribed:
					follow_friend_list.append({
						'user_icon': member.user_icon,
						'username': username_size_four(member)
					})
				else:
					unfollow_friend_list.append({
						'user_icon': member.user_icon,
						'username': username_size_four(member)
					})

		response = create_response(200)
		response.data = {
			'participances': participances_list,
			'current_member_rank_info': current_member_rank_info,
			'total_participant_count': total_participant_count,
			'member_info': member_info,
			'follow_friend_list': follow_friend_list,
			'unfollow_friend_list': unfollow_friend_list
		}
		return response.get_response()

	def get(request):
		"""
		响应GET
		"""
		record_id = request.GET.get('id', 'id')
		mpUserPreviewName = ''
		activity_status = u"未开始"
		member = request.member
		fid = 0

		user_id = request.webapp_owner_info.user_profile.user_id
		username = User.objects.get(id=user_id).username

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
				response.set_cookie('fid', member_id, max_age=60 * 60 * 24 * 365)
				return response

			cache_key = 'apps_powerme_%s_html' % record_id
			# 从redis缓存获取静态页面
			cache_data = GET_CACHE(cache_key)
			if cache_data:
				print 'redis---return'
				return HttpResponse(cache_data)

			record = app_models.PowerMe.objects(id=record_id)
			if record.count() > 0:
				record = record.first()
				# 获取公众号昵称
				mpUserPreviewName = request.webapp_owner_info.auth_appid_info.nick_name
				# 获取活动状态
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

			# 检查所有当前参与用户是否取消关注，清空其助力值同时设置为未参与
			# clear_non_member_power_info(record_id)
			else:
				c = RequestContext(request, {
					'is_deleted_data': True
				})
				return render_to_response('powerme/templates/webapp/m_powerme.html', c)

		else:
			record = app_models.PowerMe.objects(id=record_id)
			if record.count() > 0:
				record = record.first()

				# 获取活动状态
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
			'page_title': record.name if record else u"微助力",
			'page_html_content': html,
			'app_name': "powerme",
			'resource': "powerme",
			'hide_non_member_cover': True,  # 非会员也可使用该页面
			'isPC': False if request.member else True,
			'share_page_title': mpUserPreviewName,
			'share_img_url': record.material_image if record else '',
			'share_page_desc': record.name if record else u"微助力",
			'params_qrcode_url': params_qrcode_url,
			'params_qrcode_name': params_qrcode_name,
			'reply_content': record.reply_content if record else '',
			'mpUserPreviewName': mpUserPreviewName,
			'share_to_timeline_use_desc': True,  # 分享到朋友圈的时候信息变成分享给朋友的描述
			'username': username
		})
		response = render_to_string('powerme/templates/webapp/m_powerme.html', c)
		if request.member:
			SET_CACHE(cache_key, response)
		return HttpResponse(response)


def clear_non_member_power_info(record_id):
	"""
	所有取消关注的参与用户，清空其助力值同时设置为未参与,重置时间
	清空日志
	[更改需求，用户取消关注后，对其现有的数据不做任何改动]
	:param record_id: 活动id
	"""

# record_id = str(record_id)
# all_member_power_info = app_models.PowerMeParticipance.objects(belong_to=record_id, has_join=True)
# all_member_power_info_ids = [p.member_id for p in all_member_power_info]
# need_clear_member_ids = [m.id for m in Member.objects.filter(id__in=all_member_power_info_ids, is_subscribed=False)]
# app_models.PowerMeParticipance.objects(belong_to=record_id, member_id__in=need_clear_member_ids).update(set__power=0, set__has_join=False)
# 清空助力详情日志
# app_models.PoweredDetail.objects(belong_to=record_id, owner_id__in=need_clear_member_ids).delete()


import re

def username_size_four(member):
	try:
		username = unicode(member.username_for_html, 'utf8')
		_username = re.sub('<[^<]+?><[^<]+?>', ' ', username)
		if len(_username) <= 4:
			return username
		else:
			name_str = username
			span_list = re.findall(r'<[^<]+?><[^<]+?>', name_str) #保存表情符

			output_str = ""
			count = 0

			if not span_list:
				return u'%s...' % name_str[:4]

			for span in span_list:
				length = len(span)
				while not span == name_str[:length]:
					output_str += name_str[0]
					count += 1
					name_str = name_str[1:]
					if count == 4:
						break
				else:
					output_str += span
					count += 1
					name_str = name_str[length:]
					if count == 4:
						break
				if count == 4:
					break
			return u'%s...' % output_str
	except:
		return member.username_for_html[:4]
