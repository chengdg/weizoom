# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME
from webapp.modules.mall.pageobject.edit_category_page import EditCategoryPage

class CategoryListPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		self.click_navs(u"微站", u"商品分类")
		time.sleep(WAIT_SHORT_TIME)
		
	#***********************************************************************************
	# click_add_category_button: 点击“添加分类”的按钮
	#***********************************************************************************
	def click_add_category_button(self):
		self.driver.find_elements_by_css_selector("span.breadcrumRightButton a")[0].click()
		return EditCategoryPage(self.driver)

	#***********************************************************************************
	# enter_category_edit_page: 点击分类链接，进入分类编辑页面
	#***********************************************************************************
	def enter_category_edit_page(self, category_name):
		self.driver.find_element_by_link_text(category_name).click()
		return EditCategoryPage(self.driver)

	#***********************************************************************************
	# get_categories: 获得分类集合
	#***********************************************************************************
	def get_categories(self):
		categories = []
		for el in self.driver.find_elements_by_css_selector('#categoryListTable tbody tr'):
			tds = el.find_elements_by_css_selector('td')
			
			categories.append({
				'name': tds[0].text,
				'product_count': int(tds[1].text)
			})

		return categories

	#***********************************************************************************
	# delete_category: 删除分类
	#***********************************************************************************
	def delete_category(self, name):
		account_delete_button = None
		for el in self.driver.find_elements_by_css_selector('#accountListTable tbody tr'):
			tds = el.find_elements_by_css_selector('td')
			if name == tds[0].text:
				account_delete_button = el.find_elements_by_css_selector('a.btn-danger')[0]
				break

		if account_delete_button:
			account_delete_button.click()
		
		time.sleep(WAIT_SHORT_TIME)
