# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME
from account.models import UserProfile

class AccountInfoPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def is_account_info_page(self):
		return '/account/' in self.driver.current_url

	def is_account_binded(self):
		page_content = self.driver.find_element_by_tag_name('body').text
		return (not (u'我同意以上协议' in page_content)) and (u'账号昵称' in page_content)

	def bind_account(self, user_name):
		user = User.objects.get(username=user_name)
		UserProfile.objects.filter(user=user).update(is_mp_registered=True)
		
		self.driver.find_elements_by_css_selector('label.agree_checkbox #agree')[0].click()
		time.sleep(1)
		self.driver.find_element_by_id('bindMpUserBtn').click()
		time.sleep(WAIT_SHORT_TIME)
		self.driver.find_element_by_id('mpusername').clear()
		self.driver.find_element_by_id('mpusername').send_keys(user_name)
		self.driver.find_element_by_id('bind_button').click()
		time.sleep(WAIT_SHORT_TIME)
