# -*- coding: utf-8 -*-

import logging
import sys
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil
import base64
import random
import inspect

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.db import connections

from models import *
from account.models import UserProfile
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from core import apiview_util

import views

#######################################################################
# reset_data: 重置数据
#######################################################################
def reset_data(request):
	response = create_response(200)

	Order.objects.all().delete()
	CategoryHasProduct.objects.all().delete()
	Product.objects.all().delete()
	Category.objects.all().delete()

	categories = [
		Category.objects.create(name='category1'),
		Category.objects.create(name='category2'),
		Category.objects.create(name='category3')
	]
	for i in range(1, 6):
		product = Product.objects.create(
			name = 'product_%d' % i,
			price = 10 + i,
			count = i,
			detail = 'product_detail_%d' % i
		)

		index = i % 2
		CategoryHasProduct.objects.create(
			product = product,
			category = categories[index]
		)
		CategoryHasProduct.objects.create(
			product = product,
			category = categories[index+1]
		)

		for j in range(1, 6):
			Order.objects.create(
				product = product,
				receiver = 'receiver_%d' % j,
				price = product.price * 10
			)

	return response.get_response()


#######################################################################
# get_code: 获得代码
#######################################################################
def get_code(request):
	action = request.GET['action']
	response = create_response(200)
	function_name = '_exec_%s' % action
	function = getattr(views, function_name)
	code = inspect.getsource(function)
	response.data = {
		'code': code,
		'functionName': action
	}

	return response.get_response()


#######################################################################
# run_code: 执行code
#######################################################################
def run_code(request):
	function_code = request.POST['code'].strip()
	function_code = function_code.replace('    ', '\t')
	function_def_line = function_code.split('\n')[0].strip()
	beg = function_def_line.find(' ')
	end = function_def_line.find('(')
	function_name = function_def_line[beg+1:end]

	code = """
from example.models import *
from example.util import convert_code_result
%s

data = %s()
result.append(convert_code_result(data))
""" % (function_code, function_name)

	result = None
	try:
		code_obj = compile(code, '<input>', 'exec')
		function_result = []
		connections['default'].queries = []
		eval(code_obj, {'result': function_result})
		result = function_result[0]
	except:
		response = create_response(500)
		items = unicode_full_stack().split('\n')
		items.reverse()
		response.innerErrMsg = '<br/>'.join(items[:20])
		return response.get_response()

	#获取sql执行结果
	sqls = []
	for query in connections['default'].queries:
		if 'example_' in query['sql']:
			sqls.append({'time':query['time'], 'sql':query['sql']})
	
	response = create_response(200)
	response.data = {
		'result': result,
		'sqls': sqls,
		'run_code': code
	}
	return response.get_response()

def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)
