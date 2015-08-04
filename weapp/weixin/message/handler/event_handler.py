# -*- coding: utf-8 -*-
"""
微信push过来的事件类型的消息的处理，如果消息不是事件类型，直接返回None不进行任何处理。

处理过程中，对于点击事件(CLICK，一般场景为微信用户
点击了自定义菜单，此类事件主要利用的是对应的key，
行为类似直接输入关键词，因此对该类事件的默认的处理
方式为把该消息转换为文本类型的消息，交由后续的handler
处理

@note `注意`：事件类的handler一定在在文本类的消息的handler之前
触发
"""

__author__ = 'chuter'

from message_handler import *
from weixin_message import *

class EventMessageHandler(MessageHandler):
	"""
	处理微信中的事件，例如关注，取消关注，点击链接等
	"""

	def handle(self, context, is_from_simulator=False):
		received_message = context.message
		
		if WeixinMessageTypes.EVENT != received_message.msgType:
			print 'only handle event message'
			return None

		event_type = received_message.event

		if WeixinMessageEvents.SUBSCRIBE == event_type:
			response_content = self._handle_subscribe_event(context, is_from_simulator)
			if response_content is None:
				response_content = EMPTY_RESPONSE_CONTENT
			return response_content
		elif WeixinMessageEvents.UNSUBSCRIBE == event_type:
			response_content = self._handle_unsubscribe_envent(context, is_from_simulator)
			if response_content is None:
				response_content = EMPTY_RESPONSE_CONTENT
			return response_content
		elif WeixinMessageEvents.CLICK == event_type:
			return self._handle_click_event(context)
		else:
			print 'not handle event ' + event_type
			return None

	def _handle_click_event(self, context):
		"""
		自定义菜单点击事件，实际也相当于输入了关键词，因此，对点击事件的默认
		处理行为为：

		 1. 把message类型改为关键词类型的message
		 2. 不进行处理，直接返回None
		"""

		new_message = trans_to_text_message_from_event_message(context.message)
		context.message = new_message
		return None

	def _handle_subscribe_event(self, context, is_from_simulator):
		raise NotImplementedError

	def _handle_unsubscribe_envent(self, context, is_from_simulator):
		raise NotImplementedError