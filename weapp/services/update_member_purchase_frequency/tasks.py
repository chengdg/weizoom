# -*- coding: utf-8 -*-
import logging
from celery import task
from modules.member.models import *
from mall.models import Order,ORDER_STATUS_SUCCESSED
from utils.dateutil import now,get_date_after_days

import datetime

@task(bind=True, time_limit=7200, max_retries=1)
def update_member_purchase_frequency(self, webapp_id):
	now = datetime.datetime.now()
	members = Member.objects.filter(webapp_id=webapp_id, status__in=[SUBSCRIBED, CANCEL_SUBSCRIBED])
	date_before_30 = get_date_after_days(now,-30).strftime("%Y-%m-%d")
	info = "%s:%s" % (webapp_id, now)
	logging.info(info)
	logging.info('start')
	for member in members:
		webapp_user_ids = member.get_webapp_user_ids
		purchase_count_30days = Order.objects.filter(webapp_user_id__in=webapp_user_ids, payment_time__gte=date_before_30,status=ORDER_STATUS_SUCCESSED).count()
		Member.objects.filter(id=member.id).update(purchase_frequency=purchase_count_30days)
	logging.info('end')
