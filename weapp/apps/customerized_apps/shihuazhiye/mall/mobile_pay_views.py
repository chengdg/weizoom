# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

# from apps.customerized_apps.shihuazhiye.mall import request_util
from webapp.modules.mall import request_util

from apps.register import mobile_view_func

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/%s/templates' % (template_path_items[-2], template_path_items[-1])

TEMPLATE_DIR = 'webapp/mall/no_template'

########################################################################
# list_pay_interfaces: 获得支付接口列表
########################################################################
@mobile_view_func(resource='pay_interfaces', action='list')
def list_pay_interfaces(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.list_pay_interfaces(request)


########################################################################
# pay_product_order: 获得支付宝跳转页面
########################################################################
@mobile_view_func(resource='product_order', action='pay')
def pay_product_order(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.pay_alipay_order(request)

@mobile_view_func(resource='weizoompay_order', action='pay')
def pay_weizoompay_order(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.pay_weizoompay_order(request)
