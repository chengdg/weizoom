
# -*- coding: utf-8 -*-

__author__ = 'bert'


"""Unit tests for voice record process.

These tests make sure the message handling works as it should. """

if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')
	sys.path.insert(0, 'D:/weapp_project/weapp3-0/weapp')
	print sys.path

from weixin.message.handler.handler_testutil import *
init_handler_test_env()

import time

from BeautifulSoup import BeautifulSoup

from weixin.message.handler.weixin_message import parse_weixin_message_from_xml
from weixin.message.handler.message_handler import *
from weixin.message.handler.message_handle_context import *
from ticket_messge_handler import QrcodeHandler
#from answer_game import *

from account.models import *

from django.test import TestCase
from models import *
from modules.member.models import Member

class MemberQrcodeHandlerTest(TestCase):
	DUMMY_FOLLOWED_MEMBER_TOKEN = 'dummy_followed_member'
	DUMMY_MEMBER_TOKEN = 'dummy_member'
	DUMMY_WEBAPP_ID = '3102'

	def testProcessEventMessage(self):
		test_xml_message = """
		<xml><ToUserName><![CDATA[gh_33aa31ca7e17]]></ToUserName>
		<FromUserName><![CDATA[oBDYPuCQTFAjkLHffkyMBB7cFS8g]]></FromUserName>
		<CreateTime>1389078815</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[SCAN]]></Event>
		<EventKey><![CDATA[123]]></EventKey>
		<Ticket><![CDATA[gQGX7zoAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xL3BrTWZZRWZtbTRqaXBwcERBbS1BAAIEWV7KUgMEAAAAAA==]]></Ticket>
		</xml>100393258418914</msgid>
		</xml>
		"""
		test_message = parse_weixin_message_from_xml(test_xml_message)
		context = createDummyMessageHandlingContext(test_message, test_xml_message)

		print context.__dict__
		#准备数据
		user_profile = context.user_profile
		user_profile.webapp_template = 'wine'
		user_profile.save()
		context.user_profile = user_profile
		weixin_user = WeixinUser.objects.create(username=context.message.fromUserName, fake_id=u'zhangsan_1369963462474', app_id='3180',
			weixin_user_nick_name=u'张三', weixin_user_remark_name=u'张三remark',
			weixin_user_icon=u'/static/img/user-2.jpg', created_at='2013-06-05 10:00:00', is_head_image_received='1',
			head_image_retry_count='1')

		test_member = self._create_dummy_member(self.DUMMY_MEMBER_TOKEN, self.DUMMY_WEBAPP_ID)
		member_qrcode = self._create_member_qrcode(member)
		handler = ticket_messge_handler()
		handler.handle(context, False)
		# #QcrodLogin.objects.create(ticket=context.message.ticket)
		# handler = QcrodLoginHandler()
		# handler.handle(context, False)
		response_content = BeautifulSoup(handler.handle(context))
		
		self.assertEqual('oBDYPuCQTFAjkLHffkyMBB7cFS8g', response_content.tousername.text)
		print response_content.content.text

	def _create_dummy_member(self, token, webapp_id):
		return Member.objects.create(
				token = token,
				webapp_id = webapp_id
				)

	def _create_member_qrcode(member):
		ticket = 'gQGX7zoAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xL3BrTWZZRWZtbTRqaXBwcERBbS1BAAIEWV7KUgMEAAAAAA=='
		return MemberQrcode.objects.create(member_id=member.id, ticket=ticket, created_time=int(time.time()), expired_second=1800)
		
if __name__ == '__main__':
	start_test_withdb()