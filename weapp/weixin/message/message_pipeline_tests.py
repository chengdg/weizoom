# -*- coding: utf-8 -*-
"""Unit tests for message pipeline.

These tests make sure the message handling works as it should. """

__author__ = 'chuter'


if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from weixin.handler.handler_testutil import *
init_handler_test_env()

import unittest

from handler.weixin_message import parse_weixin_message_from_xml
from handler.message_handler import *

from message_pipeline import *

from django.http import HttpRequest

from watchdog.utils import *

class DummyHandlerWithoudProcessing(MessageHandler):

	def handle(self, context, is_from_simulator=False):
		return None

class DummyHandlerWithDummyProcessing(MessageHandler):

	def handle(self, context, is_from_simulator=False):
		message = context.message
		return message.msgId

class DummyHandlerThrowException(MessageHandler):

	def handle(self, context, is_from_simulator=False):
		raise ValueError('i am told to be')

class DummyNonMessageHandler():
	pass


class DummyPreProcessingHandler(object):
	def pre_processing(self, context, is_from_simulator=False):
		if context.request.GET.has_key('pre_process_count'):
			context.request.GET['pre_process_count'] = context.request.GET['pre_process_count'] + 1
		else:
			context.request.GET['pre_process_count']  = 1

class DummyPreProcessingHandlerWithException(object):
	def pre_processing(self, context, is_from_simulator=False):
		raise ValueError('i am told to be')

class DummyPostProcessingHandler(object):
	def post_processing(self, context, handler, response, is_from_simulator=False):
		if context.request.GET.has_key('post_process_count'):
			context.request.GET['post_process_count'] = context.request.GET['post_process_count'] + 1
		else:
			context.request.GET['post_process_count']  = 1

class DummyPostProcessingHandlerWithException(object):
	def post_processing(self, context, handler, response, is_from_simulator=False):
		raise ValueError('i am told to be')

DUMMY_MESSAGE = """
	<xml>
	<ToUserName><![CDATA[toUser]]></ToUserName>
	<FromUserName><![CDATA[fromUser]]></FromUserName> 
	<CreateTime>1348831860</CreateTime>
	<MsgType><![CDATA[text]]></MsgType>
	<Content><![CDATA[this is a test]]></Content>
	<MsgId>1234567890123456</MsgId>
	</xml>
	"""

def build_test_request():
	dummy_request = HttpRequest()
	dummy_request.user = getTestUserProfile().user

	dummy_request.GET = {}
	dummy_request._body = DUMMY_MESSAGE
	return dummy_request


class MessagePipelineTest(unittest.TestCase):

	def testCreatePipelineWithInvalidParams(self):
		try:
			pipeline = MessagePipeline([])
			self.fail()
		except ValueError: #due to empty handler claeeses
			self.assertTrue(True)

		try:
			pipeline = MessagePipeline(['weixin.message_pipeline_tests.DummyNonMessageHandler'])
			self.fail()
		except ValueError:
			self.assertTrue(True)

	def testMessageHandling(self):
		pipeline = MessagePipeline(['weixin.message_pipeline_tests.DummyNonMessageHandler',
				'weixin.message_pipeline_tests.DummyHandlerWithoudProcessing',
				'weixin.message_pipeline_tests.DummyHandlerWithDummyProcessing'])

		dummy_request = build_test_request()
		response = pipeline.handle(dummy_request, getTestUserProfile().shop_name)

		message = parse_weixin_message_from_xml(DUMMY_MESSAGE)
		self.assertEqual(message.msgId, response)
		
	def testMessageHandlingWithPreAndPostProcessing(self):
		Message.objects.all().delete()

		pipeline = MessagePipeline(['weixin.message_pipeline_tests.DummyNonMessageHandler',
				'weixin.message_pipeline_tests.DummyHandlerWithoudProcessing',
				'weixin.message_pipeline_tests.DummyHandlerWithDummyProcessing',
				'weixin.message_pipeline_tests.DummyPreProcessingHandler',
				'weixin.message_pipeline_tests.DummyPreProcessingHandlerWithException',
				'weixin.message_pipeline_tests.DummyPreProcessingHandler',
				'weixin.message_pipeline_tests.DummyPostProcessingHandler',
				'weixin.message_pipeline_tests.DummyPostProcessingHandlerWithException',
				'weixin.message_pipeline_tests.DummyPostProcessingHandler',
				])
		
		dummy_request = build_test_request()
		response = pipeline.handle(dummy_request, getTestUserProfile().shop_name)

		message = parse_weixin_message_from_xml(DUMMY_MESSAGE)
		self.assertEqual(message.msgId, response)

		#两个handler都分别进行了预处理和后处理
		self.assertEqual(2, dummy_request.GET['pre_process_count'])
		self.assertEqual(2, dummy_request.GET['post_process_count'])

		#且在进行预处理和后处理期间发生两次异常
		self.assertEqual(2, Message.objects.all().count())
		for message in Message.objects.all():
			self.assertTrue(message.message.find('i am told to be') > 0)

	def testMessageHandlingWithException(self):
		Message.objects.all().delete()

		#在某一个handler处理发生异常后中断处理
		pipeline = MessagePipeline(['weixin.message_pipeline_tests.DummyHandlerThrowException',
				'weixin.message_pipeline_tests.DummyHandlerWithDummyProcessing'])

		
		dummy_request = build_test_request()
		response = pipeline.handle(dummy_request, getTestUserProfile().shop_name)

		self.assertEqual(None, response)
		self.assertEqual(1, Message.objects.all().count())
		self.assertEqual('WEB', Message.objects.all()[0].type)
		self.assertEqual(WATCHDOG_WEB, Message.objects.all()[0].severity)

		#如果设置在某一个handler处理发生异常后继续后续handler的处理
		pipeline = MessagePipeline(['weixin.message_pipeline_tests.DummyHandlerThrowException',
				'weixin.message_pipeline_tests.DummyHandlerWithDummyProcessing'], False)

		response = pipeline.handle(dummy_request, getTestUserProfile().shop_name)

		message = parse_weixin_message_from_xml(DUMMY_MESSAGE)
		self.assertEqual(message.msgId, response)

if __name__ == '__main__':
	start_test_withdb()