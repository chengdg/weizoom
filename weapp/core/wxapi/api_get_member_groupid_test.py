# -*- coding: utf-8 -*-

"""
用于测试与微信api的交互

验证系统中提供的api接口中访问对应微信api接口
时地址是否正确，参数是否正确
"""

__author__ = 'chuter'


import unittest
import json

if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from test import test_env_with_db as test_env
test_env.init()

import api_settings
import weixin_api
import weixin_error_codes as errorcodes

from weixin.user.models import WeixinMpUser, WeixinMpUserAccessToken
from new_weixin_api import *
#from custom_message import TextCustomMessage, build_custom_message_json_str

fake_response_json_str = '{"errcode":0, "errmsg":""}'


class GetMemberGroupIdApiTestCase(unittest.TestCase):
	dummy_access_token_str = 'khb3suQHanISYvmZL_IsrS63p6QrbnPL1liw4cO3g08ub0XVU_r6zwc8T-56EAOJ'

	def setUp(self):
		WeixinMpUserAccessToken.objects.all().delete()
		self.weixin_http_client = WeixinHttpClient()
		self.api = WeixinApi(self._create_dummy_certified_mpuser_access_token(), self.weixin_http_client)

	def tearDown(self):
		WeixinMpUserAccessToken.objects.all().delete()

	def test_userinfo_get(self):
		#weixin_api.head_img_saver = dummy_head_img_saver

		result = self.api.get_member_group_id('oR3uquP43phGnoBZoAakpXuo6meY')
		print result
		print type(result)
		
		# self.assertEqual(errcode, error_response.errcode)
	

	def _assert_url_contains(self, parts, url):
		for part in parts:
			self.assertTrue(url.find(part) >= 0)

	def _create_dummy_certified_mpuser_access_token(self):
		return WeixinMpUserAccessToken.objects.create(
			mpuser = self._create_dummy_mpuser(),
			app_id = '-',
			app_secret = '-',
			access_token = self.dummy_access_token_str,
			created_at = '2001-01-01 00:00:00',
			#is_certified = True,
			#is_service = True
			)

	def _create_dummy_mpuser(self):
		return WeixinMpUser.objects.create(
			owner = test_env.getTestUser(),
			username = 'dummy_user_name',
			password = 'dummy_password',
			is_certified = True,
			is_service = True
			)

if __name__ == '__main__':
	test_env.start_test_withdb()