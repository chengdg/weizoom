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

class CustomerizedMenuApiTestCase(unittest.TestCase):
	#dummy_access_token_str  = 'adb-R_0VcwJitp9B-h8H-9AH0m6tXGN9t6rbyM_tJsbSS1qgU25R0Bo9C29GcBM1kevDiARj6a-zB3IksfXZ6Q6o8yODJnTSuO_T2DpbtSsX_-iAn1A13aS4eDm2VnPY3cfrVdbNceA-o8law3jgRg6Q'
	dummy_access_token_str = 'zuGmozgDRhoU80O5b_mg8QSxgNoxy_QnWF28pp5OWSayrSPV8wXeOn1j19nHOfoCjvocvh8j3Bxc0SobiRbC70u9v01F-mBjf3Oqgl7y83V5DcXTK16eX4dnYsZc089A1uWyLBEpLeYaDRIRCoI-dg'
	dummy_post_str = '{"button": [{"name": "菜单1", "sub_button": [{"type": "click", "name": "菜单项3", "key": "MENU_QUERY_3"}, {"type": "click", "name": "菜单项2", "key": "MENU_QUERY_2"}]}]}'
	dummy_post_old = "{u'button': [{u'type': u'click', u'name': u'\u5546\u57ce\u5fae\u7ad9\u54c8', u'key': u'MENU_QUERY_2', u'sub_button': []}, {u'type': u'click', u'name':u'\u7528\u6237\u4e2d\u5fc3', u'key': u'MENU_QUERY_1', u'sub_button': []}, {u'name': u'\u8425\u9500\u5de5\u5177\u5440', u'sub_button': [{u'type': u'click', u'name': u'\u5206\u4eabtitle', u'key': u'MENU_QUERY_12', u'sub_button': []}, {u'type': u'click', u'name': u'\u62bd\u5956', u'key': u'MENU_QUERY_11', u'sub_button':[]}, {u'type': u'click', u'name': u'\u5fae\u4fe1\u652f\u4ed8', u'key': u'MENU_QUERY_10', u'sub_button': []}]}]}"
	def setUp(self):
		WeixinMpUserAccessToken.objects.all().delete()
		self.weixin_http_client = WeixinHttpClient()
		self.api = WeixinApi(self._create_dummy_certified_mpuser_access_token(), self.weixin_http_client)

	def tearDown(self):
		WeixinMpUserAccessToken.objects.all().delete()

	def test_get_customerized_menu(self):
		#weixin_api.head_img_saver = dummy_head_img_saver
		# result = self.api.create_customerized_menu(self.dummy_post_str)

		# print result

		# result = self.api.get_customerized_menu()

		# print result

		# result = self.api.delete_customerized_menu()

		# assertEqual(result,"{u'errcode': 0, u'errmsg': u'ok'}")
		
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