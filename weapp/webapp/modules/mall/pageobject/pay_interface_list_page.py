# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from selenium.common.exceptions import NoSuchElementException

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME
from webapp.modules.mall.pageobject.edit_postage_page import EditPostagePage
from webapp.modules.mall.pageobject.edit_pay_interface_page import EditPayInterfacePage

class PayInterfaceListPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		self.click_navs(u"微站", u'其他选项')
		time.sleep(WAIT_SHORT_TIME)
		
	#***********************************************************************************
	# click_add_pay_interface_button: 点击“添加支付接口”的按钮
	#***********************************************************************************
	def click_add_pay_interface_button(self):
		self.driver.find_element_by_id("x-addPayInterfaceBtn").click()
		return EditPayInterfacePage(self.driver)

	#***********************************************************************************
	# enter_edit_pay_interface_page: 点击支付方式链接，进入支付方式编辑页面
	#***********************************************************************************
	def enter_edit_pay_interface_page(self, postage_config_name):
		self.driver.find_element_by_link_text(postage_config_name).click()
		return EditPayInterfacePage(self.driver)

	#***********************************************************************************
	# can_add_pay_interface: 能添加新的支付方式
	#***********************************************************************************
	def can_add_pay_interface(self):
		try:
			self.driver.find_element_by_id("x-addPayInterfaceBtn")
		except NoSuchElementException:
			return False
		return True

	#***********************************************************************************
	# get_pay_interfaces: 获得支付接口集合
	#***********************************************************************************
	def get_pay_interfaces(self):
		postage_configs = []
		for el in self.driver.find_elements_by_css_selector('#payInterfaceListTable tbody tr'):
			tds = el.find_elements_by_css_selector('td')

			img_src = tds[0].find_element_by_css_selector('img').get_attribute('src')
			if 'alipay' in img_src:
				type = u'支付宝'
			elif 'cod' in img_src:
				type = u'货到付款'
			elif 'weixin_pay' in img_src:
				type = u'微信支付'
			else:
				type = 'unknown'
			
			postage_configs.append({
				'type': type,
				'name': tds[1].text,
				'is_active': (tds[2].text.strip() == u'开启')
			})

		return postage_configs

	#***********************************************************************************
	# delete_pay_interface: 删除支付接口
	#***********************************************************************************
	def delete_pay_interface(self, name):
		account_delete_button = None
		for el in self.driver.find_elements_by_css_selector('#postageListTable tbody tr'):
			tds = el.find_elements_by_css_selector('td')
			if name == tds[0].text:
				account_delete_button = el.find_elements_by_css_selector('a.btn-danger')[0]
				break

		if account_delete_button:
			account_delete_button.click()
		
		time.sleep(WAIT_SHORT_TIME)
