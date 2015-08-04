# -*- coding: utf-8 -*-

__author__ = 'chuter'

import sys
import unittest

if __name__ == '__main__':
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from test import test_env_with_db as test_env

from django.test.client import RequestFactory

from account.social_account.models import SocialAccount

from util import *

import member_settings

########################################################################
# 会员工具类方法的测试，包括
# 	get_followed_member_token(request)
#	get_followed_member(request)
#   get_uuid(request)
#   get_member(request)
#	generate_uuid(request)
########################################################################
class UtilTest(unittest.TestCase):
	DUMMY_FOLLOWED_MEMBER_TOKEN = 'dummy_followed_member'
	DUMMY_MEMBER_TOKEN = 'dummy_member'
	DUMMY_WEBAPP_ID = '3102'

	def setUp(self):
		self.factory = RequestFactory()

	def test_followed_member_token_get_from_cookie_with_postrequest(self):
		request = self.factory.post('/')
		request.COOKIES[member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY] = self.DUMMY_FOLLOWED_MEMBER_TOKEN

		followed_member_token = get_followed_member_token(request)
		self.assertEqual(self.DUMMY_FOLLOWED_MEMBER_TOKEN, followed_member_token) 

	def test_followed_member_token_get_from_cookie_with_getrequest(self):
		request = self.factory.get('/')
		request.COOKIES[member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY] = self.DUMMY_FOLLOWED_MEMBER_TOKEN

		followed_member_token = get_followed_member_token(request)
		self.assertEqual(self.DUMMY_FOLLOWED_MEMBER_TOKEN, followed_member_token) 

	def test_followed_member_token_get_from_url_with_getrequest(self):
		request = self.factory.get('/?%s=%s' % \
			(member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, self.DUMMY_FOLLOWED_MEMBER_TOKEN))

		followed_member_token = get_followed_member_token(request)
		self.assertEqual(self.DUMMY_FOLLOWED_MEMBER_TOKEN, followed_member_token) 

	def test_followed_member_token_get_from_url_with_postrequest(self):
		request = self.factory.post('/?%s=%s' % \
			(member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, self.DUMMY_FOLLOWED_MEMBER_TOKEN))

		followed_member_token = get_followed_member_token(request)
		self.assertEqual(self.DUMMY_FOLLOWED_MEMBER_TOKEN, followed_member_token) 

	def test_followed_member_get(self):
		#准备数据
		test_member = self._create_dummy_member(self.DUMMY_FOLLOWED_MEMBER_TOKEN, self.DUMMY_WEBAPP_ID)

		try:
			request = self.factory.post('/')
			request.COOKIES[member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY] = self.DUMMY_FOLLOWED_MEMBER_TOKEN

			followed_member = get_followed_member(request)

			self.assertEqual(self.DUMMY_FOLLOWED_MEMBER_TOKEN, followed_member.token)
		finally:
			#rollback the db
			test_member.delete()

	def test_member_get_by_member_token(self):
		#准备数据
		test_member = self._create_dummy_member(self.DUMMY_MEMBER_TOKEN, self.DUMMY_WEBAPP_ID)

		try:
			#在请求中携带当前会员信息
			request = self.factory.get('/')
			request.COOKIES[member_settings.MEMBER_TOKEN_SESSION_KEY] = test_member.token

			member_get = get_member(request)
			self.assertEqual(test_member.id, member_get.id)
		finally:
			#rollback the db
			test_member.delete()

	def test_member_get_by_binded_social_account(self):
		#准备数据
		dummy_social_account_token = 'dummy_sct'
		dummy_social_account_openid = 'dummy_openid'

		#一个会员同时绑定了两个社交账号
		test_member = self._create_dummy_member(self.DUMMY_MEMBER_TOKEN, self.DUMMY_WEBAPP_ID)

		test_social_account_a = self._create_dummy_social_account(
			dummy_social_account_token, dummy_social_account_openid, self.DUMMY_WEBAPP_ID)
		test_social_account_b = self._create_dummy_social_account(
			dummy_social_account_token+'_', dummy_social_account_openid+'_', self.DUMMY_WEBAPP_ID)
		
		test_relation_a = self._build_member_social_account_relation(test_member, test_social_account_a)
		test_relation_b = self._build_member_social_account_relation(test_member, test_social_account_b)

		try:
			#在请求中携带当前社交账户信息
			request = self.factory.get('/')
			request.social_account = test_social_account_a

			member_get = get_member(request)
			self.assertEqual(test_member.id, member_get.id)
		finally:
			#rollback the db
			test_relation_a.delete()
			test_relation_b.delete()
			test_member.delete()
			test_social_account_a.delete()
			test_social_account_b.delete()

	def _build_member_social_account_relation(self, member, account):
		return MemberHasSocialAccount.objects.create(
			member = member,
			account = account,
			webapp_id = member.webapp_id
			)

	def _create_dummy_social_account(self, token, openid, webapp_id):
		return SocialAccount.objects.create(
			webapp_id = webapp_id,
			token = token,
			openid = openid
			)

	def test_uuid_get_with_getrequest(self):
		request = self.factory.get('/')
		request.COOKIES[member_settings.NON_MEMBER_UUID_SESSION_KEY] = 'dummy_uuid'
		
		uuid = get_uuid(request)
		self.assertEqual('dummy_uuid', uuid)

	def test_uuid_get_with_postrequest(self):
		request = self.factory.post('/')
		request.COOKIES[member_settings.NON_MEMBER_UUID_SESSION_KEY] = 'dummy_uuid'
		
		uuid = get_uuid(request)
		self.assertEqual('dummy_uuid', uuid)

	def test_uuid_generate(self):
		for _ in range(3):
			m = [generate_uuid(None) for _ in range(10)]
			self.assertEqual(len(m), len(set(m)), "duplicate uuid found !")

	def _create_dummy_member(self, token, webapp_id):
		return Member.objects.create(
			token = token,
			webapp_id = webapp_id
			)	


if __name__ == '__main__':
	test_env.start_test_withdb()