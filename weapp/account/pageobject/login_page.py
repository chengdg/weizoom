# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame

class LoginPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def login(self, username, password=None):
		self.driver.get('http://dev.weapp.com')
		self.driver.find_element_by_css_selector('.tx_login').click()
		time.sleep(1)

		self.driver.find_element_by_id("username").clear()
		self.driver.find_element_by_id("username").send_keys(username)
		if not password:
			password = username
		self.driver.find_element_by_name("password").clear()
		self.driver.find_element_by_name("password").send_keys(password)

		self.driver.find_element_by_css_selector("input.btn-success").click()
		time.sleep(1)
