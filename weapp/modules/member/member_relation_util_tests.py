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

########################################################################
# 会员工具类方法中会员关系相关方法的测试
########################################################################
class MemberRelationUtilTest(unittest.TestCase):

	dummy_wxsid = '123'
	dummy_followed_wxsid = '321'
	dummy_icon = 'dummy_icon'

	def setUp(self):
		self.factory = RequestFactory()
		Member.objects.all().delete()
		MemberFollowRelation.objects.all().delete()

		self.test_weixin_user = self._create_dummy_weixin_user(self.dummy_icon, '--')
		self.test_weixin_user_token = self._create_dummy_weixin_user_token(self.dummy_wxsid, '--')

		self.test_followed_weixin_user = self._create_dummy_weixin_user(self.dummy_icon, '-')
		self.test_followed_weixin_user_token = self._create_dummy_weixin_user_token(self.dummy_followed_wxsid, '-')

	def tearDown(self):
		WeixinUser.objects.all().delete()
		WeixinUserToken.objects.all().delete()

	def test_member_relation_create_when_relation_not_exist(self):
		member = self._create_dummy_member(self.test_weixin_user_token)
		followed_member = self._create_dummy_member(self.test_followed_weixin_user_token)

		request = self.factory.get('/')
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_wxsid
		request.COOKIES[settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_followed_wxsid

		build_member_follow_relation(request)
		relation_count = MemberFollowRelation.objects.filter(member_id=followed_member.id, follower_member_id=member.id).count()

		self.assertEqual(1, relation_count)

	def test_member_relation_create_when_relation_already_exist(self):
		member = self._create_dummy_member(self.test_weixin_user_token)
		followed_member = self._create_dummy_member(self.test_followed_weixin_user_token)
		self._create_dummy_member_relation(self.dummy_wxsid, self.dummy_followed_wxsid)

		request = self.factory.get('/')
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_wxsid
		request.COOKIES[settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_followed_wxsid

		build_member_follow_relation(request)
		relation_count = MemberFollowRelation.objects.filter(member_id=followed_member.id, follower_member_id=member.id).count()
		self.assertEqual(1, relation_count)

	def test_member_relation_create_for_same_weixin_user(self):
		#测试当前微信用户和所关注的微信用户信息相同时对关系的处理
		member = self._create_dummy_member(self.test_weixin_user_token)

		request = self.factory.get('/')
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_wxsid
		request.COOKIES[settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_wxsid

		build_member_follow_relation(request)
		relation_count = MemberFollowRelation.objects.filter(member_id=member.id, follower_member_id=member.id).count()
		self.assertEqual(0, relation_count)

	def test_member_relation_create_only_with_cur_weixin_user_wxsid(self):
		request = self.factory.get('/')
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_wxsid

		build_member_follow_relation(request)
		relation_count = MemberFollowRelation.objects.filter().count()
		self.assertEqual(0, relation_count)

	def test_followed_member_get_when_exist(self):
		followed_member = self._create_dummy_member(self.test_followed_weixin_user_token)

		request = self.factory.get('/')
		request.COOKIES[settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_followed_wxsid

		followed_member_get = get_followed_member_from_cookie(request)
		self.assertEqual(followed_member.id, followed_member_get.id)

	def test_followed_member_get_when_not_exist(self):
		request = self.factory.get('/')
		request.COOKIES[settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_followed_wxsid

		followed_member_get = get_followed_member_from_cookie(request)
		self.assertEqual(None, followed_member_get)

	def _create_dummy_member_relation(self, wxsid, follow_wxsdi):
		build_member_follow_relation_by_weixin_user_session(wxsid, follow_wxsdi)

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