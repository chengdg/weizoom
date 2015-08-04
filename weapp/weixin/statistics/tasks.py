# -*- coding: utf-8 -*-

__author__ = 'bert'
# from __future__ import absolute_import

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import F
from celery import task
from models import MessageDailyStatistics
from core import dateutil

@task
def process_message_statistics(user_id):
	print 'call process_message_statistics start'
	_process_message_statistics(user_id)
	print 'OK'
	

def _process_message_statistics(user_id):  #response_rule, from_weixin_user, is_from_simulator):
	if User.objects.filter(id=user_id).count() > 0:
		today = dateutil.get_today()
		owner = User.objects.get(id=user_id)
		statisticses = MessageDailyStatistics.objects.filter(owner=owner, data_date=today)
		if statisticses.count() > 0 :
			MessageDailyStatistics.objects.filter(owner=owner, data_date=today).update(count = F('count') + 1)
		else:
			MessageDailyStatistics.objects.create(
				owner = owner,
				count = 1,
				data_date = today
				)

		
