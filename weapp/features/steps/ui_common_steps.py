# -*- coding: utf-8 -*-
import json
import time

from behave import *

from django.contrib.auth.models import User

from test import bdd_util
from features.testenv.model_factory import *

from modules.member.models import Member
from account.pageobject.login_page import LoginPage
from test.pageobject.page_frame import PageFrame

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from test.helper import WAIT_SHORT_TIME
from webapp.models import Project


@given(u"{user}登录系统:ui")
def step_impl(context, user):
	if getattr(context, 'is_logined', False):
		page_frame = PageFrame(context.driver)
		page_frame.logout()
		context.is_logined = False
		context.login_user = None

	login_page = LoginPage(context.driver)
	login_page.login(user, 'test')
	context.is_logined = True
	context.login_user = user


@then(u"{webapp_user_name}获得出错提示'{error_message}':ui")
def step_impl(context, webapp_user_name, error_message):
	expected = error_message
	actual = context.page.get_error_message()
	context.tc.assertEquals(expected, actual)


@when(u"{webapp_user_name}访问{webapp_owner_name}的webapp:ui")
def step_impl(context, webapp_user_name, webapp_owner_name):
	context.page = None
	host = 'dev.weapp.com'
	driver = getattr(context, 'webapp_driver', None)
	context.webapp_owner_name = webapp_owner_name
	if not driver:
		chrome_options = Options()
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument("--disable-plugins")
		driver = webdriver.Chrome(chrome_options=chrome_options)
		driver.implicitly_wait(3)
		context.webapp_driver = driver
	driver.set_window_size(360, 850)
	driver.set_window_position(0, 0)
	driver.get('http://%s/simulator/2/' % host)
	#选择用户
	xpath = u"//select[@id='users']/option[text()='{}']".format(webapp_user_name)
	driver.find_element_by_xpath(xpath).click()
	#点击"登录"
	driver.find_element_by_css_selector('#loginPage .x-loginBtn').click()
	time.sleep(WAIT_SHORT_TIME)

	lis = driver.find_elements_by_css_selector('#accountPage .ui-content li')
	for li in lis:
		h2 = li.find_element_by_css_selector('h2')
		if webapp_owner_name in h2.text:
			li.find_element_by_css_selector('a').click()
	time.sleep(WAIT_SHORT_TIME)

	#设置member的username_hexstr
	#TODO: 模拟微信接口，去掉强制设置的逻辑
	from utils.string_util import byte_to_hex
	username_hexstr = byte_to_hex(webapp_user_name)
	latest_member = list(Member.objects.all())[-1]
	if not latest_member.username_hexstr or latest_member.username_hexstr == 'E9A284E8A788': #E9A284E8A788 = 预览
		#有可能在之前的非ui关注时，member已经创建
		#这种情况下，不需要更新username_hexstr
		#只在username_hexstr为空的情况下更新之
		latest_member.username_hexstr = username_hexstr
	latest_member.save()


