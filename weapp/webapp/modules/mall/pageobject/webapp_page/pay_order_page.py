# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME


class WAPayOrderPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass

	#############################################################
	# get_products: 获取商品列表
	#############################################################
	def get_products(self):
		products = []
		for el in self.driver.find_elements_by_css_selector('.xui-selectedProductList li'):
			name = el.find_element_by_css_selector('.xt-title').text.strip()
			price = el.find_element_by_css_selector('.xt-price').text.strip()
			purchase_count = int(el.find_element_by_css_selector('.xt-count').text.strip())
			products.append({
				'name': name,
				'price': float(price),
				'count': purchase_count
			})

		return products

	#############################################################
	# get_price_info: 获得价格信息
	#############################################################
	def get_price_info(self):
		driver = self.driver
		try:
			final_price = driver.find_element_by_css_selector('.xt-finalPrice').text.strip()
		except:
			final_price = None

		try:
			products_price = driver.find_element_by_css_selector('.xt-productsPrice').text.strip().split(u'￥')[1]
		except:
			products_price = None
		
		try:
			postage = driver.find_element_by_css_selector('.xt-postageMoney').text.strip().split(u'￥')[1]
		except:
			postage = None

		try:
			coupon_money = driver.find_element_by_css_selector('.xt-couponMoney').text.strip()
		except:
			coupon_money = None

		try:
			integral_money = float(driver.find_element_by_css_selector('.xt-integralMoney').text.strip())
		except:
			integral_money = None

		try:
			integral_count = int(driver.find_element_by_css_selector('.xt-integralCount').text.strip())
		except:
			integral_count = None

		return {
			'products_price': products_price,
			'postage': postage,
			'coupon_money': coupon_money,
			'integral_count': integral_count,
			'integral_money': integral_money,
			'final_price': final_price
		}		

	#############################################################
	# get_order_info: 获取订单信息
	#############################################################
	def get_order_info(self, expected_fields):
		driver = self.driver
		if 'status' in expected_fields:
			status = driver.find_element_by_css_selector('.xt-status').text.strip()
		else:
			status = None
		
		order_id = driver.find_element_by_css_selector('.xt-orderId').text.strip()
		
		if 'ship_name' in expected_fields:
			ship_name = driver.find_element_by_css_selector('.xt-shipName').text.strip()
			ship_tel = driver.find_element_by_css_selector('.xt-shipTel').text.strip()
			ship_area = driver.find_element_by_css_selector('.xt-shipArea').text.replace('\n', ' ').strip()
			ship_address = driver.find_element_by_css_selector('.xt-shipAddress').text.strip()
		else:
			ship_name = None
			ship_tel = None
			ship_area = None
			ship_address = None

		if 'bill' in expected_fields:
			try:
				bill = driver.find_element_by_css_selector('.xt-bill').text.strip()
			except:
				bill = ''
		else:
			bill = None
		
		if 'customer_message' in expected_fields:
			try:
				customer_message = driver.find_element_by_css_selector('.xt-customerMessage').text.strip()
			except:
				customer_message = ''
		else:
			customer_message = None

		if 'products' in expected_fields:
			products = self.get_products()
		else:
			products = None

		if 'price_info' in expected_fields:
			price_info = self.get_price_info();
		else:
			price_info = None
		
		return {
			'status': status,
			'customer_message': customer_message,
			'order_id': order_id,
			'bill': bill,
			'ship_name': ship_name,
			'ship_tel': ship_tel,
			'ship_area': ship_area,
			'ship_address': ship_address,
			'price_info': price_info,
			'products': products
		}

	#############################################################
	# do_payment: 支付
	#############################################################
	def do_payment(self):
		from webapp.modules.mall.pageobject.webapp_page.pay_interface_list_page import WAPayInterfaceListPage
		self.driver.find_element_by_id('pay_order').click()
		return WAPayInterfaceListPage(self.driver)