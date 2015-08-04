# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

from webapp.modules.mall.pageobject.webapp_page.pay_order_page import WAPayOrderPage

class WAPayResultPage(WAPayOrderPage):
	def __init__(self, webdriver):
		self.driver = webdriver

	def get_pay_result(self):
		price = self.driver.find_element_by_css_selector('.xt-price').text.strip()
		pay_interface = self.driver.find_element_by_css_selector('.xt-payInterface').text.strip()
		return {
			"price": price,
			"pay_interface": pay_interface
		}

	def enter_product_list_page(self):
		self.driver.find_element_by_css_selector(".xt-productListLink").click()
		from webapp.modules.mall.pageobject.webapp_page.index_page import WAIndexPage
		return WAIndexPage(self.driver)

	def enter_order_detail_page(self):
		self.driver.find_element_by_css_selector(".xt-orderDetailLink").click()
		# return WAProductDetailPage(self.driver)

