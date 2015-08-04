# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

from webapp.modules.mall.pageobject.webapp_page.pay_result_page import WAPayResultPage

class WAMockPayPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass

	def get_total_fee(self):
		return self.driver.find_element_by_css_selector('.tx-totalFee').text

	#############################################################
	# pay: 支付
	#############################################################
	def pay(self):
		self.driver.find_element_by_css_selector('.btn-success').click()
		return WAPayResultPage(self.driver)
