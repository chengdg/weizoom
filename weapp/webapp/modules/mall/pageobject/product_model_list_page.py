# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME
from webapp.modules.mall.pageobject.edit_product_model_page import EditProductModelPage

class ProductModelListPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		self.click_navs(u"微站", u'其他选项')
		time.sleep(WAIT_SHORT_TIME)
		
	#***********************************************************************************
	# click_add_product_model_button: 点击“添加商品规格”的按钮
	#***********************************************************************************
	def click_add_product_model_button(self):
		self.driver.find_element_by_id("x-addProductModelPropertyBtn").click()
		return EditProductModelPage(self.driver)

	#***********************************************************************************
	# enter_edit_product_model_page: 点击商品规格链接，进入商品规格编辑页面
	#***********************************************************************************
	def enter_edit_product_model_page(self, name):
		self.driver.find_element_by_link_text(name).click()
		return EditProductModelPage(self.driver)

	#***********************************************************************************
	# get_product_models: 获得商品规格集合
	#***********************************************************************************
	def get_product_models(self):
		models = []
		for el in self.driver.find_elements_by_css_selector('#productModelListTable tbody tr'):
			tds = el.find_elements_by_css_selector('td')
			
			models.append({
				'name': tds[0].text.strip(),
				'content': tds[1].text.strip()
			})

		return models

	#***********************************************************************************
	# delete_product_model: 删除商品规格
	#***********************************************************************************
	def delete_product_model(self, name):
		pass
