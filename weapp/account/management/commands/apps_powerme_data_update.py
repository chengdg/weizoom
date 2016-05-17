# -*- coding: utf-8 -*-

import time

from django.core.management.base import BaseCommand, CommandError

from utils.cache_util import SET_CACHE, delete_cache, delete_pattern
from apps.customerized_apps.powerme import models as app_models
from modules.member.models import Member


class Command(BaseCommand):
	help = 'start powerme stats task'
	args = ''
	
	def handle(self, *args, **options):


		powermes = app_models.PowerMe.objects(status=1)
		for powerme in powermes:
			print powerme.id
			powerme_id = str(powerme.id)
			participances = app_models.PowerMeParticipance.objects(belong_to=powerme_id, has_join=True)
			for participance in participances:
				member_id = participance.member_id
				cur_count = app_models.PoweredDetail.objects(belong_to=powerme_id, owner_id=member_id, has_powered=True).count()
				print cur_count, participance.power
				participance.power = cur_count
				participance.save()



		