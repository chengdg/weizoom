# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from eaglet.utils.resource_client import Resource

from mall.models import *
from modules.member.models import *


class Command(BaseCommand):
	help = ''
	args = ''
	
	def handle(self, member_id, level, **options):
		"""
		指定星级会员
		"""
		tengyi_member = TengyiMember.objects.filter(member_id=member_id).first()
		if tengyi_member:
			print member_id, ' already been tengyi member'
			if int(level) == tengyi_member.level:
				print 'and have been a {} star member'.format(level)
			else:
				tengyi_member.level = level
				tengyi_member.save()
				print 'change to {} star member'.format(level)
		else:
			tengyi_member = TengyiMember.objects.create(
				member_id = member_id,
				recommend_by_member_id = 0,
				level = level
			)
			print 'create {} star member'.format(level)

		if tengyi_member.card_number == '':
			# 创建卡
			resp = Resource.use('card_apiserver').get({
				'resource': 'card.membership_card',
				'data': {
					'card_condition': json.dumps({
						'weizoom_card_batch_id': 32,
						'sold_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
						'member_id': member_id,
						'phone_num': '13111111111'
					})
				}
			})

			if resp and resp['code'] == 200:
				card_number = resp['data']['card_number']
				tengyi_member.card_number = card_number
				tengyi_member.save()
				print 'create card: ', card_number
			else:
				print 'create card failed'

			if tengyi_member.level == 1:
				cycle = range(6)
			else:
				cycle = range(12)
			for i in cycle:
				recommend_member_rebate_money = 10
				if i > 5:
					recommend_member_rebate_money = 20

				start_time = tengyi_member.created_at.date() + timedelta(30 * i)
				end_time = start_time + timedelta(30)

				TengyiMemberRebateCycle.objects.create(
					member_id=tengyi_member.member_id,
					start_time=start_time,
					end_time=end_time,
					recommend_member_rebate_money=recommend_member_rebate_money,
				)
		else:
			print 'already have a card'