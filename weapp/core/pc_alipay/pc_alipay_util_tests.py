# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import sys
import unittest

if __name__ == '__main__':
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from test import test_env_with_db as test_env

from account.models import *
from core.pc_alipay.pc_alipay_submit import PCAlipaySubmit
from core.weibo.weibo_access_token import WeiboAccessToken
from core.weibo.weibo_token_info import WeiboTokenInfo
from core.weibo.weibo_user_info import WeiboUserInfo
from core.weibo.weibo_config import WeiboConfig
import urllib
import urllib2
from account.models import UserAlipayOrderConfig


class PCAlipayUtilTest(unittest.TestCase):
	def setUp(self):
		self.user_profile = UserProfile.objects.get(webapp_id='3180')
		try:
			UserAlipayOrderConfig.objects.create(
				owner=self.user_profile.user,
				partner='2088901733939709',
				key='w8z9sfly9yyx59mnsjbzkwnngf0zzc0r',
				seller_email='pay@weizoom.com')
		except:
			pass
		self.request_test = RequestInfo
		self.request_test.user_profile = self.user_profile


	def test_get_pc_alipay_submit_url(self):
		return_url = "http://wx.weizoom.com/m/rice/pay_result/3181/"
		notify_url = "http://wx.weizoom.com/rice/api/pay_result_notify/3181/"
		pay_order = Order
		pay_order.price = 2
		pay_order.number = 3
		pay_order.order_id = 'A00201'
		pc_alipay = PCAlipaySubmit(pay_order, return_url, notify_url, self.user_profile)
		url = pc_alipay.submit()
		print 'test_get_pc_alipay_submit_url'
		print url
		self.assertTrue(True)


class RequestInfo():
	def __init__(self):
		pass

class Order():
	def __init__(self):
		pass

if __name__ == '__main__':
	test_env.start_test_withdb()