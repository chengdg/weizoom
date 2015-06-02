# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

class EditPayInterfacePage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver


	###################################################################################
	# add_pay_interface: 添加支付接口
	###################################################################################
	def add_pay_interface(self, config):
		if config.get('is_active', None) == u'停用':
			self.driver.find_elements_by_css_selector('input[name="is_active"]')[1].click()

		if config['type'] == u'微信支付':
			self.add_weixinpay_interface(config)
		elif config['type'] == u'支付宝':
			self.add_alipay_interface(config)
		elif config['type'] == u'货到付款':
			self.add_cod_interface(config)
		else:
			pass

	###################################################################################
	# active_pay_interface: 启用支付接口
	###################################################################################
	def active_pay_interface(self):
		self.driver.find_elements_by_css_selector('input[name="is_active"]')[0].click()
		self.submit()


	###################################################################################
	# inactive_pay_interface: 停用支付接口
	###################################################################################
	def inactive_pay_interface(self):
		self.driver.find_elements_by_css_selector('input[name="is_active"]')[1].click()
		self.submit()


	###################################################################################
	# get_pay_interface: 获得支付接口信息
	###################################################################################
	def get_pay_interface(self):
		type = self.driver.find_element_by_css_selector('select').get_attribute('value')
		if type == '2':
			type = u'微信支付'
		elif type == '0':
			type = u'支付宝'
		elif type == '9':
			type = u'货到付款'
		else:
			pass

		if type == u'微信支付':
			result = self.get_weixinpay_interface()
		elif type == u'支付宝':
			result = self.get_alipay_interface()
		elif type == u'货到付款':
			result = self.get_cod_interface()
		else:
			pass

		result['type'] = type
		is_active = u'启用' if self.driver.find_elements_by_css_selector('input[name="is_active"]')[0].is_selected() else u'停用'
		result['is_active'] = is_active
		return result


	###################################################################################
	# add_alipay_interface: 添加“支付宝”接口
	###################################################################################
	def add_alipay_interface(self, config):
		time.sleep(WAIT_SHORT_TIME)
		driver = self.driver

		xpath = u"//select/option[text()='{}']".format(u'支付宝')
		self.driver.find_element_by_xpath(xpath).click()

		name_input = driver.find_element_by_css_selector('#generalConfig #description')
		name_input.clear()
		name_input.send_keys(config['description'])

		partner_input = driver.find_element_by_css_selector('#alipayConfig #partner')
		partner_input.clear()
		partner_input.send_keys(config['partner'])

		key_input = driver.find_element_by_css_selector('#alipayConfig #key')
		key_input.clear()
		key_input.send_keys(config['key'])

		ali_public_key_input = driver.find_element_by_css_selector('#alipayConfig #ali_public_key')
		ali_public_key_input.clear()
		ali_public_key_input.send_keys(config['ali_public_key'])

		private_key_input = driver.find_element_by_css_selector('#alipayConfig #private_key')
		private_key_input.clear()
		private_key_input.send_keys(config['private_key'])

		seller_email_input = driver.find_element_by_css_selector('#alipayConfig #seller_email')
		seller_email_input.clear()
		seller_email_input.send_keys(config['seller_email'])


	###################################################################################
	# get_alipay_interface: 获得“支付宝”接口
	###################################################################################
	def get_alipay_interface(self):
		driver = self.driver
		description = driver.find_element_by_css_selector('#generalConfig #description').get_attribute('value')
		partner = driver.find_element_by_css_selector('#alipayConfig #partner').get_attribute('value')
		key = driver.find_element_by_css_selector('#alipayConfig #key').get_attribute('value')
		ali_public_key = driver.find_element_by_css_selector('#alipayConfig #ali_public_key').get_attribute('value')
		private_key = driver.find_element_by_css_selector('#alipayConfig #private_key').get_attribute('value')
		seller_email = driver.find_element_by_css_selector('#alipayConfig #seller_email').get_attribute('value')
		
		return {
			'description': description,
			'partner': partner,
			'key': key,
			'ali_public_key': ali_public_key,
			'private_key': private_key,
			'seller_email': seller_email
		}


	###################################################################################
	# add_cod_interface: 添加“货到付款”接口
	###################################################################################
	def add_cod_interface(self, config):
		time.sleep(WAIT_SHORT_TIME)
		driver = self.driver

		xpath = u"//select/option[text()='{}']".format(u'货到付款')
		self.driver.find_element_by_xpath(xpath).click()

		name_input = driver.find_element_by_css_selector('#generalConfig #description')
		name_input.clear()
		name_input.send_keys(config['description'])


	###################################################################################
	# get_cod_interface: 获得“货到付款”接口
	###################################################################################
	def get_cod_interface(self):
		driver = self.driver
		description = driver.find_element_by_css_selector('#generalConfig #description').get_attribute('value')

		return {
			'description': description
		}


	###################################################################################
	# add_weixinpay_interface: 添加“微信支付”接口
	###################################################################################
	def add_weixinpay_interface(self, config):
		time.sleep(WAIT_SHORT_TIME)
		driver = self.driver

		xpath = u"//select/option[text()='{}']".format(u'微信支付')
		self.driver.find_element_by_xpath(xpath).click()

		name_input = driver.find_element_by_css_selector('#generalConfig #description')
		name_input.clear()
		name_input.send_keys(config['description'])

		app_id_input = driver.find_element_by_css_selector('#weixinPayConfig #app_id')
		app_id_input.clear()
		app_id_input.send_keys(config['weixin_appid'])

		partner_id_input = driver.find_element_by_css_selector('#weixinPayConfig #partner_id')
		partner_id_input.clear()
		partner_id_input.send_keys(config['weixin_partner_id'])

		partner_key_input = driver.find_element_by_css_selector('#weixinPayConfig #partner_key')
		partner_key_input.clear()
		partner_key_input.send_keys(config['weixin_partner_key'])

		paysign_key_input = driver.find_element_by_css_selector('#weixinPayConfig #paysign_key')
		paysign_key_input.clear()
		paysign_key_input.send_keys(config['weixin_sign'])


	###################################################################################
	# get_weixinpay_interface: 获得“微信支付”接口
	###################################################################################
	def get_weixinpay_interface(self):
		driver = self.driver

		type = driver.find_element_by_css_selector('select').get_attribute('value')
		description = driver.find_element_by_css_selector('#generalConfig #description').get_attribute('value')
		weixin_appid = driver.find_element_by_css_selector('#weixinPayConfig #app_id').get_attribute('value')
		weixin_partner_id = driver.find_element_by_css_selector('#weixinPayConfig #partner_id').get_attribute('value')
		weixin_partner_key = driver.find_element_by_css_selector('#weixinPayConfig #partner_key').get_attribute('value')
		weixin_sign = driver.find_element_by_css_selector('#weixinPayConfig #paysign_key').get_attribute('value')

		return {
			"type": type,
			"description": description,
			"weixin_appid": weixin_appid,
			"weixin_partner_id": weixin_partner_id,
			"weixin_partner_key": weixin_partner_key,
			"weixin_sign": weixin_sign
		}


	#***********************************************************************************
	# delete: 点击“删除”按钮
	#***********************************************************************************
	def delete(self):
		self.driver.find_element_by_id('deleteBtn').click()
		self.driver.find_element_by_css_selector('.tx_submit').click()
		time.sleep(WAIT_SHORT_TIME)


	#***********************************************************************************
	# submit: 点击“提交”按钮
	#***********************************************************************************
	def submit(self):
		self.driver.find_element_by_id('submitBtn').click()
