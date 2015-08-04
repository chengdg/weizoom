# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME


class WAUserCouponPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		pass

	def __extract_coupons(self, css_selector):
		id2coupon = {}
		for el in self.driver.find_elements_by_css_selector(css_selector):
			price = float(el.find_element_by_css_selector('.xt-price').text.strip())
			coupon_id = el.find_element_by_css_selector('.xt-couponId').text.strip()
			status = el.find_element_by_css_selector('.xt-status').text.strip()
			id2coupon[coupon_id] = {
				"price": price,
				"status": status
			}

		return id2coupon
		
	def get_coupons(self):
		links = self.driver.find_elements_by_css_selector('.wui-swiper-tabs a')

		unused_coupons = self.__extract_coupons('.xt-unusedCoupon')

		links[1].click()
		time.sleep(0.5)
		used_coupons = self.__extract_coupons('.xt-usedCoupon')
		
		links[2].click()
		time.sleep(0.5)
		expired_coupons = self.__extract_coupons('.xt-expiredCoupon')

		return {
			"unused": unused_coupons,
			"used": used_coupons,
			"expired": expired_coupons
		}
