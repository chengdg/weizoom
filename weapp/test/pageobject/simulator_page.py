# -*- coding: utf-8 -*-

from datetime import datetime
import time

import BeautifulSoup

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from test.pageobject.page_frame import PageFrame

class SimulatorPage(PageFrame):
	def __init__(self, webdriver):
		self.driver = webdriver
		self.root_selector = 'body'

	#***********************************************************************************
	# open: 打开模拟器
	#***********************************************************************************
	def open(self):
		self.driver.get('http://dev.viper.com/simulator/')

	#***********************************************************************************
	# close: 关闭模拟器
	#***********************************************************************************
	def close(self):
		self.driver.get('http://dev.viper.com/')

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
			if isinstance(message_div, BeautifulSoup.NavigableString):
				continue
			divs = message_div.findAll('div')
			img = divs[0].img
			text = self.get_html_content(divs[1])
			message = {'type': 'text', 'img': img['src'], 'text': text, 'css_class': message_div['class']}
			messages.append(message)

		return messages

	#***********************************************************************************
	# send: 发送消息
	#***********************************************************************************
	def send(self, message):
		driver = self.driver
		input = driver.find_element_by_id("weixinInput-contentInput")
		input.clear()
		input.send_keys(message)
		input.send_keys(Keys.ENTER)
		time.sleep(2)
