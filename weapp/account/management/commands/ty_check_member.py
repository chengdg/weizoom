# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from eaglet.utils.resource_client import Resource

from mall.models import *
from modules.member.models import *

FIRST_LIMIT = 50.0
SECOND_LIMIT = 100.0

weizoom_card_batch_id = 362
weizoom_card_batch_name = u'腾易星级会员卡'
tengyi_user_id = 1346

class Command(BaseCommand):
	help = ''
	args = ''
	
	def handle(self, *args, **options):
		"""
		定时检查腾易会员扫码关注的新会员，是否达到星级会员的要求
		如果达到要求则同时加入到对应的分组中: 一星会员、二星会员
		"""
		relations = TengyiMemberRelation.objects.all()
		member_ids = [r.member_id for r in relations]
		member_id_exists = [t.member_id for t in TengyiMember.objects.filter(member_id__in=member_ids)]
		member_id2rec_id = {t.member_id: t.recommend_by_member_id for t in relations}

		webapp_users = WebAppUser.objects.filter(member_id__in=member_ids)

		all_webapp_user_ids = [w.id for w in webapp_users]

		webapp_user_id2member_id = {w.id: w.member_id for w in webapp_users}

		member_id2webapp_id = {w.member_id: w.webapp_id for w in webapp_users}
		one_tag_webapp_ids = [m.webapp_id for m in MemberTag.objects.filter(name=u'一星会员')]
		two_tag_webapp_ids = [m.webapp_id for m in MemberTag.objects.filter(name=u'二星会员')]

		orders = Order.objects.filter(webapp_user_id__in=all_webapp_user_ids)

		for order in orders:
			member_id = webapp_user_id2member_id[order.webapp_user_id]
			webapp_id = member_id2webapp_id[member_id]
			recommend_by_member_id = member_id2rec_id[member_id]
			if member_id not in member_id_exists and order.is_first_order and order.status >= ORDER_STATUS_PAYED_NOT_SHIP and order.origin_order_id <= 0:
				if order.final_price >= FIRST_LIMIT:
					if order.final_price >= SECOND_LIMIT:
						print 'two star'
						tengyi_member = TengyiMember.objects.create(
							member_id = member_id,
							recommend_by_member_id = recommend_by_member_id,
							level = 2
						)


						if webapp_id not in two_tag_webapp_ids:
							member_tag = MemberTag.objects.create(
								webapp_id = webapp_id,
								name = u'二星会员'
							)
						else:
							member_tag = MemberTag.objects.filter(webapp_id=webapp_id, name=u'二星会员').first()

						if member_tag and MemberHasTag.objects.filter(member_id=member_id, member_tag_id=member_tag.id).count() == 0:
							print 'add to two star tag'
							MemberHasTag.objects.create(member_id=member_id, member_tag_id=member_tag.id)

					else:
						print 'one star'
						tengyi_member = TengyiMember.objects.create(
							member_id = member_id,
							recommend_by_member_id = recommend_by_member_id,
							level = 1
						)

						if webapp_id not in one_tag_webapp_ids:
							member_tag = MemberTag.objects.create(
								webapp_id = webapp_id,
								name = u'一星会员'
							)
						else:
							member_tag = MemberTag.objects.filter(webapp_id=webapp_id, name=u'一星会员').first()

						if member_tag and MemberHasTag.objects.filter(member_id=member_id, member_tag_id=member_tag.id).count() == 0:
							print 'add to one star tag'
							MemberHasTag.objects.create(member_id=member_id, member_tag_id=member_tag.id)

					#创建卡
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
						print 'created card', card_number

						card_password = resp['data']['card_password']

						member_card = MemberCard.objects.create(
							owner_id = tengyi_user_id,
							member_id = member_id,
							batch_id = weizoom_card_batch_id,
							card_number = card_number,
							card_password = card_password,
							card_name = weizoom_card_batch_name
						)

						resp = Resource.use('card_apiserver').get({
							'resource': 'card.membership_batch',
							'data': {'membership_batch_id': weizoom_card_batch_id}
						})
						if resp and resp['code'] == 200:
							batch_info = resp['data']['card_info']
							MemberCardLog.objects.create(
								member_card = member_card,
								reason = u"开通腾易星级会员卡",
								price = batch_info['first_money']
							)

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