# -*- coding: utf-8 -*-

import unittest
import time
import sys
from datetime import datetime

from django.db.models import Q

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.chrome.options import Options

from account.models import *
from test import helper

from account.pageobject.login_page import LoginPage
from webapp.pageobject.template_list_page import TemplateListPage
from test.pageobject.page_frame import PageFrame
from webapp.modules.mall.pageobject.category_list_page import CategoryListPage
from webapp.modules.mall.pageobject.postage_list_page import PostageListPage
from webapp.modules.mall.pageobject.pay_interface_list_page import PayInterfaceListPage
from webapp.modules.mall.pageobject.product_list_page import ProductListPage

from webapp.modules.mall.pageobject.webapp_page.home_page import WAHomePage


class TestCase(helper.FunctionFilterMixin, helper.TestHelperMixin, unittest.TestCase):
	def setUp(self):
		chrome_options = Options()
		chrome_options.add_argument("--disable-extensions")

		test_method = sys._getframe(1).f_locals['testMethod'].__func__.func_name
		if '_webapp' in test_method:
			#如果是webapp，则缩小浏览器窗口
			#chrome_options.add_argument("window-size=400,800")
			pass

		self.driver = webdriver.Chrome(chrome_options=chrome_options)
		self.driver.implicitly_wait(3)
		self.verificationErrors = []

	def tearDown(self):
		page_frame = PageFrame(self.driver)
		page_frame.logout()
		self.driver.quit()

	#==============================================================================
	# test_template: 测试编辑template
	#==============================================================================
	@helper.register('template')
	def test_template(self):
		login_page = LoginPage(self.driver)
		login_page.login('test1', 'test1')

		template_list_page = TemplateListPage(self.driver)
		template_list_page.load()
		self.assertEquals(u'极简主义', template_list_page.get_active_template())
		template_list_page.select_template(u'简单爱')
		self.assertEquals(u'简单爱', template_list_page.get_active_template())
		template_list_page.select_template(u'极简主义') #恢复默认模板

		#编辑模板
		template_list_page.select_template(u'简约风尚') #恢复默认模板
		edit_template_page = template_list_page.edit_template(u'简约风尚')
		edit_template_page.select_nav_targets()






TestClass = TestCase
def suite(group='all'):
	if group == 'all':
		suite = unittest.makeSuite(TestClass, 'test')
	else:
		suite = unittest.TestSuite()
		for function in TestClass.filter_function_by_group(group):
			suite.addTest(TestClass(function))
		
	return suite