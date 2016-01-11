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

from core.jsonresponse import decode_json_str

from models import *
from message.models import WeixinUser
from account.models import WeixinUserToken

from api_views import get_presented_award

########################################################################
# 积分奖励的单元测试
########################################################################
class IntegralAwardTestCase(unittest.TestCase):
	dummy_wxsid = 'dummy_wxsid'
	dummy_icon = 'dummy_icon'
	dummy_webapp_id = '2013'

	def setUp(self):
		self.factory = RequestFactory()
		Member.objects.all().delete()

		self.test_weixin_user = self._create_dummy_weixin_user(self.dummy_icon, '-')
		self.test_weixin_user_token = self._create_dummy_weixin_user_token(self.dummy_wxsid, '-')
		self.test_member = self._create_dummy_member(self.test_weixin_user_token)
		self.dummy_integral_strategy_settings = self._create_dummy_integral_strategy_settings()

	def tearDown(self):
		#rollback the db
		WeixinUser.objects.all().delete()
		WeixinUserToken.objects.all().delete()
		Member.objects.all().delete()

		self.dummy_integral_strategy_settings.delete()

	def test_presented_award_get_for_gold_award(self):
		request = self.factory.get('/?medal_type={}&mid={}'.format(GOLD_MEDAL_VALUE, self.test_member.id))

		response = get_presented_award(request, self.dummy_webapp_id)
		self._assert_integral_equal_with_increase_by_award(response, self.test_member, self.dummy_integral_strategy_settings.reward_integral_count_for_gold_medal)

	def test_presented_award_get_for_silver_award(self):
		request = self.factory.get('/?medal_type={}&mid={}'.format(SILVER_MEDAL_VALUE, self.test_member.id))

		response = get_presented_award(request, self.dummy_webapp_id)
		self._assert_integral_equal_with_increase_by_award(response, self.test_member, self.dummy_integral_strategy_settings.reward_integral_count_for_silver_medal)

	def test_presented_award_get_for_bronze_award(self):
		request = self.factory.get('/?medal_type={}&mid={}'.format(BRONZE_MEDAL_VALUE, self.test_member.id))

		response = get_presented_award(request, self.dummy_webapp_id)
		self._assert_integral_equal_with_increase_by_award(response, self.test_member, self.dummy_integral_strategy_settings.reward_integral_count_for_bronze_medal)

	def test_presented_award_get_when_lack_param(self):
		request = self.factory.get('/')

		response = get_presented_award(request, self.dummy_webapp_id)
		self._assert_integral_equal_with_increase_by_award(response, self.test_member, 0)		

	def _assert_integral_equal_with_increase_by_award(self, response, member, expected_increase_count):
		latest_member = self._reload_member(self.test_member)

		expected_new_integral = self.test_member.integral + expected_increase_count
		self.assertEqual(expected_new_integral, latest_member.integral)

		response_json = decode_json_str(response.content)
		self.assertEqual(expected_increase_count, response_json['data']['integral_increase_count'])

	def _reload_member(self, member):
		return Member.objects.get(id=member.id)

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
			shop = self.dummy_webapp_id,
			weixin_user_name = username,
			token = token
			)

	def _create_dummy_member(self, weixinuser_token):
		return Member.objects.create(
			wxuser_token = weixinuser_token,
			webapp_id = '-',
			user_icon = '-'
		)

	def _create_dummy_integral_strategy_settings(self):
		return IntegralStrategySttings.objects.create(
			webapp_id = self.dummy_webapp_id
			)


if __name__ == '__main__':
	test_env.start_test_withdb()