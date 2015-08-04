# # -*- coding: utf-8 -*-

# """@package mall.product_model_views
# 商品规格模块的页面的实现文件

# @see 关于商品规格的设计文档，请参阅http://www.baidu.com
# """

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


# COUNT_PER_PAGE = 20
# FIRST_NAV = export.PRODUCT_FIRST_NAV


# ########################################################################
# # get_model_properties: 显示商品规格列表
# ########################################################################
# @view(app='mall', resource='model_properties', action='get')
# @login_required
# def get_model_properties(request):
# 	"""
# 	商品规格列表页面
# 	"""
# 	model_properties = ProductModelProperty.objects.filter(owner=request.manager, is_deleted=False)
# 	id2property = {}
# 	for model_property in model_properties:
# 		model_property.property_values = []
# 		t_name = model_property.name
# 		model_property.shot_name = t_name[:6]+'...' if len(t_name) > 6 else t_name
# 		id2property[model_property.id] = model_property

# 	property_ids = [property.id for property in model_properties]
# 	for property_value in ProductModelPropertyValue.objects.filter(property_id__in=property_ids):
# 		if property_value.is_deleted:
# 			continue
# 		property_id = property_value.property_id
# 		property = id2property[property_id]
# 		property_value.is_image_property_value = (property.is_image_property and property_value.pic_url)
# 		t_name = property_value.name
# 		property_value.shot_name = t_name[:10]+'...' if len(t_name) > 10 else t_name
# 		property.property_values.append(property_value)

# 	c = RequestContext(request, {
# 		'first_nav_name': FIRST_NAV,
# 		'second_navs': export.get_second_navs(request),
# 		'second_nav_name': export.PRODUCT_MANAGE_MODEL_NAV,
# 		'model_properties': model_properties
# 	})
# 	return render_to_response('mall/editor/model_properties.html', c)
