# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

class AddUserDialog(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver
		
	#***********************************************************************************
	# add_user: 添加用户
	#***********************************************************************************
	def add_user(self, username, password):
		time.sleep(WAIT_SHORT_TIME)
		selector = 'div.x-dialog-managerAddUer input[name="name"]'
		username_input = self.driver.find_element_by_css_selector(selector)
		username_input.clear()
		username_input.send_keys(username)
		selector = 'div.x-dialog-managerAddUer input[name="password"]'
		password_input = self.driver.find_element_by_css_selector(selector)
		password_input.clear()
		password_input.send_keys(password)
		selector = 'div.x-dialog-managerAddUer .btn-success'
		self.driver.find_element_by_css_selector(selector).click()
		time.sleep(WAIT_SHORT_TIME)
