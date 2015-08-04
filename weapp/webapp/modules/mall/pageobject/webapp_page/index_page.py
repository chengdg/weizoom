# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

from webapp.modules.mall.pageobject.webapp_page.product_detail_page import WAProductDetailPage
from webapp.modules.mall.pageobject.webapp_page.shopping_cart_page import WAShoppingCartPage

class WAIndexPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass
		
	def is_index_page(self):
		return 'module=mall&model=products&action=list' in self.driver.current_url

	def get_products(self):
		products = []
		for el in self.driver.find_elements_by_css_selector('.xt-oneProduct'):
			name = el.find_element_by_css_selector('.xt-productName').text.strip()
			price = el.find_element_by_css_selector('.xt-productPrice').text.strip()[1:]
			products.append({
				'name': name,
				'price': price
			})

		return products

	#***********************************************************************************
	# can_switch_category: 是否可切换商品分类
	#***********************************************************************************
	def can_switch_category(self):
		try:
			self.driver.find_element_by_css_selector('[data-ui-role="top-dropdown-nav"]')
			return True
		except:
			return False

	#***********************************************************************************
	# switch_category: 选择分类
	#***********************************************************************************
	def switch_category(self, category_name):
		time.sleep(WAIT_SHORT_TIME)
		self.driver.find_element_by_css_selector('a.wui-dropdownTrigger .wui-dropdownIndicator').click()
		time.sleep(WAIT_SHORT_TIME)
		self.driver.find_element_by_link_text(category_name).click()
		time.sleep(WAIT_SHORT_TIME)

	def enter_product_detail_page(self, name):
		self.driver.find_element_by_partial_link_text(name).click()
		return WAProductDetailPage(self.driver)

	def enter_shopping_cart_page(self):
		self.driver.find_element_by_css_selector('.xt-shoppingCartBtn').click()
		return WAShoppingCartPage(self.driver)
