# -*- coding: utf-8 -*-

__author__ = 'chuter'

"""
该文件在执行manage.py test时会自动装载该app下所有的单元测试

如果在该文件中也有单元测试，可直接追加load_testsuits_from_app
获取到的TestSuite中

例如：

class TestCase1(TestCase):
    ...

class TestCase2(TestCase):
    ...

import unittest
from django.test import TestCase

from test.app_test_suites_loader import *

test_cases = [
    TestCase1,
    TestCase2,
]

def suite():
    test_suites_in_cur_file = build_test_suite_from(test_cases)
    test_suites_in_all_others = load_testsuits_from_app('cur_app_name')

    test_suites_in_all_others.addTests(test_suites_in_cur_file)
    return test_suites_in_all_others
"""

import unittest
from django.test import TestCase

from test.app_test_suites_loader import *

def suite():
    return load_testsuits_from_app('tools')