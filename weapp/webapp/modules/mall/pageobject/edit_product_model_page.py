# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

from webapp.modules.mall.pageobject.select_product_model_icon_dialog import SelectProductModelIconDialog

class EditProductModelPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	#############################################################################
	# edit_product_model: 编辑product model
	#############################################################################
	def edit_product_model(self, model):
		if 'name' in model:
			input = self.driver.find_element_by_id('name')
			input.clear()
			input.send_keys(model['name'])

		if 'type' in model:
			type = model['type']
			if type == u'文字':
				self.driver.find_elements_by_css_selector('input[name="type"]')[0].click()
			elif type == u'图片':
				self.driver.find_elements_by_css_selector('input[name="type"]')[1].click()
			else:
				pass

		if not 'values' in model:
			return

		add_value_button = self.driver.find_element_by_css_selector('.xa-addValueBtn')
		table = self.driver.find_element_by_css_selector('tbody')
		for value in model['values']:
			if 'original_name' in value:
				#update
				for tr in table.find_elements_by_css_selector('tr'):
					input = tr.find_elements_by_css_selector('td')[0].find_element_by_tag_name('input')
					if input.get_attribute('value') == value['original_name']:
						input.clear()
						input.send_keys(value['name'])

						#选择图片
						if 'image' in value:
							try:
								trigger = tr.find_element_by_css_selector('.xa-selectIcon')
							except:
								trigger = tr.find_element_by_css_selector('.xa-changeIcon')
							trigger.click()
							time.sleep(WAIT_SHORT_TIME)
							dialog = SelectProductModelIconDialog(self.driver)
							dialog.select_uploaded_image(value['image'])
							time.sleep(0.5)

						break
			else:
				#add
				add_value_button.click()
				time.sleep(0.5)
				tr = table.find_elements_by_css_selector('tr')[-1]
				input = tr.find_element_by_css_selector('input[type="text"]')
				input.clear()
				input.send_keys(value['name'])

				#选择图片
				if 'image' in value:
					tr.find_element_by_css_selector('.xa-selectIcon').click()
					time.sleep(WAIT_SHORT_TIME)
					dialog = SelectProductModelIconDialog(self.driver)
					dialog.select_uploaded_image(value['image'])
					time.sleep(0.5)


	#############################################################################
	# update_product_model: 更新product model
	#############################################################################
	def update_product_model(self, model):
		self.edit_product_model(model)


	#############################################################################
	# get_product_model: 获取商品规格
	#############################################################################
	def get_product_model(self):
		name = self.driver.find_element_by_id('name').get_attribute('value')
		
		for label in self.driver.find_elements_by_css_selector('label.radio'):
			if label.find_element_by_css_selector('input').is_selected():
				type = label.text.strip()

		values = []
		trs = self.driver.find_elements_by_css_selector('tbody tr')
		for tr in trs:
			tds = tr.find_elements_by_css_selector('td')
			image = tds[1].find_element_by_tag_name('img').get_attribute('src')
			if image:
				image = 'valid'
			else:
				image = None

			value_name = tds[0].find_element_by_tag_name('input').get_attribute('value').strip()
			values.append({
				'name': value_name,
				'image': image
			})


		return {
			'name': name,
			'type': type,
			'values': values
		}

	#***********************************************************************************
	# delete_model_property: 删除model property
	#***********************************************************************************
	def delete_model_property(self, property_value):
		trs = self.driver.find_elements_by_css_selector('tbody tr')
		for tr in trs:
			tds = tr.find_elements_by_css_selector('td')
			value = tds[0].find_element_by_tag_name('input').get_attribute('value').strip()
			if value == property_value:
				tr.find_element_by_css_selector('.xa-removeValueBtn').click()
				time.sleep(0.5)

		self.submit()


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

		from webapp.modules.mall.pageobject.product_model_list_page import ProductModelListPage
		return ProductModelListPage(self.driver)
