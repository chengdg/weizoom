# -*- coding: utf-8 -*-

__author__ = 'chuter'

"""Unit tests for text message handler.

These tests make sure the text message handling works as it should. """

if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from weixin.message.handler.handler_testutil import *
init_handler_test_env()

import unittest

from weixin_message import *
from keyword_handler import *

from message_handle_context import *

class DummyTextMessageHandler(KeywordHandler):
	def _handle_keyword(self, context, from_weixin_user, is_from_simulator):
		return context.message.content

def createDummyMessageHandlingContext(message, xml_message):
	return MessageHandlingContext(message, xml_message, '-')

class KeywordHandlerTest(unittest.TestCase):
	def testHandleWithNotTextMessage(self):
		event_xml_message = """
		<xml><ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>123456789</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[CLICK]]></Event>
		<EventKey><![CDATA[__key__]]></EventKey>
		</xml>
		"""
		event_message = parse_weixin_message_from_xml(event_xml_message)
		context = createDummyMessageHandlingContext(event_message, event_xml_message)
		dummy_handler = DummyTextMessageHandler()
		response = dummy_handler.handle(context)
		self.assertEqual(None, response)

	def testKyewordHandle(self):
		text_xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName> 
		<CreateTime>1348831860</CreateTime>
		<MsgType><![CDATA[text]]></MsgType>
		<Content><![CDATA[keyword]]></Content>
		<MsgId>1234567890123456</MsgId>
		</xml>
		"""

		text_message = parse_weixin_message_from_xml(text_xml_message)
		weixin_user_test = WeixinUser.objects.create(username='fromUser')
		context = createDummyMessageHandlingContext(text_message, text_xml_message)

		dummy_handler = DummyTextMessageHandler()
		response = dummy_handler.handle(context)
		self.assertEqual('keyword', response)

if __name__ == '__main__':
	start_test_withdb()