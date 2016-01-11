# -*- coding: utf-8 -*-
""" @package account.account_util
account_util单元测试

@warning `from test import test_env_with_db as test_env` 已经失效了。

"""

import sys
import unittest
import os

__author__ = 'chuter'

if __name__ == '__main__':
	WEAPP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	sys.path.insert(0, WEAPP_DIR)
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weapp.settings')
	for path in sys.path:
		print("{}".format(path))


from test import test_env_with_db as test_env

from account.models import *
from util import get_binding_weixin_mpuser, get_mpuser_accesstoken

class AccountUtilTest(unittest.TestCase):
	def setUp(self):
		WeixinMpUser.objects.all().delete()
		WeixinMpUserAccessToken.objects.all().delete()

	def test_binding_weixin_mpuser_get_when_nobinding(self):
		#在没有绑定任何微信公众号的时候获取的为空
		binding_mp_user = get_binding_weixin_mpuser(test_env.getTestUserProfile().user)
		self.assertTrue(binding_mp_user is None)

	def test_binding_weixin_mpuser_get_when_binding(self):
		#绑定微信公众号
		test_mpuser = self._create_dummy_weixin_mpuser(test_env.getTestUserProfile().user, 'dummymp')
		binding_mp_user = get_binding_weixin_mpuser(test_env.getTestUserProfile().user)

		self.assertEqual('dummymp', binding_mp_user.username)

		#rollback db
		binding_mp_user.delete()

	def test_binding_mpuser_accesstoken_when_has_no_accesstoken(self):
		#没有公众号对应的access_token信息时
		test_mpuser = self._create_dummy_weixin_mpuser(test_env.getTestUserProfile().user, 'dummymp')
		binding_mp_user = get_binding_weixin_mpuser(test_env.getTestUserProfile().user)
		mp_user_access_token = get_mpuser_accesstoken(binding_mp_user)
		self.assertTrue(mp_user_access_token is None)		

	def test_binding_mpuser_accesstoken_when_has_accesstoken(self):
		#没有公众号对应的access_token信息时
		test_mpuser = self._create_dummy_weixin_mpuser(test_env.getTestUserProfile().user, 'dummymp')
		binding_mp_user = get_binding_weixin_mpuser(test_env.getTestUserProfile().user)
		test_mp_user_access_token = self._create_dummy_weixin_mpuser_accesstoken(test_mpuser, 'dummytoken')
		mp_user_access_token = get_mpuser_accesstoken(binding_mp_user)
		self.assertEqual('dummytoken', mp_user_access_token.access_token)

		#rollback db
		test_mpuser.delete()
		test_mp_user_access_token.delete()

	def _create_dummy_weixin_mpuser(self, user, mpusername):
		return WeixinMpUser.objects.create(
			owner = user,
			username = mpusername,
			password = '',
			access_token = '',
			fakeid = '',
			expire_time = '2001-01-01 00:00:00'
			)
	
	def _create_dummy_weixin_mpuser_accesstoken(self, mpuser, access_token):
		return WeixinMpUserAccessToken.objects.create(
			username = mpuser.username,
			app_id = '',
			app_secret = '',
			access_token = access_token,
			created_at = '2001-01-01 00:00:00'
			)

if __name__ == '__main__':
	test_env.start_test_withdb()