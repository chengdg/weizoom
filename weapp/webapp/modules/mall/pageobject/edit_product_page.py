# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.pageobject.image_view import ImageView
from test.helper import WAIT_SHORT_TIME

from webapp.modules.mall.pageobject.webapp_page.upload_swipe_image_dialog import UploadSwipeImageDialog

class EditProductPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver
		self.thumbnail_image_view = ImageView(webdriver, '.x-thumbnailUrl')
		self.image_view = ImageView(webdriver, '.x-picUrl')

	def get_product_content(self):
		driver = self.driver
		name = driver.find_element_by_id("name").get_attribute('value')
		physical_unit = driver.find_element_by_id("physical_unit").get_attribute('value')
		thumbnails_url = driver.find_element_by_id("thumbnails_url").get_attribute('value')
		remark = driver.find_element_by_id('remark').get_attribute('value')

		#获取上下架信息
		shelve_type = ''
		for el in driver.find_elements_by_css_selector('input[name="shelve_type"]'):
			if el.is_selected():
				value = el.get_attribute('value')
				if value == '1':
					shelve_type = u'上架'
				else:
					shelve_type = u'下架'

		#获取富文本编辑器中内容
		driver.switch_to_frame(0);
		body = driver.find_element_by_tag_name("body")
		detail = body.text
		driver.switch_to_default_content()

		#获取分类信息
		category = ''
		for el in driver.find_elements_by_css_selector('.xui-category'):
			if el.find_element_by_css_selector('input').is_selected():
				category = el.text.strip()

		#获取规格信息
		is_enable_custom_model = False
		checkbox = driver.find_element_by_css_selector('input[name="is_use_custom_model"]')
		if checkbox.is_selected():
			#定制规格
			is_enable_custom_model = True
		else:
			#标准规格
			price = float(driver.find_element_by_id("price").get_attribute('value'))
			weight = float(driver.find_element_by_id("weight").get_attribute('value'))
			#获取库存信息
			stocks = 0
			stock_type = ''
			for el in driver.find_elements_by_css_selector('input[name="stock_type"]'):
				if el.is_selected():
					value = el.get_attribute('value')
					if value == '0':
						stock_type = u'无限'
					else:
						stock_type = u'有限'
						stocks = int(driver.find_element_by_css_selector('.xa-stockCount').get_attribute('value'))

		result = {
			'name': name,
			'physical_unit': physical_unit,
		    'thumbnails_url': thumbnails_url,
		    #'pic_url': pic_url,
			'detail': detail,
			'category': category,
			'shelve_type': shelve_type,
			'is_enable_model': u'启用规格' if is_enable_custom_model else u'不启用规格',
			"is_use_custom_model": u"否",
			'remark': remark,
			'model': {
				'models': {
					
				}
			}
		}
		if is_enable_custom_model:
			trs = self.driver.find_elements_by_css_selector('.xa-customModelTable tbody tr')
			for tr in trs:
				tds = tr.find_elements_by_css_selector('td')
				items = []
				for name_td in tds[0:-5]:
					items.append(name_td.text.strip())
				name = u' '.join(items)
				weight = float(tds[-5].find_element_by_tag_name('input').get_attribute('value'))
				market_price = float(tds[-4].find_element_by_tag_name('input').get_attribute('value'))
				price = float(tds[-3].find_element_by_tag_name('input').get_attribute('value'))

				#获取库存信息
				stocks = 0
				labels = tds[-2].find_elements_by_css_selector('label')
				for label in labels:
					if label.find_element_by_tag_name('input').is_selected():
						stock_type = label.text.strip()
				if stock_type == u'有限':
					stocks = int(tds[-2].find_element_by_css_selector('.xa-stockCount').get_attribute('value'))

				result['model']['models'][name] = {
					'market_price': market_price,
					'price': price,
					'weight': weight,
					'stock_type': stock_type,
					'stocks': stocks
				}
		else:
			result['model']['models']['standard'] = {
				'price': price,
				'weight': weight,
				'stock_type': stock_type,
				'stocks': stocks
			}

		return result

	#***********************************************************************************
	# __input_detail: 在富文本编辑器中输入文本
	#***********************************************************************************
	def __input_detail(self, text):
		driver = self.driver
		driver.switch_to_frame(0);
		body = driver.find_element_by_tag_name("body")
		body.clear()
		body.click()
		body.send_keys(text)
		body.click()
		driver.switch_to_default_content()
		time.sleep(1)

	#***********************************************************************************
	# submit_product: 提交商品
	#***********************************************************************************
	def submit_product(self, args, url2uploaded_url={}):
		driver = self.driver

		if 'model' in args:
			model = args['model']['models']['standard']
			price = str(model.get('price', ''))
			weight = str(model.get('weight', ''))
			stock_type = model.get('stock_type', u'无限')
			stocks = str(model.get('stocks', '0'))
		else:
			if 'is_from_update' in args:
				price = None
				weight = None
				stock_type = None
				stocks = None
			else:
				price = ''
				weight = ''
				stock_type = u'无限'
				stocks = '0'
		
		name = args.get('name', '')
		category = args.get('category', '')
		physical_unit = args.get('physical_unit', '')
		#introduction = args.get('introduction', '')
		shelve_type = args.get('shelve_type', u'上架')
		detail = args.get('detail', '')
		thumbnails_url = args.get('thumbnails_url', '')
		swipe_images = args.get('swipe_images', '')
		remark = args.get('remark', '')

		#输入name
		if name:
			input = driver.find_element_by_id("name")
			input.clear()
			input.send_keys(name)

		#选择category
		if category:
			for el in driver.find_elements_by_css_selector('.xui-category'):
				if el.text.strip() == category:
					el.click()

		#输入physical_unit
		if physical_unit:
			input = driver.find_element_by_id("physical_unit")
			input.click()
			input.clear()
			input.send_keys(physical_unit)

		#输入上下架信息
		if shelve_type == u'下架':
			input = driver.find_elements_by_css_selector('input[name="shelve_type"]')[1]
			input.click()
		else:
			input = driver.find_elements_by_css_selector('input[name="shelve_type"]')[0]
			input.click()

		#输入weight
		if weight:
			input = driver.find_element_by_id("weight")
			input.click()
			input.clear()
			input.send_keys(weight)

		#输入price
		if price:
			input = driver.find_element_by_id("price")
			input.click()
			input.clear()
			input.send_keys(price)

		#输入stock_type和stocks
		if stock_type == u'有限':
			radio = driver.find_elements_by_css_selector('input[name="stock_type"]')[1]
			radio.click()
			input = driver.find_element_by_css_selector('.xa-stockCount')
			input.click()
			input.clear()
			input.send_keys(stocks)

		if remark:
			input = driver.find_element_by_id('remark')
			input.click()
			input.clear()
			input.send_keys(remark)

		#输入introduction
		# if introduction:
		# 	input = driver.find_element_by_id("introduction")
		# 	input.click()
		# 	input.clear()
		# 	input.send_keys(introduction)

		#上传图片
		if thumbnails_url:
			image_url = ''
			image_url = self.thumbnail_image_view.upload_image(thumbnails_url)
			self.thumbnail_image_view.show_image(image_url)
			url2uploaded_url['thumbnails_url_'+thumbnails_url] = image_url

		#swipe_image_urls = []
		pic_url = ''
		if swipe_images:
			pic_url = swipe_images[0]['url']
			driver.find_element_by_id('swipeImageList-addBtn').click()
			upload_swipe_image_dialog = UploadSwipeImageDialog(driver)
			upload_swipe_image_dialog.load()
			image_url = upload_swipe_image_dialog.upload_image(pic_url)
			#swipe_image_urls.append(image_url)
			#url2uploaded_url['pic_url_'+pic_url] = image_url

		#输入detail
		if detail:
			self.__input_detail(detail)

		self.submit()
		time.sleep(1)

		return {
			'thumbnails_url': thumbnails_url,
			'pic_url': pic_url
		}

	def update_product(self, args, url2uploaded_url={}):
		args['is_from_update'] = True
		self.submit_product(args, url2uploaded_url)

	#***********************************************************************************
	# get_stock_info: 获得库存信息
	#***********************************************************************************
	def get_stock_info(self):
		stock_type = None
		radio = None
		for el in self.driver.find_elements_by_css_selector('.x-stockTypeRadio'):
			if el.is_selected():
				radio = el
				stock_type = el.get_attribute('value')

		if stock_type == '0':
			return {
				'type': u'无限',
				'count': '0'
			}
		else:
			stock = self.driver.find_element_by_css_selector('.xa-stockCount').get_attribute('value')
			return {
				'type': u'有限',
				'count': stock
			}

	#***********************************************************************************
	# input_stock_info: 获得库存信息
	#***********************************************************************************
	def input_stock_info(self, options):
		driver = self.driver
		stock_type = options['type']
		if stock_type == u'无限':
			driver.find_element_by_css_selector('input.x-stockTypeRadio[value="0"]').click()
		else:
			radio = driver.find_element_by_css_selector('input.x-stockTypeRadio[value="1"]')
			radio.click()
			time.sleep(WAIT_SHORT_TIME)
			count_input = driver.find_element_by_css_selector('.xa-stockCount')
			count_input.clear()
			count_input.send_keys(options['count'])

		
	#***********************************************************************************
	# delete: 点击“删除”按钮
	#***********************************************************************************
	def delete(self):
		self.driver.find_element_by_css_selector('.btn-delete').click()
		time.sleep(WAIT_SHORT_TIME)

	#***********************************************************************************
	# submit: 点击“提交”按钮
	#***********************************************************************************
	def submit(self):
		self.driver.find_element_by_id('submitBtn').click()
		from webapp.modules.mall.pageobject.product_list_page import ProductListPage
		return ProductListPage(self.driver)
