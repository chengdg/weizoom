# -*- coding: utf-8 -*-

import json
from datetime import datetime
from apps.customerized_apps.red_packet.red_packet_participance import participate_red_packet
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
from weixin.user.module_api import get_mp_qrcode_img
from modules.member.models import Member


class MRedPacket(resource.Resource):
	app = 'apps/red_packet'
	resource = 'm_red_packet'

	def api_get(request):
		record_id = request.GET.get('id', None)
		member = request.member
		member_id = member.id
		fid = request.GET.get('fid', member_id)
		response = create_response(500)
		if not record_id or not member_id:
			response.errMsg = u'活动信息出错'
			return response.get_response()
		record = app_models.RedPacket.objects(id=record_id)
		if record.count() <= 0:
			response.errMsg = 'is_deleted'
			return response.get_response()

		# 统计帮助者信息
		helpers_info_list = []
		helpers = app_models.RedPacketDetail.objects(belong_to=record_id, owner_id=fid,has_helped=True,is_valid=True).order_by('-created_at')
		member_ids = [h.helper_member_id for h in helpers]
		member_id2member = {m.id: m for m in Member.objects.filter(id__in=member_ids)}
		for h in helpers:
			temp_dict = {
				'member_id': h.helper_member_id,
				'user_icon': member_id2member[h.helper_member_id].user_icon,
				'username': member_id2member[h.helper_member_id].username_size_ten,
				'help_money': h.help_money
			}
			helpers_info_list.append(temp_dict)
		isMember = False
		timing = 0
		mpUserPreviewName = ''
		mpUserHeadImg = ''
		is_already_participanted = False
		is_helped = False
		self_page = False
		red_packet_status = False
		page_owner_name = ''
		page_owner_icon = ''
		page_owner_member_id = 0
		red_packet_money = 0
		current_money = 0
		activity_status = u"未开始"

		# fid = request.COOKIES['fid']

		if 'new_app:' in record_id:
			project_id = record_id
			record_id = 0
			record = None
		elif member:
			isMember =member.is_subscribed
			record = app_models.RedPacket.objects(id=record_id)
			if record.count() >0:
				record = record.first()
				#获取公众号昵称
				mpUserPreviewName = request.webapp_owner_info.auth_appid_info.nick_name
				#获取公众号头像
				mpUserHeadImg = request.webapp_owner_info.auth_appid_info.head_img
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

				project_id = 'new_app:red_packet:%s' % record.related_page_id

				#检查所有当前参与用户是否取消关注，设置为未参与
				reset_member_helper_info(record_id)
				reset_re_subscribed_member_helper_info(record_id)
				#未关注进行点赞，后来又关注的会员将帮助值加上
				update_be_member_help_details(record_id)

				curr_member_red_packet_info = app_models.RedPacketParticipance.objects(belong_to=record_id, member_id=member_id)
				if curr_member_red_packet_info.count()> 0:
					curr_member_red_packet_info = curr_member_red_packet_info.first()
					if (not curr_member_red_packet_info.is_valid) or (not curr_member_red_packet_info.has_join):
							if fid is None or str(fid) == str(member_id):#判断分享页是否自己的主页
								if isMember:
									#曾经参与过又取关了，或者帮助过他人但是自己没参与，都需要参与一次
									participate_response = participate_red_packet(record_id,member_id)
									print('participate_red_packet in line:107')
									if json.loads(participate_response.content)['errMsg'] == 'is_run_out':
										response.errMsg = 'is_run_out'
										return response.get_response()
									curr_member_red_packet_info.reload()
								else:
									response.errMsg = u'请先关注公众号'
									return response.get_response()
				else:
					curr_member_red_packet_info = app_models.RedPacketParticipance(
						belong_to = record_id,
						member_id = member_id,
						created_at = datetime.now()
					)
					curr_member_red_packet_info.save()
					#未帮助好友情况下，判断分享页是否自己的主页，是自己的主页则参与拼红包
					if fid is None or str(fid) == str(member_id):
						participate_response = participate_red_packet(record_id,member_id)
						print('participate_red_packet in line:122')
						if json.loads(participate_response.content)['errMsg'] == 'is_run_out':
							response.errMsg = 'is_run_out'
							return response.get_response()
						curr_member_red_packet_info.reload()

				is_already_participanted = curr_member_red_packet_info.has_join

				#判断分享页是否自己的主页
				if fid is None or str(fid) == str(member_id):
					page_owner_name = member.username_size_ten
					page_owner_icon = member.user_icon
					page_owner_member_id = member_id
					self_page = True
					red_packet_money = curr_member_red_packet_info.red_packet_money
					current_money = curr_member_red_packet_info.current_money
					red_packet_status = curr_member_red_packet_info.red_packet_status
				else:
					page_owner = Member.objects.get(id=fid)
					page_owner_name = page_owner.username_size_ten
					page_owner_icon = page_owner.user_icon
					page_owner_member_id = fid

					page_owner_member_info = app_models.RedPacketParticipance.objects.get(belong_to=record_id, member_id=page_owner_member_id)
					red_packet_money = page_owner_member_info.red_packet_money
					current_money = page_owner_member_info.current_money
					red_packet_status = page_owner_member_info.red_packet_status

					if curr_member_red_packet_info.helped_member_id:
						is_helped = True if fid in curr_member_red_packet_info.helped_member_id else False
			else:
				response.errMsg = u'活动信息出错'
				return response.get_response()
		else:
			record = app_models.RedPacket.objects(id=record_id)
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

				project_id = 'new_app:red_packet:%s' % record.related_page_id
			else:
				response.errMsg = 'is_deleted_data'
				return response.get_response()


		if u"进行中" == activity_status:
			timing = (record.end_time - datetime.today()).total_seconds()

		member_info = {
			'isMember': isMember,
			'timing': timing,
			'mpUserPreviewName': mpUserPreviewName,
			'mpUserHeadImg': mpUserHeadImg,
			'is_already_participanted': is_already_participanted,
			'is_helped': is_helped,
			'self_page': self_page,
			'member_id': member_id,
			'page_owner_name': page_owner_name,
			'page_owner_icon': page_owner_icon,
			'page_owner_member_id': page_owner_member_id,
			'activity_status': activity_status,
			'red_packet_status': red_packet_status,
			'red_packet_money': '%.2f' % red_packet_money,
			'current_money': '%.2f' % current_money
		}

		response = create_response(200)
		response.data = {
			'member_info': member_info,
			'helpers_info': helpers_info_list
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
			
			# cache_key = 'apps_red_packet_%s_html' % record_id
			#从redis缓存获取静态页面
			# cache_data = GET_CACHE(cache_key)
			# if cache_data:
			# 	print 'redis---return'
			# 	return HttpResponse(cache_data)
			
			record = app_models.RedPacket.objects(id=record_id)
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
				project_id = 'new_app:red_packet:%s' % record.related_page_id

				#检查所有当前参与用户是否取消关注，设置为未参与
				reset_member_helper_info(record_id)
				reset_re_subscribed_member_helper_info(record_id)

				#未关注进行点赞，后来又关注的会员将帮助值加上
				update_be_member_help_details(record_id)
			else:
				c = RequestContext(request, {
					'is_deleted_data': True
				})
				return render_to_response('red_packet/templates/webapp/m_red_packet.html', c)

		else:
			record = app_models.RedPacket.objects(id=record_id)
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

				project_id = 'new_app:red_packet:%s' % record.related_page_id
			else:
				c = RequestContext(request, {
					'is_deleted_data': True
				})
				return render_to_response('red_packet/templates/webapp/m_red_packet.html', c)

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
			'page_title': record.name if record else u"拼红包",
			'page_html_content': html,
			'app_name': "red_packet",
			'resource': "red_packet",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': False if request.member else True,
			'share_page_title': mpUserPreviewName,
			'share_img_url': record.material_image if record else '',
			'share_page_desc': record.name if record else u"拼红包",
			'params_qrcode_url': params_qrcode_url,
			'params_qrcode_name': params_qrcode_name,
			'reply_content': record.reply_content if record else '',
			'mpUserPreviewName': mpUserPreviewName,
			'share_to_timeline_use_desc': True  #分享到朋友圈的时候信息变成分享给朋友的描述
		})
		response = render_to_string('red_packet/templates/webapp/m_red_packet.html', c)
		# if request.member:
		# 	SET_CACHE(cache_key, response)
		return HttpResponse(response)

