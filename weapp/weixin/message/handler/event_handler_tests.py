# -*- coding: utf-8 -*-

__author__ = 'chuter'

"""Unit tests for event message handler.

These tests make sure the event message handling works as it should. """

if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from weixin.message.handler.handler_testutil import *
init_handler_test_env()

import unittest

from weixin_message import *
from event_handler import *

from message_handler import *
from message_handle_context import *

SUSCRIBE_EVENT_HANDLE_RESPONSE = 'subscribe'
UNSUSCRIBE_EVENT_HANDLE_RESPONSE = 'unsubscribe'

class DummyEventMessageHandler(EventMessageHandler):
	def _handle_subscribe_event(self, context, is_from_simulator):
		return SUSCRIBE_EVENT_HANDLE_RESPONSE

	def _handle_unsubscribe_envent(self, context, is_from_simulator):
		return UNSUSCRIBE_EVENT_HANDLE_RESPONSE

def createDummyMessageHandlingContext(message, xml_message):
	return MessageHandlingContext(message, xml_message, '-')

class EventMessageHandlerTest(unittest.TestCase):
	def testHandleWithNotEventMessage(self):
		test_xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName> 
		<CreateTime>1348831860</CreateTime>
		<MsgType><![CDATA[text]]></MsgType>
		<Content><![CDATA[this is a test]]></Content>
		<MsgId>1234567890123456</MsgId>
		</xml>
		"""
		test_message = parse_weixin_message_from_xml(test_xml_message)
		context = createDummyMessageHandlingContext(test_message, test_xml_message)

		dummy_handler = DummyEventMessageHandler()
		response = dummy_handler.handle(context)
		self.assertEqual(None, response)
		
	def testHandleWithClickEventMessage(self):
		xml_message = """
		<xml><ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>123456789</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[CLICK]]></Event>
		<EventKey><![CDATA[__key__]]></EventKey>
		</xml>
		"""
		message = parse_weixin_message_from_xml(xml_message)
		context = createDummyMessageHandlingContext(message, xml_message)

		dummy_handler = DummyEventMessageHandler()
		response = dummy_handler.handle(context)
		new_message = context.message

		self.assertEqual(TextWeixinMessage, type(new_message))
		self.assertEqual(DUMMY_TEXT_MSGID_TRANSED_FROM_EVENT, new_message.msgId)
		self.assertEqual('__key__', new_message.content)

	def testHandleWithSubcribeEventMessage(self):
		xml_message = """
		<xml><ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>123456789</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[subscribe]]></Event>
		<EventKey><![CDATA[__key__]]></EventKey>
		</xml>
		"""
		message = parse_weixin_message_from_xml(xml_message)
		context = createDummyMessageHandlingContext(message, xml_message)

		dummy_handler = DummyEventMessageHandler()
		response = dummy_handler.handle(context)
		new_message = context.message

		self.assertEqual(EventWeixinMessage, type(new_message)) #消息没有变化
		self.assertEqual(SUSCRIBE_EVENT_HANDLE_RESPONSE, response)

	def testHandleWithUnsubcribeEventMessage(self):
		xml_message = """
		<xml><ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>123456789</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[unsubscribe]]></Event>
		<EventKey><![CDATA[__key__]]></EventKey>
		</xml>
		"""
		message = parse_weixin_message_from_xml(xml_message)
		context = createDummyMessageHandlingContext(message, xml_message)

		dummy_handler = DummyEventMessageHandler()
		response = dummy_handler.handle(context)
		new_message = context.message

		self.assertEqual(EventWeixinMessage, type(new_message)) #消息没有变化
		self.assertEqual(UNSUSCRIBE_EVENT_HANDLE_RESPONSE, response)

if __name__ == '__main__':
    unittest.main()