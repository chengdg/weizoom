# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from selenium.common.exceptions import NoSuchElementException


class PageView(object):
	def __init__(self, webdriver):
		pass

	def is_element_present(self, how, what):
		try:
			self.driver.find_element(by=how, value=what)
		except NoSuchElementException, e:
			return False
		return True


	def is_element_visible(self, how, what):
		try:
			el = self.driver.find_element(by=how, value=what)
			return el.is_displayed()
		except NoSuchElementException, e:
			return False
