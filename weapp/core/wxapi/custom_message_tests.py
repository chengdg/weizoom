# -*- coding: utf-8 -*-

__author__ = 'chuter'

import re
import unittest

from custom_message import *

class CustomMessageTestCase(unittest.TestCase):
	def test_text_custom_message_json_str_build(self):
		test_text_custom_message = TextCustomMessage('dummy_content')
		message_json_str = build_custom_message_json_str('dummy_openid', test_text_custom_message)

		expected_json_str = """
		{
			"msgtype" : "text",
			"touser" : "dummy_openid",
			"text" : {
				"content" : "dummy_content"
			}
		}
		"""

		self._assert_json_str_equal(expected_json_str, message_json_str)
		
	def _assert_json_str_equal(self, jsonstr_this, jsonstr_that):
		jsonstr_this = re.sub(r'\s+', '', jsonstr_this)
		jsonstr_that = re.sub(r'\s+', '', jsonstr_that)
		self.assertEqual(jsonstr_this, jsonstr_that)

if __name__ == '__main__':
	unittest.main()


