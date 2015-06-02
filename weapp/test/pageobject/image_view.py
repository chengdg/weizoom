# -*- coding: utf-8 -*-

from datetime import datetime

import BeautifulSoup

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from selenium.common.exceptions import NoSuchElementException

from test.pageobject.page_view import PageView

class ImageView(PageView):
	def __init__(self, webdriver, el):
		self.driver = webdriver
		self.root_selector = el
		self.show_image_script_template = '''
$("{root_selector} #imageView-uploadZone").hide();
$("{root_selector} .imageView-imgContainer").html("").append("{img}");
$("{root_selector} #imageView-imgZone").show();
$("{root_selector} input[type='hidden']").val("{picture_url}");
'''

	#***********************************************************************************
	# upload_image: 上传图片
	#***********************************************************************************
	def upload_image(self, picture):
		if not picture:
			return None
		# test_client.py
		from poster.encode import multipart_encode
		from poster.streaminghttp import register_openers
		import urllib2

		# Register the streaming http handlers with urllib2
		register_openers()

		# Start the multipart/form-data encoding of the file "DSC0001.jpg"
		# "image1" is the name of the parameter, which is normally set
		# via the "name" parameter of the HTML <input> tag.

		# headers contains the necessary Content-Type and Content-Length
		# datagen is a generator object that yields the encoded parameters
		file_name = picture.split('/')[-1]
		datagen, headers = multipart_encode({"Filedata": open(picture, "rb"), "Filename": file_name, 'uid':'xxx1'})

		# Create the Request object
		request = urllib2.Request("http://dev.weapp.com/account/upload_picture/?", datagen, headers)
		# Actually do the request, and get the response
		return urllib2.urlopen(request).read()

	#***********************************************************************************
	# delete_image: 删除图片
	#***********************************************************************************
	def delete_image(self):
		selector = '%s #imageView-imgZone button.close' % self.root_selector
		self.driver.find_element_by_css_selector(selector).click()

	#***********************************************************************************
	# show_image: 显示图片
	#***********************************************************************************
	def show_image(self, picture_url):
		if not picture_url:
			return
		driver = self.driver
		img = "<img src='%s' width='300' style='width: 300px' />" % picture_url
		show_image_script = self.show_image_script_template.format(**{
			'root_selector': self.root_selector,
			'img': img,
			'picture_url': picture_url
		})
		driver.execute_script(show_image_script)
