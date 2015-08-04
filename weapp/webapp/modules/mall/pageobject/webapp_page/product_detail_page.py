# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

from webapp.modules.mall.pageobject.webapp_page.edit_order_page import WAEditOrderPage

class WAProductDetailPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass

	#############################################################
	# get_product_info: 获取商品信息
	#############################################################
	def get_product_info(self):
		#获取name
		name = self.driver.find_element_by_css_selector('.xt-productName').text

		#获取价格
		price = float(self.driver.find_element_by_css_selector('.xt-price').text.strip())
		try:
			market_price = float(self.driver.find_element_by_css_selector('.xt-marketPrice').text.strip())
		except:
			market_price = None

		#获得购买价格
		purchase_price = float(self.driver.find_element_by_css_selector('.xt-purchasePrice').text.strip())

		#获取重量
		weight = float(self.driver.find_element_by_css_selector('.xt-weight').text.strip())

		#获取运费策略
		postage_config_name = self.driver.find_element_by_css_selector('.xt-postageConfigName').text.strip()		
		#获取运费
		try:
			postage = float(self.driver.find_element_by_css_selector('.xt-postage').text.strip())
		except:
			postage = None	

		#获取库存
		try:
			stocks = self.driver.find_element_by_css_selector('.xt-stocks').text.split(u'库存')[1]
		except:
			stocks = u'无限'
		if not stocks:
			stocks = u'无限'

		#获取商品详情
		detail = self.driver.find_element_by_css_selector('.xui-productDetail-content').text.strip()

		return {
			'name': name,
			'price': price,
			'purchase_price': purchase_price,
			'stocks': stocks,
			'market_price': market_price,
			'weight': weight,
			'postage_config_name': postage_config_name,
			'postage': postage,
			'detail': detail
		}

	#############################################################
	# get_purchase_count: 获取购买数量
	#############################################################
	def get_purchase_count(self):
		return int(self.driver.find_element_by_css_selector('.wui-counter .wui-counterText').text)

	#############################################################
	# increase_purchase_count: 增加购买数量
	#############################################################
	def increase_purchase_count(self, count):
		for i in range(count):
			self.driver.find_element_by_css_selector('.wui-counter .wa-up').click()

	#############################################################
	# increase_purchase_count_to: 增加购买数量到count
	#############################################################
	def increase_purchase_count_to(self, count):
		self.increase_purchase_count(count-1)

	#############################################################
	# decrease_purchase_count: 减少购买数量
	#############################################################
	def decrease_purchase_count(self, count):
		for i in range(count):
			self.driver.find_element_by_css_selector('.wui-counter .wa-down').click()

	#############################################################
	# select_model: 选择规格
	#############################################################
	def select_model(self, model):
		script = "$('.xa-propertyValue').removeClass('xui-unSelectable')"
		self.driver.execute_script(script)
		script = "$('.xui-inner-selected-tag').removeClass('xui-inner-selected-tag')"
		self.driver.execute_script(script)

		items = set(model.split(' '))
		for el in self.driver.find_elements_by_css_selector('.xa-propertyValue'):
			propertyValueName = el.get_attribute('data-property-value-name')
			if propertyValueName in items:
				el.click()

	#############################################################
	# add_to_shopping_cart: 加入购物车
	#############################################################
	def add_to_shopping_cart(self):
		self.driver.find_element_by_css_selector('.xa-addShoppingCartBtn').click()

	#############################################################
	# get_shopping_cart_product_count: 获得购物车中商品数量
	#############################################################
	def get_shopping_cart_product_count(self):
		return int(self.driver.find_element_by_css_selector('.xui-shoppingCartBtn .ui-btn-text').text.strip())

	#############################################################
	# show_purchase_panel: 显示购买panel
	#############################################################
	def show_purchase_panel(self):
		self.driver.find_element_by_css_selector('.xa-slidePanelShow').click()
		time.sleep(WAIT_SHORT_TIME)

	#############################################################
	# show_add_to_shopping_cart_panel: 显示加入购物车panel
	#############################################################
	def show_add_to_shopping_cart_panel(self):
		apply_box = self.driver.find_element_by_css_selector('.xt-applyBox')
		if not apply_box.is_displayed():
			self.driver.find_element_by_css_selector('.xa-addCart').click()
			time.sleep(WAIT_SHORT_TIME)

	#############################################################
	# do_purchase: 进行购买
	#############################################################
	def do_purchase(self):
		self.driver.find_element_by_css_selector('.xa-buyBtn').click()
		'''
		edit_order_page = WAEditOrderPage(self.driver)
		return edit_order_page
		'''