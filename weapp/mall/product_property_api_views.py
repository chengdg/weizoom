# -*- coding: utf-8 -*-
"""@package mall.product_property_api_views
商品属性模块的API的实现文件
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


@api(app='mall', resource='template_properties', action='get')
@login_required
def get_template_properties(request):
	"""
	获得属性模板中的属性集合

	Method: GET

	@param id 属性模板id

	@return 如下格式的json
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
	[{
		id: 1,
		name: "属性1",
		value: "属性1的描述"
	}, {
		......
	}]
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	template_id = int(request.GET['id'])
	if template_id == -1:
		properties = []
	else:
		properties = list(TemplateProperty.objects.filter(template_id=template_id))

	result_properties = []
	for property in properties:
		result_properties.append({
			"id": property.id,
			"name": property.name,
			"value": property.value
		})

	response = create_response(200)
	response.data = result_properties
	return response.get_response()


@api(app='mall', resource='property_template', action='create')
@login_required
def create_property_template(request):
	"""
	创建属性模板

	Method: POST

	@param title 属性模板标题
	@param newProperties 属性模板中需要新建的property信息的json字符串
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
	[{
		id: -1, //id=-1, 代表需要新建的属性
		name: "属性1",
		value: "属性1的描述"
	}, ......]
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	title = request.POST['title']
	new_properties = json.loads(request.POST.get('newProperties', "[]"))

	template = ProductPropertyTemplate.objects.create(
		owner = request.manager,
		name = title
	)

	#创建新的property
	for property in new_properties:
		if property['id'] < 0:
			#需要新建property
			TemplateProperty.objects.create(
				owner = request.manager,
				template = template,
				name = property['name'],
				value = property['value']
			)

	response = create_response(200)
	return response.get_response()


@api(app='mall', resource='property_template', action='update')
@login_required
def update_property_template(request):
	"""
	更新属性模板

	Method: POST

	@param id 属性模板id
	@param title 属性模板标题
	@param newProperties 属性模板中需要新建的property信息的json字符串
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
	[{
		id: -1, //id=-1, 代表需要新建的属性
		name: "属性1",
		value: "属性1的描述"
	}, ......]
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	@param updateProperties 属性模板中需要更新的property信息的json字符串
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
	[{
		id: 2, //id>0, 代表需要更新的属性
		name: "属性2",
		value: "属性2的描述"
	}, ......]
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	@param deletedIds 属性模板中需要删除的property的id数据的json字符串
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
	[3, 4, 5, ......]
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	template_id = request.POST['id']
	title = request.POST['title']
	new_properties = json.loads(request.POST.get('newProperties', "[]"))
	update_properteis = json.loads(request.POST.get('updateProperties', "[]"))
	deleted_property_ids = json.loads(request.POST.get('deletedIds', "[]"))

	template = ProductPropertyTemplate.objects.filter(id=template_id).update(
		name = title
	)

	#创建新的property
	for property in new_properties:
		if property['id'] < 0:
			#需要新建property
			TemplateProperty.objects.create(
				owner = request.manager,
				template_id = template_id,
				name = property['name'],
				value = property['value']
			)

	#更新已有的property
	for property in update_properteis:
		try:
			TemplateProperty.objects.filter(id=property['id']).update(
				name = property['name'],
				value = property['value']
			)
		except:
			pass

	#删除property
	TemplateProperty.objects.filter(id__in=deleted_property_ids).delete()

	response = create_response(200)
	return response.get_response()


@api(app='mall', resource='property_template', action='delete')
@login_required
def delete_property_template(request):
	"""
	删除属性模板

	Method: POST

	@param id 属性模板id
	"""
	template_id = request.POST['id']

	ProductPropertyTemplate.objects.filter(owner=request.manager, id=template_id).delete()

	response = create_response(200)
	return response.get_response()