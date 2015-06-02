# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME
from webapp.modules.mall.pageobject.edit_postage_page import EditPostagePage

class PostageListPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		self.click_navs(u"微站", u'其他选项')
		time.sleep(WAIT_SHORT_TIME)
		
	#***********************************************************************************
	# click_add_postage_config_button: 点击“添加运费配置”的按钮
	#***********************************************************************************
	def click_add_postage_config_button(self):
		self.driver.find_element_by_id("x-addPostageConfigBtn").click()
		return EditPostagePage(self.driver)

	#***********************************************************************************
	# enter_edit_postage_config_page: 点击邮费配置链接，进入邮费配置编辑页面
	#***********************************************************************************
	def enter_edit_postage_config_page(self, postage_config_name):
		self.driver.find_element_by_link_text(postage_config_name).click()
		return EditPostagePage(self.driver)

	#***********************************************************************************
	# get_postage_configs: 获得运费配置集合
	#***********************************************************************************
	def get_postage_configs(self):
		postage_configs = []
		for el in self.driver.find_elements_by_css_selector('#postageListTable tbody tr'):
			tds = el.find_elements_by_css_selector('td')
			
			postage_configs.append({
				'name': tds[1].text.strip(),
				'content': tds[2].text.strip()
			})

		return postage_configs

	#***********************************************************************************
	# delete_postage_config: 删除运费配置
	#***********************************************************************************
	def delete_postage_config(self, name):
		account_delete_button = None
		for el in self.driver.find_elements_by_css_selector('#postageListTable tbody tr'):
			tds = el.find_elements_by_css_selector('td')
			if name == tds[0].text:
				account_delete_button = el.find_elements_by_css_selector('a.btn-danger')[0]
				break

		if account_delete_button:
			account_delete_button.click()
		
		time.sleep(WAIT_SHORT_TIME)

	#***********************************************************************************
	# get_selected_postage_config: 获得选中的运费配置
	#***********************************************************************************
	def get_selected_postage_config(self):
		postage_config = {}
		for el in self.driver.find_elements_by_css_selector('#postageListTable tbody tr'):
			select_radio = el.find_elements_by_css_selector('input[type="radio"]')[0]
			if select_radio.is_selected():
				tds = el.find_elements_by_css_selector('td')
			
				postage_config['name'] = tds[1].text
				postage_config['content'] = tds[2].text
				break

		return postage_config

	#***********************************************************************************
	# select_postage_config: 选中运费配置
	#***********************************************************************************
	def select_postage_config(self, name):
		for el in self.driver.find_elements_by_css_selector('#postageListTable tbody tr'):
			tds = el.find_elements_by_css_selector('td')
			if name == tds[1].text:
				select_radio = el.find_elements_by_css_selector('input[type="radio"]')[0]
				select_radio.click()
				break

		self.driver.find_element_by_id('submitBtn').click()
