# -*- coding: utf-8 -*-

import time

from django.core.management.base import BaseCommand, CommandError

from utils.cache_util import SET_CACHE, delete_cache, delete_pattern
from apps.customerized_apps.red_packet import models as app_models
from modules.member.models import Member


class Command(BaseCommand):
	help = 'start red_packet stats task'
	args = ''
	
	def handle(self, *args, **options):
		"""

		@param args: clear: 清除所有apps_red_packet_*的缓存
		@param options:
		@return:
		"""
		print 'red_packet timer task start...'
		l = len(args)
		if l == 1:
			action = args[0]
			if action == 'clear':
				delete_pattern("apps_red_packet_*")
				print 'delete all cache those have the prefix apps_red_packet_'
				return
		elif l == 2:
			action = args[0]
			if action == 'clear':
				red_packet_id = args[1]
				delete_cache("apps_red_packet_"+str(red_packet_id))
				print 'delete cache names apps_red_packet_'+str(red_packet_id)
				return

		start_time = time.time()

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

		"""
		所有取消关注再关注的参与用户，清空其金额，但是红包状态、发放状态暂时不改变（防止完成拼红包后，通过取关方式再次参与）
		清空日志
		:param record_id: 活动id
		"""

		all_unvalid_member_red_packets_info = app_models.RedPacketParticipance.objects(belong_to=record_id, is_valid=False)
		all_member_red_packet_info_ids = [p.member_id for p in all_unvalid_member_red_packets_info]
		re_subscribed_ids = [m.id for m in Member.objects.filter(id__in=all_member_red_packet_info_ids, is_subscribed=True)]

		#已成功的不清除记录，只是使之有效，且不可以重新领取红包（has_join=True）
		need_reset_member_ids = [p.member_id for p in app_models.RedPacketParticipance.objects.filter(belong_to=record_id, member_id__in=re_subscribed_ids, red_packet_status=True)]
		app_models.RedPacketParticipance.objects(belong_to=record_id, member_id__in=need_reset_member_ids).update(set__has_join = True,set__is_valid = True)

		"""
		更新已关注会员的点赞详情
		"""
		need_del_red_packet_logs_ids = []
		red_packets = app_models.RedPacket.objects(status=1)
		red_packet_ids = [str(p.id) for p in red_packets]
		red_packet_logs = app_models.RedPacketLog.objects(belong_to__in=red_packet_ids)
		red_packet_member_ids = [p.helper_member_id for p in red_packet_logs]
		member_id2subscribe = {m.id: m.is_subscribed for m in Member.objects.filter(id__in=red_packet_member_ids)}

		need_be_add_logs_list = [p for p in red_packet_logs if member_id2subscribe[p.helper_member_id]]
		red_packet_log_ids = [p.id for p in need_be_add_logs_list]
		be_helped_member_ids = [p.be_helped_member_id for p in need_be_add_logs_list]

		need_be_add_logs = app_models.RedPacketLog.objects(be_helped_member_id__in=be_helped_member_ids)
		#计算点赞金额值
		need_helped_member_id2money = {}
		for m_id in be_helped_member_ids:
			red_packet_log_info = need_be_add_logs.filter(be_helped_member_id=m_id)
			total_help_money = 0
			for i in red_packet_log_info:
				total_help_money += i.help_money
			if not need_helped_member_id2money.has_key(m_id):
				need_helped_member_id2money[m_id] = total_help_money
			else:
				need_helped_member_id2money[m_id] += total_help_money
		for m_id in need_helped_member_id2money.keys():
			need_helped_member_info = app_models.RedPacketParticipance.objects(belong_to=record_id,member_id=m_id)
			if not need_helped_member_info.first().red_packet_status: #如果红包已经拼成功，则不把钱加上去
				need_helped_member_info.update(inc__current_money=need_helped_member_id2money[m_id])

		#更新已关注会员的点赞详情
		detail_helper_member_ids = [p.helper_member_id for p in need_be_add_logs_list]
		app_models.RedPacketDetail.objects(belong_to=record_id, helper_member_id__in=detail_helper_member_ids).update(set__has_helped=True)
		need_del_red_packet_logs_ids += red_packet_log_ids

		#删除计算过的log
		app_models.RedPacketLog.objects(id__in=need_del_red_packet_logs_ids).delete()
		end_time = time.time()
		diff = (end_time-start_time)*1000
		print 'red_packet timer task end...expend %s' % diff
