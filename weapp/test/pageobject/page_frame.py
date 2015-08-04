# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_view import PageView

class PageFrame(PageView):
	def __init__(self, webdriver):
		self.driver = webdriver

	#########################################################
	# enter_shell: 进入python交互式环境，方便调试和开发
	#########################################################
	def enter_shell(self, global_dicts, local_dicts):
		print '***************** enter python shell *****************'
		while True:
			try:
				line = raw_input('>>> ').strip()
				if line == 'exit':
					break
				code = compile(line, 'selenium shell', 'exec')
				eval(code, global_dicts, local_dicts)
			except:
				import sys
				type, value, tb = sys.exc_info()
				print type
				print value
				import traceback
				traceback.print_tb(tb)


	def click_navs(self, *navs):
		first_nav = navs[0]
		selector = 'div#header a[title="%s"]' % first_nav
		self.driver.find_element_by_css_selector(selector).click()
		script = "$('#main-mask').hide();"
		self.driver.execute_script(script)

		if len(navs) > 1:
			second_nav = navs[1]
			selector = 'div#x-leftNavZone a[title="%s"]' % second_nav
			self.driver.find_element_by_css_selector(selector).click()
		
		return self

	def logout(self):
		self.driver.get("http://dev.weapp.com/logout/")
		time.sleep(2)


	#***********************************************************************************
	# get_error_hints: 获得错误信息
	#***********************************************************************************
	def get_error_hints(self):
		driver = self.driver
		return [el.text for el in driver.find_elements_by_css_selector("div.errorHint") if len(el.text.strip()) != 0]


	#***********************************************************************************
	# goto_webapp_home_page: 任意条件下都可使用的返回首页
	#***********************************************************************************
	def goto_webapp_home_page(self):
		script = "return $('#homePageUrlZone').text();"
		url = 'http://dev.weapp.com%s' % self.driver.execute_script(script)
		self.driver.get(url)
		from webapp.modules.mall.pageobject.webapp_page.home_page import WAHomePage
		return WAHomePage(self.driver)

	#***********************************************************************************
	# return_to_webapp_home_page: 返回webapp的首页
	#***********************************************************************************
	def return_to_webapp_home_page(self):
		links = self.driver.find_elements_by_css_selector('#footerNavBar li a')
		links[1].click()
		from webapp.modules.mall.pageobject.webapp_page.home_page import WAHomePage
		return WAHomePage(self.driver)


	#***********************************************************************************
	# click_webapp_global_nav: 点击webapp的全局导航
	#***********************************************************************************
	def click_webapp_global_nav(self, name):
		links = self.driver.find_elements_by_css_selector('#footerNavBar li a')
		links[2].click()
		time.sleep(1)
		for link in self.driver.find_elements_by_css_selector('#footerNavBar-subNav-menu li a'):
			if name == link.text.strip():
				link.click()
				from webapp.modules.user_center.pageobject.webapp_page.user_center_page import WAUserCenterPage
				return WAUserCenterPage(self.driver)


	#***********************************************************************************
	# get_webapp_alert: 获得webapp页面弹出的alert信息
	#***********************************************************************************
	def get_webapp_alert(self):
		return self.driver.find_element_by_id('xt-errMsg').get_attribute('value').strip()


	#***********************************************************************************
	# get_error_message: 获得错误信息
	#***********************************************************************************
	def get_error_message(self):
		return self.driver.find_element_by_id('xt-errMsg').get_attribute('value').strip()


	#***********************************************************************************
	# scroll_to_bottom: 滚动到最下方
	#***********************************************************************************
	def scroll_to_bottom(self):
		script = 'window.scroll(0, 10000);'
		self.driver.execute_script(script)


	def is_webapp_pay_interface_list_page(self):
		url = self.driver.current_url
		return ('model=pay_interfaces' in url) and ('action=list' in url)

	def is_webapp_pay_result_page(self):
		url = self.driver.current_url
		if ('model=pay_result' in url) and ('action=get' in url):
			return True

		if ('model=order' in url) and ('action=pay' in url):
			return True		

		return False

	def is_webapp_edit_order_page(self):
		url = self.driver.current_url
		return ('model=order' in url) and ('action=edit' in url)

	def is_shopping_cart_page(self):
		url = self.driver.current_url
		return ('model=shopping_cart' in url) and ('action=show' in url)

	def get_title(self):
		return self.driver.title
