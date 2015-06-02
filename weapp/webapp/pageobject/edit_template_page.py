# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

class EditTemplatePage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		time.sleep(5) #等待加载完成

	#***********************************************************************************
	# __select_workspace: 从下拉列表中选择一个workspace
	#***********************************************************************************
	def __select_workspace(self, workspace):
		xpath = u"//select[@name='workspace']/option[text()='{}']".format(workspace)
		self.driver.find_element_by_xpath(xpath).click()

	#***********************************************************************************
	# __select_data_category: 从下拉列表中选择一个data category
	#***********************************************************************************
	def __select_data_category(self, data_category):
		xpath = u"//select[@name='data_category']/option[text()='{}']".format(data_category)
		self.driver.find_element_by_xpath(xpath).click()

	#***********************************************************************************
	# __select_data: 从单选列表中选中一个具体的数据
	#***********************************************************************************
	def __select_data(self, data):
		for el in self.driver.find_elements_by_css_selector('div.x-dataContent label'):
			if data == el.text:
				el.find_element_by_css_selector('input[type="radio"]').click()

	#***********************************************************************************
	# __select_target_link: 选择链接目标
	#***********************************************************************************
	def __select_target_link(self, el, workspace, data_category, data):
		el.click()
		time.sleep(WAIT_SHORT_TIME)
		el.find_element_by_css_selector('[data-target-dialog="W.dialog.workbench.SelectLinkTargetDialog"]').click()
		time.sleep(WAIT_SHORT_TIME)
		self.__select_workspace(workspace)
		time.sleep(WAIT_SHORT_TIME)
		self.__select_data_category(data_category)
		time.sleep(WAIT_SHORT_TIME)
		self.__select_data(data)
		time.sleep(WAIT_SHORT_TIME)
		self.driver.find_element_by_css_selector('.modal-footer .btn-submit').click()
		time.sleep(WAIT_SHORT_TIME)

	def __select_listview_nav_targets(self):
		driver = self.driver
		driver.switch_to_frame(0);
		listview = driver.find_element_by_css_selector('.ui-listview')
		listview.click()
		driver.switch_to_default_content()

		#确定各个nav grid的激活元素
		mall_el = None
		user_center_el = None
		cms_el = None
		for el in self.driver.find_elements_by_css_selector('.propertyGroup_property_dynamicControlField_control'):
			title_el = el.find_element_by_css_selector('.propertyGroup_property_dynamicControlField_title')
			nav_title = title_el.text.strip()
			if nav_title == u'春装专场':
				mall_el = el
			elif nav_title == u'清凉夏风':
				user_center_el = el

		#选择各个导航按钮的链接目标
		self.__select_target_link(mall_el, u'微商城', u'页面', u'商品列表页')
		self.__select_target_link(user_center_el, u'用户中心', u'页面', u'用户中心页面')

	def __select_icon_nav_targets(self):
		driver = self.driver
		driver.switch_to_frame(0);
		grid = driver.find_element_by_css_selector(".x-ui-grid li a")
		grid.click()
		driver.switch_to_default_content()

		#确定各个nav grid的激活元素
		user_center_el = None
		shopping_cart_el = None
		for el in self.driver.find_elements_by_css_selector('.propertyGroup_property_dynamicControlField_control'):
			title_el = el.find_element_by_css_selector('.propertyGroup_property_dynamicControlField_title')
			nav_title = title_el.text.strip()
			if nav_title == u'用户中心':
				user_center_el = el
			elif nav_title == u'购物车':
				shopping_cart_el = el
			else:
				pass

		#选择各个导航按钮的链接目标
		self.__select_target_link(user_center_el, u'用户中心', u'页面', u'用户中心页面')
		
	#***********************************************************************************
	# select_nav_targets: 选择nav grid组件的目标页面
	#***********************************************************************************
	def select_nav_targets(self):
		driver = self.driver
		self.__select_listview_nav_targets()
		self.__select_icon_nav_targets()

		#保存页面
		driver.find_element_by_id('saveMobilePageBtn').click()
		time.sleep(WAIT_SHORT_TIME*2)