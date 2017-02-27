# -*- coding: utf-8 -*-

__author__ = 'jiangzhe'

import time
from datetime import datetime, timedelta
import array

from django.core.management.base import BaseCommand, CommandError

from utils import cache_util
from bson import json_util
import json

from mall.models import *
from modules.member.models import *

date_fmt = "%Y-%m-%d"
LEVEL_INFO = {
	1: {
		'order_money': 50,
		'consumer_rebates': 20
	}, 
	2: {
		'order_money': 100,
		'consumer_rebates': 40
	},
}

class Command(BaseCommand):
	help = "json.dumps cached value"
	args = ''
	
	def handle(self, today_str='today', **options):
		print '===service start==='
		all_tengyi_members = TengyiMember.objects.all()
		member_id2level = dict([(m.member_id, m.level) for m in all_tengyi_members])
		member_id2recommend_by_member_id = dict([(m.member_id, m.recommend_by_member_id) for m in all_tengyi_members])
		member_id2card_number = dict([(m.member_id, m.card_number) for m in all_tengyi_members])

		if today_str == 'today':
			today = datetime.today().date()
		else:
			today = datetime.strptime(today_str, date_fmt).date()
		#计算会员的推荐返利
		#每月1号去结算上月所有推荐人的返利情况
		this_month_first_day = today.replace(day=1)
		last_month_last_day = this_month_first_day - timedelta(1)
		last_month_first_day = last_month_last_day.replace(day=1)
		recommend_members = TengyiMember.objects.exclude(recommend_by_member_id=0)
		#获取所有上线（有推荐）会员
		recommend_member_ids = set([m.recommend_by_member_id for m in recommend_members])
		print 'need all recommend_member count', len(recommend_member_ids)
		for recommend_member_id in recommend_member_ids:
			#获取上线的信息
			tengyi_member = TengyiMember.objects.get(member_id=recommend_member_id)
			cur_member_id = tengyi_member.member_id
			cur_member_created_at = tengyi_member.created_at

			if tengyi_member.level == 1:
				recommend_member_rebate_money = 10
			#由于不同阶段返款不同，特殊处理
			elif tengyi_member.level == 2:
				recommend_member_rebate_money = 10
				#获取会员入会6个月后的日期
				after_six_month_first_day = (cur_member_created_at.date() + timedelta(6*31)).replace(day=1)
				if after_six_month_first_day <= this_month_first_day:
					recommend_member_rebate_money = 20
			else:
				recommend_member_rebate_money = 0

			print '>>>cur_member_id', cur_member_id
			#获取上月内所有该返利的人
			all_recommend_members = TengyiMember.objects.filter(recommend_by_member_id=cur_member_id)
			all_recommend_member_ids = [m.member_id for m in all_recommend_members]
			print 'all_recommend_member_ids', all_recommend_member_ids
			all_recommend_member_rebate_sycle = TengyiMemberRebateCycle.objects.filter(member_id__in=all_recommend_member_ids, receive_reward_at__range=(last_month_first_day, this_month_first_day), is_receive_reward=True, is_recommend_member_receive_reward=False)
			print 'need recharge',all_recommend_member_rebate_sycle.count()
			#返利
			for recommend_member_rebate_sycle in all_recommend_member_rebate_sycle:
				#标记被推荐人已收到返利
				recommend_member_rebate_sycle.is_recommend_member_receive_reward = True
				recommend_member_rebate_sycle.save()
				#将发奖记录保存在返利记录中
				TengyiRebateLog.objects.create(
					member_id = cur_member_id,
					is_self_order = False,
					supply_member_id = recommend_member_rebate_sycle.member_id,
					is_exchanged = False,
					rebate_money = recommend_member_rebate_money
					)


		#根据未充值的返利记录，最终调用接口充值
		need_recharge_rebate_logs = TengyiRebateLog.objects.filter(is_exchanged=False)
		for need_recharge_rebate_log in need_recharge_rebate_logs:
			member_id = need_recharge_rebate_log.member_id
			rebate_money = need_recharge_rebate_log.rebate_money
			supply_member_id = need_recharge_rebate_log.supply_member_id
			is_self_order = need_recharge_rebate_log.is_self_order
			card_number = member_id2card_number[member_id]

			if is_self_order:
				remark = u'购物返利'
			else:
				remark = u'推荐返利'
			from eaglet.utils.resource_client import Resource
			params = {
				'card_number': card_number,
				'money': rebate_money,
				'remark': remark
			}
			resp = Resource.use('card_apiserver').post({
				'resource': 'card.recharged_card',
				'data': params
			})
			if resp and resp['code'] == 200:
				print u'为%s充值%d' % (member_id, rebate_money)
				need_recharge_rebate_log.is_exchanged = True
				need_recharge_rebate_log.save()
