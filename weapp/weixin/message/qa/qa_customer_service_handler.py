# -*- coding: utf-8 -*-

__author__ = 'chuter'

import util as qa_util
from weixin.message.handler.message_handler import MessageHandler

from core import emotion
from weixin.message import generator

from watchdog.utils import watchdog_warning, watchdog_error


"""
默认的消息处理，对任何消息均回复自动回复内容
"""								
class AutoQaDefaultMessageHandler(MessageHandler):

	def handle(self, context, is_from_simulator=False):
		return self._get_auto_reply_response(context.user_profile, context.message, is_from_simulator)	

	def _get_auto_reply_response(self, user_profile, message, is_from_simulator):
		if message.content == 'weizoom_coustomer':
			from_weixin_user = self._get_from_weixin_user(message)
			response = generator.get_counstomer_service_text(from_weixin_user.username, message.toUserName)
			return response
		else:
			return None

	