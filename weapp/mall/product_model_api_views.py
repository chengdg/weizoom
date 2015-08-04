# -*- coding: utf-8 -*-

"""@package mall.product_model_api_views
商品规格的API的实现文件
"""

# import time
# from datetime import timedelta, datetime, date
# import urllib, urllib2
# import os
# import json
# import MySQLdb
# import random
# import string

# from django.http import HttpResponseRedirect, HttpResponse, Http404
# from django.template import Context, RequestContext
# from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from django.shortcuts import render_to_response
# from django.contrib.auth.models import User, Group, Permission
# from django.contrib import auth
# from django.db.models import Q, F
# from django.db.models.aggregates import Sum, Count

# import models as mall_models
# from models import *
# import export
# from core.restful_url_route import *
# from core.jsonresponse import create_response
# import signals


# @api(app='mall', resource='product_model_property', action='create')
# @login_required
# def create_product_model_property(request):
# 	"""
# 	创建一个空的规格属性

# 	Method: POST
# 	"""
# 	if request.POST:
# 		property = ProductModelProperty.objects.create(
# 			owner = request.manager,
# 			name = ''
# 		)

# 		response = create_response(200)
# 		response.data = property.id
# 		return response.get_response()
# 	else:
# 		response = create_response(501)
# 		return response.get_response()


# @api(app='mall', resource='product_model_property', action='update')
# @login_required
# def update_product_model_property(request):
# 	"""
# 	更新规格属性

# 	Method: POST

# 	@param id 规格id
# 	@param filed 指定更新规格的哪个属性
# 	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
# 		POST['filed']='name'：更新规格名
# 		POST['filed']='type'：更新规格类型，可以取text或image
# 	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 	@param name 新的规格名
# 	@param type 新的规格类型
# 	"""
# 	if request.POST:
# 		id = request.POST['id']
# 		field = request.POST['field']
# 		if 'name' == field:
# 			name = request.POST['name']
# 			ProductModelProperty.objects.filter(id=id).update(name=name)
# 		elif 'type' == field:
# 			type = PRODUCT_MODEL_PROPERTY_TYPE_TEXT if request.POST['type'] == 'text' else PRODUCT_MODEL_PROPERTY_TYPE_IMAGE
# 			ProductModelProperty.objects.filter(id=id).update(type=type)

# 		response = create_response(200)
# 		return response.get_response()
# 	else:
# 		response = create_response(501)
# 		return response.get_response()


# @api(app='mall', resource='product_model_property', action='delete')
# @login_required
# def delete_product_model_property(request):
# 	"""
# 	删除规格属性

# 	Method: POST

# 	@param id 规格id

# 	@note 删除规格属性后，会send pre_delete_product_model_property signal，处理由于规格变化引起的商品状态的变化
# 	"""
# 	if request.POST:
# 		property_id = request.POST['id']
# 		signals.pre_delete_product_model_property.send(sender=ProductModelProperty, model_property=ProductModelProperty.objects.get(id=property_id), request=request)

# 		ProductModelPropertyValue.objects.filter(property_id=property_id).update(is_deleted=True)
# 		ProductModelProperty.objects.filter(id=property_id).update(is_deleted=True)

# 		response = create_response(200)
# 		return response.get_response()
# 	else:
# 		response = create_response(501)
# 		return response.get_response()

pass
# @api(app='mall', resource='product_model_property_value', action='create')
# @login_required
# def create_product_model_property_value(request):
# 	"""
# 	创建规格属性值

# 	Method: POST

# 	@param id 规格id
# 	@param name 规格值的名字
# 	@param pic_url 规格值的图片地址
# 	"""
# 	if request.POST:
# 		property_id = request.POST['id']
# 		pic_url = request.POST['pic_url']
# 		name = request.POST['name']
# 		property_value = ProductModelPropertyValue.objects.create(
# 			property_id = property_id,
# 			name = name,
# 			pic_url = pic_url
# 		)

# 		response = create_response(200)
# 		response.data = property_value.id
# 		return response.get_response()
# 	else:
# 		response = create_response(501)
# 		return response.get_response()

pass
# @api(app='mall', resource='product_model_property_value', action='delete')
# @login_required
# def delete_product_model_property_value(request):
# 	"""
# 	删除规格属性值

# 	Method: POST

# 	@param id 规格值id

# 	@note 删除规格值后，会处理由于规格值变化引起的商品状态的改变
# 	"""
# 	if request.POST:
# 		property_value_id = request.POST['id']
# 		ProductModelPropertyValue.objects.filter(id=property_value_id).update(is_deleted=True)

# 		model_ids = [relation.model_id for relation in ProductModelHasPropertyValue.objects.filter(property_value_id = property_value_id)]
# 		ProductModel.objects.filter(id__in=model_ids).update(is_deleted=True)

# 		product_ids = set(list(ProductModel.objects.filter(id__in=model_ids).values_list('product_id', flat=True)))
# 		Product.objects.record_cache_args(ids=product_ids).filter(id__in=product_ids).update(shelve_type=PRODUCT_SHELVE_TYPE_OFF)

# 		response = create_response(200)
# 		return response.get_response()
# 	else:
# 		response = create_response(501)
# 		return response.get_response()

pass
# @api(app='mall', resource='product_model_properties', action='get')
# @login_required
# def get_product_model_properties(request):
# 	"""
# 	获取全部规格属性集合

# 	Method: GET

# 	@return 如下格式的json
# 	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
# 	[{
# 		id: 1,
# 		name: "颜色",
# 		type: "text",
# 		values: [{
# 			id: 1,
# 			full_id: "1:1", //full_id表示${property.id}:${value.id}
# 			name: "红",
# 			image: ""
# 		}, {
# 			id: 2,
# 			name: "白"
# 			image: ""
# 		}, {
# 			......
# 		}]
# 	}, {
# 		......
# 	}]
# 	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 	"""
# 	properties = []
# 	for property in ProductModelProperty.objects.filter(owner=request.manager, is_deleted=False):
# 		values = []
# 		for value in ProductModelPropertyValue.objects.filter(property=property, is_deleted=False):
# 			shot_name = value.name
# 			if len(shot_name) > 9:
# 				shot_name = shot_name[:9]+'...'
# 			values.append({
# 				"id": value.id,
# 				"fullId": '%s:%s' % (property.id, value.id),
# 				"name": value.name,
# 				"shot_name": shot_name,
# 				"image": value.pic_url
# 			})

# 		properties.append({
# 			"id": property.id,
# 			"name": property.name,
# 			"type": "text" if property.type == PRODUCT_MODEL_PROPERTY_TYPE_TEXT else "image",
# 			"values": values
# 		})

# 	response = create_response(200)
# 	response.data = properties
# 	return response.get_response()
