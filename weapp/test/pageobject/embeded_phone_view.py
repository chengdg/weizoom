# -*- coding: utf-8 -*-

from datetime import datetime

import BeautifulSoup

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from selenium.common.exceptions import NoSuchElementException

from test.pageobject.page_view import PageView

class EmbededPhoneView(PageView):
	def __init__(self, webdriver, el):
		self.driver = webdriver
		self.root_selector = el

	#***********************************************************************************
	# get_mobile_page: 获得mobile browser中的网页内容
	#***********************************************************************************
	def get_mobile_page(self):
		mobile_page_content = self.driver.execute_script('return window.frames[0].window.document.body.innerHTML;')
		return mobile_page_content

	#***********************************************************************************
	# get_html_content: 获得node节点下的html文本内容
	#***********************************************************************************
	def get_html_content(self, node):
		results = []
		for content in node.contents:
			if isinstance(content, BeautifulSoup.NavigableString):
				content = content.strip()
			else:
				content = unicode(content).strip()
			print content
			if content:
				results.append(content)
		result_content = ''.join(results)
		if result_content.endswith('<br />'):
			return result_content[:-6]
		else:
			return result_content

	#***********************************************************************************
	# get_weixin_messages: 获得微信消息列表
	#***********************************************************************************
	def get_weixin_messages(self):
		messages = []
		driver = self.driver
		script = "return $('%s #timeline-zone').html();" % self.root_selector
		html = driver.execute_script(script)
		html_node = BeautifulSoup.BeautifulSoup(html)
		for message_div in html_node.contents:
			divs = message_div.findAll('div')
			img = divs[0].img
			text = self.get_html_content(divs[1])
			message = {'type': 'text', 'img': img['src'], 'text': text, 'css_class': message_div['class']}
			messages.append(message)

		return messages
