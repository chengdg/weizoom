# -*- coding: utf-8 -*-
import logging
from django.core.management.base import BaseCommand, CommandError


from modules.member.models import MemberHasSocialAccount,Member
from mall.models import Order,ORDER_STATUS_SUCCESSED
from utils.dateutil import now,get_date_after_days

from account.models import UserProfile
import datetime

from services.update_member_purchase_frequency.tasks import update_member_purchase_frequency
class Command(BaseCommand):
	help = "update member purchase frequency"
	args = ''
	
	def handle(self,*args, **options):
		for user_profile in UserProfile.objects.filter(is_active=True):
			update_member_purchase_frequency(user_profile.webapp_id)
			logging.info(user_profile.webapp_id)