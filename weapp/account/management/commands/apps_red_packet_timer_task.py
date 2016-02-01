# -*- coding: utf-8 -*-

import time
from datetime import datetime

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
		start_time = time.time()

		"""
		更新已关注会员的点赞详情
		"""
		need_del_red_packet_logs_ids = []
		all_red_packets = app_models.RedPacket.objects(status=1)
		red_packet_ids = [str(p.id) for p in all_red_packets]
		red_packet_logs = app_models.RedPacketLog.objects(belong_to__in=red_packet_ids)
		red_packet_participances = app_models.RedPacketParticipance.objects(belong_to__in=red_packet_ids)
		red_packet_member_ids = [p.helper_member_id for p in red_packet_logs]
		member_id2subscribe = {m.id: m.is_subscribed for m in Member.objects.filter(id__in=red_packet_member_ids)}

		need_be_add_logs_list = [p for p in red_packet_logs if member_id2subscribe[p.helper_member_id]]
		red_packet_log_ids = [p.id for p in need_be_add_logs_list]
		be_helped_member_ids = [p.be_helped_member_id for p in need_be_add_logs_list]

		need_be_add_logs = red_packet_logs.filter(be_helped_member_id__in=be_helped_member_ids)
		need_be_add_record_ids = [p.belong_to for p in need_be_add_logs]
		#计算点赞金额值
		need_helped_member_id2money = {}
		record_id2member_id = {}
		for m_id in be_helped_member_ids:
			red_packet_log_info = need_be_add_logs.filter(be_helped_member_id=m_id)
			total_help_money = 0
			for i in red_packet_log_info:
				total_help_money += i.help_money
				#构造record_id2member_id键值对
				record_id2member_id[m_id] = i.belong_to
			if not need_helped_member_id2money.has_key(m_id):
				need_helped_member_id2money[m_id] = total_help_money
			else:
				need_helped_member_id2money[m_id] += total_help_money
		for r_id in need_be_add_record_ids:
			for m_id in need_helped_member_id2money.keys():
				need_helped_member_info = red_packet_participances.filter(belong_to=r_id,member_id=m_id)
				if not need_helped_member_info.first().red_packet_status: #如果红包已经拼成功，则不把钱加上去
					need_helped_member_info.update(inc__current_money=need_helped_member_id2money[m_id])
					need_helped_member_info.reload()
					#最后一个通过非会员参与完成目标金额，设置红包状态为成功
					if need_helped_member_info.current_money == need_helped_member_info.red_packet_money:
						need_helped_member_info.update(set__red_packet_status=True, set__finished_time=datetime.now())

		#更新已关注会员的点赞详情
		detail_helper_member_ids = [p.helper_member_id for p in need_be_add_logs_list]
		app_models.RedPacketDetail.objects(belong_to__in=need_be_add_record_ids, helper_member_id__in=detail_helper_member_ids).update(set__has_helped=True)
		need_del_red_packet_logs_ids += red_packet_log_ids

		#删除计算过的log
		app_models.RedPacketLog.objects(id__in=need_del_red_packet_logs_ids).delete()

		"""
		所有取消关注的用户，设置为未参与，参与记录无效，但是红包状态、发放状态暂时不改变（防止完成拼红包后，通过取关方式再次参与）
		"""
		record_id2members = {}
		all_has_join_member_ids = []
		all_has_join_participances = red_packet_participances.filter(has_join=True)
		for p in all_has_join_participances:
			all_has_join_member_ids.append(p.member_id)
			if record_id2members.has_key(p.belong_to):
				record_id2members[p.belong_to].append(p)
			else:
				record_id2members[p.belong_to] = [p]

		un_subscribed_ids = [m.id for m in Member.objects.filter(id__in=all_has_join_member_ids, is_subscribed=False)]
		need_clear_participances = all_has_join_participances.filter(member_id__in=un_subscribed_ids)
		need_clear_participances_record_ids = [p.belong_to for p in need_clear_participances]
		need_clear_participances.update(set__has_join=False,set__is_valid=False)

		for record_id in need_clear_participances_record_ids:
			red_packet_info = all_red_packets.get(id=record_id)
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
		"""
		all_unvalid_member_participance = red_packet_participances.filter(is_valid=False)
		all_unvalid_member_participance_ids = [p.member_id for p in all_unvalid_member_participance]
		re_subscribed_ids = [m.id for m in Member.objects.filter(id__in=all_unvalid_member_participance_ids, is_subscribed=True)]

		#已成功的不清除记录，只是使之有效，且不可以重新领取红包（has_join=True）
		need_reset_member_ids = [p.member_id for p in red_packet_participances.filter(member_id__in=re_subscribed_ids, red_packet_status=True)]
		red_packet_participances.filter(member_id__in=need_reset_member_ids).update(set__has_join = True,set__is_valid = True)


		end_time = time.time()
		diff = (end_time-start_time)*1000
		print 'red_packet timer task end...expend %s' % diff
