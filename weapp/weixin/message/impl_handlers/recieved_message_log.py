# -*- coding: utf-8 -*-

__author__ = 'chuter'

from watchdog.utils import watchdog_info

"""
记录所收到的消息
"""

class ReceivedMessageLogger(object):
	def pre_processing(self, context, is_from_simulator=False):
		#来自模拟器的消息不进行记录
		if not is_from_simulator:
			watchdog_info(context.xml_message, user_id=context.user_profile.user_id)
