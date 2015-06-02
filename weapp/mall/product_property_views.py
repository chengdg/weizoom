# -*- coding: utf-8 -*-
"""@package mall.product_property_views
商品属性模块的页面的实现文件

一个商品属性是诸如<"产地", "北京">这样的<属性, 值>的值对

一个"商品属性模板"中包含了多个属性
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


COUNT_PER_PAGE = 20
FIRST_NAV = export.PRODUCT_FIRST_NAV


@view(app='mall', resource='property_templates', action='get')
@login_required
def get_property_templates(request):
	"""
	商品属性模板列表页面
	"""
	templates = list(ProductPropertyTemplate.objects.filter(owner=request.manager))
	for template in templates:
		template.properties = []
	id2templates = dict([(template.id, template) for template in templates])

	template_ids = [template.id for template in templates]
	properties = TemplateProperty.objects.filter(template_id__in=template_ids)
	for property in properties:
		template = id2templates.get(property.template_id, None)
		if template:
			template.properties.append(property)
	
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': export.PRODUCT_MANAGE_MODEL_NAV,
		'templates': templates
	})
	return render_to_response('mall/editor/property_templates.html', c)
