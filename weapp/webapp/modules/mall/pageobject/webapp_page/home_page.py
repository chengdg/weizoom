# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals
from django.conf import settings

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME

from webapp.models import Project


class WAHomePage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		#寻找jobs的首页
		time.sleep(0.1)
		jobs = User.objects.get(username='jobs')
		project = Project.objects.get(owner=jobs, inner_name='default')
		webapp_home = 'http://%s/workbench/jqm/preview/?project_id=%d' % (settings.DOMAIN, project.id)

		self.driver.get(webapp_home)
		
	def enter_product_list_page(self):
		self.driver.find_elements_by_css_selector('li a')[1].click()
		from webapp.modules.mall.pageobject.webapp_page.index_page import WAIndexPage
		return WAIndexPage(self.driver)

	def enter_user_center_page(self):
		self.driver.find_elements_by_css_selector('li a')[2].click()
		from webapp.modules.user_center.pageobject.webapp_page.user_center_page import WAUserCenterPage
		return WAUserCenterPage(self.driver)
