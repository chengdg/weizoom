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

def dummy_head_img_saver(img_url):
	return img_url

class GetUserInfoTestCase(unittest.TestCase):
	dummy_access_token_str  = 'K3DcpkO-otKGniFgfm7TSG0W8qdNhQGU2zV2YHzzni5-q_iEgSgG-qIYorCW85M61lOVjh4z3-C3Zw9QEZtJ-viDI-OsiJFpmCB5qTBrQwdy0I7kJvcFo79BsXRR-bhQUey-NzcUGne9UFlCshJmpQ'

	def setUp(self):
		WeixinMpUserAccessToken.objects.all().delete()
		self.weixin_http_client = WeixinHttpClient()
		self.api = WeixinApi(self._create_dummy_certified_mpuser_access_token(), self.weixin_http_client)

	def tearDown(self):
		WeixinMpUserAccessToken.objects.all().delete()

	def test_userinfo_get(self):
		#weixin_api.head_img_saver = dummy_head_img_saver

		result = self.api.get_user_info('oR3uquP43phGnoBZoAakpXuo6meY')
		# excepted_url_parts = [
		# 	"{}://{}/cgi-bin/user/info?".format(api_settings.WEIXIN_API_PROTOCAL, api_settings.WEIXIN_API_DOMAIN),
		# 	"access_token={}".format(self.dummy_access_token_str),
		# 	"openid=oR3uquP43phGnoBZoAakpXuo6meY"
		# ]

		# request_url = self.weixin_http_client.url
		# self._assert_url_contains(excepted_url_parts, request_url)

	# def test_text_custom_message_send(self):
	# 	self.api.send_custom_msg('dummy_openid', TextCustomMessage(u'测试'))

	# 	expected_param_dict = json.loads(build_custom_message_json_str('dummy_openid', TextCustomMessage(u'测试')))
	# 	self._assert_param_dict_equals(expected_param_dict, self.weixin_http_client.param_dict)

	# def _assert_param_dict_equals(self, dict_this, dict_that):
	# 	self.assertEqual(len(dict_this), len(dict_that))
	# 	for key in dict_this.keys():
	# 		self.assertEqual(dict_this[key], dict_that[key])

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