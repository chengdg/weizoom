# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

class EditPostagePage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	#############################################################################
	# add_postage_config: 添加运费配置
	#############################################################################
	def add_postage_config(self, config):
		name = config['name']
		first_weight = config['first_weight']
		first_weight_price = config['first_weight_price']
		added_weight = config.get('added_weight', None)
		added_weight_price = config.get('added_weight_price', None)
		self.__add_postage_config(name, first_weight, first_weight_price, added_weight, added_weight_price)

	def __add_postage_config(self, name, first_weight, first_weight_price, added_weight=None, added_weight_price=None):
		first_weight = str(first_weight)
		first_weight_price = str(first_weight_price)
		if added_weight:
			added_weight = str(added_weight)
		if added_weight_price:
			added_weight_price = str(added_weight_price)

		name_input = self.driver.find_element_by_id('name')
		name_input.clear()
		name_input.send_keys(name)

		#首重
		first_weight_input = self.driver.find_element_by_id('first_weight')
		first_weight_input.clear()
		first_weight_input.send_keys(first_weight)

		#首重价格
		first_weight_price_input = self.driver.find_element_by_id('first_weight_price')
		first_weight_price_input.clear()
		first_weight_price_input.send_keys(first_weight_price)

		enable_added_weight_input = self.driver.find_element_by_id('is_enable_added_weight')
		if added_weight:
			enable_added_weight_input.click()
			time.sleep(0.5)
			
			#续重
			added_weight_input = self.driver.find_element_by_id('added_weight')
			added_weight_input.clear()
			added_weight_input.send_keys(added_weight)

			#续重价格
			added_weight_price_input = self.driver.find_element_by_id('added_weight_price')
			added_weight_price_input.clear()
			added_weight_price_input.send_keys(added_weight_price)
		else:
			if enable_added_weight_input.is_selected():
				enable_added_weight_input.click()

	#############################################################################
	# get_postage_config: 获取运费配置
	#############################################################################
	def get_postage_config(self):
		name = self.driver.find_element_by_id('name').get_attribute('value')
		first_weight = self.driver.find_element_by_id('first_weight').get_attribute('value')
		first_weight_price = self.driver.find_element_by_id('first_weight_price').get_attribute('value')
		is_enable_added_weight = self.driver.find_element_by_id('is_enable_added_weight').is_selected()
		if is_enable_added_weight:
			added_weight = self.driver.find_element_by_id('added_weight').get_attribute('value')
			added_weight_price = self.driver.find_element_by_id('added_weight_price').get_attribute('value')
		else:
			added_weight = ''
			added_weight_price = ''

		return {
			'name': name,
			'first_weight': first_weight,
			'first_weight_price': first_weight_price,
			'is_enable_added_weight': is_enable_added_weight,
			'added_weight': added_weight,
			'added_weight_price': added_weight_price
		}

	#***********************************************************************************
	# delete: 点击“删除”按钮
	#***********************************************************************************
	def delete(self):
		self.driver.find_element_by_id('deleteBtn').click()
		time.sleep(WAIT_SHORT_TIME)
		self.driver.find_elements_by_css_selector('.tx_submit')[0].click()
		time.sleep(WAIT_SHORT_TIME)

	#***********************************************************************************
	# submit: 点击“提交”按钮
	#***********************************************************************************
	def submit(self):
		self.driver.find_element_by_id('submitBtn').click()
