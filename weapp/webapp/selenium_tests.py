# -*- coding: utf-8 -*-

import unittest
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.chrome.options import Options

from django.contrib.auth.models import User, Group

from account.models import *
from test import helper
from account.pageobject.login_page import LoginPage
from test.pageobject.page_frame import PageFrame
from webapp.models import *
from webapp.pageobject.account_list_page import AccountListPage
from account.pageobject.account_info_page import AccountInfoPage


class TestWebApp(helper.FunctionFilterMixin, unittest.TestCase):
	def setUp(self):
		#ff_profile = FirefoxProfile()
		#ff_profile.set_preference("webdriver_enable_native_events", False)
		#self.driver = webdriver.Firefox()
		chrome_options = Options()
		chrome_options.add_argument("--disable-extensions")
		self.driver = webdriver.Chrome(chrome_options=chrome_options)
		self.driver.implicitly_wait(3)

	def tearDown(self):
		page_frame = PageFrame(self.driver)
		page_frame.logout()
		self.driver.quit()

	#==============================================================================
	# test_01_account: 测试账号
	#==============================================================================
	@helper.register('account')
	def test_01_account(self):
		login_page = LoginPage(self.driver)
		login_page.login('manager', 'test')

		account_list_page = AccountListPage(self.driver)
		account_list_page.load()

		'''
		添加账号
		'''
		#添加账号test1
		account_list_page.add_user('test1', 'test1')
		account_list_page.add_webapp_modules_for_last_user()
		#添加账号test2
		account_list_page.add_user('test2', 'test2')
		#添加账号test3
		account_list_page.add_user('test3', 'test3')

		accounts = account_list_page.get_accounts()
		self.assertEquals(3, len(accounts))
		#验证第一个account: test1
		account = accounts[0]
		self.assertEquals('test1', account['name'])
		self.assertEquals(4, len(account['modules']))
		self.assertTrue(u'文章管理' in account['modules'])
		self.assertTrue(u'微商城' in account['modules'])
		self.assertTrue(u'用户中心' in account['modules'])
		self.assertTrue(u'首页' in account['modules'])
		#验证第二个account: test2
		account = accounts[1]
		self.assertEquals('test2', account['name'])
		self.assertEquals(0, len(account['modules']))
		#验证第三个account: test3
		account = accounts[2]
		self.assertEquals('test3', account['name'])
		self.assertEquals(0, len(account['modules']))

		'''
		删除账号
		'''
		account_list_page.delete_user('test2')
		accounts = account_list_page.get_accounts()
		self.assertEquals(2, len(accounts))
		#验证第一个account: test1
		account = accounts[0]
		self.assertEquals('test1', account['name'])
		self.assertEquals(4, len(account['modules']))
		self.assertTrue(u'文章管理' in account['modules'])
		self.assertTrue(u'微商城' in account['modules'])
		self.assertTrue(u'用户中心' in account['modules'])
		self.assertTrue(u'首页' in account['modules'])
		#验证第二个account: test3
		account = accounts[1]
		self.assertEquals('test3', account['name'])
		self.assertEquals(0, len(account['modules']))

		time.sleep(1)

	#==============================================================================
	# test_02_bind_account: 测试绑定微信公众号
	#==============================================================================
	@helper.register('bind_account')
	def test_02_bind_account(self):
		login_page = LoginPage(self.driver)
		login_page.login('test1', 'test1')

		account_info_page = AccountInfoPage(self.driver)
		self.assertTrue(account_info_page.is_account_info_page())
		self.assertFalse(account_info_page.is_account_binded())

		account_info_page.bind_account('test1')
		self.driver.refresh()
		self.assertTrue(account_info_page.is_account_binded())
		time.sleep(5)


def init():
	print 'init db environment for mall'
	UserProfile.objects.filter(user_id__gt=2).delete()	
	User.objects.filter(id__gt=2).delete()

	Project.objects.filter(owner_id__gt=2).delete()
	Workspace.objects.filter(owner_id__gt=2).delete()
	

def clear():
	print 'clear db environment for mall'


TestClass = TestWebApp
def suite(group='all'):
	if group == 'all':
		suite = unittest.makeSuite(TestClass, 'test')
	else:
		suite = unittest.TestSuite()
		for function in TestClass.filter_function_by_group(group):
			suite.addTest(TestClass(function))
		
	return suite

if __name__ == "__main__":
	unittest.main()