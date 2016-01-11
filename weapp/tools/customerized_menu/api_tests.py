# -*- coding: utf-8 -*-

__author__ = 'chuter'


"""Unit tests for customerized menu api.

These tests make sure the message handling works as it should. """


if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')
	sys.path.insert(0, './')

from test import test_env_with_db as test_env

import unittest
import settings as menu_settings
from datetime import datetime

from tools.customerized_menu.views import create_customerized_menu, delete_customerized_menu, update_customerized_menu
import tools.customerized_menu.views as menu_view

from core.jsonresponse import decode_json_str

def stub_send_notify(notify_type, msg, extra):
	pass

class MockWeixinMenuRequest(object):
	def __init__(self):
		self.is_to_failed = False
		self.request_url = None
		self.menu_json = None

	def set_to_failed(self, is_to_failed):
		self.is_to_failed = is_to_failed

	def do_weixin_menu_create_request(self, request_url, menu_json):
		self.request_url = request_url
		self.menu_json = menu_json

		if self.is_to_failed:
			return u'{"errcode":-1,"errmsg":"系统繁忙"}'
		else:
			return u'{"errcode":0,"errmsg":"ok"}'

	def do_weixin_menu_delete_request(self, request_url):
		self.request_url = request_url
		
		if self.is_to_failed:
			return u'{"errcode":-1,"errmsg":"系统繁忙"}'
		else:
			return u'{"errcode":0,"errmsg":"ok"}'

from django.test.client import RequestFactory

from weixin.user.models import WeixinMpUserAccessToken, WeixinMpUser

class CustomerizedMenuApiTest(unittest.TestCase):
	fake_access_token = 'dummy_token'
	fake_menu_json_str = u"""
		{
		     "button":[
		     {	
		          "type":"click",
		          "name":"今日歌曲",
		          "key":"V1001_TODAY_MUSIC"
		      },
		      {
		           "type":"click",
		           "name":"歌手简介",
		           "key":"V1001_TODAY_SINGER"
		      },
		      {
		           "name":"菜单",
		           "sub_button":[
		           {	
		               "type":"view",
		               "name":"搜索",
		               "url":"http://www.soso.com/"
		            },
		            {
		               "type":"view",
		               "name":"视频",
		               "url":"http://v.qq.com/"
		            },
		            {
		               "type":"click",
		               "name":"赞一下我们",
		               "key":"V1001_GOOD"
		            }]
		       }]
		 }
		"""

	def setUp(self):
		menu_view.weixin_menu_request = MockWeixinMenuRequest()
		menu_view.notify_send_func = stub_send_notify

		self.factory = RequestFactory()
		self.test_user = test_env.getTestUserProfile().user
		WeixinMpUser.objects.all().delete()
		WeixinMpUserAccessToken.objects.all().delete()

		self._create_test_weixin_user_access_token()

	def _create_test_weixin_user_access_token(self):
		WeixinMpUser.objects.create(
			owner = self.test_user,
			username = self.test_user.username,
			password = '-',
			access_token = '-',
			fakeid = '-',
			expire_time = '2001-01-01 00:00:00'
			)
		WeixinMpUserAccessToken.objects.create(
			username = self.test_user.username,
			app_id = '-',
			app_secret = '-',
			access_token = self.fake_access_token,
			created_at = '2001-01-01 00:00:00'
			)

	def testMenuCreateWithoudError(self):
		request = self.factory.post('/tools/api/customerized_menu/create',
			{"menu_json" : self.fake_menu_json_str})
		request.user = self.test_user

		response = create_customerized_menu(request)

		#验证向微信平台请求的请求信息正确
		self.assertEqual("{}/create?access_token={}".format(
			menu_settings.WEIXIN_MP_CUSTOMERIZED_MENU_REQUEST_URL_PREFIX, self.fake_access_token), menu_view.weixin_menu_request.request_url)
		self.assertEqual(self.fake_menu_json_str, menu_view.weixin_menu_request.menu_json)

		#验证api返回response的code为200
		response_json = decode_json_str(response.content)
		self.assertEqual(200, response_json['code'])

	def testMenuCreateWithError(self):
		menu_view.weixin_menu_request.set_to_failed(True)

		request = self.factory.post('/tools/api/customerized_menu/create',
			{"menu_json" : self.fake_menu_json_str})
		request.user = self.test_user

		response = create_customerized_menu(request)

		#验证api返回response的code为500
		response_json = decode_json_str(response.content)
		self.assertEqual(500, response_json['code'])

	def testMenuDeleteWithoudError(self):
		request = self.factory.post('/tools/api/customerized_menu/delete')
		request.user = self.test_user

		response = delete_customerized_menu(request)

		#验证向微信平台请求的请求信息正确
		self.assertEqual("{}/delete?access_token={}".format(
			menu_settings.WEIXIN_MP_CUSTOMERIZED_MENU_REQUEST_URL_PREFIX, self.fake_access_token), menu_view.weixin_menu_request.request_url)

		#验证api返回response的code为200
		response_json = decode_json_str(response.content)
		self.assertEqual(200, response_json['code'])

	def testMenuDeleteWithError(self):
		menu_view.weixin_menu_request.set_to_failed(True)

		request = self.factory.post('/tools/api/customerized_menu/delete')
		request.user = self.test_user

		response = delete_customerized_menu(request)

		#验证api返回response的code为500
		response_json = decode_json_str(response.content)
		self.assertEqual(500, response_json['code'])

	def testMenuUpdateWithoudError(self):
		request = self.factory.post('/tools/api/customerized_menu/update',
			{"menu_json" : self.fake_menu_json_str})
		request.user = self.test_user

		response = update_customerized_menu(request)

		#验证向微信平台请求的请求信息正确, 由于更新操作会先删除然后重新创建，因此
		#最后一次请求是针对创建操作的
		self.assertEqual("{}/create?access_token={}".format(
			menu_settings.WEIXIN_MP_CUSTOMERIZED_MENU_REQUEST_URL_PREFIX, self.fake_access_token), menu_view.weixin_menu_request.request_url)
		self.assertEqual(self.fake_menu_json_str, menu_view.weixin_menu_request.menu_json)

		#验证api返回response的code为200
		response_json = decode_json_str(response.content)
		self.assertEqual(200, response_json['code'])

	def testMenuCreateWithError(self):
		menu_view.weixin_menu_request.set_to_failed(True)

		request = self.factory.post('/tools/api/customerized_menu/create',
			{"menu_json" : self.fake_menu_json_str})
		request.user = self.test_user

		response = update_customerized_menu(request)

		#验证向微信平台请求的请求信息正确，由于更新操作会先进行删除操作，因此
		#最后一次请求是针对删除操作的
		self.assertEqual("{}/delete?access_token={}".format(
			menu_settings.WEIXIN_MP_CUSTOMERIZED_MENU_REQUEST_URL_PREFIX, self.fake_access_token), menu_view.weixin_menu_request.request_url)

		#验证api返回response的code为500
		response_json = decode_json_str(response.content)
		self.assertEqual(500, response_json['code'])

if __name__ == '__main__':
	test_env.init()
	test_env.start_test_withdb()