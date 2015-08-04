# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME
from add_user_dialog import AddUserDialog
from add_module_dialog import AddModuleDialog

class AccountListPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		self.click_navs(u"账户")
		
	#***********************************************************************************
	# add_user: 添加账户
	#***********************************************************************************
	def add_user(self, username, password):
		time.sleep(WAIT_SHORT_TIME)
		self.driver.find_element_by_id("addUserBtn").click()
		add_user_dialog = AddUserDialog(self.driver)
		add_user_dialog.add_user(username, password)

	#***********************************************************************************
	# add_webapp_modules: 添加webapp模块
	#***********************************************************************************
	def add_webapp_modules_for_last_user(self):
		time.sleep(WAIT_SHORT_TIME)
		add_module_buttons = self.driver.find_elements_by_css_selector('.x-manageModules')
		add_module_buttons[-1].click()
		add_module_dialog = AddModuleDialog(self.driver)
		add_module_dialog.add_all_modules()

	#***********************************************************************************
	# get_accounts: 获得账户集合
	#***********************************************************************************
	def get_accounts(self):
		accounts = []
		for el in self.driver.find_elements_by_css_selector('#accountListTable tbody tr'):
			tds = el.find_elements_by_css_selector('td')
			
			#获得module集合
			modules = tds[1].text.split(u', ')
			if len(modules) == 1 and len(modules[0].strip()) == 0:
				#处理切分后为空的情况
				modules = []

			accounts.append({
				'name': tds[0].text,
				'modules': modules
			})

		return accounts

	#***********************************************************************************
	# delete_user: 删除账号
	#***********************************************************************************
	def delete_user(self, name):
		account_delete_button = None
		for el in self.driver.find_elements_by_css_selector('#accountListTable tbody tr'):
			tds = el.find_elements_by_css_selector('td')
			if name == tds[0].text:
				account_delete_button = el.find_elements_by_css_selector('a.btn-danger')[0]
				break

		if account_delete_button:
			account_delete_button.click()
		
		time.sleep(WAIT_SHORT_TIME)
