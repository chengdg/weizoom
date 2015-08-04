# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

class EditCategoryPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	#***********************************************************************************
	# add_category: 添加分类
	#***********************************************************************************
	def add_category(self, name, product_names=[]):
		name_input = self.driver.find_element_by_id('name')
		name_input.clear()
		name_input.send_keys(name)

		if product_names:
			self.select_products(product_names)

	#***********************************************************************************
	# get_category_name: 获取分类名
	#***********************************************************************************
	def get_category_name(self):
		name_input = self.driver.find_element_by_id('name')
		return name_input.get_attribute('value')

	#***********************************************************************************
	# get_category_products: 获取分类商品集合
	#***********************************************************************************
	def get_category_products(self):
		products = []
		for el in self.driver.find_elements_by_css_selector('tbody#product_list tr'):
			checkbox = el.find_element_by_tag_name('input')
			tds = el.find_elements_by_css_selector('td')
			name = tds[2].text
			products.append({
				'name': name,
				'is_selected': checkbox.is_selected()
			})

		return products

	#***********************************************************************************
	# select_products: 选择一批商品
	#***********************************************************************************
	def select_products(self, product_names):
		for el in self.driver.find_elements_by_css_selector('tbody#product_list tr'):
			checkbox = el.find_element_by_tag_name('input')
			tds = el.find_elements_by_css_selector('td')
			if tds[2].text in product_names:
				checkbox.click()

	#***********************************************************************************
	# unselect_products: 取消对一批商品的选中
	#***********************************************************************************
	def unselect_products(self, product_names):
		#select之后再次select，即为unselect
		self.select_products(product_names)

	#***********************************************************************************
	# delete: 删除分类
	#***********************************************************************************
	def delete(self):
		self.driver.find_elements_by_css_selector('a.btn-danger')[0].click()

	#***********************************************************************************
	# submit: 点击“提交”按钮
	#***********************************************************************************
	def submit(self):
		self.driver.find_element_by_id('submitBtn').click()
