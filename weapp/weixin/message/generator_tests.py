# -*- coding: utf-8 -*-

__author__ = 'chuter'

import unittest
import generator

if __name__ == '__main__':
	import os
	import sys
	path = os.path.abspath(os.path.join('.', '..'))
	sys.path.append(path)
	path = os.path.abspath('.')
	sys.path.append(path)

	from viper import settings
	os.environ['DJANGO_SETTINGS_MODULE'] = 'viper.settings'
	settings.DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

from django.conf import settings

class GeneratorTestCase(unittest.TestCase):
	def test_add_token_to_url_with_origurl_endswith_slash(self):
		dummy_token = 'dummy_token'

		#第一种情况，原始url地址以'/'结尾
		orig_url = 'http://wx.weizoom.com/'
		new_url = generator.add_token_to_url(orig_url, dummy_token)
		expected_new_url = u'%s?%s=%s&%s=%s' % (orig_url, settings.WEIXIN_USER_SESSION_KEY_URL_QUERY_FILED,
				dummy_token, settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, dummy_token)
		self.assertEqual(expected_new_url, new_url)

	def test_add_token_to_url_with_origurl_already_contain_querystr(self):
		dummy_token = 'dummy_token'

		#第二种情况，原始url已经有query str
		orig_url = 'http://wx.weizoom.com/?k=v'
		new_url = generator.add_token_to_url(orig_url, dummy_token)
		expected_new_url = u'%s&%s=%s&%s=%s' % (orig_url, settings.WEIXIN_USER_SESSION_KEY_URL_QUERY_FILED,
				dummy_token, settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, dummy_token)
		self.assertEqual(expected_new_url, new_url)

	def test_add_token_to_url_with_origurl_donot_contain_querystr_and_not_endswith_slash(self):
		dummy_token = 'dummy_token'
		
		#第三种情况，原始url没有query str，且不以'/'结尾
		orig_url = 'http://wx.weizoom.com'
		new_url = generator.add_token_to_url(orig_url, dummy_token)
		expected_new_url = u'%s/?%s=%s&%s=%s' % (orig_url, settings.WEIXIN_USER_SESSION_KEY_URL_QUERY_FILED,
				dummy_token, settings.FOLLOWED_WEIXIN_USER_URL_QUERY_FILED, dummy_token)
		self.assertEqual(expected_new_url, new_url)

if __name__ == '__main__':
	unittest.main()

