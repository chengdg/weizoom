# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.pageobject.image_view import ImageView
from test.helper import WAIT_SHORT_TIME

class UploadSwipeImageDialog(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver
		self.image_view = ImageView(webdriver, '#commonSelectSwipeImageDialog')

	def load(self):
		time.sleep(WAIT_SHORT_TIME)
		
	#***********************************************************************************
	# upload_image: 添加用户
	#***********************************************************************************
	def upload_image(self, image_path):
		image_url = self.image_view.upload_image(image_path)
		self.image_view.show_image(image_url)
		time.sleep(WAIT_SHORT_TIME)
		self.driver.find_element_by_css_selector('#commonSelectSwipeImageDialog .btn-success').click()
		time.sleep(WAIT_SHORT_TIME)
		return image_url
