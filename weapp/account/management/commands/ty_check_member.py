# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from mall.models import *
from modules.member.models import *

FIRST_LIMIT = 50
SECOND_LIMIT = 100

class Command(BaseCommand):
	help = ''
	args = ''
	
	def handle(self, key, **options):
		relations = TengyiMemberRelation.objects.all()
		member_ids = [r.member_id for r in relations]
		member_id2rec_id = {t.member_id: t.recommend_by_member_id for t in relations}

		webapp_users = WebAppUser.objects.filter(member_id__in=member_ids)

		all_webapp_user_ids = [w.id for w in webapp_users]

		webapp_user_id2member_id = {w.id: w.member_id for w in webapp_users}

		orders = Order.objects.filter(webapp_user_id__in=all_webapp_user_ids)

		for order in orders:
			if order.is_first_order:
				if order.final_price >= FIRST_LIMIT:
					member_id = webapp_user_id2member_id[order.webapp_user_id]
					recommend_by_member_id = member_id2rec_id[member_id]
					if order.final_price >= SECOND_LIMIT:
						TengyiMember.create(
							member_id = member_id,
							recommend_by_member_id = recommend_by_member_id,
							level = 2
						)
					else:
						TengyiMember.create(
							member_id=member_id,
							recommend_by_member_id=recommend_by_member_id,
							level=1
						)