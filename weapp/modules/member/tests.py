"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


from test.app_test_suites_loader import *

test_cases = [
	SimpleTest,
]

def suite():
	test_suites_in_cur_file = build_test_suite_from(test_cases)
	test_suites_in_all_others = load_testsuits_from_app('member')

	test_suites_in_all_others.addTests(test_suites_in_cur_file)
	return test_suites_in_all_others