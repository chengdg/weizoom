# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

from webapp.modules.mall.pageobject.webapp_page.mock_pay_page import WAMockPayPage
from webapp.modules.mall.pageobject.webapp_page.pay_result_page import WAPayResultPage

class WAPayInterfaceListPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass

	#############################################################
	# select_pay_interface: 选择支付接口
	#############################################################
	def select_pay_interface(self, name):
		for el in self.driver.find_elements_by_css_selector('.x-payInterfaceLink'):
			if name in el.text:
				el.click()
				break

		if u'货到付款' in name:
			return WAPayResultPage(self.driver)
		else:
			return WAMockPayPage(self.driver)
