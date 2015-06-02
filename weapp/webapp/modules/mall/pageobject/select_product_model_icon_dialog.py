# -*- coding: utf-8 -*-

from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from test.pageobject.page_frame import PageFrame
from test.pageobject.image_view import ImageView
from test.helper import WAIT_SHORT_TIME

class SelectProductModelIconDialog(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver
		self.image_view = ImageView(webdriver, '#selectIconDialog')

	def load(self):
		time.sleep(WAIT_SHORT_TIME+WAIT_SHORT_TIME)
		
	#***********************************************************************************
	# select_uploaded_image: 选择上传图片
	#***********************************************************************************
	def select_uploaded_image(self, image_path):
		image_url = self.image_view.upload_image(image_path)
		script = 'W.dialog.NAME2DIALOG["W.dialog.common.SelectUserIconDialog"].onFinishUpload("'+image_url+'");';
		self.driver.execute_script(script);

		self.driver.find_element_by_css_selector('#selectIconDialog .btn-success').click()
		return image_url
