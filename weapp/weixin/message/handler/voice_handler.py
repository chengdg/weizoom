# -*- coding: utf-8 -*-

__author__ = 'bert'

from message_handler import *
from weixin_message import *
from message.models import WeixinUser

class VoiceHandler(MessageHandler):
	"""
	微信push过来的文本类型的消息的处理（即处理微信用户输入的关键词）。如果消息不是文本类型，直接返回None不进行任何处理
	"""

	def handle(self, context, is_from_simulator=False):
		message = context.message
		if WeixinMessageTypes.VOICE != message.msgType:
			print 'only handle voice message'
			return None

		return self._handle_voice(context, self._get_from_weixin_user(message), is_from_simulator)

	def _get_from_weixin_user(self, message):
		try:
			weixin_user = WeixinUser.objects.get(username=message.fromUserName)
		except Exception, e:
			return None
		
		return weixin_user

	def _handle_voice(self, context, from_weixin_user, is_from_simulator):
		raise NotImplementedError