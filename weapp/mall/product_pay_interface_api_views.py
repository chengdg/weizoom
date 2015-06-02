# -*- coding: utf-8 -*-
"""@package mall.product_pay_interface_api_views
支付接口模块的API的实现文件
"""

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import MySQLdb
import random
import string

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count

import models as mall_models
from models import *
import export
from core.restful_url_route import *
from core.jsonresponse import create_response


@api(app='mall', resource='pay_interface', action='enable')
@login_required
def enable_pay_interface(request):
	"""
	启用支付接口

	Method: POST

	@param id 支付接口id
	@param is_enable 是否启用
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
		 true: 启用
		false: 禁用
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	pay_interface_id = int(request.POST['id'])
	is_enable = (request.POST['is_enable'] == 'true')
	PayInterface.objects.filter(id=pay_interface_id).update(is_active=is_enable)

	response = create_response(200)
	return response.get_response()