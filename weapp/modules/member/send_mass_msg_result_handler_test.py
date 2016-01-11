
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
from send_mass_msg_result_handler import SendMassMessageResultHandler
#from answer_game import *

from account.models import *

from django.test import TestCase
from models import *
from modules.member.models import Member
from util import *

class MemberQrcodeHandlerTest(TestCase):
	DUMMY_FOLLOWED_MEMBER_TOKEN = 'dummy_followed_member'
	DUMMY_MEMBER_TOKEN = 'dummy_member'
	DUMMY_WEBAPP_ID = '3102'

	def testProcessEventMessage(self):
		test_xml_message = """
		<xml><ToUserName><![CDATA[gh_4878200514f0]]></ToUserName>
		<FromUserName><![CDATA[ogd-KuOtiyZA5IMU1RKJXUiJc7s8]]></FromUserName>
		<CreateTime>1399860973</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[MASSSENDJOBFINISH]]></Event>
		<MsgID>2347649618</MsgID>
		<Status><![CDATA[send success]]></Status>
		<TotalCount>2</TotalCount>
		<FilterCount>2</FilterCount>
		<SentCount>2</SentCount>
		<ErrorCount>0</ErrorCount>
		</xml>
		"""
		test_message = parse_weixin_message_from_xml(test_xml_message)
		context = createDummyMessageHandlingContext(test_message, test_xml_message)

		print context.__dict__
		#准备数据
		user_profile = context.user_profile

		context.user_profile = user_profile
		weixin_user = WeixinUser.objects.create(username=context.message.fromUserName, fake_id=u'zhangsan_1369963462474', app_id='3180',
			weixin_user_nick_name=u'张三', weixin_user_remark_name=u'张三remark',
			weixin_user_icon=u'/static/img/user-2.jpg', created_at='2013-06-05 10:00:00', is_head_image_received='1',
			head_image_retry_count='1')

		test_member = self._create_dummy_member(self.DUMMY_MEMBER_TOKEN, self.DUMMY_WEBAPP_ID)
		self._create_msg_log(self.DUMMY_WEBAPP_ID)
		handler = SendMassMessageResultHandler()
		handler.handle(context, False)
		# #QcrodLogin.objects.create(ticket=context.message.ticket)
		# handler = QcrodLoginHandler()
		# handler.handle(context, False)
		response_content = BeautifulSoup(handler.handle(context))
		
		#self.assertEqual('oBDYPuCQTFAjkLHffkyMBB7cFS8g', response_content.tousername.text)
		print response_content.content.text

	def _create_dummy_member(self, token, webapp_id):
		return Member.objects.create(
				token = token,
				webapp_id = webapp_id
				)

	def _create_msg_log(webapp_id, ):
		UserSentMassMsgLog.create(webapp_id, 0, 'test')
		
if __name__ == '__main__':
	start_test_withdb()