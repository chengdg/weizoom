# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME


class WAIntegralLogPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass
		
	def get_logs(self):
		integralEvents = []
		for el in self.driver.find_elements_by_css_selector('.xt-integral'):
			event = el.find_element_by_css_selector('.xt-integralEvent').text.strip()
			integral = int(el.find_element_by_css_selector('.xt-integralCount').text.strip())
			integralEvents.append({
				"event": event,
				"integral": integral
			})
		return integralEvents
