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

import integral
from integral import *
from visit_session_util import record_shared_page_visit, get_request_path_digest

from models import MemberSharedUrlInfo, MemberClickedUrl, AnonymousClickedUrl

def stube_whether_buyed_checker_always_return_false(wxsid):
	return False

def stube_whether_buyed_checker_always_return_true(wxsid):
	return True

class IntegralCaculatorTestCase(unittest.TestCase):
	dummy_token = 'dummy_token'
	dummy_username = 'dummy_username'
	dummy_shop_name = '3120'

	def setUp(self):
		MemberClickedUrl.objects.all().delete()
		AnonymousClickedUrl.objects.all().delete()

		self.factory = RequestFactory()
		self._update_test_user_profile_shop_name(self.dummy_shop_name)

		self.dummy_weixin_user_token = self._create_dummy_weixin_user_token(self.dummy_token, self.dummy_username)
		self.dummy_member = self._create_dummy_member(self.dummy_weixin_user_token)
		self.dummy_integral_strategy_settings = self._create_dummy_integral_strategy_settings(self.dummy_member)

	def tearDown(self):
		#rollback the db
		MemberClickedUrl.objects.all().delete()
		AnonymousClickedUrl.objects.all().delete()

		self.dummy_weixin_user_token.delete()
		self.dummy_member.delete()
		self.dummy_integral_strategy_settings.delete()

	def test_integral_increase_for_be_member_first(self):
		request = self.factory.get('/')
		request.user_profile = test_env.getTestUserProfile()

		increase_for_be_member_first(request, self.dummy_member)

		new_dummy_member = Member.objects.get(id=self.dummy_member.id)
		self.assertEqual(self.dummy_integral_strategy_settings.be_member_increase_count, new_dummy_member.integral)

	def test_integral_increase_for_click_shared_url_by_author_itself(self):
		#测试在分享者自己点击自己分享的链接的积分计算
		request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_token
		request.user_profile = test_env.getTestUserProfile()

		increase_for_click_shared_url(request)

		new_dummy_member = self._reload_member(self.dummy_member)
		
		#结果应该是分享者的积分不变
		self._assert_member_integral_equal(self.dummy_member, new_dummy_member)

	def test_integral_increase_for_click_shared_url_without_followd_wxsid(self):
		request = self.factory.get('/')
		request.user_profile = test_env.getTestUserProfile()

		increase_for_click_shared_url(request)

		new_dummy_member = self._reload_member(self.dummy_member)
		self._assert_member_integral_equal(self.dummy_member, new_dummy_member)

	def test_integral_increase_for_click_shared_url_with_author_didnot_buyed(self):
		integral.is_buyed_querier = stube_whether_buyed_checker_always_return_false
		request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		request.user_profile = test_env.getTestUserProfile()

		increase_for_click_shared_url(request)

		new_dummy_member = self._reload_member(self.dummy_member)

		#结果应该是分享者积分增加self.dummy_integral_strategy_settings.click_shared_url_increase_count_before_buy
		self.assertEqual(self.dummy_integral_strategy_settings.click_shared_url_increase_count_before_buy, new_dummy_member.integral)

	def test_integral_increase_for_click_shared_url_with_author_buyed_and_fist_visit(self):
		integral.is_buyed_querier = stube_whether_buyed_checker_always_return_true
		request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		request.user_profile = test_env.getTestUserProfile()

		increase_for_click_shared_url(request)

		new_dummy_member = self._reload_member(self.dummy_member)

		#结果应该是分享者积分增加self.dummy_integral_strategy_settings.click_shared_url_increase_count_after_buy
		self.assertEqual(self.dummy_integral_strategy_settings.click_shared_url_increase_count_after_buy, new_dummy_member.integral)

	def test_integral_increase_for_click_shared_url_with_author_buyed_and_has_visit_by_uuid(self):
		integral.is_buyed_querier = stube_whether_buyed_checker_always_return_true
		request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		request.COOKIES[settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_token
		request.COOKIES[settings.NON_WEIXIN_USER_COOKIE_UUID_FILED] = 'dummy_uuid'
		request.user_profile = test_env.getTestUserProfile()

		#该用户已经访问过当前请求的页面
		record_shared_page_visit(request)

		increase_for_click_shared_url(request)

		new_dummy_member = self._reload_member(self.dummy_member)

		#结果应该是分享者的积分不变
		self._assert_member_integral_equal(self.dummy_member, new_dummy_member)

	def test_integral_increase_for_click_shared_url_with_author_buyed_and_has_visit_by_wxsid(self):
		integral.is_buyed_querier = stube_whether_buyed_checker_always_return_true
		request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		request.COOKIES[settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_token
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = 'dummy_wxsid'
		request.user_profile = test_env.getTestUserProfile()

		#该用户已经访问过当前请求的页面
		record_shared_page_visit(request)

		increase_for_click_shared_url(request)

		new_dummy_member = self._reload_member(self.dummy_member)

		#结果应该是分享者的积分不变
		self._assert_member_integral_equal(self.dummy_member, new_dummy_member)

	def test_integral_increase_for_buy_via_shared_url_buyed_by_author_itself(self):
		#测试分享者自己通过自己分享的链接进行购买的积分计算
		request = self.factory.get("/")
		request.COOKIES[settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_token
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_token
		request.user_profile = test_env.getTestUserProfile()

		increase_for_buy_via_shared_url(request)

		new_dummy_member = self._reload_member(self.dummy_member)

		#结果应该是分享者的积分不变
		self._assert_member_integral_equal(self.dummy_member, new_dummy_member)

	def test_integral_increase_for_buy_via_shared_url(self):
		dummy_buyer_wxsid = 'dummy_buyer'
		dummy_buyer_weixin_user_token = self._create_dummy_weixin_user_token(dummy_buyer_wxsid, 'dummy_buyer')
		dummy_buyer_member = self._create_dummy_member(dummy_buyer_weixin_user_token)

		request = self.factory.get("/")
		request.COOKIES[settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_token
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = dummy_buyer_wxsid
		request.user_profile = test_env.getTestUserProfile()

		increase_for_buy_via_shared_url(request)

		new_author_member = self._reload_member(self.dummy_member)
		new_buyer_member = self._reload_member(dummy_buyer_member)

		#结果应该是:
		#分享者的积分增加self.dummy_integral_strategy_settings.buy_via_shared_url_increase_count_for_author
		#购买者的积分增加self.dummy_integral_strategy_settings.buy_via_shared_url_increase_count_for_buyer
		self.assertEqual(self.dummy_integral_strategy_settings.buy_via_shared_url_increase_count_for_author, new_author_member.integral)
		self.assertEqual(self.dummy_integral_strategy_settings.buy_via_shared_url_increase_count_for_buyer, new_buyer_member.integral)

		#rollback the db
		dummy_buyer_weixin_user_token.delete()
		dummy_buyer_member.delete()

	#测试在第一种情况下对分享链接被访问时对跳转的处理:
	#即如果cookie携带当前微信用户的session(假设为b)信息，但是和url中携带的session
    #信息(假设为a)不同，那么进行跳转(url中fwxsid改为b)
	def test_shared_url_request_process_first_case_for_redirect(self):
		dummy_buyer_wxsid = 'dummy_buyer'
		dummy_buyer_weixin_user_token = self._create_dummy_weixin_user_token(dummy_buyer_wxsid, 'dummy_buyer')
		dummy_buyer_member = self._create_dummy_member(dummy_buyer_weixin_user_token)

		try:
			#请求url中仅包含fwxsid参数
			request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
			request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = dummy_buyer_wxsid
			request.user_profile = test_env.getTestUserProfile()

			response = process_shared_url_request(request)
			new_url = response.get('Location')

			expected_new_url = "/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, dummy_buyer_wxsid)
			self.assertEqual(expected_new_url, new_url)

			#请求url中包含除了fwxsid之外的其他参数
			request = self.factory.get("/?{}={}&k=v".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
			request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = dummy_buyer_wxsid
			request.user_profile = test_env.getTestUserProfile()

			response = process_shared_url_request(request)
			new_url = response.get('Location')

			expected_new_url = "/?{}={}&k=v".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, dummy_buyer_wxsid)
			self.assertEqual(expected_new_url, new_url)

			request = self.factory.get("/?k=v&{}={}&k=v".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
			request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = dummy_buyer_wxsid
			request.user_profile = test_env.getTestUserProfile()

			response = process_shared_url_request(request)
			new_url = response.get('Location')

			expected_new_url = "/?k=v&{}={}&k=v".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, dummy_buyer_wxsid)
			self.assertEqual(expected_new_url, new_url)
		finally:
			#rollback the db
			dummy_buyer_weixin_user_token.delete()
			dummy_buyer_member.delete()

	#测试在第一种情况下对分享链接被访问时对积分的计算:
	#即如果cookie携带当前微信用户的session(假设为b)信息，但是和url中携带的session
    #信息(假设为a)不同，假设分享者已经购买，测试对分享者积分的计算
	def test_shared_url_request_process_first_case_for_integral_caculate(self):
		integral.is_buyed_querier = stube_whether_buyed_checker_always_return_true

		dummy_buyer_wxsid = 'dummy_buyer'
		dummy_buyer_weixin_user_token = self._create_dummy_weixin_user_token(dummy_buyer_wxsid, 'dummy_buyer')
		dummy_buyer_member = self._create_dummy_member(dummy_buyer_weixin_user_token)

		try:
			request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
			request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = dummy_buyer_wxsid
			request.user_profile = test_env.getTestUserProfile()

			response = process_shared_url_request(request)

			new_dummy_member = self._reload_member(self.dummy_member)
			self.assertEqual(self.dummy_integral_strategy_settings.click_shared_url_increase_count_after_buy, new_dummy_member.integral)
		finally:
			#rollback the db
			dummy_buyer_weixin_user_token.delete()
			dummy_buyer_member.delete()

	def _assert_equal_redirect_to_with_fwxsid_and_uuid_cookie(self, expected_new_url, expected_fwxsid_cookie, response):
		new_url = response.get('Location')
		self.assertEqual(expected_new_url, new_url)
		followed_wxsid_cookie = response.cookies[settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED].value
		self.assertEqual(expected_fwxsid_cookie, followed_wxsid_cookie)
		uuid_cookie = response.cookies[settings.NON_WEIXIN_USER_COOKIE_UUID_FILED].value
		self.assertTrue(len(uuid_cookie) > 0)

	def test_shared_url_request_process_without_followed_wxsid(self):
		#请求url中仅包含fwxsid参数
		request = self.factory.get("/")
		response = process_shared_url_request(request)
		self.assertEqual(None, response)
	
	#测试在第二种情况下对分享链接被访问时的处理:
	#即如果cookie中携带当前微信用户的session(假设为a)信息，但是和url中携带的session
    #信息(假设为a)相同，那么不进行任何任何操作
	def test_shared_url_request_process_second_case(self):
		#请求url中仅包含fwxsid参数
		request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_token

		response = process_shared_url_request(request)
		self.assertEqual(None, response)

	#测试在第三种情况下对分享链接被访问时对跳转处理:
	#测试跳转链接和cookie设置的处理
	def test_shared_url_request_process_third_case_for_redirect_process(self):
		#请求url中仅包含fwxsid参数
		request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		request.user_profile = test_env.getTestUserProfile()
		response = process_shared_url_request(request)
		self._assert_equal_redirect_to_with_fwxsid_and_uuid_cookie('/', self.dummy_token, response)

		#请求url中包含除了fwxsid之外的其他参数
		request = self.factory.get("/?{}={}&k=v".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		request.user_profile = test_env.getTestUserProfile()

		response = process_shared_url_request(request)
		self._assert_equal_redirect_to_with_fwxsid_and_uuid_cookie('/?k=v', self.dummy_token, response)

		request = self.factory.get("/?k=v&{}={}&k=v".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		request.user_profile = test_env.getTestUserProfile()

		response = process_shared_url_request(request)
		self._assert_equal_redirect_to_with_fwxsid_and_uuid_cookie('/?k=v&k=v', self.dummy_token, response)

	#测试在第三种情况下对分享链接被访问时对积分的计算:
	#即请求中不携带当前微信用户的session信息
	#
	#cookie中有分享者的session信息，且与url中携带的分享者session信息相同，
	#此时分享者的积分不变，只是发生跳转
	def test_shared_url_request_process_third_case_with_shared_session_in_cookie_and_same_with_from_url(self):
		request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		request.COOKIES[settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_token
		request.user_profile = test_env.getTestUserProfile()

		response = process_shared_url_request(request)

		new_dummy_member = self._reload_member(self.dummy_member)

		#结果应该是分享者的积分不变, 仅发生url跳转
		self._assert_member_integral_equal(self.dummy_member, new_dummy_member)

	#测试在第三种情况下对分享链接被访问时对积分的计算:
	#即请求中不携带当前微信用户的session信息
	#
	#cookie中有分享者的session信息，且与url中携带的分享者session信息相同，
	#此时分享者的积分不变，只是发生跳转
	def test_shared_url_request_process_third_case_with_shared_session_in_cookie_and_notsame_with_from_url(self):
		integral.is_buyed_querier = stube_whether_buyed_checker_always_return_true
		request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		request.COOKIES[settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED] = 'balabala'
		request.COOKIES[settings.NON_WEIXIN_USER_COOKIE_UUID_FILED] = 'dummy_uuid'
		request.user_profile = test_env.getTestUserProfile()

		response = process_shared_url_request(request)

		new_dummy_member = self._reload_member(self.dummy_member)

		#结果应该是分享者的积分增加, 且发生url跳转，同时cookie中uuid信息不变
		self.assertEqual(self.dummy_integral_strategy_settings.click_shared_url_increase_count_after_buy, new_dummy_member.integral)

		expected_uuid_cookie = response.cookies[settings.NON_WEIXIN_USER_COOKIE_UUID_FILED].value
		self.assertTrue('dummy_uuid', expected_uuid_cookie)

	#测试在第三种情况下对分享链接被访问时对积分的计算:
	#即请求中不携带当前微信用户的session信息
	#
	#cookie中没有分享者的session信息，进行积分计算，同时在cookie中设置uuid和
	#分享者的session信息
	def test_shared_url_request_process_third_case_with_shared_session_in_cookie_and_notsame_with_from_url(self):
		integral.is_buyed_querier = stube_whether_buyed_checker_always_return_true
		request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		request.user_profile = test_env.getTestUserProfile()

		response = process_shared_url_request(request)

		new_dummy_member = self._reload_member(self.dummy_member)

		#结果应该是分享者的积分增加
		self.assertEqual(self.dummy_integral_strategy_settings.click_shared_url_increase_count_after_buy, new_dummy_member.integral)

	def test_shared_url_request_process_without_followed_wxsid(self):
		dummy_buyer_wxsid = 'dummy_buyer'
		dummy_buyer_weixin_user_token = self._create_dummy_weixin_user_token(dummy_buyer_wxsid, 'dummy_buyer')
		dummy_buyer_member = self._create_dummy_member(dummy_buyer_weixin_user_token)

		request = self.factory.get("/")
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = dummy_buyer_wxsid

		response = process_shared_url_request(request)

		#当连接中不携带分享者信息时不进行处理
		self.assertEqual(None, response)

	def test_integral_increase_without_userprofile(self):
		request = self.factory.get('/')
		request.user_profile = None

		increase_for_be_member_first(request, self.dummy_member)
		increase_for_click_shared_url(request)
		increase_for_buy_via_shared_url(request)

		new_dummy_member = self._reload_member(self.dummy_member)
		self._assert_member_integral_equal(self.dummy_member, new_dummy_member)

	def test_shared_url_pv_update(self):
		request = self.factory.get("/?{}={}".format(settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, self.dummy_token))
		
		update_shared_url_pv(request)

		shared_url_digest = get_request_path_digest(request)
		shared_url_info = MemberSharedUrlInfo.objects.get(shared_url_digest=shared_url_digest)
		self.assertEqual(1, shared_url_info.pv)

		#rollback the db
		MemberSharedUrlInfo.objects.all().delete()
		
	def _reload_member(self, member):
		return Member.objects.get(id=member.id)

	def _assert_member_integral_equal(self, thismember, thatmember):
		self.assertEqual(thismember.integral, thatmember.integral)

	def _update_test_user_profile_shop_name(self, shop_name):
		test_user_profile = test_env.getTestUserProfile()
		test_user_profile.shop_name = shop_name
		test_user_profile.save()

	def _create_dummy_integral_strategy_settings(self, member):
		return IntegralStrategySttings.objects.create(
				webapp_id = self.dummy_shop_name
				)

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
			shop = self.dummy_shop_name,
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
