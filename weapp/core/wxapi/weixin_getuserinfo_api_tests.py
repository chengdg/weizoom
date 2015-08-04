# -*- coding: utf-8 -*-

"""
测试获取微信用户基本信息接口
"""

__author__ = 'chuter'

if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from test import test_env_with_db as test_env

from weixin_api_test_base import *

class WeixinApiTestCaseBase(WeixinApiTestCaseBase):

	def test_userinfo_get_with_error_response(self):
		weixin_api.head_img_saver = dummy_head_img_saver
		#测试在微信api有错误的情况下获取用户api的行为
		response_json_str = """{"errcode":1000, "errmsg":"i am told to be"}"""
		self.weixin_http_client.set_response_json_str(response_json_str)

		try:
			self.api.get_user_info('dummy_open_id')
			self.fail()
		except WeixinApiError, cause:
			error_response = cause.error_response
			self._assert_error_response_eqaul(1000, 'i am told to be', error_response)

	def test_userinfo_get_with_system_error(self):
		weixin_api.head_img_saver = dummy_head_img_saver
		#测试在微信api有错误的情况下获取用户api的行为
		self.weixin_http_client.set_to_fail(True)

		try:
			self.api.get_user_info('dummy_open_id')
			self.fail()
		except WeixinApiError, cause:
			error_response = cause.error_response
			self.assertEqual(errorcodes.SYSTEM_ERROR_CODE, error_response.errcode)

	def test_userinfo_get_without_error_response(self):
		#测试在微信api返回正确用户信息情况下api的行为
		response_json_str = """
		{
		    "subscribe": 1, 
		    "openid": "o6_bmjrPTlm6_2sgVt7hMZOPfL2M", 
		    "nickname": "Band", 
		    "sex": 1, 
		    "language": "zh_CN", 
		    "city": "广州", 
		    "province": "广东", 
		    "country": "中国", 
		    "headimgurl":    "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0", 
		    "subscribe_time": 1382694957
		}
		"""
		self.weixin_http_client.set_response_json_str(response_json_str)

		userinfo = self.api.get_user_info('dummy_open_id')
		self._assert_userinfo_equal(response_json_str, userinfo)

	def _assert_userinfo_equal(self, user_json_str, userinfo):
		user_json = json.loads(user_json_str)

		self.assertEqual(user_json['subscribe'], userinfo.subscribe)
		self.assertEqual(user_json['openid'], userinfo.openid)
		self.assertEqual(user_json['nickname'], userinfo.nickname)
		self.assertEqual(user_json['sex'], userinfo.sex)
		self.assertEqual(user_json['language'], userinfo.language)
		self.assertEqual(user_json['city'], userinfo.city)
		self.assertEqual(user_json['province'], userinfo.province)
		self.assertEqual(user_json['country'], userinfo.country)
		self.assertEqual(user_json['headimgurl'], userinfo.headimgurl)
		self.assertEqual(user_json['subscribe_time'], userinfo.subscribe_time)

	def _assert_error_response_eqaul(self, errcode, errmsg, error_response):
		self.assertEqual(errcode, error_response.errcode)
		self.assertEqual(errmsg, error_response.errmsg)			

if __name__ == '__main__':
	test_env.start_test_withdb()