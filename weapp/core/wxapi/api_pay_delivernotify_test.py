# -*- coding: utf-8 -*-

"""
用于测试与微信api的交互

验证系统中提供的api接口中访问对应微信api接口
时地址是否正确，参数是否正确
"""

__author__ = 'bert'


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
from custom_message import TextCustomMessage
from util import *
from api_pay_delivernotify import *
from core.wxpay.sign import sha1_sign

#from custom_message import TextCustomMessage, build_custom_message_json_str

fake_response_json_str = '{"errcode":0, "errmsg":""}'


class PayDeliverNotifyApiTestCase(unittest.TestCase):
	dummy_access_token_str  = 'DFRAzuxtCBjSRY5HAfs2PyHEk8F34iK22OiB4wALTUrXF10DJkjo-N3Lpkt7OzxD'
	dummy_oppid = 'appid'
	dummy_appkey = 'dummy_appkey'
	dummy_openid = 'ommVKt1I6wUuB0mM3SNjPZfd4mOw'
	dummy_transid = 'dummy_transid'
	dummy_out_trade_no = 'dummy_out_trade_no'
	dummy_deliver_timestamp = '123456789'
	dummy_app_signature = 'app_signature'
	dummy_sign_method = 'dummy_sign_method'
	dummy_deliver_status = 'dummy_deliver_status'
	dummy_deliver_msg = 'dummy_deliver_msg'

	def setUp(self):
		WeixinMpUserAccessToken.objects.all().delete()
		self.weixin_http_client = WeixinHttpClient()
		self.api = WeixinApi(self._create_dummy_certified_mpuser_access_token(), self.weixin_http_client)

	def tearDown(self):
		WeixinMpUserAccessToken.objects.all().delete()

	def test_api_pay_delivernotify(self):
		#weixin_api.head_img_saver = dummy_head_img_saver

		message = PayDeliverMessage(
			self.dummy_oppid,
			self.dummy_appkey,
			self.dummy_openid,
			self.dummy_transid,
			self.dummy_out_trade_no,
			self.dummy_deliver_timestamp,
			self.dummy_deliver_status,
			self.dummy_deliver_msg)
		sha1_sign_str = sha1_sign(self.dummy_oppid, self.dummy_appkey, self.dummy_openid, self.dummy_transid, self.dummy_out_trade_no, self.dummy_deliver_timestamp, self.dummy_deliver_status, self.dummy_deliver_msg)

		self.assertEqual(sha1_sign_str, message.app_signature)	

		post_date = message.get_message_json_str()

		self.assertEqual(post_date,json.dumps({"appid" : self.dummy_oppid, 
			"deliver_timestamp":self.dummy_deliver_timestamp, "openid" : self.dummy_openid, "transid":self.dummy_transid, "out_trade_no":self.dummy_out_trade_no,"app_signature":sha1_sign_str,"sign_method":'sha1',"deliver_status":self.dummy_deliver_status,"deliver_msg":self.dummy_deliver_msg}) )

		result = self.api.create_deliverynotify(message, True)
		

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