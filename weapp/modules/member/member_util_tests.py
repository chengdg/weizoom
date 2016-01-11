# -*- coding: utf-8 -*-

__author__ = 'chuter'

import sys
import unittest

if __name__ == '__main__':
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

	from test import test_env_with_db as test_env

from django.test.client import RequestFactory
from django.conf import settings

from account.models import WeixinUserToken
from message.models import WeixinUser
from models import Member

from util import *
import util as member_util

def stub_member_basic_info_update(request, member, weixinuser):
	return

########################################################################
# 会员工具类方法中创建会员获取会员方法的测试
########################################################################
class MemberUtilTest(unittest.TestCase):

	dummy_wxsid = '123'
	dummy_icon = 'dummy_icon'

	def setUp(self):
		member_util.member_basic_info_updater = stub_member_basic_info_update
		self.factory = RequestFactory()
		Member.objects.all().delete()

		self.test_weixin_user = self._create_dummy_weixin_user(self.dummy_icon, '-')
		self.test_weixin_user_token = self._create_dummy_weixin_user_token(self.dummy_wxsid, '-')

	def tearDown(self):
		WeixinUser.objects.all().delete()
		WeixinUserToken.objects.all().delete()

	def test_member_create_if_already_is_member_with_getrequest(self):
		request = self.factory.get('/')
		
		request.COOKIES[settings.WEIXIN_USER_COOKIE_MEMBER_ID_FILED] = self.dummy_wxsid

		create_member(request)
		members_count = Member.objects.all().count()
		self.assertEqual(0, members_count)

	def test_member_create_if_already_is_member_with_postrequest(self):
		request = self.factory.post('/')
		
		request.COOKIES[settings.WEIXIN_USER_COOKIE_MEMBER_ID_FILED] = self.dummy_wxsid

		create_member(request)
		members_count = Member.objects.all().count()
		self.assertEqual(0, members_count)

	def test_member_create_by_session_with_getrequest(self):
		request = self.factory.get('/')
		
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_wxsid

		create_member(request)
		created_member = Member.objects.get(wxuser_token=self.dummy_wxsid)
		self.assertEqual(self.dummy_icon, created_member.user_icon)

	def test_member_create_by_session_with_postrequest(self):
		request = self.factory.post('/')
		
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_wxsid

		create_member(request)
		created_member = Member.objects.get(wxuser_token=self.dummy_wxsid)
		self.assertEqual(self.dummy_icon, created_member.user_icon)

	def test_member_get_with_wxsid_in_cookie(self):
		test_member = self._create_dummy_member(self.test_weixin_user_token)

		try:
			request = self.factory.get('/')
			request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_wxsid

			member = get_member(request)
			self.assertEqual(test_member.id, member.id)
		finally:
			#rollback db
			test_member.delete()


	def _create_dummy_weixin_user(self, icon, username):
		return WeixinUser.objects.create(
			username = username,
			fake_id = '1',
			app_id = '1',
			weixin_user_nick_name = '-',
			weixin_user_remark_name = '-',
			weixin_user_icon = icon
			)

	def _create_dummy_weixin_user_token(self, token, username):
		return WeixinUserToken.objects.create(
			shop = '3120',
			weixin_user_name = username,
			token = token
			)

	def _create_dummy_member(self, weixinuser_token):
		return Member.objects.create(
			wxuser_token = weixinuser_token,
			shop_name = '-',
			user_icon = '-'
		)


if __name__ == '__main__':
	test_env.start_test_withdb()