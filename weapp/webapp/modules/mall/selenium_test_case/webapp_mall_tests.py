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
from modules.member.models import ShipInfo
from test import helper
from webapp.modules.mall.models import *

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
		
		#清空webapp相关的数据库
		OrderHasProduct.objects.all().delete()
		Order.objects.all().delete()
		ShoppingCart.objects.all().delete()

		#恢复商品库存
		#Product.objects.all().update(stock_type=0, stocks=0)

		#创建浏览器
		chrome_options = Options()
		chrome_options.add_argument("--disable-extensions")
		self.driver = webdriver.Chrome(chrome_options=chrome_options)

		self.driver.implicitly_wait(3)
		self.verificationErrors = []

		self.main_window = None
		self.preview_window = None


	def tearDown(self):
		page_frame = PageFrame(self.driver)
		page_frame.logout()
		self.driver.quit()


	#==============================================================================
	# test_webapp_01_success_purchase: 测试webapp, 一次完整的购买
	#==============================================================================
	@helper.register('webapp')
	def not_test_webapp_01_success_purchase(self):
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
	        'name': u'西湖醋鱼',
	        'category': u'分类4',
			'price': '24.0'
        }, {
	        'name': u'武昌鱼',
	        'category': u'分类4',
			'price': '23.0'
        }, {
	        'name': u'黄桥烧饼',
	        'category': u'分类3',
			'price': '3.0'
        }, {
	        'name': u'东坡肘子',
	        'category': u'新分类1',
			'price': '11.0'
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
		
		#提交订单
		pay_order_page = edit_order_page.submit_order()

		'''
		进入订单支付页面
		'''
		expected_order_products = [{
			'name': u'东坡肘子',
			'price': u'11.0',
			'purchase_count': 2
		}]
		expected_price_info = {
			'products_price': '22.0',
			'postage': None,
			'coupon_money': None,
			'integral_money': None,
			'final_price': '22.0',
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
		mock_pay_page = pay_interface_list_page.select_pay_interface(u'微信支付')

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


	def __enter_product_detail_page(self, product):
		home_page = WAHomePage(self.driver)
		index_page = home_page.enter_product_list_page()
		product_detail_page = index_page.enter_product_detail_page(product)


	def __buy(self, options={}):
		'''
		进入商品列表页
		'''
		home_page = WAHomePage(self.driver)
		index_page = home_page.enter_product_list_page()

		'''
		进入商品详情页
		'''
		product_detail_page = index_page.enter_product_detail_page(options.get('product', u'东坡肘子'))
		#调整购买数量
		increase_count = options.get('purchase_count', 1) - 1
		if increase_count > 0:
			product_detail_page.increase_purchase_count(increase_count)
		#hook
		hook_func = options.get('hook_product_detail_page', None)
		if hook_func:
			if hook_func(product_detail_page, options):
				home_page = product_detail_page.goto_webapp_home_page()
				return home_page
		edit_order_page = product_detail_page.do_purchase()

		'''
		进入订单编辑页
		'''
		#输入收货人信息
		ship_info = options.get('ship_info', None)
		ignore_default_ship_info = options.get('ignore_default_ship_info', False)
		if not ship_info and not ignore_default_ship_info:
			ship_info = {
				'name': u'郭靖',
				'province': u'北京市', #北京市
				'city': u'北京市', #北京市
				'district': u'东城区', #东城区
				'address': u'长安大街',
				'tel': u'13811223344'
			}
			edit_order_page.input_ship_info(ship_info)
		#hook
		hook_func = options.get('hook_edit_order_page', None)
		if hook_func:
			if hook_func(edit_order_page, options):
				home_page = edit_order_page.goto_webapp_home_page()
				return home_page		
		#提交订单
		pay_order_page = edit_order_page.submit_order()

		'''
		进入订单支付页
		'''
		#hook
		hook_func = options.get('hook_pay_order_page', None)
		if hook_func:
			if hook_func(pay_order_page, options):
				home_page = pay_order_page.goto_webapp_home_page()
				return home_page
		pay_interface_list_page = pay_order_page.do_payment()

		'''
		进入支付方式选择页面
		'''
		mock_pay_page = pay_interface_list_page.select_pay_interface(u'微信支付')

		'''
		进入模拟支付宝支付页面
		'''
		pay_result_page = mock_pay_page.pay()

		'''
		进入支付结果页面
		'''
		index_page = pay_result_page.click_back_button()

		return index_page


	#==============================================================================
	# __start_preview_webapp: 开始预览
	#==============================================================================
	def __start_preview_webapp(self):
		login_page = LoginPage(self.driver)
		login_page.login('test1', 'test1')

		template_list_page = TemplateListPage(self.driver)
		template_list_page.load()
		template_list_page.select_template(u'简约风尚')
		template_list_page.preview_template(u'简约风尚')

		self.main_window, self.preview_window = self.driver.window_handles[:2]

		#print self.driver.window_handles
		self.driver.switch_to_window(self.preview_window)
		return self.main_window

	#==============================================================================
	# __switch_to_preview_window: 切换到预览窗口
	#==============================================================================
	def __switch_to_preview_window(self):
		self.driver.switch_to_window(self.preview_window)

	#==============================================================================
	# __switch_to_main_window: 切换到主编辑窗口
	#==============================================================================
	def __switch_to_main_window(self):
		self.driver.switch_to_window(self.main_window)


	#==============================================================================
	# __finish_preview_webapp: 结束预览
	#==============================================================================
	def __finish_preview_webapp(self, main_window=None):
		self.driver.switch_to_window(self.main_window)


	#==============================================================================
	# test_webapp_02_use_integral: 测试webapp, 使用积分
	#==============================================================================
	@helper.register('webapp_integral')
	def not_test_webapp_02_use_integral(self):
		def hook_edit_order_page(edit_order_page, options):
			#验证：积分不能为空
			edit_order_page.use_integral('')
			edit_order_page.click_submit_button()
			self.assertEquals(u'积分不能为空', edit_order_page.get_webapp_alert())
			time.sleep(2)
			#验证：积分必须是整数
			#edit_order_page.use_integral('abc')
			#edit_order_page.click_submit_button()
			#self.assertEquals(u'请输入整数积分', edit_order_page.get_webapp_alert())
			#time.sleep(2)
			#验证：积分不能超过总积分
			edit_order_page.use_integral(100)
			edit_order_page.click_submit_button()
			self.assertEquals(u'积分不能大于41', edit_order_page.get_webapp_alert())
			time.sleep(2)
			#正常使用10个积分
			edit_order_page.use_integral(10)
			time.sleep(1)
			return False

		def hook_pay_order_page(pay_order_page, options):
			order_info = pay_order_page.get_order_info()
			price_info = order_info['price_info']
			self.assertEquals(None, price_info['postage'])
			self.assertEquals(None, price_info['coupon_money'])
			self.assertEquals(u'3.0', price_info['products_price'])
			self.assertEquals(u'2.0', price_info['integral_money'])
			self.assertEquals(u'1.0', price_info['final_price'])
			return False

		main_window = self.__start_preview_webapp()
		
		#设置初始积分
		from modules.member.models import Member
		Member.objects.all().update(integral=41)
		#进行购买
		options = {
			'product': u'黄桥烧饼',
			'hook_edit_order_page': hook_edit_order_page,
			'hook_pay_order_page': hook_pay_order_page
		}
		index_page = self.__buy(options)
		home_page = index_page.return_to_webapp_home_page()
		user_center_page = home_page.enter_user_center_page()
		self.assertEquals('31', user_center_page.get_integral())

		self.__finish_preview_webapp(main_window)


	#==============================================================================
	# test_webapp_03_shopping_cart: 测试webapp, 1. 使用购物车
	#==============================================================================
	@helper.register('webapp_shopping_cart')
	def not_test_webapp_03_shopping_cart(self):
		main_window = self.__start_preview_webapp()
		
		'''
		添加2个"武昌鱼"到购物车
		'''
		def hook_product_detail_page_1(product_detail_page, options):
			time.sleep(1)
			product_detail_page.add_to_shopping_cart()
			time.sleep(1)
			self.assertEquals(1, product_detail_page.get_shopping_cart_product_count())
			return True

		options = {
			'product': u'武昌鱼',
			'purchase_count': 2,
			'hook_product_detail_page': hook_product_detail_page_1
		}
		home_page = self.__buy(options)

		'''
		添加3个"西湖醋鱼"到购物车
		'''
		def hook_product_detail_page_2(product_detail_page, options):
			time.sleep(1)
			#验证：当前购物车中商品为1
			self.assertEquals(1, product_detail_page.get_shopping_cart_product_count())
			#添加到购物车
			product_detail_page.add_to_shopping_cart()
			time.sleep(1)
			#验证：购物车中商品为2
			self.assertEquals(2, product_detail_page.get_shopping_cart_product_count())
			#调整数量为2，再次添加购物车
			product_detail_page.increase_purchase_count(1)
			product_detail_page.add_to_shopping_cart()
			time.sleep(1)
			#验证：购物车中商品为2
			self.assertEquals(2, product_detail_page.get_shopping_cart_product_count())
			return True

		options = {
			'product': u'西湖醋鱼',
			'purchase_count': 1,
			'hook_product_detail_page': hook_product_detail_page_2
		}
		home_page = self.__buy(options)

		'''
		添加1个"东坡肘子"到购物车
		'''
		def hook_product_detail_page_3(product_detail_page, options):
			time.sleep(1)
			#验证：当前购物车中商品为1
			self.assertEquals(2, product_detail_page.get_shopping_cart_product_count())
			#添加到购物车
			product_detail_page.add_to_shopping_cart()
			time.sleep(1)
			#验证：购物车中商品为2
			self.assertEquals(3, product_detail_page.get_shopping_cart_product_count())
			return True

		options = {
			'product': u'东坡肘子',
			'purchase_count': 1,
			'hook_product_detail_page': hook_product_detail_page_3
		}
		home_page = self.__buy(options)

		'''
		进入购物车页面
		'''
		expected_products = [{
	        'name': u'东坡肘子',
			'price': '11.0',
			'purchase_count': 1
        }, {
	        'name': u'武昌鱼',
			'price': '23.0',
			'purchase_count': 2
        }, {
	        'name': u'西湖醋鱼',
			'price': '24.0',
			'purchase_count': 3
        }]
		user_center_page = home_page.enter_user_center_page()
		self.assertEquals(u'6', user_center_page.get_shopping_cart_product_count())
		shopping_cart_page = user_center_page.enter_shopping_cart_page()
		actual_products = shopping_cart_page.get_products()
		self.assert_list(expected_products, actual_products)
		self.assertEquals(129.00, shopping_cart_page.get_total_price())
		#删除商品，调整数量
		shopping_cart_page.delete_product(u'东坡肘子')
		shopping_cart_page.increase_purchase_count(u'武昌鱼', 2)
		shopping_cart_page.decrease_purchase_count(u'西湖醋鱼', 1)
		expected_products = [{
	        'name': u'武昌鱼',
			'price': '23.0',
			'purchase_count': 4
        }, {
	        'name': u'西湖醋鱼',
			'price': '24.0',
			'purchase_count': 2
        }]
		actual_products = shopping_cart_page.get_products()
		self.assert_list(expected_products, actual_products)
		self.assertEquals(140.00, shopping_cart_page.get_total_price())
		edit_order_page = shopping_cart_page.submit_order()

		'''
		进入订单编辑页
		'''
		#验证商品列表
		expected_order_products = expected_products
		actual_order_products = edit_order_page.get_products()
		self.assert_list(expected_order_products, actual_order_products)
		#验证订单总价
		self.assertEquals('140.00', edit_order_page.get_total_price())

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
		#提交订单
		pay_order_page = edit_order_page.submit_order()

		'''
		进入订单支付页面
		'''
		expected_price_info = {
			'products_price': '140.0',
			'postage': None,
			'coupon_money': None,
			'integral_money': None,
			'final_price': '140.0',
		}
		order_info = pay_order_page.get_order_info()
		self.assertEquals(u'郭靖 13811223344 北京市 北京市 东城区 长安大街', order_info['ship_info'])
		self.assertEquals(u'待支付', order_info['status'])
		self.assertEquals(u'无', order_info['bill'])
		self.assert_list(expected_order_products, order_info['products'])
		self.assert_dict(expected_price_info, order_info['price_info'])

		self.__finish_preview_webapp(main_window)


	#==============================================================================
	# test_webapp_04_ship_info: 测试收货地址
	#==============================================================================
	@helper.register('ship_info')
	def not_test_webapp_04_ship_info(self):
		main_window = self.__start_preview_webapp()

		home_page = WAHomePage(self.driver)
		user_center_page = home_page.enter_user_center_page()
		ship_info_page = user_center_page.enter_ship_info_page()

		#验证收货人信息
		expected_ship_info = {
			'name': u'',
			'province': u'-1',
			'city': u'-1',
			'district': '-1',
			'address': u'',
			'tel': u''
		}
		actual_ship_info = ship_info_page.get_ship_info()
		self.assert_dict(expected_ship_info, actual_ship_info)

		#输入收货人信息
		expected_ship_info_huangrong = {
			'name': u'黄蓉',
			'province': u'江苏省',
			'city': u'无锡市',
			'district': u'滨湖区',
			'address': u'大街',
			'tel': u'13844332211'
		}
		ship_info_page.input_ship_info(expected_ship_info_huangrong)
		user_center_page = ship_info_page.submit()		
		
		#重新进入收货人页面
		ship_info_page = user_center_page.enter_ship_info_page()
		actual_ship_info = ship_info_page.get_ship_info()
		self.assert_dict(expected_ship_info_huangrong, actual_ship_info)

		'''
		开始购物
		'''
		#清空收货人信息
		ship_info = ShipInfo.objects.all().order_by('-id')[0]
		ship_info.ship_name = ''
		ship_info.ship_tel = ''
		ship_info.ship_address = ''
		ship_info.area = ''
		ship_info.save()
		#开始购物
		def hook_pay_order_page_1(pay_order_page, options):
			return True
		options = {
			'product': u'东坡肘子',
			'purchase_count': 1,
			'hook_pay_order_page': hook_pay_order_page_1
		}
		ship_info_page.return_to_webapp_home_page()
		home_page = self.__buy(options)

		'''
		进入收货人信息页面，验证收货人信息被修改
		'''
		user_center_page = home_page.enter_user_center_page()
		ship_info_page = user_center_page.enter_ship_info_page()
		expected_ship_info_guojing = {
			'name': u'郭靖',
			'province': u'北京市',
			'city': u'北京市',
			'district': u'东城区',
			'address': u'长安大街',
			'tel': u'13811223344'
		}
		actual_ship_info = ship_info_page.get_ship_info()
		self.assert_dict(expected_ship_info_guojing, actual_ship_info)
		#将收货人修改为"黄蓉"
		ship_info_page.input_ship_info(expected_ship_info_huangrong)
		user_center_page = ship_info_page.submit()

		'''
		再次购物
		'''
		#开始购物
		def hook_edit_order_page(edit_order_page, options):
			actual_ship_info = ship_info_page.get_ship_info()
			self.assert_dict(expected_ship_info_huangrong, actual_ship_info)
			return False
		def hook_pay_order_page_2(pay_order_page, options):
			return True
		options = {
			'product': u'武昌鱼',
			'purchase_count': 1,
			'ignore_default_ship_info': True,
			'hook_pay_order_page': hook_pay_order_page_2
		}
		ship_info_page.goto_webapp_home_page()
		home_page = self.__buy(options)

		'''
		进入订单页面，验证两个订单的收货人不一样
		'''
		#验证第一个订单
		user_center_page = home_page.enter_user_center_page()
		order_list_page = user_center_page.enter_all_order_list_page()
		pay_order_page = order_list_page.enter_order_page_by_index(1)
		order_info = pay_order_page.get_order_info()
		self.assertEquals(u'黄蓉 13844332211 江苏省 无锡市 滨湖区 大街', order_info['ship_info'])
		self.assertEquals(u'武昌鱼', order_info['products'][0]['name'])
		#验证第二个订单
		home_page = pay_order_page.goto_webapp_home_page()
		user_center_page = home_page.enter_user_center_page()
		order_list_page = user_center_page.enter_all_order_list_page()
		pay_order_page = order_list_page.enter_order_page_by_index(2)
		order_info = pay_order_page.get_order_info()
		self.assertEquals(u'郭靖 13811223344 北京市 北京市 东城区 长安大街', order_info['ship_info'])
		self.assertEquals(u'东坡肘子', order_info['products'][0]['name'])

		#结束测试
		self.__finish_preview_webapp(main_window)


	#==============================================================================
	# test_webapp_05_stocks: 测试库存
	#==============================================================================
	@helper.register('stocks')
	def test_webapp_05_stocks(self):
		self.__start_preview_webapp()

		'''
		切换到main window
		'''
		# #验证当前库存为“无限”
		# self.__switch_to_main_window()
		# product_list_page = ProductListPage(self.driver)
		# product_list_page.load()
		# edit_product_page = product_list_page.enter_edit_product_page(u'东坡肘子')
		# expected_stocks = {
		# 	'type': u'无限',
		# 	'count': '0'
		# }
		# actual_stocks = edit_product_page.get_stock_info()
		# self.assert_dict(expected_stocks, actual_stocks)
		# #改变库存
		# expected_stocks = {
		# 	'type': u'有限',
		# 	'count': '3'
		# }
		# edit_product_page.input_stock_info(expected_stocks)
		# product_list_page = edit_product_page.submit()
		# #验证：库存变为3
		# edit_product_page = product_list_page.enter_edit_product_page(u'东坡肘子')
		# actual_stocks = edit_product_page.get_stock_info()
		# self.assert_dict(expected_stocks, actual_stocks)

		'''
		切换到preview window
		'''
		self.__switch_to_preview_window()
		def hook_product_detail_page_1(product_detail_page, options):
			time.sleep(5)
			return True
		options = {
			'product': u'东坡肘子',
			'purchase_count': 1,
			'hook_product_detail_page': hook_product_detail_page_1
		}
		self.__buy(options)

		self.__finish_preview_webapp()




TestClass = TestCase
def suite(group='all'):
	if group == 'all':
		suite = unittest.makeSuite(TestClass, 'test')
	else:
		suite = unittest.TestSuite()
		for function in TestClass.filter_function_by_group(group):
			suite.addTest(TestClass(function))
		
	return suite