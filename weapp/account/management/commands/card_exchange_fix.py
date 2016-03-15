# -*- coding: utf-8 -*-

import time

from django.core.management.base import BaseCommand, CommandError

from mall.promotion.models import CardHasExchanged
from market_tools.tools.weizoom_card.models import WeizoomCardHasOrder


class Command(BaseCommand):
	help = ''
	args = ''
	
	def handle(self, **options):
		"""

		清除mallpromotion_card_has_exchanged表中同一个用户重复的记录
		@param options:
		@return:
		"""
		print 'fix card_exchange start...'
		all_records = CardHasExchanged.objects.all()
		owner_id2cardlist = {}
		for r in all_records:
			owner_id2cardlist[r.owner_id] = r.card_id
		usefull_card_ids = owner_id2cardlist.values()
		crs = WeizoomCardHasOrder.objects.exclude(order_id__in = [-1])
		ids = [c.id for c in crs]
		finally_ids = []
		for uid in usefull_card_ids:
			if uid not in ids:
				finally_ids.append(uid)
		CardHasExchanged.objects.exclude(card_id__in=finally_ids).delete()

		print 'fix card_exchange end...'