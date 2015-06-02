# -*- coding: utf-8 -*-

__author__ = 'chuter'


"""Unit tests for answer game process.

These tests make sure the message handling works as it should. """

if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from weixin.handler.handler_testutil import *
init_handler_test_env()

from weixin_user_handler import WeixinUserHandler

from weixin.handler.weixin_message import parse_weixin_message_from_xml

from django.test import TestCase

from message.models import WeixinUser

class WeixinUserHandlerTest(TestCase):
	def testWeixinUserHanding(self):
		WeixinUser.objects.all().delete()

		test_xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUserName]]></FromUserName> 
		<CreateTime>1348831860</CreateTime>
		<MsgType><![CDATA[text]]></MsgType>
		<Content><![CDATA[just a test]]></Content>
		<MsgId>1234567890123456</MsgId>
		</xml>
		"""
		test_message = parse_weixin_message_from_xml(test_xml_message)
		context = createDummyMessageHandlingContext(test_message, test_xml_message)
		handler = WeixinUserHandler()

		#如果用户信息还不存在，那么会创建微信用户信息
		self.assertEqual(None, handler.handle(context))
		self.assertEqual('fromUserName', WeixinUser.objects.get(username='fromUserName').username)
		
		#如果用户信息已经存在，不进行任何处理
		self.assertEqual(None, handler.handle(context))
		self.assertEqual('fromUserName', WeixinUser.objects.get(username='fromUserName').username)


if __name__ == '__main__':
	start_test_withdb()