def reset_re_subscribed_member_helper_info(record_id):
	"""
	所有取消关注再关注的参与用户，清空其金额，但是红包状态、发放状态暂时不改变（防止完成拼红包后，通过取关方式再次参与）
	清空日志
	:param record_id: 活动id
	"""
	record_id = str(record_id)
	all_unvalid_member_red_packets_info = app_models.RedPacketParticipance.objects(belong_to=record_id, is_valid=False)
	all_member_red_packet_info_ids = [p.member_id for p in all_unvalid_member_red_packets_info]
	re_subscribed_ids = [m.id for m in Member.objects.filter(id__in=all_member_red_packet_info_ids, is_subscribed=True)]

	#已成功的不清除记录，只是使之有效，且不可以重新领取红包（has_join=True）
	need_reset_member_ids = [p.member_id for p in app_models.RedPacketParticipance.objects.filter(member_id__in=re_subscribed_ids, red_packet_status=True)]
	app_models.RedPacketParticipance.objects(belong_to=record_id, member_id__in=need_reset_member_ids).update(set__has_join = True,set__is_valid = True)


def reset_member_helper_info(record_id):
	"""
	所有取消关注的用户，设置为未参与，参与记录无效，但是红包状态、发放状态暂时不改变（防止完成拼红包后，通过取关方式再次参与）
	:param record_id: 活动id
	"""
	record_id = str(record_id)
	all_member_red_packets_info = app_models.RedPacketParticipance.objects(belong_to=record_id, has_join=True)
	all_member_red_packet_info_ids = [p.member_id for p in all_member_red_packets_info]
	need_clear_member_ids = [m.id for m in Member.objects.filter(id__in=all_member_red_packet_info_ids, is_subscribed=False)]
	need_clear_participances = app_models.RedPacketParticipance.objects(belong_to=record_id, member_id__in=need_clear_member_ids)
	need_clear_participances.update(set__has_join=False,set__is_valid=False)

	red_packet_info = app_models.RedPacket.objects.get(id=record_id)
	type = red_packet_info.type
	# 拼手气红包，取关了的参与者，需要把已领取的放回总红包池中
	if type == u'random':
		random_total_money = float(red_packet_info.random_total_money)
		random_packets_number = float(red_packet_info.random_packets_number)
		random_average = round(random_total_money/random_packets_number,2) #红包金额/红包个数
		for p in need_clear_participances:
			red_packet_info.random_random_number_list.append(p.red_packet_money-random_average )
		red_packet_info.save()

