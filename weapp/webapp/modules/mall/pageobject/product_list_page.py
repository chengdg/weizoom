# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME
from webapp.modules.mall.pageobject.edit_product_page import EditProductPage

class ProductListPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		self.click_navs(u"微站", u"商品列表")
		time.sleep(WAIT_SHORT_TIME)
		
	#***********************************************************************************
	# click_add_product_button: 点击“添加商品”的按钮
	#***********************************************************************************
	def click_add_product_button(self):
		self.driver.find_element_by_id("addProductBtn").click()
		return EditProductPage(self.driver)

	#***********************************************************************************
	# enter_edit_product_page: 点击商品名链接，进入商品编辑页面
	#***********************************************************************************
	def enter_edit_product_page(self, product_name):
		self.driver.find_element_by_link_text(product_name).click()
		return EditProductPage(self.driver)

	#***********************************************************************************
	# sort_product: 对商品进行排序
	#***********************************************************************************
	def sort_product(self, product_name, direction):
		trs = self.driver.find_elements_by_css_selector('tbody tr')
		for tr in trs:
			td = tr.find_elements_by_css_selector('td')[1]
			if product_name == td.text:
				button = tr.find_element_by_css_selector('[data-direction="'+direction+'"]')
				button.click()
				time.sleep(WAIT_SHORT_TIME)
				break

	#***********************************************************************************
	# set_product_to_top: 置顶商品
	#***********************************************************************************
	def set_product_to_top(self, product_name):
		trs = self.driver.find_elements_by_css_selector('tbody tr')
		for tr in trs:
			td = tr.find_elements_by_css_selector('td')[1]
			if product_name == td.text:
				button = tr.find_element_by_css_selector('[data-direction="top"]')
				button.click()
				time.sleep(WAIT_SHORT_TIME)
				break


	#***********************************************************************************
	# get_products: 获得商品集合
	#***********************************************************************************
	def get_products(self):
		products = []
		for el in self.driver.find_elements_by_css_selector('tbody#product_list tr'):
			tds = el.find_elements_by_css_selector('td')
			
			products.append({
				'thumbnails_url': tds[0].find_element_by_tag_name('img').get_attribute('src'),
				'name': tds[1].text,
				'category': tds[2].text,
				'price': tds[3].text
			})

		return products
