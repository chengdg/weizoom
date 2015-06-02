# -*- coding: utf-8 -*-

__author__ = 'chuter'

import sys
import unittest

if __name__ == '__main__':
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

	from test import test_env_with_db as test_env

from django.test.client import RequestFactory
from url_util import get_appid_from_request, APPID_QUERY_STR_KEY

class UrlUtilTestCase(unittest.TestCase):
	def setUp(self):
		self.factory = RequestFactory()

	def test_appid_get_when_url_with_only_appid(self):
		request = self.factory.get("/?{}=123".format(APPID_QUERY_STR_KEY))
		app_id = get_appid_from_request(request)
		self.assertEqual('123', app_id)

	def test_appid_get_when_url_with_appid_and_others(self):
		request = self.factory.get("/?k=v&{}=123&k=v".format(APPID_QUERY_STR_KEY))
		app_id = get_appid_from_request(request)
		self.assertEqual('123', app_id)

	def test_appid_get_when_url_without_appid(self):
		request = self.factory.get("/?k=v&k=v".format(APPID_QUERY_STR_KEY))
		app_id = get_appid_from_request(request)
		self.assertEqual(None, app_id)

if __name__ == '__main__':
	unittest.main()