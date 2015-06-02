# -*- coding: utf-8 -*-

__author__ = 'bert'

from django.conf import settings

from message_handler import *
from weixin_message import *

"""
微信push过来的文本类型的消息的处理（即处理微信用户输入的关键词），
如果消息不是文本类型，直接返回None不进行任何处理
"""
class KeywordHandler(MessageHandler):
	
	def handle(self, context, is_from_simulator=False):
		message = context.message
		if WeixinMessageTypes.TEXT != message.msgType and WeixinMessageTypes.VOICE != message.msgType and  WeixinMessageTypes.IMAGE != message.msgType:
			print 'only handle text,voice,image message'
			return None

		
		if settings.IS_MESSAGE_OPTIMIZATION:
			return self._handle_keyword(context, None, is_from_simulator)
		else:
			return self._handle_keyword(context, self._get_from_weixin_user(message), is_from_simulator)
		return self._handle_keyword(context, self._get_from_weixin_user(message), is_from_simulator)

	def _handle_keyword(self, context, from_weixin_user, is_from_simulator):
		raise NotImplementedError