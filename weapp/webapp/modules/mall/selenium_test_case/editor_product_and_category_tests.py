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
	# test_product_category: 测试商品分类
	#==============================================================================
	@helper.register('product_category')
	def test_01_product_category(self):
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
		time.sleep(1)
		#添加“分类2”
		category_list_page = CategoryListPage(self.driver)
		edit_category_page = category_list_page.click_add_category_button()
		edit_category_page.add_category(u'分类2')
		edit_category_page.submit()
		time.sleep(1)
		#添加“分类3”
		category_list_page = CategoryListPage(self.driver)
		edit_category_page = category_list_page.click_add_category_button()
		edit_category_page.add_category(u'分类3')
		edit_category_page.submit()
		time.sleep(1)
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
	# test_product: 测试商品管理
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
	def test_02_product(self):
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
		self.assertEquals(u"格式不正确，请输入'3.147'或'5'这样的数字", error_hints[4])
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





TestClass = TestCase
def suite(group='all'):
	if group == 'all':
		suite = unittest.makeSuite(TestClass, 'test')
	else:
		suite = unittest.TestSuite()
		for function in TestClass.filter_function_by_group(group):
			suite.addTest(TestClass(function))
		
	return suite