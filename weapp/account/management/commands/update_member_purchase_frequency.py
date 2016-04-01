# -*- coding: utf-8 -*-
import logging
from django.core.management.base import BaseCommand, CommandError


from modules.member.models import *
from mall.models import Order,ORDER_STATUS_SUCCESSED
from utils.dateutil import now,get_date_after_days

from account.models import UserProfile
import datetime

# from services.update_member_purchase_frequency.tasks import update_member_purchase_frequency
class Command(BaseCommand):
	help = "update member purchase frequency"
	args = ''
	
	def handle(self,*args, **options):
		for user_profile in UserProfile.objects.filter(is_active=True):
			now = datetime.datetime.now()
			webapp_id = user_profile.webapp_id
			members = Member.objects.filter(webapp_id=webapp_id, status__in=[SUBSCRIBED, CANCEL_SUBSCRIBED])
			date_before_30 = get_date_after_days(now,-30)
			info = "%s:%s" % (webapp_id, now)
			logging.info(info)
			logging.info('start')
			for member in members:
				webapp_user_ids = member.get_webapp_user_ids
				purchase_count_30days = Order.objects.filter(webapp_user_id__in=webapp_user_ids, payment_time__gte=date_before_30,status=ORDER_STATUS_SUCCESSED).count()
				Member.objects.filter(id=member.id).update(purchase_frequency=purchase_count_30days)
			logging.info('end')