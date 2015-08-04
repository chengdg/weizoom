# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

from webapp.modules.mall.pageobject.webapp_page.edit_ship_address_page import WAEditShipAddressPage


class WAShipInfoPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass

	def enter_edit_ship_info_page(self, name=None):
		if not name:
			self.driver.find_element_by_css_selector('.xt-addShipAddress').click()
		else:
			self.driver.find_element_by_partial_link_text(name).click()
		edit_ship_address_page = WAEditShipAddressPage(self.driver)
		return edit_ship_address_page		

	def select_ship_info(self, ship_name):
		for el in self.driver.find_elements_by_css_selector('.xt-shipInfo'):
			name = el.find_element_by_css_selector('.xt-name').text.strip()
			if name == ship_name:
				el.find_element_by_css_selector('.xt-shipInfoSelector').click()
				time.sleep(0.2)
				break
		
	#############################################################
	# get_ship_infos: 获取收货人信息列表
	#############################################################
	def get_ship_infos(self):
		ship_infos = []
		for el in self.driver.find_elements_by_css_selector('.xt-shipInfo'):
			name = el.find_element_by_css_selector('.xt-name').text.strip()
			tel = el.find_element_by_css_selector('.xt-tel').text.strip()
			province, city, district, address = el.find_element_by_css_selector('.xt-areaAddress').text.split(' ')
			is_selected = el.find_element_by_css_selector('.xt-selectRadio').is_selected()
			ship_infos.append({
				'ship_name': name,
				'ship_tel': tel,
				'ship_area': '%s %s %s' % (province, city, district),
				'ship_address': address,
				'is_selected': is_selected
			})

		return ship_infos
