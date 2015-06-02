# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
import shutil
try:
    import Image
except:
    from PIL import Image
import copy

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth

from webapp.modules.mall.models import Order
from core.jsonresponse import create_response
from account.models import UserAlipayOrderConfig, UserTenpayOrderConfig
from webapp.modules.mall.models import PayInterface, PAY_INTERFACE_ALIPAY, PAY_INTERFACE_TENPAY


#===============================================================================
# request_call_back_url: 调用支付的回调函数，获取结果
#===============================================================================
def request_call_back_url(request):
	url = request.GET['call_back_url']

	conn = urllib.urlopen(url)
	content = conn.read()
	conn.close()

	if '<h2>Request information</h2>' in content:
		return HttpResponse(content)
	else:
		return HttpResponseRedirect(url)


#===============================================================================
# show_alipay_page: 显示模拟支付宝支付页面
#===============================================================================
def show_alipay_page(request):
	config_id = request.GET['config_id']
	alipay_config = UserAlipayOrderConfig.objects.get(id=config_id)
	pay_interface = PayInterface.objects.get(type=PAY_INTERFACE_ALIPAY, related_config_id=config_id)

	order_id = request.GET['order_id']
	success_call_back_url = '%s?out_trade_no=%s&request_token=requestToken&result=success&trade_no=2014022521609718&sign=e6e18a2286de7fc1a55497c8a46dfbbd&sign_type=MD5' % (request.GET['call_back_url'], order_id)
	fail_call_back_url = '%s?out_trade_no=%s&request_token=requestToken&result=fail&trade_no=2014022521609718&sign=e6e18a2286de7fc1a55497c8a46dfbbd&sign_type=MD5' % (request.GET['call_back_url'], order_id)
	c = RequestContext(request, {
		'name': '%s(partner:%s)' % (pay_interface.description, alipay_config.partner),
		'price': request.GET.get('price', 'unknown'),
		'success_call_back_url': success_call_back_url,
		'fail_call_back_url': fail_call_back_url,
	})
	return render_to_response('mockapi/alipay.html', c)


#===============================================================================
# show_tenpay_page: 显示模拟财付通支付页面
#===============================================================================
def show_tenpay_page(request):
	config_id = request.GET['config_id']
	tenpay_config = UserTenpayOrderConfig.objects.get(id=config_id)
	pay_interface = PayInterface.objects.get(type=PAY_INTERFACE_TENPAY, related_config_id=config_id)

	order_id = request.GET['order_id']
	success_call_back_url = '%s?out_trade_no=%s&request_token=requestToken&trade_status=0&trade_no=2014022521609718&sign=e6e18a2286de7fc1a55497c8a46dfbbd&sign_type=MD5' % (request.GET['call_back_url'], order_id)
	fail_call_back_url = '%s?out_trade_no=%s&request_token=requestToken&trade_status=1&trade_no=2014022521609718&sign=e6e18a2286de7fc1a55497c8a46dfbbd&sign_type=MD5' % (request.GET['call_back_url'], order_id)
	c = RequestContext(request, {
		'name': '%s(partner:%s)' % (pay_interface.description, tenpay_config.partner),
		'price': request.GET.get('price', 'unknown'),
		'success_call_back_url': success_call_back_url,
		'fail_call_back_url': fail_call_back_url,
	})
	return render_to_response('mockapi/tenpay.html', c)


#===============================================================================
# do_async_weixin_pay: 执行微信支付的异步支付流程
#===============================================================================
def do_async_weixin_pay(request):
	notify_url = request.GET['notify_url']
	order_id = request.GET['order_id']
	notify_url = '%s?trade_state=0&out_trade_no=%s&pay_info=' % (notify_url, order_id)

	conn = urllib.urlopen(notify_url)
	content = conn.read()
	conn.close()

	if '<html' in content:
		response = create_response(500)
		response.data = content
		dst = open('async_weixin_pay_error.html', 'wb')
		print >> dst, content
		dst.close()
		return response.get_jsonp_response(request)
	else:
		response = create_response(200)
		response.data = content
		return response.get_jsonp_response(request)
