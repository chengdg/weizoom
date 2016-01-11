# -*- coding: utf-8 -*-

__author__ = 'bert'

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
from voice_handler import *

from message_handle_context import *

class DummyTextMessageHandler(VoiceHandler):
	def _handle_voice(self, context, from_weixin_user, is_from_simulator):
		message = context.message
		return message.fromUserName

def createDummyMessageHandlingContext(message, xml_message):
	return MessageHandlingContext(message, xml_message, '-')

class VoiceHandlerTest(unittest.TestCase):
	def testHandleWithNotTextMessage(self):
		event_xml_message = """
		<xml><tousername><![CDATA[gh_a228243fb3c6]]></tousername>
		<fromusername><![CDATA[]]></fromusername>
		<createtime>1382321767</createtime>
		<msgtype><![CDATA[voice]]></msgtype>
		<mediaid><![CDATA[ZR-9kKB2Nsvgyto_WcWtMF3LYdsv2dp9VQFlIoNE1hllhth9Rl00P3_XZxIfz1C8]]></mediaid>
		<format><![CDATA[amr]]></format>
		<msgid>5937026781913946205</msgid>
		<recognition><![CDATA[ ]]></recognition>
		</xml>
		"""
		event_message = parse_weixin_message_from_xml(event_xml_message)
		context = createDummyMessageHandlingContext(event_message, event_xml_message)

		dummy_handler = DummyTextMessageHandler()
		response = dummy_handler.handle(context)
		self.assertEqual('', response)

	def testKyewordHandle(self):
		text_xml_message = """
			<xml><tousername><![CDATA[gh_a228243fb3c6]]></tousername>
			<fromusername><![CDATA[oWOb_jqKXo7Aql8pJ_chaWKAVL1A]]></fromusername>
			<createtime>1382321767</createtime>
			<msgtype><![CDATA[voice]]></msgtype>
			<mediaid><![CDATA[ZR-9kKB2Nsvgyto_WcWtMF3LYdsv2dp9VQFlIoNE1hllhth9Rl00P3_XZxIfz1C8]]></mediaid>
			<format><![CDATA[amr]]></format>
			<msgid>5937026781913946205</msgid>
			<recognition><![CDATA[ ]]></recognition>
			</xml>
			"""

		text_message = parse_weixin_message_from_xml(text_xml_message)
		context = createDummyMessageHandlingContext(text_message, text_xml_message)

		dummy_handler = DummyTextMessageHandler()
		response = dummy_handler.handle(context)
		self.assertEqual('oWOb_jqKXo7Aql8pJ_chaWKAVL1A', response)

if __name__ == '__main__':
   start_test_withdb()