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
		#ff_profile = FirefoxProfile()
		#ff_profile.set_preference("webdriver_enable_native_events", False)
		#self.driver = webdriver.Firefox()
		
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
	# test_postage_config: 测试运费配置
	#==============================================================================
	@helper.register('postage_config')
	def test_01_postage_config(self):
		login_page = LoginPage(self.driver)
		login_page.login('test1', 'test1')

		postage_list_page = PostageListPage(self.driver)
		postage_list_page.load()

		#验证：运费配置列表为[免运费]
		postage_configs = postage_list_page.get_postage_configs()
		self.assertEquals(1, len(postage_configs))
		postage_config = postage_configs[0]
		self.assertEquals(u'免运费', postage_config['name'])
		self.assertEquals(0, len(postage_config['content']))

		#验证：编辑运费配置时提交时的默认提示
		edit_postage_page = postage_list_page.click_add_postage_config_button()
		edit_postage_page.submit()
		error_hints = edit_postage_page.get_error_hints()
		self.assertEquals(3, len(error_hints))
		error_hint = error_hints[0]
		self.assertEquals(u'内容不能为空', error_hint)
		error_hint = error_hints[1]
		self.assertEquals(u"格式不正确，请输入'3.14'或'5'这样的数字", error_hint)
		error_hint = error_hints[2]
		self.assertEquals(u"价格不正确，请输入0-99999之间的价格", error_hint)

		#添加“顺丰”
		edit_postage_page.add_postage_config(u'顺丰', 1.5, 5)
		edit_postage_page.submit()
		#验证：运费配置列表为[免运费，顺丰]
		postage_configs = postage_list_page.get_postage_configs()
		self.assertEquals(2, len(postage_configs))
		postage_config = postage_configs[0]
		self.assertEquals(u'免运费', postage_config['name'])
		self.assertEquals(0, len(postage_config['content']))
		postage_config = postage_configs[1]
		self.assertEquals(u'顺丰', postage_config['name'])
		self.assertEquals(u'首重1.5公斤 【5.0元】， 无续重', postage_config['content'])

		#添加“圆通”，“EMS”
		edit_postage_page = postage_list_page.click_add_postage_config_button()
		edit_postage_page.add_postage_config(u'圆通', 1.5, 10, 1, 1)
		edit_postage_page.submit()
		postage_configs = postage_list_page.get_postage_configs()
		edit_postage_page = postage_list_page.click_add_postage_config_button()
		edit_postage_page.add_postage_config(u'EMS', 1, 1, 1, 0.5)
		edit_postage_page.submit()
		#验证：运费配置列表为[免运费，顺丰，圆通，EMS]
		postage_configs = postage_list_page.get_postage_configs()
		self.assertEquals(4, len(postage_configs))
		postage_config = postage_configs[0]
		self.assertEquals(u'免运费', postage_config['name'])
		self.assertEquals(0, len(postage_config['content']))
		postage_config = postage_configs[1]
		self.assertEquals(u'顺丰', postage_config['name'])
		self.assertEquals(u'首重1.5公斤 【5.0元】， 无续重', postage_config['content'])
		postage_config = postage_configs[2]
		self.assertEquals(u'圆通', postage_config['name'])
		self.assertEquals(u'首重1.5公斤 【10.0元】， 续重1公斤 【1元】', postage_config['content'])
		postage_config = postage_configs[3]
		self.assertEquals(u'EMS', postage_config['name'])
		self.assertEquals(u'首重1.0公斤 【1.0元】， 续重1公斤 【0.5元】', postage_config['content'])
		#验证: “免运费”被选中
		selected_postage_config = postage_list_page.get_selected_postage_config()
		self.assertEquals(u'免运费', selected_postage_config['name'])
		self.assertEquals(0, len(selected_postage_config['content']))

		'''
		选中EMS
		'''
		postage_list_page.select_postage_config(u'EMS')
		time.sleep(3)
		#验证：刷新页面后，选中“EMS”
		self.driver.refresh()
		selected_postage_config = postage_list_page.get_selected_postage_config()
		self.assertEquals(u'EMS', postage_config['name'])
		self.assertEquals(u'首重1.0公斤 【1.0元】， 续重1公斤 【0.5元】', postage_config['content'])

		'''
		编辑EMS
		'''
		edit_postage_page = postage_list_page.enter_edit_postage_config_page(u'EMS')
		edit_postage_page.add_postage_config(u'EMS*', 2, 2)
		edit_postage_page.submit()
		#验证：运费配置更新
		postage_configs = postage_list_page.get_postage_configs()
		self.assertEquals(4, len(postage_configs))
		postage_config = postage_configs[0]
		self.assertEquals(u'免运费', postage_config['name'])
		self.assertEquals(0, len(postage_config['content']))
		postage_config = postage_configs[1]
		self.assertEquals(u'顺丰', postage_config['name'])
		self.assertEquals(u'首重1.5公斤 【5.0元】， 无续重', postage_config['content'])
		postage_config = postage_configs[2]
		self.assertEquals(u'圆通', postage_config['name'])
		self.assertEquals(u'首重1.5公斤 【10.0元】， 续重1公斤 【1元】', postage_config['content'])
		postage_config = postage_configs[3]
		self.assertEquals(u'EMS*', postage_config['name'])
		self.assertEquals(u'首重2.0公斤 【2.0元】， 无续重', postage_config['content'])
		#验证: edit_postage_page中的内容
		#EMS
		edit_postage_page = postage_list_page.enter_edit_postage_config_page(u'EMS*')
		postage_config = edit_postage_page.get_postage_config()
		self.assertEquals(u'EMS*', postage_config['name'])
		self.assertEquals(u'2.0', postage_config['first_weight'])
		self.assertEquals(u'2.0', postage_config['first_weight_price'])
		self.assertFalse(postage_config['is_enable_added_weight'])
		#圆通
		postage_list_page = PostageListPage(self.driver)
		postage_list_page.load()
		edit_postage_page = postage_list_page.enter_edit_postage_config_page(u'圆通')
		postage_config = edit_postage_page.get_postage_config()
		self.assertEquals(u'圆通', postage_config['name'])
		self.assertEquals(u'1.5', postage_config['first_weight'])
		self.assertEquals(u'10.0', postage_config['first_weight_price'])
		self.assertTrue(postage_config['is_enable_added_weight'])
		self.assertEquals(u'1', postage_config['added_weight'])
		self.assertEquals(u'1', postage_config['added_weight_price'])

		'''
		删除“EMS”
		'''
		postage_list_page = PostageListPage(self.driver)
		postage_list_page.load()
		edit_postage_page = postage_list_page.enter_edit_postage_config_page(u'EMS*')
		edit_postage_page.delete()
		postage_configs = postage_list_page.get_postage_configs()
		self.assertEquals(3, len(postage_configs))
		postage_config = postage_configs[0]
		self.assertEquals(u'免运费', postage_config['name'])
		self.assertEquals(0, len(postage_config['content']))
		postage_config = postage_configs[1]
		self.assertEquals(u'顺丰', postage_config['name'])
		self.assertEquals(u'首重1.5公斤 【5.0元】， 无续重', postage_config['content'])
		postage_config = postage_configs[2]
		self.assertEquals(u'圆通', postage_config['name'])
		self.assertEquals(u'首重1.5公斤 【10.0元】， 续重1公斤 【1元】', postage_config['content'])

		time.sleep(1)


	#==============================================================================
	# test_pay_interface: 测试支付方式
	#==============================================================================
	@helper.register('pay_interface')
	def test_02_pay_interface(self):
		login_page = LoginPage(self.driver)
		login_page.login('test1', 'test1')

		pay_interface_list_page = PayInterfaceListPage(self.driver)
		pay_interface_list_page.load()

		#验证：支付接口列表为[]
		pay_interfaces = pay_interface_list_page.get_pay_interfaces()
		self.assertEquals(0, len(pay_interfaces))

		#添加“微信支付”接口
		expected_pay_interface = {
			'type': u'微信支付',
			'name': u'我的微信支付',
			'app_id': '111',
			'partner_id': '222',
			'partner_key': '333',
			'paysign_key': '444'
		}
		edit_pay_interface_page = pay_interface_list_page.click_add_pay_interface_button()
		edit_pay_interface_page.add_weixinpay_interface(expected_pay_interface)
		edit_pay_interface_page.submit()
		#验证：支付接口列表为['我的微信支付']
		pay_interface_list_page = PayInterfaceListPage(self.driver)
		pay_interface_list_page.load()
		pay_interfaces = pay_interface_list_page.get_pay_interfaces()
		self.assertEquals(1, len(pay_interfaces))
		pay_interface = pay_interfaces[0]
		self.assertEquals(u'微信支付', pay_interface['type'])
		self.assertEquals(u'我的微信支付', pay_interface['name'])
		self.assertTrue(pay_interface['is_active'])

		#添加“货到付款”的接口
		expected_pay_interface = {
			'name': u'我的货到付款'
		}
		edit_pay_interface_page = pay_interface_list_page.click_add_pay_interface_button()
		edit_pay_interface_page.add_cod_interface(expected_pay_interface)
		edit_pay_interface_page.submit()
		#验证：支付接口列表为['我的微信支付', '我的货到付款']
		pay_interface_list_page = PayInterfaceListPage(self.driver)
		pay_interface_list_page.load()
		pay_interfaces = pay_interface_list_page.get_pay_interfaces()
		self.assertEquals(2, len(pay_interfaces))
		pay_interface = pay_interfaces[0]
		self.assertEquals(u'微信支付', pay_interface['type'])
		self.assertEquals(u'我的微信支付', pay_interface['name'])
		self.assertTrue(pay_interface['is_active'])
		pay_interface = pay_interfaces[1]
		self.assertEquals(u'货到付款', pay_interface['type'])
		self.assertEquals(u'我的货到付款', pay_interface['name'])
		self.assertTrue(pay_interface['is_active'])

		time.sleep(1)





TestClass = TestCase
def suite(group='all'):
	if group == 'all':
		suite = unittest.makeSuite(TestClass, 'test')
	else:
		suite = unittest.TestSuite()
		for function in TestClass.filter_function_by_group(group):
			suite.addTest(TestClass(function))
		
	return suite