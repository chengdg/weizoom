# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

from webapp.modules.mall.pageobject.webapp_page.pay_order_page import WAPayOrderPage
from webapp.modules.mall.pageobject.webapp_page.pay_interface_list_page import WAPayInterfaceListPage
from webapp.modules.mall.pageobject.webapp_page.pay_result_page import WAPayResultPage
from webapp.modules.user_center.pageobject.webapp_page.ship_info_page import WAShipInfoPage

from mall.promotion.models import Coupon

class WAEditOrderPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass

	#############################################################
	# get_products: 获取商品列表
	#############################################################
	def get_product_groups(self):
		product_groups = []
		for product_group_el in self.driver.fs('.xt-productGroup'):
			#获取商品集合
			products = []
			for product_el in product_group_el.fs('.xt-product'):
				name = product_el.f('.xt-name').text.strip()
				price = float(product_el.f('.xt-price').text.strip())
				purchase_count = int(product_el.f('.xt-count').text.strip())
				try:
					model = product_el.f('.xt-model').text.strip()
				except:
					model = ''
				products.append({
					'name': name,
					'model': model,
					'price': price,
					'count': purchase_count
				})

			#获取促销信息
			promotion = None
			try:
				promotion_el = product_group_el.f('.xt-promotion')
				promotion_type = promotion_el.f('.xt-promotionType').text
				if u'满减' in promotion_type:
					promotion_type = 'price_cut'
					price = promotion_el.f('.xt-price').text
					cut_money = promotion_el.f('.xt-cutMoney').text
					promotion = {
						"type": promotion_type,
						"result": {
							"price": price,
							"cut_money": cut_money
						}
					}
				elif u'买赠' in promotion_type:
					premium_products = []
					for premium_product_el in promotion_el.fs('.xt-premiumProduct'):
						try:
							stock_info = premium_product_el.f('.xt-stockInfo').text
						except:
							stock_info = ''
						premium_products.append({
							"name": premium_product_el.f('.xt-name').text,
							"count": premium_product_el.f('.xt-count').text,
							'stock_info': stock_info
						})
					promotion = {
						"type": 'premium_sale',
						"result": {
							"premium_products": premium_products
						}
					}
				elif u'积分' in promotion_type:
					try:
						usable_integral = promotion_el.f('.xt-usableIntegral').text
					except:
						usable_integral = 0
					try:
						total_integral = promotion_el.f('.xt-totalIntegral').text
					except:
						total_integral = 0
					try:
						used_integral = promotion_el.f('.xt-usedIntegral').text
					except:
						used_integral = 0
					money = promotion_el.f('.xt-money').text
					promotion = {
						"type": 'integral_sale',
						"result": {
							"usable_integral": usable_integral,
							"total_integral": total_integral,
							"used_integral": used_integral,
							"money": money
						}
					}
			except:
				promotion = None

			#获取小计
			try:
				subtotal = {
					"money": product_group_el.f('.xt-subtotal').text,
					"count": product_group_el.f('.xt-subtotalCount').text
				}
			except:
				subtotal = None


			product_groups.append({
				'products': products,
				'promotion': promotion,
				'subtotal': subtotal
			})

		return product_groups

	#############################################################
	# get_total_price: 获取订单总价
	#############################################################
	def get_total_price(self):
		return self.driver.find_element_by_css_selector('.xt-totalPrice').text.strip()

	def __find_group(self, name):
		for el in self.driver.find_elements_by_css_selector('.xt-triggerGroup'):
			if name in el.text:
				return el

	#############################################################
	# get_ship_info: 获取收货人信息
	#############################################################
	def get_ship_info(self):
		name = self.driver.find_element_by_css_selector('.xt-shipName').text.strip()
		address = self.driver.find_element_by_css_selector('.xt-shipAddress').text.strip()
		tel = self.driver.find_element_by_css_selector('.xt-shipTel').text.strip()

		province, city, district = self.driver.find_element_by_css_selector('.xt-shipArea').text.strip().split(' ')

		return {
			'name': name,
			'province': province,
			'city': city,
			'district': district,
			'address': address,
			'tel': tel
		}

	def get_price_info(self, options):
		time.sleep(0.2)
		price_info = {}
		if 'final_price' in options:
			price_info['final_price'] = self.get_total_price()
		if 'product_price' in options:
			product_price = self.driver.find_element_by_css_selector('.xt-totalProductPrice').text.strip()
			if len(product_price) == 0:
				product_price = 0.0
			price_info['product_price'] = product_price
		if 'postage' in options:
			postage = self.driver.find_element_by_css_selector('.xt-postage').text.strip()
			if len(postage) == 0:
				postage = 0.0				
			price_info['postage'] = postage
		if 'integral_money' in options:
			integral_money = self.driver.find_element_by_css_selector('.xt-integralMoney').text.strip()
			if len(integral_money) == 0:
				integral_money = 0.0				
			price_info['integral_money'] = integral_money
		if 'coupon_money' in options:
			coupon_money = self.driver.find_element_by_css_selector('.xt-couponMoney').text.strip()
			if len(coupon_money) == 0:
				coupon_money = 0.0				
			price_info['coupon_money'] = coupon_money
		if 'promotion_money' in options:
			promotion_money = self.driver.find_element_by_css_selector('.xt-promotionMoney').text.strip()
			if len(promotion_money) == 0:
				promotion_money = 0.0				
			price_info['promotion_money'] = promotion_money

		return price_info

	def use_integral(self, product_name, product_model):
		product_groups = []
		for product_group_el in self.driver.fs('.xt-productGroup'):
			#获取商品集合
			products = []
			for product_el in product_group_el.fs('.xt-product'):
				name = product_el.f('.xt-name').text.strip()
				try:
					model = product_el.f('.xt-model').text.strip()
				except:
					model = ''

				if name == product_name and model == product_model:
					product_group_el.f('.xt-useIntegralTrigger').click()
					time.sleep(0.3)
					break

	def unuse_integral(self, product_name, product_model):
		self.use_integral(product_name, product_model)

	#############################################################
	# switch_ship_info: 输入收货人信息
	#############################################################
	def switch_ship_info(self, ship_info, force=False):
		driver = self.driver
		driver.find_element_by_css_selector('.xt-shipInfo').click()
		
		ship_info_page = WAShipInfoPage(self.driver)
		ship_infos = ship_info_page.get_ship_infos()
		is_found_ship_name = False
		for one_ship_info in ship_infos:
			if one_ship_info['ship_name'] == ship_info['ship_name']:
				is_found_ship_name = True

		if is_found_ship_name:
			ship_info_page.select_ship_info(ship_info['ship_name'])
		else:
			edit_ship_address_page = ship_info_page.enter_edit_ship_info_page()
			edit_ship_address_page.input_ship_info(ship_info)
			edit_ship_address_page.click_submit_button()

	#############################################################
	# use_coupon: 使用优惠券
	#############################################################
	def use_coupon(self, coupon_id):
		self.scroll_to_bottom()
		el = self.__find_group(u'优惠券')
		el.click()
		#这里hide和show出发repaint，解决在测试环境中对话框显示不完全的问题
		self.driver.execute_script('$("#orderCouponDialog").hide()');
		self.driver.execute_script('$("#orderCouponDialog").show()');

		#进入优惠券选择对话框
		coupon = Coupon.objects.get(coupon_id=coupon_id)
		for el in self.driver.find_elements_by_css_selector('.xa-coupon'):
			if int(el.get_attribute('data-id')) == coupon.id:
				el.click()
		time.sleep(WAIT_SHORT_TIME)

	#############################################################
	# input_coupon: 输入优惠券
	#############################################################
	def input_coupon(self, coupon_id):
		self.scroll_to_bottom()
		el = self.__find_group(u'优惠券')
		el.click()
		#这里hide和show出发repaint，解决在测试环境中对话框显示不完全的问题
		self.driver.execute_script('$("#orderCouponDialog").hide()');
		self.driver.execute_script('$("#orderCouponDialog").show()');

		#点击"使用优惠码"
		self.driver.find_elements_by_css_selector('#orderCouponDialog a')[1].click()
		time.sleep(0.5)
		input = self.driver.find_element_by_css_selector('input[name="coupon_coupon_id"]')
		input.clear()
		input.send_keys(coupon_id)
		self.driver.find_element_by_css_selector('.xa-useCouponCode').click()
		time.sleep(WAIT_SHORT_TIME)

		# self.scroll_to_bottom()
		# el = self.__find_group(u'使用优惠劵')
		# el.find_element_by_css_selector('label .ui-icon').click()

		# xpath = u"//select[@id='coupon_id']/option[@value='-1']"
		# self.driver.find_element_by_xpath(xpath).click()
		# time.sleep(0.5)
		# input = self.driver.find_element_by_css_selector('input[name="coupon_coupon_id"]')
		# input.clear()
		# input.send_keys(coupon_id)

	#############################################################
	# input_customer_message: 输入商家留言
	#############################################################
	def input_customer_message(self, customer_message):
		self.scroll_to_bottom()
		input = self.driver.find_element_by_css_selector('.xt-customerMessage')
		input.click()
		input.clear()
		input.send_keys(customer_message)

	#############################################################
	# get_purchase_count: 获取购买数量
	#############################################################
	def get_purchase_count(self):
		return int(self.driver.find_element_by_css_selector('.wui-counter .wui-counterText').text)

	#############################################################
	# click_submit_button: 点击“提交”按钮
	#############################################################
	def click_submit_button(self):
		self.driver.find_element_by_id('submit-order').click()
		time.sleep(0.5)

	#############################################################
	# submit_order: 提交订单
	#############################################################
	def submit_order(self):
		self.driver.find_element_by_id('submit-order').click()
		time.sleep(2)
		pay_result_page = WAPayResultPage(self.driver)
		return pay_result_page
		# dialog_links = self.driver.find_elements_by_css_selector('.ui-simpledialog-controls a')
		# if len(dialog_links) != 0:
		# 	dialog_links[0].click()
		# 	time.sleep(2)
		# 	pay_result_page = WAPayResultPage(self.driver)
		# 	return pay_result_page
		# else:
		# 	if self.is_webapp_edit_order_page():
		# 		#停留在编辑订单页面，出错了
		# 		err_message = self.driver.find_element_by_id('xt-errMsg').get_attribute('value')
		# 		self.err_message = err_message
		# 		return self
		# 	elif self.is_webapp_pay_result_page():
		# 		pay_result_page = WAPayResultPage(self.driver)
		# 		return pay_result_page
		# 	else:
		# 		pay_interface_list_page = WAPayInterfaceListPage(self.driver)
		# 		return pay_interface_list_page


	def is_encounter_error(self):
		message = self.driver.find_element_by_id('xt-errMsg').get_attribute('value').strip()
		return (not not message)

	def select_pay_interface(self, pay_interface_type):
		if pay_interface_type == u'货到付款':
			self.driver.find_element_by_css_selector('.xt-payInterface-cod').click()
		elif pay_interface_type == u'微信支付':
			self.driver.find_element_by_css_selector('.xt-payInterface-weixin').click()
