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

from core.dateutil import get_today

from account.models import WeixinUserDailyStatistics
from message.models import WeixinUser
from qa.models import *

from BeautifulSoup import BeautifulSoup

from weixin.handler.message_handler import *
from default_event_handler import *

from django.test import TestCase

class DefaultEventHandlerTest(TestCase):
	def test_unsubscribe_event_handle(self):
		#清空信息
		Rule.objects.all().delete()
		Category.objects.all().delete()
		WeixinUserDailyStatistics.objects.all().delete()
		WeixinFollowers.objects.all().delete()
		WeixinUser.objects.all().delete()

		test_xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>123456789</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[unsubscribe]]></Event>
		<EventKey><![CDATA[EVENTKEY]]></EventKey>
		</xml>
		"""
		test_message = parse_weixin_message_from_xml(test_xml_message)
		context = createDummyMessageHandlingContext(test_message, test_xml_message)
		weixin_user_test = WeixinUser.objects.create(username='fromUser')
		handler = DefaultEventHandler()

		#当发送消息的微信用户在系统中还没有关注店铺时
		#处理前，系统中对应店铺的粉丝数为0，没有店铺当天新增用户数记录
		self.assertEqual(0, WeixinUserDailyStatistics.objects.filter(data_date=get_today(), webapp_id=context.user_profile.webapp_id
			).count())
		self.assertEqual(0, WeixinFollowers.objects.filter(weixin_user='fromUser', webapp_id=context.user_profile.webapp_id).count())

		#进行取消关注处理
		self.assertEqual(EMPTY_RESPONSE_CONTENT, handler.handle(context))
		#店铺当天新增用户数-1，为-1
		self.assertEqual(-1, WeixinUserDailyStatistics.objects.get(data_date=get_today(), webapp_id=context.user_profile.webapp_id
			).count)	
		#粉丝数为0, 仍然不是粉丝
		self.assertEqual(0, WeixinFollowers.objects.filter(weixin_user='fromUser', webapp_id=context.user_profile.webapp_id).count())	

		#当发送消息的微信用户在系统中已经关注店铺时
		test_xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>123456789</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[subscribe]]></Event>
		<EventKey><![CDATA[EVENTKEY]]></EventKey>
		</xml>
		"""
		subscribe_test_message = parse_weixin_message_from_xml(test_xml_message)
		subscrib_context = createDummyMessageHandlingContext(subscribe_test_message, test_xml_message)
		handler.handle(subscrib_context)

		#系统中店铺当天新增用户数-1，为0
		self.assertEqual(0, WeixinUserDailyStatistics.objects.get(data_date=get_today(), webapp_id=context.user_profile.webapp_id
			).count)
		#已经成为粉丝
		self.assertEqual(1, WeixinFollowers.objects.filter(weixin_user='fromUser', webapp_id=context.user_profile.webapp_id).count())

 		#此时再处理取消关注事件
		self.assertEqual(EMPTY_RESPONSE_CONTENT, handler.handle(context))
		#粉丝数-1，为-1
		self.assertEqual(-1, WeixinUserDailyStatistics.objects.get(data_date=get_today(), webapp_id=context.user_profile.webapp_id
			).count)	
		#已不是粉丝
		self.assertEqual(0, WeixinFollowers.objects.filter(weixin_user='fromUser', webapp_id=context.user_profile.webapp_id).count())	

		#如果消息来自模拟器，那么店铺点天新增用户数不发生变化
		self.assertEqual(EMPTY_RESPONSE_CONTENT, handler.handle(context, True))
		self.assertEqual(-1, WeixinUserDailyStatistics.objects.get(data_date=get_today(), webapp_id=context.user_profile.webapp_id
			).count)
		self.assertEqual(0, WeixinFollowers.objects.filter(weixin_user='fromUser', webapp_id=context.user_profile.webapp_id).count())	

	def test_subscribe_event_handle(self):
		#清空信息
		Rule.objects.all().delete()
		Category.objects.all().delete()
		WeixinUserDailyStatistics.objects.all().delete()
		WeixinFollowers.objects.all().delete()
		WeixinUser.objects.all().delete()

		test_xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>123456789</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[subscribe]]></Event>
		<EventKey><![CDATA[EVENTKEY]]></EventKey>
		</xml>
		"""
		test_message = parse_weixin_message_from_xml(test_xml_message)
		context = createDummyMessageHandlingContext(test_message, test_xml_message)
		weixin_user_test = WeixinUser.objects.create(username='fromUser')
		handler = DefaultEventHandler()

		#处理前，系统中对应店铺的粉丝数为0
		self.assertEqual(0, WeixinUserDailyStatistics.objects.filter(data_date=get_today(), webapp_id=context.user_profile.webapp_id
			).count())

		#没有对应的关注回复，处理后返回None
		self.assertEqual(EMPTY_RESPONSE_CONTENT, handler.handle(context))
		#系统中对应店铺的的粉丝数+1
		self.assertEqual(1, WeixinUserDailyStatistics.objects.get(data_date=get_today(), webapp_id=context.user_profile.webapp_id
			).count)
		#已经成为店铺粉丝
		self.assertEqual(1, WeixinFollowers.objects.filter(weixin_user='fromUser', webapp_id=context.user_profile.webapp_id).count())

		#有对应的关注回复，处理后返回所设定的关注回复内容
		category = self._create_subsribe_auto_response_category(context.user_profile.user)
		subscribe_response_rule = self._create_subscribe_response_rule(category, context.user_profile.user, '---')

		response_content = handler.handle(context)
		response_soup = BeautifulSoup(response_content)
		self.assertEqual(subscribe_response_rule.answer, response_soup.content.text)

		#系统中对应店铺的的粉丝数+1
		self.assertEqual(2, WeixinUserDailyStatistics.objects.get(data_date=get_today(), webapp_id=context.user_profile.webapp_id
			).count)

		#如果消息来自模拟器，店铺当天新增用户数不发生变化
		response_content = handler.handle(context, True)
		response_soup = BeautifulSoup(response_content)
		self.assertEqual(subscribe_response_rule.answer, response_soup.content.text)
		self.assertEqual(2, WeixinUserDailyStatistics.objects.get(data_date=get_today(), webapp_id=context.user_profile.webapp_id
			).count)

	def _create_subsribe_auto_response_category(self, user):
		return Category.objects.create(
			owner = user,
			name = 'subscribe_auto_response'
			)

	def _create_subscribe_response_rule(self, category, user, response_text):
		return Rule.objects.create(
				owner = user,
				category = category,
				type = FOLLOW_TYPE,
				patterns = '',
				answer = response_text
			)
		
if __name__ == '__main__':
	start_test_withdb()
