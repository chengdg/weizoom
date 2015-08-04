# -*- coding: utf-8 -*-

__author__ = 'chuter'


"""Unit tests for answer event message process.

These tests make sure the message handling works as it should. """

if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from weixin.handler.handler_testutil import *
init_handler_test_env()

from django.test import TestCase
from django.http import HttpRequest

from weixin.handler.weixin_message import *

from qa.models import *
from account.models import WeixinMpUser
from message.models import *

from auto_qa_message_handler import AutoQaMessageHandler

class AutoQaMessageHandlerTest(TestCase):
	def test_keyword_handle_with_matched_rule(self):
		#清空信息
		Rule.objects.all().delete()
		Category.objects.all().delete()
		WeixinUser.objects.all().delete()
		Session.objects.all().delete()
		Message.objects.all().delete()
		WeixinMpUser.objects.all().delete()

		#有与关键词匹配的规则，回复内容为规则中所设定的回复内容
		category = self._create_dummy_category(getTestUserProfile().user)
		rule = self._create_dummy_rule(category, getTestUserProfile().user, TEXT_TYPE, 'key1|key2', 'val')

		test_xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName> 
		<CreateTime>1348831860</CreateTime>
		<MsgType><![CDATA[text]]></MsgType>
		<Content><![CDATA[key1]]></Content>
		<MsgId>1234567890123456</MsgId>
		</xml>
		"""
		test_message = parse_weixin_message_from_xml(test_xml_message)
		context = createDummyMessageHandlingContext(test_message, test_xml_message)
		context.request = HttpRequest()
		weixin_user_test = WeixinUser.objects.create(username='fromUser')
		weixin_mpuser = self._create_dummy_mpuser(getTestUserProfile(), 'toUser')

		handler = AutoQaMessageHandler()
		response_message = handler.handle(context)
		from BeautifulSoup import BeautifulSoup
		self.assertEquals(rule.answer, BeautifulSoup(response_message).content.text)

		test_xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName> 
		<CreateTime>1348831860</CreateTime>
		<MsgType><![CDATA[text]]></MsgType>
		<Content><![CDATA[key2]]></Content>
		<MsgId>1234567890123456</MsgId>
		</xml>
		"""
		test_message = parse_weixin_message_from_xml(test_xml_message)
		context = createDummyMessageHandlingContext(test_message, test_xml_message)
		context.request = HttpRequest()

		response_message = handler.handle(context)
		self.assertEquals(rule.answer, BeautifulSoup(response_message).content.text)

		#此时会话历史中会记录4条消息，其中有两条是系统自动回复内容
		self.assertEquals(1, Session.objects.all().count())	
		self.assertEquals('key2', Session.objects.all()[0].latest_contact_content)
		self.assertEquals(4, Message.objects.all().count())	
		self.assertEquals(2, Message.objects.filter(is_reply=1).count())		

	def test_keyword_handle_with_matched_rule_with_emotion(self):
		#清空信息
		Rule.objects.all().delete()
		Category.objects.all().delete()
		WeixinUser.objects.all().delete()
		Session.objects.all().delete()
		Message.objects.all().delete()
		WeixinMpUser.objects.all().delete()

		#有与关键词匹配的规则，回复内容为规则中所设定的回复内容(表情信息)
		category = self._create_dummy_category(getTestUserProfile().user)
		rule = self._create_dummy_rule(category, getTestUserProfile().user, TEXT_TYPE, 'key', u'/微笑')

		test_xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName> 
		<CreateTime>1348831860</CreateTime>
		<MsgType><![CDATA[text]]></MsgType>
		<Content><![CDATA[key]]></Content>
		<MsgId>1234567890123456</MsgId>
		</xml>
		"""
		test_message = parse_weixin_message_from_xml(test_xml_message)
		context = createDummyMessageHandlingContext(test_message, test_xml_message)
		context.request = HttpRequest()
		weixin_user_test = WeixinUser.objects.create(username='fromUser')
		weixin_mpuser = self._create_dummy_mpuser(getTestUserProfile(), 'toUser')

		handler = AutoQaMessageHandler()
		response_message = handler.handle(context)
		from BeautifulSoup import BeautifulSoup
		self.assertEquals(rule.answer, BeautifulSoup(response_message).content.text)

		handler = AutoQaMessageHandler()
		response_message = handler.handle(context, True)

		#模拟器中的表情需要转换为图片
		from BeautifulSoup import BeautifulSoup
		self.assertEquals('<img src="/static/ueditor-1.2.6.1/dialogs/emotion/images/weixin/1.gif"  />', BeautifulSoup(response_message).content.text)

	def test_keyword_handle_without_matched_rule(self):
		#清空信息
		Rule.objects.all().delete()
		Category.objects.all().delete()
		WeixinUser.objects.all().delete()
		Session.objects.all().delete()
		Message.objects.all().delete()
		WeixinMpUser.objects.all().delete()

		#如果没有配置自动回复, 回复为None

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
		context.request = HttpRequest()
		weixin_user_test = WeixinUser.objects.create(username='fromUser')
		weixin_mpuser = self._create_dummy_mpuser(getTestUserProfile(), 'toUser')

		handler = AutoQaMessageHandler()
		self.assertEquals(None, handler.handle(context))

		#会记录接收到的信息
		self.assertEquals(1, Session.objects.all().count())		
		self.assertEquals(True, Session.objects.all()[0].is_show)
		
		self.assertEquals(1, Message.objects.all().count())		
		self.assertEquals(test_message.content, Message.objects.all()[0].content)

		#但是如果消息来自登录后的模拟器来，那么消息则不进行消息记录
		Session.objects.all().delete()
		Message.objects.all().delete()
		context.request.POST['is_user_logined'] = '1'

		self.assertEquals(None, handler.handle(context, True))
		#不会记录接收到的信息
		self.assertEquals(0, Session.objects.all().count())	
		self.assertEquals(0, Message.objects.all().count())	

		#如果消息来自模拟器，但是没有登录，那么消息仍会被记录
		#会记录接收到的信息
		Session.objects.all().delete()
		Message.objects.all().delete()
		context.request.POST['is_user_logined'] = '0'

		self.assertEquals(None, handler.handle(context, True))
		self.assertEquals(1, Session.objects.all().count())		
		self.assertEquals(True, Session.objects.all()[0].is_show)
		
		self.assertEquals(1, Message.objects.all().count())		
		self.assertEquals(test_message.content, Message.objects.all()[0].content)

		#如果设置了自动回复，那么会返回自动回复内容
		Session.objects.all().delete()
		Message.objects.all().delete()

		category = self._create_dummy_category(getTestUserProfile().user)
		rule = self._create_dummy_rule(category, getTestUserProfile().user, UNMATCH_TYPE, '', 'auto_response')
		response_message = handler.handle(context)
		from BeautifulSoup import BeautifulSoup
		self.assertEquals(rule.answer, BeautifulSoup(response_message).content.text)

		#此时会在回话历史记录中记录自动回复的消息
		self.assertEquals(1, Session.objects.all().count())	
		self.assertEquals(2, Message.objects.all().count())		
		for message in Message.objects.all():
			self.assertTrue(test_message.content==message.content or \
					u"[自动回复]: {}".format(rule.answer)==message.content )

	def _create_dummy_category(self, user):
		return Category.objects.create(
			owner = user,
			name = '--'
			)

	def _create_dummy_rule(self, category, user, rule_type, patterns, answer):
		return Rule.objects.create(
			owner = user,
			category = category,
			type = rule_type,
			patterns = patterns,
			answer = answer
			)	

	def _create_dummy_mpuser(self, user_profile, username):
		return WeixinMpUser.objects.create(
			owner = user_profile.user,
			username = username,
			password = '-',
			access_token = '-',
			fakeid = '-',
			expire_time = '2001-01-01 00:00:00'
			)

if __name__ == '__main__':
	start_test_withdb()