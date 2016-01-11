# -*- coding: utf-8 -*-

__author__ = 'chuter'

from watchdog.utils import watchdog_info

"""
记录所收到的消息
"""

class ResponseedMessageLogger(object):
	def post_processing(self, context, handler, response_content, is_from_simulator=False):
		#来自模拟器的消息不进行记录
		if not is_from_simulator:
			watchdog_info(u"{} response:\n {}".format(handler.__class__.__name__, response_content), user_id=context.user_profile.user_id)