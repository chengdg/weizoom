# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from eaglet.utils.resource_client import Resource

from mall.models import *
from modules.member.models import *

weizoom_card_batch_id = 362 #docker测试用32，生产用362
weizoom_card_batch_name = u'腾易星级会员卡'
tengyi_user_id = 1346 #docker测试用119，生产用1346


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
			one_tag_webapp_ids = [m.webapp_id for m in MemberTag.objects.filter(name=u'一星会员')]
			two_tag_webapp_ids = [m.webapp_id for m in MemberTag.objects.filter(name=u'二星会员')]

			use_tag_webapp_ids = one_tag_webapp_ids if int(level) == 1 else two_tag_webapp_ids
			tag_name = u'一星会员' if int(level) == 1 else u'二星会员'

			webapp_id = WebAppUser.objects.filter(member_id=member_id).first().id

			if webapp_id not in use_tag_webapp_ids:
				member_tag = MemberTag.objects.create(
					webapp_id=webapp_id,
					name=tag_name
				)
				print 'create member_tag'
			else:
				member_tag = MemberTag.objects.filter(webapp_id=webapp_id, name=tag_name).first()

			if member_tag and MemberHasTag.objects.filter(member_id=member_id,
														  member_tag_id=member_tag.id).count() == 0:
				print 'add to {} star tag'.format(level)
				MemberHasTag.objects.create(member_id=member_id, member_tag_id=member_tag.id)

		if tengyi_member.card_number == '':
			# 创建卡
			resp = Resource.use('card_apiserver').get({
				'resource': 'card.membership_card',
				'data': {
					'card_condition': json.dumps({
						'weizoom_card_batch_id': weizoom_card_batch_id,
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
				card_password = resp['data']['card_password']

				member_card = MemberCard.objects.create(
					owner_id=tengyi_user_id,
					member_id=member_id,
					batch_id=weizoom_card_batch_id,
					card_number=card_number,
					card_password=card_password,
					card_name=weizoom_card_batch_name
				)

				resp = Resource.use('card_apiserver').get({
					'resource': 'card.membership_batch',
					'data': {'membership_batch_id': weizoom_card_batch_id}
				})
				if resp and resp['code'] == 200:
					batch_info = resp['data']['card_info']
					MemberCardLog.objects.create(
						member_card=member_card,
						reason=u"开通腾易星级会员卡",
						price=batch_info['first_money']
					)
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