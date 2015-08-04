# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

class AddModuleDialog(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver
		
	#***********************************************************************************
	# add_all_modules: 添加模块
	#***********************************************************************************
	def add_all_modules(self):
		time.sleep(WAIT_SHORT_TIME)
		for el in self.driver.find_elements_by_css_selector('div.x-dialog-manageWebappModule input[type="checkbox"]'):
			el.click()

		selector = 'div.x-dialog-manageWebappModule .btn-success'
		self.driver.find_element_by_css_selector(selector).click()
		time.sleep(WAIT_SHORT_TIME)

		return None
