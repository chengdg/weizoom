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


class TestMall(helper.FunctionFilterMixin, helper.TestHelperMixin, unittest.TestCase):
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
	# test_01_product_category: 测试商品分类
	#==============================================================================
	@helper.register('product_category')
	def not_test_01_product_category(self):
		login_page = LoginPage(self.driver)
		login_page.login('test1', 'test1')

		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()

		#验证：分类列表为空
		categories = category_list_page.get_categories()
		self.assertEquals(0, len(categories))

		#验证：分类编辑页面默认提交的提示
		edit_category_page = category_list_page.click_add_category_button()
		edit_category_page.submit()
		error_hints = edit_category_page.get_error_hints()
		self.assertEquals(1, len(error_hints))
		error_hint = error_hints[0]
		self.assertEquals(u'内容不能为空', error_hint)

		#添加“分类1”
		edit_category_page.add_category(u'分类1')
		edit_category_page.submit()
		#添加“分类2”
		category_list_page = CategoryListPage(self.driver)
		edit_category_page = category_list_page.click_add_category_button()
		edit_category_page.add_category(u'分类2')
		edit_category_page.submit()
		#添加“分类3”
		category_list_page = CategoryListPage(self.driver)
		edit_category_page = category_list_page.click_add_category_button()
		edit_category_page.add_category(u'分类3')
		edit_category_page.submit()
		#验证：分类列表为[分类1，分类2，分类3]
		categories = category_list_page.get_categories()
		self.assertEquals(3, len(categories))
		category = categories[0]
		self.assertEquals(u'分类3', category['name'])		
		self.assertEquals(0, category['product_count'])
		category = categories[1]
		self.assertEquals(u'分类2', category['name'])		
		self.assertEquals(0, category['product_count'])
		category = categories[2]
		self.assertEquals(u'分类1', category['name'])		
		self.assertEquals(0, category['product_count'])		

		#删除“分类2”
		edit_category_page = category_list_page.enter_category_edit_page(u'分类2')
		edit_category_page.delete()
		#验证：分类列表为[分类1，分类3]
		categories = category_list_page.get_categories()
		self.assertEquals(2, len(categories))
		category = categories[0]
		self.assertEquals(u'分类3', categories[0]['name'])		
		self.assertEquals(u'分类1', categories[1]['name'])
		
		#更新“分类1”
		edit_category_page = category_list_page.enter_category_edit_page(u'分类1')
		edit_category_page.add_category(u'新分类1')
		edit_category_page.submit()
		#验证：分类列表为[新分类1，分类3]
		categories = category_list_page.get_categories()
		self.assertEquals(2, len(categories))
		category = categories[0]
		self.assertEquals(u'分类3', categories[0]['name'])		
		self.assertEquals(u'新分类1', categories[1]['name'])

		#验证：“新分类1”编辑页面中出现更新后的内容
		edit_category_page = category_list_page.enter_category_edit_page(u'新分类1')
		self.assertEquals(u'新分类1', edit_category_page.get_category_name())
		time.sleep(1)

	#==============================================================================
	# test_02_postage_config: 测试运费配置
	#==============================================================================
	@helper.register('postage_config')
	def not_test_02_postage_config(self):
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
	# test_03_pay_interface: 测试支付方式
	#==============================================================================
	@helper.register('postage_config')
	def not_test_03_pay_interface(self):
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


	#==============================================================================
	# test_04_product: 测试商品管理
	#==============================================================================
	def __assert_product(self, expected, actual, url2uploaded_url):
		for key in actual:
			if key == 'price':
				self.assertEquals(float(expected[key]), float(actual[key]))
			elif key == 'thumbnails_url':
				uploaded_url = 'http://dev.weapp.com' + url2uploaded_url['thumbnails_url_'+expected['thumbnails_url']]
				self.assertEquals(uploaded_url, actual['thumbnails_url'])
			elif key == 'pic_url':
				uploaded_url = 'http://dev.weapp.com' + url2uploaded_url['pic_url_'+expected['pic_url']]
				self.assertEquals(uploaded_url, actual['pic_url'])
			else:
				self.assertEquals(expected[key], actual[key])

	@helper.register('product')
	def not_test_04_product(self):
		login_page = LoginPage(self.driver)
		login_page.login('test1', 'test1')
		url2uploaded_url = {}

		product_list_page = ProductListPage(self.driver)
		product_list_page.load()

		#验证：商品列表为空
		products = product_list_page.get_products()
		self.assertEquals(0, len(products))

		#期望商品
		expected_products = [{
	        'name': u'东坡肘子',
	        'category': u'新分类1',
	        'physical_unit': u'包',
			'price': '11.0',
			'weight': '5',
			'thumbnails_url': './test/imgs/hangzhou1.jpg',
			'pic_url': './test/imgs/hangzhou1.jpg',
			'introduction': u'东坡肘子的简介',
			'detail': u'东坡肘子的详情'
        }, {
	        'name': u'叫花鸡',
	        'category': u'新分类1',
	        'physical_unit': u'盘',
			'price': '12.0',
			'weight': '5',
			'thumbnails_url': './test/imgs/hangzhou2.jpg',
			'pic_url': './test/imgs/hangzhou2.jpg',
			'introduction': u'叫花鸡的简介',
			'detail': u'叫花鸡的详情'
        }, {
	        'name': u'黄桥烧饼',
	        'category': u'分类3',
	        'physical_unit': u'个',
			'price': '3.0',
			'weight': '5',
			'thumbnails_url': './test/imgs/mian1.jpg',
			'pic_url': './test/imgs/mian1.jpg',
			'introduction': u'黄桥烧饼的简介',
			'detail': u'黄桥烧饼的详情'
        }, {
	        'name': u'武昌鱼',
	        'category': u'',
	        'physical_unit': u'条',
			'price': '23.0',
			'weight': '5',
			'thumbnails_url': './test/imgs/yu1.jpg',
			'pic_url': './test/imgs/yu1.jpg',
			'introduction': u'武昌鱼的简介',
			'detail': u'武昌鱼的详情'
        }, {
	        'name': u'西湖醋鱼',
	        'category': u'',
	        'physical_unit': u'条',
			'price': '24.0',
			'weight': '5',
			'thumbnails_url': './test/imgs/yu2.jpg',
			'pic_url': './test/imgs/yu2.jpg',
			'introduction': u'西湖醋鱼的简介',
			'detail': u'西湖醋鱼的详情'
        }]

		'''
		添加商品:
		'''
		#验证：提交时的默认错误提示
		edit_product_page = product_list_page.click_add_product_button()
		edit_product_page.submit_product({}, url2uploaded_url)
		error_hints = edit_product_page.get_error_hints()
		self.assertEquals(7, len(error_hints))
		self.assertEquals(u'内容不能为空', error_hints[0])
		self.assertEquals(u'内容不能为空', error_hints[1])
		self.assertEquals(u"价格不正确，请输入0-99999之间的价格", error_hints[2])
		self.assertEquals(u'内容不能为空', error_hints[3])
		self.assertEquals(u"格式不正确，请输入'3.14'或'5'这样的数字", error_hints[4])
		self.assertEquals(u"请选择一张图片", error_hints[5])
		self.assertEquals(u"请选择一张图片", error_hints[6])
		#添加5个商品
		edit_product_page.submit_product(expected_products[0], url2uploaded_url)
		for product in expected_products[1:]:
			edit_product_page = product_list_page.click_add_product_button()
			edit_product_page.submit_product(product, url2uploaded_url)
			
		#验证：商品列表为[东坡肘子, 叫花鸡，黄桥烧饼，武昌鱼，西湖醋鱼]
		products = product_list_page.get_products()
		self.assertEquals(5, len(products))
		for i in range(5):
			#验证倒序排列
			self.__assert_product(expected_products[4-i], products[i], url2uploaded_url)

		'''
		更新商品“叫花鸡”为“龙井虾仁”
		'''
		expected_products[1] = {
	        'name': u'龙井虾仁',
	        'category': u'分类3',
	        'physical_unit': u'盘',
			'price': '9.0',
			'weight': '5',
			'thumbnails_url': './test/imgs/hangzhou3.jpg',
			'pic_url': './test/imgs/hangzhou3.jpg',
			'introduction': u'龙井虾仁的简介',
			'detail': u'龙井虾仁的详情'
        }
		edit_product_page = product_list_page.enter_edit_product_page(u'叫花鸡')
		edit_product_page.update_product(expected_products[1], url2uploaded_url)
		#验证：商品列表为[东坡肘子, 龙井虾仁，黄桥烧饼，武昌鱼，西湖醋鱼]
		products = product_list_page.get_products()
		self.assertEquals(5, len(products))
		for i in range(5):
			#验证倒序排列
			self.__assert_product(expected_products[4-i], products[i], url2uploaded_url)
		time.sleep(1)

		'''
		分类浏览
		'''
		#验证：新分类1
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'新分类1')
		category_products = edit_category_page.get_category_products()
		self.assertEquals(3, len(category_products))
		self.assert_dict({'name':u'东坡肘子', 'is_selected':True}, category_products[0])
		self.assert_dict({'name':u'武昌鱼', 'is_selected':False}, category_products[1])
		self.assert_dict({'name':u'西湖醋鱼', 'is_selected':False}, category_products[2])
		#验证：分类3
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'分类3')
		category_products = edit_category_page.get_category_products()
		self.assertEquals(4, len(category_products))
		self.assert_dict({'name':u'龙井虾仁', 'is_selected':True}, category_products[0])
		self.assert_dict({'name':u'黄桥烧饼', 'is_selected':True}, category_products[1])
		self.assert_dict({'name':u'武昌鱼', 'is_selected':False}, category_products[2])
		self.assert_dict({'name':u'西湖醋鱼', 'is_selected':False}, category_products[3])
		#分类1中，选中“武昌鱼”
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'新分类1')
		edit_category_page.select_products([u'武昌鱼'])
		edit_category_page.submit()
		#验证：新分类1
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'新分类1')
		category_products = edit_category_page.get_category_products()
		self.assertEquals(3, len(category_products))
		self.assert_dict({'name':u'东坡肘子', 'is_selected':True}, category_products[0])
		self.assert_dict({'name':u'武昌鱼', 'is_selected':True}, category_products[1])
		self.assert_dict({'name':u'西湖醋鱼', 'is_selected':False}, category_products[2])
		#验证：分类3
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'分类3')
		category_products = edit_category_page.get_category_products()
		self.assertEquals(3, len(category_products))
		self.assert_dict({'name':u'龙井虾仁', 'is_selected':True}, category_products[0])
		self.assert_dict({'name':u'黄桥烧饼', 'is_selected':True}, category_products[1])
		self.assert_dict({'name':u'西湖醋鱼', 'is_selected':False}, category_products[2])
		#分类3中，选中“西湖醋鱼”
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'分类3')
		edit_category_page.select_products([u'西湖醋鱼'])
		edit_category_page.submit()
		#验证：新分类1
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'新分类1')
		category_products = edit_category_page.get_category_products()
		self.assertEquals(2, len(category_products))
		self.assert_dict({'name':u'东坡肘子', 'is_selected':True}, category_products[0])
		self.assert_dict({'name':u'武昌鱼', 'is_selected':True}, category_products[1])
		#验证：分类3
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'分类3')
		category_products = edit_category_page.get_category_products()
		self.assertEquals(3, len(category_products))
		self.assert_dict({'name':u'龙井虾仁', 'is_selected':True}, category_products[0])
		self.assert_dict({'name':u'黄桥烧饼', 'is_selected':True}, category_products[1])
		self.assert_dict({'name':u'西湖醋鱼', 'is_selected':True}, category_products[2])
		#新分类1中，取消选中“武昌鱼”；分类3中，取消选中“西湖醋鱼”
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'新分类1')
		edit_category_page.unselect_products([u'武昌鱼'])
		edit_category_page.submit()
		edit_category_page = category_list_page.enter_category_edit_page(u'分类3')
		edit_category_page.unselect_products([u'西湖醋鱼'])
		edit_category_page.submit()
		#验证：新分类1
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'新分类1')
		category_products = edit_category_page.get_category_products()
		self.assertEquals(3, len(category_products))
		self.assert_dict({'name':u'东坡肘子', 'is_selected':True}, category_products[0])
		self.assert_dict({'name':u'武昌鱼', 'is_selected':False}, category_products[1])
		self.assert_dict({'name':u'西湖醋鱼', 'is_selected':False}, category_products[2])
		#验证：分类3
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'分类3')
		category_products = edit_category_page.get_category_products()
		self.assertEquals(4, len(category_products))
		self.assert_dict({'name':u'龙井虾仁', 'is_selected':True}, category_products[0])
		self.assert_dict({'name':u'黄桥烧饼', 'is_selected':True}, category_products[1])
		self.assert_dict({'name':u'武昌鱼', 'is_selected':False}, category_products[2])
		self.assert_dict({'name':u'西湖醋鱼', 'is_selected':False}, category_products[3])
		#添加“分类4”
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.click_add_category_button()
		edit_category_page.add_category(u'分类4', [u'武昌鱼', u'西湖醋鱼'])
		edit_category_page.submit()
		#验证：新分类1
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'新分类1')
		category_products = edit_category_page.get_category_products()
		self.assertEquals(1, len(category_products))
		self.assert_dict({'name':u'东坡肘子', 'is_selected':True}, category_products[0])
		#验证：分类3
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'分类3')
		category_products = edit_category_page.get_category_products()
		self.assertEquals(2, len(category_products))
		self.assert_dict({'name':u'龙井虾仁', 'is_selected':True}, category_products[0])
		self.assert_dict({'name':u'黄桥烧饼', 'is_selected':True}, category_products[1])
		#验证：分类4
		category_list_page = CategoryListPage(self.driver)
		category_list_page.load()
		edit_category_page = category_list_page.enter_category_edit_page(u'分类4')
		category_products = edit_category_page.get_category_products()
		self.assertEquals(2, len(category_products))
		self.assert_dict({'name':u'武昌鱼', 'is_selected':True}, category_products[0])
		self.assert_dict({'name':u'西湖醋鱼', 'is_selected':True}, category_products[1])

		'''
		删除商品
		'''
		product_list_page = ProductListPage(self.driver)
		product_list_page.load()
		edit_product_page = product_list_page.enter_edit_product_page(u'龙井虾仁')
		edit_product_page.delete()
		expected_products[3]['category'] = u'分类4' #更新'武昌鱼'的分类
		expected_products[4]['category'] = u'分类4' #更新'西湖醋鱼'的分类
		expected_products.remove(expected_products[1]) #删除"龙井虾仁"

		#验证：商品列表为[东坡肘子, 黄桥烧饼，武昌鱼，西湖醋鱼]
		product_list_page = ProductListPage(self.driver)
		product_list_page.load()
		products = product_list_page.get_products()
		self.assertEquals(4, len(products))
		for i in range(4):
			#验证倒序排列
			self.__assert_product(expected_products[3-i], products[i], url2uploaded_url)


	#==============================================================================
	# test_05_template: 测试编辑template
	#==============================================================================
	@helper.register('template')
	def test_05_template(self):
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


	#==============================================================================
	# test_06_webapp_1_success_purchase: 测试webapp, 一次完整的购买
	#==============================================================================
	@helper.register('webapp')
	def not_test_06_webapp_1_success_purchase(self):
		login_page = LoginPage(self.driver)
		login_page.login('test1', 'test1')

		template_list_page = TemplateListPage(self.driver)
		template_list_page.load()
		template_list_page.select_template(u'简约风尚')
		template_list_page.preview_template(u'简约风尚')

		main_window, preview_window = self.driver.window_handles[:2]

		#print self.driver.window_handles
		self.driver.switch_to_window(preview_window)
		
		#期望商品
		expected_products = [{
	        'name': u'东坡肘子',
	        'category': u'新分类1',
			'price': '11.0'
        }, {
	        'name': u'黄桥烧饼',
	        'category': u'分类3',
			'price': '3.0'
        }, {
	        'name': u'武昌鱼',
	        'category': u'分类4',
			'price': '23.0'
        }, {
	        'name': u'西湖醋鱼',
	        'category': u'分类4',
			'price': '24.0'
        }]

		'''
		进入商品列表页
		'''
		home_page = WAHomePage(self.driver)
		index_page = home_page.enter_product_list_page()
		products = index_page.get_products()
		self.assert_list(products, expected_products)

		'''
		进入商品详情页
		'''
		product_detail_page = index_page.enter_product_detail_page(u'东坡肘子')
		expected_product = {
			'name': u'东坡肘子',
			'price': u'11.0',
			'original_price': None,
			'weight': u'5.0',
			'postage_config_name': u'免运费',
			'postage': None,
			'detail': u'东坡肘子的详情'
		}
		self.assert_dict(expected_product, product_detail_page.get_product_info())
		self.assertEquals(1, product_detail_page.get_purchase_count())
		#调整购买数量
		product_detail_page.increase_purchase_count(2) #加2个，变为3
		self.assertEquals(3, product_detail_page.get_purchase_count())
		product_detail_page.decrease_purchase_count(5) #减5个，维持在1
		self.assertEquals(1, product_detail_page.get_purchase_count())
		product_detail_page.increase_purchase_count(1)
		self.assertEquals(2, product_detail_page.get_purchase_count())
		edit_order_page = product_detail_page.do_purchase()

		'''
		进入订单编辑页
		'''
		#验证商品列表
		expected_order_products = [{
			'name': u'东坡肘子',
			'price': u'11.0',
			'purchase_count': 2
		}]
		actual_order_products = edit_order_page.get_products()
		self.assert_list(expected_order_products, actual_order_products)
		#验证积分
		self.assertEquals('20', edit_order_page.get_integral())
		#验证订单总价
		self.assertEquals('22.00', edit_order_page.get_total_price())

		#验证收货人信息
		expected_ship_info = {
			'name': u'',
			'province': u'-1',
			'city': u'-1',
			'district': '-1',
			'address': u'',
			'tel': u''
		}
		actual_ship_info = edit_order_page.get_ship_info()
		self.assert_dict(expected_ship_info, actual_ship_info)
		#输入收货人信息
		expected_ship_info = {
			'name': u'郭靖',
			'province': u'北京市', #北京市
			'city': u'北京市', #北京市
			'district': u'东城区', #东城区
			'address': u'长安大街',
			'tel': u'13811223344'
		}
		edit_order_page.input_ship_info(expected_ship_info)
		
		#验证购买数量
		self.assertEquals(2, edit_order_page.get_purchase_count())
		edit_order_page.decrease_purchase_count(1)
		self.assertEquals(1, edit_order_page.get_purchase_count())
		#验证订单总价变为11.00
		self.assertEquals('11.00', edit_order_page.get_total_price())
		edit_order_page.increase_purchase_count(2)
		self.assertEquals(3, edit_order_page.get_purchase_count())
		#验证订单总价变为33.00
		self.assertEquals('33.00', edit_order_page.get_total_price())

		#提交订单
		pay_order_page = edit_order_page.submit_order()

		'''
		进入订单支付页面
		'''
		expected_order_products = [{
			'name': u'东坡肘子',
			'price': u'11.0',
			'purchase_count': 3
		}]
		expected_price_info = {
			'products_price': '33.0',
			'postage': None,
			'coupon_money': None,
			'integral_money': None,
			'final_price': '33.0',
		}
		order_info = pay_order_page.get_order_info()
		self.assertEquals(u'郭靖 13811223344 北京市 北京市 东城区 长安大街', order_info['ship_info'])
		self.assertEquals(u'待支付', order_info['status'])
		self.assertEquals(u'无', order_info['bill'])
		self.assert_list(expected_order_products, order_info['products'])
		self.assert_dict(expected_price_info, order_info['price_info'])
		pay_interface_list_page = pay_order_page.do_payment()

		'''
		进入支付方式选择页面
		'''
		mock_pay_page = pay_interface_list_page.select_pay_interface(u'我的支付宝')

		'''
		进入模拟支付宝支付页面
		'''
		pay_result_page = mock_pay_page.pay()

		'''
		进入支付结果页面
		'''
		result_order_info = pay_result_page.get_order_info()
		self.assertEquals(u'待发货', result_order_info['status'])
		self.assertEquals(order_info['order_id'], result_order_info['order_id'])
		index_page = pay_result_page.click_back_button()

		'''
		返回商品列表页
		'''
		self.assertTrue(index_page.is_index_page())

		#返回main window
		self.driver.switch_to_window(main_window)


from webapp.modules.mall.models import *
def init():
	print 'init db environment for mall'

	#CategoryHasProduct.objects.all().delete()
	#Product.objects.all().delete()
	#ProductCategory.objects.all().delete()

	#PostageConfig.objects.filter(~Q(name=u'免运费')).delete()
	#PostageConfig.objects.filter(name=u'免运费').update(is_used=True)
	#PayInterface.objects.all().delete()

	#清空webapp相关的数据库
	OrderHasProduct.objects.all().delete()
	Order.objects.all().delete()
	ShoppingCart.objects.all().delete()
	
	
def clear():
	print 'clear db environment for mall'


TestClass = TestMall
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