# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

from webapp.modules.mall.pageobject.webapp_page.pay_order_page import WAPayOrderPage

class WAOrderListPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass

	#############################################################
	# get_orders: 获取订单列表
	#############################################################
	def get_orders(self):
		orders = []
		for el in self.driver.find_elements_by_css_selector('.xt-orderList a'):
			product_count = el.find_element_by_css_selector('.xt-productCount').text.split(u'件')[0]
			status = el.find_element_by_css_selector('.xt-status').text[1:-1]
			orders.append({
				'product_count': product_count,
				'status': status
			})

		return orders

	#############################################################
	# enter_order_page_by_index: 进入订单支付页面
	#############################################################
	def enter_order_page_by_index(self, index):
		links = self.driver.find_elements_by_css_selector('.xt-orderList a')
		links[index-1].click()
		return WAPayOrderPage(self.driver)