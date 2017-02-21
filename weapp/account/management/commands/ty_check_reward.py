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
	}, {
	2: {
		'order_money': 100,
		'consumer_rebates': 40
	},
}



class Command(BaseCommand):
	help = "json.dumps cached value"
	args = ''
	
	def handle(self, key, **options):
		all_tengyi_members = TengyiMember.objects.all()
		member_id2level = dict([(m.member_id, m.level) for m in all_tengyi_members])
		member_id2recommend_by_member_id = dict([(m.member_id, m.recommend_by_member_id) for m in all_tengyi_members])
		member_id2card_number = dict([(m.member_id, m.card_number) for m in all_tengyi_members])

		today = datetime.today().date()
		seven_days_ago_date = datetime.today().date() - timedelta(7)
		yesterday = today - timedelta(1)
		#计算会员自身购物返利情况
		all_tengyi_member_rebate_sycle = TengyiMemberRebateCycle.objects.filter(is_receive_reward=False,)
		for tengyi_member_sycle in all_tengyi_member_sycle:
			start_at = datetime.strptime(tengyi_member_sycle.start_time, date_fmt).date()
			end_at = datetime.strptime(tengyi_member_sycle.end_time, date_fmt).date() + timedelta(1) #查订单时候需要把截止日期后延一天
			orders = Orders.objects.filter(created_at__range=(start_at, end_at), status=ORDER_STATUS_SUCCESSED)
			order_ids = list(orders.values_list('order_id', flat=True))
			status_logs = OrderStatusLog.filter(order_id__in=order_ids, to_status=ORDER_STATUS_SUCCESSED, created_at__lt=seven_days_ago_date)
			order_ids = list(status_logs.values_list('order_id', flat=True))
			orders = Orders.objects.filter(order_id__in=order_ids)
			money_sum = 0
			for order in orders:
				money_sum += order.final_price

			cur_member_level = member_id2level[tengyi_member_sycle.member_id]
			order_money = LEVEL_INFO[cur_member_level]['order_money']
			consumer_rebates = LEVEL_INFO[cur_member_level]['consumer_rebates']
			if money_sum >= tengyi_member_sycle.rebate_money:
				#满足金额发放奖励，更新sycle表为已经发过奖励，下次不再计算
				tengyi_member_sycle.recommend_money_end_at = datetime.today()
				tengyi_member_sycle.is_receive_reward = True
				tengyi_member_sycle.save()
				#将发奖记录保存在返利记录中
				TengyiRebateLog.objects.create(
					member_id = tengyi_member_sycle.member_id,
					is_self_order = True,
					supply_member_id = 0,
					is_exchanged = False,
					rebate_money = consumer_rebates
					)

		#计算会员的推荐返利
		#因：需求是结算周期的后一天去结算周期内所有推荐人的返利情况
		#故：统计当前日期的前一天和cycle中end_time在同一天的会员的所有推荐者的信息
		all_tengyi_member_rebate_sycle = TengyiMemberRebateCycle.objects.filter(end_time__startswith=yesterday)
		member_ids = list(all_tengyi_member_rebate_sycle.values_list('member_id', flat=True))
		for tengyi_member_sycle in all_tengyi_member_sycle:
			cur_membre_id = tengyi_member_sycle.member_id
			#获取当前会员推广的所有会员
			all_recommend_members = TengyiMember.objects.filter(recommend_by_member_id=cur_membre_id)
			#获取在账期内所有的获得购物返利的推广会员
			start_at = datetime.strptime(tengyi_member_sycle.start_time, date_fmt).date()
			end_at = yesterday
			all_recommend_member_rebate_sycle = TengyiMemberRebateCycle.objects.filter(receive_reward_at__range=(start_at, end_at), is_recommend_member_receive_reward=False)
			#返利
			for recommend_member_rebate_sycle in all_recommend_member_rebate_sycle:
				#标记被推荐人已收到返利
				recommend_member_rebate_sycle.is_recommend_member_receive_reward = True
				recommend_member_rebate_sycle.save()
				#将发奖记录保存在返利记录中
				TengyiRebateLog.objects.create(
					member_id = tengyi_member_sycle.member_id,
					is_self_order = False,
					supply_member_id = recommend_member_rebate_sycle.member_id,
					is_exchanged = False,
					rebate_money = recommend_member_rebate_sycle.recommend_member_rebate_money
					)


		#根据未充值的返利记录，最终调用接口充值
		need_recharge_rebate_logs = TengyiRebateLog.objects(is_exchanged=False)
		for need_recharge_rebate_log in need_recharge_rebate_logs:
			member_id = need_recharge_rebate_log.member_id
			rebate_money = need_recharge_rebate_log.rebate_money

			print u'为%s充值%d' % (member_id, rebate_money)
			need_recharge_rebate_log.is_exchanged = True
			need_recharge_rebate_log.save()



		


