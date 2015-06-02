# -*- coding: utf-8 -*-

__author__ = 'chuter'

import sys
import unittest

if __name__ == '__main__':
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

	from test import test_env_with_db as test_env

from django.test.client import RequestFactory

from url_helper import *


class UrlHelperTestCase(unittest.TestCase):
	def setUp(self):
		self.factory = RequestFactory()

	def test_get_request_url_complete_with_empty_params(self):
		url = complete_get_request_url('http', 'api.weixin.qq.com', 'cgi-bin/user/info')
		expected_url = 'http://api.weixin.qq.com/cgi-bin/user/info'
		self.assertEqual(expected_url, url)

	def test_get_request_url_complete_with_en_params(self):
		url = complete_get_request_url('http', 'api.weixin.qq.com', 'cgi-bin/user/info',
			 {'access_token':'ACCESS_TOKEN'})
		expected_url = 'http://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN'
		self.assertEqual(expected_url, url)

	def test_get_request_url_complete_with_zh_params(self):
		url = complete_get_request_url('http', 'api.weixin.qq.com', 'cgi-bin/user/info',
			 {'name':'无名'})
		expected_url = 'http://api.weixin.qq.com/cgi-bin/user/info?name=%E6%97%A0%E5%90%8D'
		self.assertEqual(expected_url, url)

	def test_querystr_filed_remove_from_request_url_when_with_no_querystr(self):
		request = self.factory.get('/')
		new_url = remove_querystr_filed_from_request_url(request, 'k')

		expected_url = '/'
		self.assertEqual(expected_url, new_url)

	def test_querystr_filed_remove_from_request_url_when_with_one_query(self):
		request = self.factory.get('/?k=v')
		new_url = remove_querystr_filed_from_request_url(request, 'k')

		expected_url = '/'
		self.assertEqual(expected_url, new_url)

	def test_querystr_filed_remove_from_request_url_when_with_multi_diffrent_query(self):
		request = self.factory.get('/?k2=v2&k=v&k1=v1')
		new_url = remove_querystr_filed_from_request_url(request, 'k')

		expected_url = '/?k2=v2&k1=v1'
		self.assertEqual(expected_url, new_url)

	def test_querystr_filed_remove_from_request_url_when_with_multi_same_query(self):
		request = self.factory.get('/?k=v&k=v&k=v')
		new_url = remove_querystr_filed_from_request_url(request, 'k')

		expected_url = '/'
		self.assertEqual(expected_url, new_url)


if __name__ == '__main__':
	unittest.main()
