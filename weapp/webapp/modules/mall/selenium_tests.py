# -*- coding: utf-8 -*-

import unittest
import time
import sys
from datetime import datetime

from django.db.models import Q

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.chrome.options import Options

from account.models import *
from test import helper

from account.pageobject.login_page import LoginPage
from webapp.pageobject.template_list_page import TemplateListPage
from test.pageobject.page_frame import PageFrame
from webapp.modules.mall.pageobject.category_list_page import CategoryListPage
from webapp.modules.mall.pageobject.postage_list_page import PostageListPage
from webapp.modules.mall.pageobject.pay_interface_list_page import PayInterfaceListPage
from webapp.modules.mall.pageobject.product_list_page import ProductListPage

from webapp.modules.mall.pageobject.webapp_page.home_page import WAHomePage

from webapp.modules.mall.selenium_test_case import editor_mall_config_tests, editor_product_and_category_tests, editor_template_tests, webapp_mall_tests


from webapp.modules.mall.models import *
def init():
	print 'init db environment for mall'

	#CategoryHasProduct.objects.all().delete()
	#Product.objects.all().delete()
	#ProductCategory.objects.all().delete()

	#PostageConfig.objects.filter(~Q(name=u'免运费')).delete()
	#PostageConfig.objects.filter(name=u'免运费').update(is_used=True)
	#PayInterface.objects.all().delete()
	
	
def clear():
	print 'clear db environment for mall'


sub_tests = [
	#editor_mall_config_tests, 
	#editor_product_and_category_tests, 
	#editor_template_tests, 
	webapp_mall_tests
]
