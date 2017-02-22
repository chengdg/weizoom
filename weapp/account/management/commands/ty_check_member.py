# -*- coding: utf-8 -*-

from datetime import datetime

from django.core.management.base import BaseCommand

from eaglet.utils.resource_client import Resource

from mall.models import *
from modules.member.models import *

FIRST_LIMIT = 50
SECOND_LIMIT = 100

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
		member_id2rec_id = {t.member_id: t.recommend_by_member_id for t in relations}

		webapp_users = WebAppUser.objects.filter(member_id__in=member_ids)

		all_webapp_user_ids = [w.id for w in webapp_users]

		webapp_user_id2member_id = {w.id: w.member_id for w in webapp_users}

		member_id2webapp_id = {w.member_id: w.webapp_id for w in webapp_users}
		one_tag_webapp_ids = [m.webapp_id for m in MemberTag.objects.filter(name=u'一星会员')]
		two_tag_webapp_ids = [m.webapp_id for m in MemberTag.objects.filter(name=u'二星会员')]

		orders = Order.objects.filter(webapp_user_id__in=all_webapp_user_ids)



		for order in orders:
			if order.is_first_order:
				if order.final_price >= FIRST_LIMIT:
					member_id = webapp_user_id2member_id[order.webapp_user_id]
					webapp_id = member_id2webapp_id[member_id]
					recommend_by_member_id = member_id2rec_id[member_id]
					if order.final_price >= SECOND_LIMIT:
						tengyi_member = TengyiMember.objects.create(
							member_id = member_id,
							recommend_by_member_id = recommend_by_member_id,
							level = 2
						)


						if webapp_id not in one_tag_webapp_ids:
							member_tag = MemberTag.objects.create(
								webapp_id = webapp_id,
								name = u'一星会员'
							)
						else:
							member_tag = MemberTag.objects.filter(webapp_id=webapp_id, name=u'一星会员').first()

						if member_tag and MemberHasTag.objects.filter(member_id=member_id, member_tag_id=member_tag.id).count() == 0:
							MemberHasTag.objects.create(member_id=member_id, member_tag_id=member_tag.id)

					else:
						tengyi_member = TengyiMember.objects.create(
							member_id=member_id,
							recommend_by_member_id=recommend_by_member_id,
							level=1
						)

						if webapp_id not in two_tag_webapp_ids:
							member_tag = MemberTag.objects.create(
								webapp_id = webapp_id,
								name = u'二星会员'
							)
						else:
							member_tag = MemberTag.objects.filter(webapp_id=webapp_id, name=u'二星会员').first()

						if member_tag and MemberHasTag.objects.filter(member_id=member_id, member_tag_id=member_tag.id).count() == 0:
							MemberHasTag.objects.create(member_id=member_id, member_tag_id=member_tag.id)

					#创建卡
					resp = Resource.use('card_apiserver').get({
						'resource': 'card.membership_card',
						'data': {
							'card_condition': json.dumps({
								'weizoom_card_batch_id': 1,
								'sold_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
								'member_id': member_id,
								'phone_num': ''
							})
						}
					})

					if resp and resp['code'] == 200:
						card_number = resp['data']['card_number']
						tengyi_member.card_number = card_number
						tengyi_member.save()