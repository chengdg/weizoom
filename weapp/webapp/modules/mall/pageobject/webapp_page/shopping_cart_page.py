# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

from webapp.modules.mall.pageobject.webapp_page.edit_order_page import WAEditOrderPage

class WAShoppingCartPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass

	#############################################################
	# get_product_groups: 获取商品列表
	#############################################################
	def get_product_groups(self):
		product_groups = []
		try:
			productGropu_els = self.driver.fs('.xt-productGroup')
		except:
			productGropu_els = None
		if productGropu_els:
			for productGropu_el in productGropu_els:
				#获取商品信息
				products = []
				for el in productGropu_el.fs('.xt-product'):
					name = el.f('.xt-name').text.strip()
					price = float(el.f('.xt-price').text.split(u'￥')[1])
					purchase_count = int(el.f('.wui-counterText').text)
					try:
						model = el.f('.xt-productCustomModel').text
					except:
						model = ''
					products.append({
						'name': name,
						'price': price,
						'count': purchase_count,
						'model': model
					})

				#获取促销信息
				promotion = None
				try:
					promotion_el = productGropu_el.f('.xt-promotion')
					promotion_type = promotion_el.f('.xt-promotionType').text
					if u'限时抢购' in promotion_type:
						promotion_type = 'flash_sale'
						saved_money = promotion_el.f('.xt-savedMoney').text
						promotion = {
							"type": promotion_type,
							"result": {
								"saved_money": saved_money
							}
						}
					elif u'满减' in promotion_type:
						promotion_type = 'price_cut'
						price = promotion_el.f('.xt-price').text
						if not price:
							price = promotion_el.f('.xt-detail-price').text
						cut_money = promotion_el.f('.xt-cutMoney').text
						if not cut_money:
							cut_money = promotion_el.f('.xt-detail-cutMoney').text
						subtotal = productGropu_el.f('.xt-subtotal').text[1:]
						promotion = {
							"type": promotion_type,
							"result": {
								"price": price,
								"cut_money": cut_money,
								"subtotal": subtotal
							}
						}
					elif u'赠品' in promotion_type:
						premium_products = []
						for premium_product_el in promotion_el.fs('.xt-premiumProduct'):
							premium_products.append({
								"name": premium_product_el.f('.xt-name').text,
								"count": premium_product_el.f('.xt-count').text,
							})
						promotion = {
							"type": 'premium_sale',
							"result": {
								"premium_products": premium_products
							}
						}
				except:
					promotion = None

				product_groups.append({
					"products": products,
					"promotion": promotion
				})

		return product_groups

	#############################################################
	# get_total_price: 获取订单总价
	#############################################################
	def get_total_price(self):
		try:
			return float(self.driver.find_element_by_css_selector('.xt-totalPrice').text.strip())
		except:
			return 0.0

	def get_total_product_count(self):
		try:
			return float(self.driver.find_element_by_css_selector('.xt-totalAccount').text.strip())		
		except:
			return 0

	#############################################################
	# delete_product: 删除商品
	#############################################################
	def delete_product(self, name):
		for el in self.driver.find_elements_by_css_selector('.xt-product'):
			if name == el.find_element_by_css_selector('.xt-name').text.strip():
				el.find_element_by_css_selector('.xa-deleteBtn').click()
				break

	#############################################################
	# select_products: 选择商品
	#############################################################
	def select_product(self, name):
		for el in self.driver.fs('.xt-product'):
			if (name == 'all') or (name == el.f('.xt-name').text.strip()):
				el.f('label[name="checkbox-cart"]').click()
				
	#############################################################
	# increase_purchase_count_to: 增加购买数量到count数量
	#############################################################
	def increase_purchase_count_to(self, name, count):
		current_count = int(self.driver.find_element_by_css_selector('.wui-counterText').text.strip())
		delta = count - current_count
		if delta > 0:
			self.increase_purchase_count(name, delta)

	#############################################################
	# increase_purchase_count: 增加购买数量
	#############################################################
	def increase_purchase_count(self, name, count):
		for el in self.driver.fs('.xt-product'):
			if name != el.f('.xt-name').text.strip():
				continue
			
			for i in range(count):
				el.f('.wui-counter .wa-up').click()
		time.sleep(0.5)

	#############################################################
	# decrease_purchase_count: 减少购买数量
	#############################################################
	def decrease_purchase_count(self, name, count):
		for el in self.driver.fs('.xt-product'):
			if name != el.f('.xt-name').text.strip():
				continue

			for i in range(count):
				el.f('.wui-counter .wa-down').click()
		time.sleep(0.5)

	#############################################################
	# submit_order: 提交订单
	#############################################################
	def submit_order(self):
		self.driver.find_element_by_id('submit-order').click()
		time.sleep(2)
		if self.is_shopping_cart_page():
			#出错，停留在购物车页面
			return self
		elif self.is_webapp_edit_order_page():
			edit_order_page = WAEditOrderPage(self.driver)
			return edit_order_page
		else :
			return self