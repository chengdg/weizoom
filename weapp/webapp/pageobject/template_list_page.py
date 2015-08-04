# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.helper import WAIT_SHORT_TIME
from webapp.pageobject.edit_template_page import EditTemplatePage

class TemplateListPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver

	def load(self):
		time.sleep(WAIT_SHORT_TIME)
		self.click_navs(u"模板")
		self.select_template(u'极简主义')
		
	#***********************************************************************************
	# edit_template: 编辑名为name的模板
	#***********************************************************************************
	def edit_template(self, name):
		link = self.driver.find_element_by_css_selector('a[data-template-name="'+name+'"]')
		link.click()
		edit_template_page = EditTemplatePage(self.driver)
		edit_template_page.load()
		return edit_template_page

	#***********************************************************************************
	# preview_template: 编辑名为name的模板
	#***********************************************************************************
	def preview_template(self, name):
		link = self.driver.find_element_by_css_selector('button.x-preview[data-template-name="'+name+'"]')
		link.click()
		time.sleep(6) #等待预览初始化结束

	#***********************************************************************************
	# get_active_template: 获得当前选中的模板
	#***********************************************************************************
	def get_active_template(self):
		script = "return $('.templates_templateCover.active').parents('li').eq(0).find('.x-preview').attr('data-template-name');"
		active_template = self.driver.execute_script(script)
		return active_template

	#***********************************************************************************
	# select_template: 选择模板
	#***********************************************************************************
	def select_template(self, name):
		script = "$('[data-template-name=\""+name+"\"]').parents('li').eq(0).find('a.templates_templateImg').trigger('click')"
		self.driver.execute_script(script)
		time.sleep(3) #等待ajax操作完成
