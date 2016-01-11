# -*- coding: utf-8 -*-

__author__ = 'bert'

from django.conf import settings
from django.db.models import F

from models import MessageDailyStatistics
from core import dateutil
from weixin.statistics.tasks import process_message_statistics, _process_message_statistics

"""
对收到的消息进行统计
"""
class MessageStatistics(object):
	def pre_processing(self, context, is_from_simulator=False):
		#来自模拟器的不进行统计
		if is_from_simulator:
			return

		if settings.TASKQUEUE_ENABLED:
			process_message_statistics.delay(context.user_profile.user_id)
		else:
			_process_message_statistics(context.user_profile.user_id)