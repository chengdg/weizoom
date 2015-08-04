# -*- coding: utf-8 -*-

__author__ = 'chuter'

import sys
import unittest

if __name__ == '__main__':
	sys.path.insert(0, '../')

from test import test_env
test_env.init_test_env_without_db()

import nose2
from nose2.tools import params

from string_util import *

class StringUtilTestCase(unittest.TestCase):

	@params(None, '', 'a', 'ab,d', u'哈')
	def test_nonhex_str_check(self, str):
		self.assertFalse(is_hax_str(str))

	@params('00', 'abcd')
	def test_is_hex_str_check(self, str):
		self.assertTrue(is_hax_str(str))

	@params(None, '', '中文', '中文a中文', 'a')
	def test_byte_and_hex_convert(self, byte):
		self.assertEquals(byte, hex_to_byte(byte_to_hex(byte)))

	@params(u'中文', u'中文a中文', u'aeb')
	def test_byte_and_hex_convert_for_unicode(self, byte):
		self.assertEquals(byte.encode('utf-8'), hex_to_byte(byte_to_hex(byte)))

	@params('00', '0ea4')
	def test_byte_to_hex_str_for_hex_str(self, byte):
		self.assertEquals(byte.encode('utf-8'), byte_to_hex(byte))

	@params(None, '', '-')
	def test_hex_to_byte_str_for_non_hex_str(self, hex_str):
		self.assertEquals(hex_str, hex_to_byte(hex_str))

if __name__ == '__main__':
	test_env.run_test()