def update_be_member_help_details(record_id):
	#更新已关注会员的点赞详情
	need_del_red_packet_logs_ids = []
	red_packets = app_models.RedPacket.objects(status=1)
	red_packet_ids = [str(p.id) for p in red_packets]
	red_packet_logs = app_models.RedPacketLog.objects(belong_to__in=red_packet_ids)
	red_packet_member_ids = [p.helper_member_id for p in red_packet_logs]
	member_id2subscribe = {m.id: m.is_subscribed for m in Member.objects.filter(id__in=red_packet_member_ids)}

	need_be_add_logs = [p for p in red_packet_logs if member_id2subscribe[p.helper_member_id]]
	red_packet_log_ids = [p.id for p in need_be_add_logs]
	be_helped_member_ids = [p.be_helped_member_id for p in need_be_add_logs]

	red_packet_details = app_models.RedPacketDetail.objects(belong_to__in=red_packet_ids)
	#计算点赞金额值
	need_helped_member_id2money = {}
	for m_id in be_helped_member_ids:
		help_money = red_packet_details.filter(owner_id=m_id).first().help_money
		if not need_helped_member_id2money.has_key(m_id):
			need_helped_member_id2money[m_id] = help_money
		else:
			need_helped_member_id2money[m_id] += help_money
	for m_id in need_helped_member_id2money.keys():
		app_models.RedPacketParticipance.objects(belong_to=record_id,member_id=m_id).update(inc__current_money=need_helped_member_id2money[m_id])

	#更新已关注会员的点赞详情
	detail_helper_member_ids = [p.helper_member_id for p in need_be_add_logs]
	app_models.RedPacketDetail.objects(belong_to=record_id, helper_member_id__in=detail_helper_member_ids).update(set__has_helped=True)
	need_del_red_packet_logs_ids += red_packet_log_ids

	#删除计算过的log
	app_models.RedPacketLog.objects(id__in=need_del_red_packet_logs_ids).delete()