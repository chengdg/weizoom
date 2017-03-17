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
		seven_days_ago_date = today - timedelta(6)
		print seven_days_ago_date, '================='
		yesterday = today - timedelta(1)
		#计算会员自身购物返利情况
		all_tengyi_member_rebate_sycle = TengyiMemberRebateCycle.objects.filter(is_receive_reward=False, start_time__lt=today)
		print 'need consumer_rebates count', all_tengyi_member_rebate_sycle.count()
		for tengyi_member_sycle in all_tengyi_member_rebate_sycle:
			cur_member_id = tengyi_member_sycle.member_id
			cur_webapp_user_id = WebAppUser.objects.get(member_id=cur_member_id).id
			start_at = tengyi_member_sycle.start_time.date()
			end_at = tengyi_member_sycle.end_time.date() #查订单时候需要把截止日期后延一天
			#获取区间内下单、状态为已支付、待发货、已发货、已完成的订单
			# orders = Order.objects.filter(webapp_user_id=cur_webapp_user_id, created_at__range=(start_at, end_at), status__in=[3,4,5], origin_order_id__lte=0, payment_time__lt=seven_days_ago_date)
			orders = Order.objects.filter(webapp_user_id=cur_webapp_user_id, created_at__range=(start_at, end_at), status__in=[3,4,5], origin_order_id__lte=0)
			order_ids = list(orders.values_list('order_id', flat=True))
			print '>>>cur_member_id', cur_member_id
			print 'order_ids',order_ids
			money_sum = 0
			for order in orders:
				money_sum += order.final_price

			cur_member_level = member_id2level[cur_member_id]
			order_money = LEVEL_INFO[cur_member_level]['order_money']
			consumer_rebates = LEVEL_INFO[cur_member_level]['consumer_rebates']
			#TODO特殊处理 需改进
			if int(tengyi_member_sycle.recommend_member_rebate_money) == 20:
				consumer_rebates = 50
			print 'order_money:', order_money, '||||||', 'money_sum:', money_sum
			if money_sum >= order_money:
				#满足金额发放奖励，更新sycle表为已经发过奖励，下次不再计算
				tengyi_member_sycle.receive_reward_at = today
				tengyi_member_sycle.is_receive_reward = True
				tengyi_member_sycle.save()
				#将发奖记录保存在返利记录中
				TengyiRebateLog.objects.create(
					member_id = cur_member_id,
					is_self_order = True,
					supply_member_id = 0,
					is_exchanged = False,
					rebate_money = consumer_rebates
					)

		print '===end of consumer_rebates==='


		#根据未充值的返利记录，最终调用接口充值
		need_recharge_rebate_logs = TengyiRebateLog.objects.filter(is_exchanged=False,created_at__lt=seven_days_ago_date)
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
				need_recharge_rebate_log.exchanged_at = today
				need_recharge_rebate_log.save()

