# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from webapp.modules.mall import request_util

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/%s/templates' % (template_path_items[-2], template_path_items[-1])


########################################################################
# list_pay_interfaces: 获得支付接口列表
########################################################################
def list_pay_interfaces(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.list_pay_interfaces(request)


########################################################################
# pay_product_order: 获得支付宝跳转页面
########################################################################
def pay_product_order(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.pay_alipay_order(request)

def pay_weizoompay_order(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.pay_weizoompay_order(request)
