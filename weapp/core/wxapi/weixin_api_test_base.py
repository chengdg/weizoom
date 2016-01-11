# -*- coding: utf-8 -*-

"""
测试系统中提供的封装了微信api的api接口的基础数据和
共用的方法集

用于验证是否能正确处理微信api的返回结果，满足系统中
api的定义行为预期
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

from weixin.user.models import WeixinMpUser, WeixinMpUserAccessToken
from weixin_api import *
import weixin_api
import weixin_error_codes as errorcodes

fake_response_json_str = '{"errcode":1000, "errmsg":""}'

def dummy_head_img_saver(img_url):
	return img_url

class StubeWeixinHttpClient(object):
	def __init__(self):
		global fake_response_json_str
		self.response_json_str = fake_response_json_str
		self.should_fail = False

	def set_response_json_str(self, response_json_str):
		self.response_json_str =  response_json_str

	def get(self, url):
		if self.should_fail:
			raise ValueError('i am told to be')

		return json.loads(self.response_json_str) 

	def post(self, url, param_dict):
		if self.should_fail:
			raise ValueError('i am told to be')

		return json.loads(self.response_json_str)

	def set_to_fail(self, should_fail):
		self.should_fail = should_fail


class WeixinApiTestCaseBase(unittest.TestCase):
	dummy_access_token_str  = 'dummy_access_token'
	
	def setUp(self):
		WeixinMpUserAccessToken.objects.all().delete()
		self.weixin_http_client = StubeWeixinHttpClient()
		self.weixin_http_client.set_to_fail(False)
		self.api = WeixinApi(self._create_dummy_certified_mpuser_access_token(), self.weixin_http_client)

	def tearDown(self):
		WeixinMpUserAccessToken.objects.all().delete()

	def _assert_error_response_eqaul(self, errcode, errmsg, error_response):
		self.assertEqual(errcode, error_response.errcode)
		self.assertEqual(errmsg, error_response.errmsg)			

	def _create_dummy_certified_mpuser_access_token(self):
		return WeixinMpUserAccessToken.objects.create(
			mpuser = self._create_dummy_mpuser(),
			app_id = '-',
			app_secret = '-',
			access_token = self.dummy_access_token_str,
			created_at = '2001-01-01 00:00:00',
			is_certified = True,
			is_service = True
			)

	def _create_dummy_mpuser(self):
		return WeixinMpUser.objects.create(
			owner = test_env.getTestUser(),
			username = 'dummy_user_name',
			password = 'dummy_password',
			expire_time = '2001-01-01'
			)