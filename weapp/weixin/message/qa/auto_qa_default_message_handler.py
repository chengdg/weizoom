# -*- coding: utf-8 -*-

__author__ = 'chuter'

from weixin.message.qa import cache_util
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
		
		#response_rule = qa_util.find_unmatch_answer_for(user_profile.webapp_id)
		#从缓存中获取数据  duhao  2015-03-09
		response_rule = cache_util.find_unmatch_answer_from_cache_for(user_profile.webapp_id)

		if response_rule and response_rule.is_active:
			return self._build_response_to_weixin_user(user_profile, message, response_rule, is_from_simulator)
		else:
			return None

	def _build_response_to_weixin_user(self, user_profile, message, response_rule, is_from_simulator):
		from_weixin_user = self._get_from_weixin_user(message)
		token = self._get_token_for_weixin_user(user_profile, from_weixin_user, is_from_simulator)

		if is_from_simulator:
			response = generator.get_text_response(from_weixin_user.username, message.toUserName, emotion.change_emotion_to_img(response_rule.answer), token, user_profile)
		else:
			response = generator.get_text_response(from_weixin_user.username, message.toUserName, response_rule.answer, token, user_profile)
		
		return response