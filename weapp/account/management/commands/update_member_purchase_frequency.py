# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError


from modules.member.models import MemberHasSocialAccount,Member
from mall.models import Order,ORDER_STATUS_SUCCESSED
from utils.dateutil import now,get_date_after_days

from account.models import UserProfile
import datetime
class Command(BaseCommand):
	help = "update member purchase frequency"
	args = ''
	
	def handle(self,*args, **options):

		now = datetime.datetime.now()
		date_before_30 = get_date_after_days(now,-30)
		webapp_appids = [user_profile.webapp_id for user_profile in UserProfile.objects.filter(is_active=True)]
		for webapp_id in webapp_appids:
			members = Member.objects.filter(webapp_id=webapp_id)
			for member in members:
				webapp_user_ids = member.get_webapp_user_ids
				orders = Order.by_webapp_user_id(webapp_user_ids)
				#二次过滤，创建时间和订单状态
				orders = orders.filter(payment_time__gte=date_before_30,status=ORDER_STATUS_SUCCESSED)
				purchase_count_30days = orders.count()
				Member.objects.filter(id=member.id).update(purchase_frequency=purchase_count_30days)
