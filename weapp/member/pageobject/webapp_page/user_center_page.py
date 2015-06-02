# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

from webapp.modules.user_center.pageobject.webapp_page.integral_log_page import WAIntegralLogPage
from webapp.modules.user_center.pageobject.webapp_page.ship_info_page import WAShipInfoPage
from webapp.modules.user_center.pageobject.webapp_page.integral_log_page import WAIntegralLogPage
from webapp.modules.user_center.pageobject.webapp_page.user_coupon_page import WAUserCouponPage
from webapp.modules.mall.pageobject.webapp_page.shopping_cart_page import WAShoppingCartPage
from webapp.modules.mall.pageobject.webapp_page.order_list_page import WAOrderListPage
from webapp.modules.mall.pageobject.webapp_page.order_list_page import WAOrderListPage

class WAUserCenterPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass
		
	def get_integral(self):
		value = self.driver.find_element_by_css_selector('.xt-integral').text
		return value.split(u'个')[0]

	def get_shopping_cart_product_count(self):
		value = self.driver.find_element_by_css_selector('.xt-shopping-cart').text
		return value[:-1]

	def enter_shopping_cart_page(self):
		self.driver.find_element_by_partial_link_text(u'购物车').click()
		return WAShoppingCartPage(self.driver)

	def enter_ship_info_page(self):
		self.driver.find_element_by_partial_link_text(u'收货地址').click()
		return WAShipInfoPage(self.driver)

	def enter_all_order_list_page(self):
		self.driver.find_element_by_partial_link_text(u'全部订单').click()
		return WAOrderListPage(self.driver)

	def enter_integral_log_page(self):
		self.driver.find_element_by_partial_link_text(u'积分').click()
		return WAIntegralLogPage(self.driver)

	def enter_user_coupon_page(self):
		self.driver.find_element_by_partial_link_text(u'我的优惠券').click()
		return WAUserCouponPage(self.driver)
