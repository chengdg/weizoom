# -*- coding: utf-8 -*-

__author__ = 'chuter'


import unittest

import os
import sys

from weapp import settings
from test import test_env_with_db as test_env

"""
用于测试消息处理实现的工具包：
其中对测试时需要使用数据库环境进行初始化，测试代码中可直接使用Model进行数据库操作
提供获取用于测试用的账户信息
创建假的消息处理过程中的上下文(包括了进行消息处理时必需的信息)，方便测试

使用示例：

if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from weixin.handler.handler_testutil import *
init_handler_test_env()

...
#your test code
...

if __name__ == '__main__':
	start_test_withdb()
"""

def init_handler_test_env():
	test_env.init()

def getTestUserProfile():
	return test_env.getTestUserProfile()

def createDummyMessageHandlingContext(message, xml_message):
	from weixin.handler.message_handle_context import MessageHandlingContext
	return MessageHandlingContext(message, xml_message, getTestUserProfile())

def start_test_without_db():
	unittest.main()

def start_test_withdb():
	test_env.start_test_withdb()