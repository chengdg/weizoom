# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME


class WAEditShipAddressPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass

	#############################################################
	# get_ship_info: 获取收货人信息
	#############################################################
	def get_ship_info(self):
		name = self.driver.find_element_by_id('ship_name').get_attribute('value')
		address = self.driver.find_element_by_id('ship_address').get_attribute('value')
		tel = self.driver.find_element_by_id('ship_tel').get_attribute('value')

		area = self.driver.find_element_by_css_selector('.xa-openSelect').text.strip()
		province, city, district = area.split(' ')

		return {
			'name': name,
			'province': province,
			'city': city,
			'district': district,
			'address': address,
			'tel': tel
		}


	#############################################################
	# input_ship_info: 输入收货人信息
	#############################################################
	def input_ship_info(self, ship_info, force=False):
		driver = self.driver

		name_input = driver.find_element_by_id('ship_name')
		name = name_input.get_attribute('value').strip()
		if len(name) > 0 and not force:
			#no need to input ship info
			return
		name_input.clear()
		name_input.send_keys(ship_info['ship_name'])

		address_input = self.driver.find_element_by_id('ship_address')
		address_input.clear()
		address_input.send_keys(ship_info['ship_address'])

		tel_input = self.driver.find_element_by_id('ship_tel')
		tel_input.clear()
		tel_input.send_keys(ship_info['ship_tel'])

		#选择省市
		province, city, district = ship_info['ship_area'].split(' ')
		self.driver.find_element_by_css_selector('.xa-openSelect').click()
		time.sleep(0.5)
		for el in self.driver.find_elements_by_css_selector('#areaWidget-province .liInner'):
			if el.text.strip() == province:
				el.click()

		time.sleep(0.5)
		for el in self.driver.find_elements_by_css_selector('#areaWidget-city .liInner'):
			if el.text.strip() == city:
				el.click()

		time.sleep(0.5)
		for el in self.driver.find_elements_by_css_selector('#areaWidget-district .liInner'):
			if el.text.strip() == district:
				el.click()


	#############################################################
	# click_submit_button: 点击“提交”按钮
	#############################################################
	def click_submit_button(self):
		self.driver.find_element_by_css_selector('.xa-submit').click()
		time.sleep(0.5)