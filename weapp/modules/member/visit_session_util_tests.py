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

from member.models import AnonymousClickedUrl, MemberClickedUrl
from visit_session_util import *

class VisitSessionUtilTestCase(unittest.TestCase):
	dummy_uuid = 'dummy_uuid'
	dummy_wxsid = 'dummy_wxsid'

	def setUp(self):
		self.factory = RequestFactory()
		MemberClickedUrl.objects.all().delete()
		AnonymousClickedUrl.objects.all().delete()

	def test_page_visit_record_with_uuid(self):
		request = self.factory.get("/a/b/?k=v&{}={}".format(settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED, 'dummy_followed_wxsid'))
		request.COOKIES[settings.NON_WEIXIN_USER_COOKIE_UUID_FILED] = self.dummy_uuid

		record_shared_page_visit(request)

		self.assertTrue(has_visit(request, None, self.dummy_uuid))

	def test_page_visit_record_with_wxsid(self):
		request = self.factory.get("/a/b/?k=v&{}={}".format(settings.FOLLOWED_WEIXIN_USER_SESSION_KEY_FILED, 'dummy_followed_wxsid'))
		request.COOKIES[settings.WEIXIN_USER_SESSION_KEY_FILED] = self.dummy_wxsid

		record_shared_page_visit(request)

		self.assertTrue(has_visit(request, self.dummy_wxsid, None))


if __name__ == '__main__':
	test_env.start_test_withdb()