# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME
from webapp.modules.mall.pageobject.order_detail_page import OrderDetailPage

class OrderListPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		self.click_navs(u"微站")
		time.sleep(WAIT_SHORT_TIME)

	#***********************************************************************************
	# enter_latest_order_detail_page: 点击最新的订单链接，进入订单详情页面
	#***********************************************************************************
	def enter_latest_order_detail_page(self):
		links = self.driver.find_elements_by_css_selector('.xt-orderLink')
		if len(links) > 0:
			link = links[0]
			link.click()
		# trs = self.driver.find_elements_by_css_selector('tbody tr')
		# if len(trs) > 0:
		# 	td = trs[0].find_elements_by_css_selector('td')[1]
		# 	link = td.find_element_by_css_selector('a')
		# 	link.click()

		#订单详情会新开一个窗口，所以这里要switch_to_window
		new_window = self.driver.window_handles[-1]
		self.driver.switch_to_window(new_window)
		return OrderDetailPage(self.driver)
