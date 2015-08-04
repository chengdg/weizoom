# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

class OrderDetailPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	#***********************************************************************************
	# get_order_detail: 获取订单详情
	#***********************************************************************************
	def get_order_detail(self):
		customer_message = self.driver.find_element_by_css_selector('.xt-customerMessage').text.strip()

		return {
			'customer_message': customer_message
		}
