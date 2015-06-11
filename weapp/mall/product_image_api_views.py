# -*- coding: utf-8 -*-
"""@package mall.product_image_api_views
图片管理模块的API的实现文件
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


@api(app='mall', resource='image_group', action='create')
@login_required
def create_image_group(request):
	"""
	创建图片分组

	Method: POST

	@param name 图片分组名
	@param images 分组中的图片集合，如下格式的json字符串。id为-1，表示该图片需要新建
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
	[{
		"path": "...",
		"width": "100",
		"height": "100,
	}, {
		......
	}]
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	name = request.POST['name']
	images = json.loads(request.POST.get('images', '[]'))

	image_group = ImageGroup.objects.create(
		owner = request.manager,
		name = name
	)

	for image in images:
		Image.objects.create(
			owner = request.manager,
			group = image_group,
			url = image['path'],
			width = image['width'],
			height = image['height']
		)

	response = create_response(200)
	return response.get_response()


@api(app='mall', resource='image_group', action='update')
@login_required
def update_image_group(request):
	"""
	更新图片分组

	Method: POST

	@note 更新策略；
		- 新建db中没有的(id为-1)
		- 更新db中已有的(id为正数)
		- 删除db中有的而POST中没有的

	@param name 图片分组名
	@param images 分组中的图片集合，如下格式的json字符串。id为-1，表示该图片需要新建；若不为-1，表示该图片需要更新
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
	[{
		"id": -1,
		"path": "...",
		"width": "100",
		"height": "100,
	}, {
		"id": 2,
		"path": "...",
		"width": "100",
		"height": "100,
	}, {
		......
	}]
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	id = request.POST['id']
	name = request.POST['name']
	images = json.loads(request.POST.get('images', '[]'))

	image_group = ImageGroup.objects.get(id=id)
	if image_group.name != name:
		ImageGroup.objects.filter(id=id).update(name=name)

	#更新image
	image_ids = set([image['id'] for image in images])
	existed_image_ids = set([image.id for image in Image.objects.filter(group_id=id)])
	for image in images:
		if int(image['id']) < 0:
			Image.objects.create(
				owner = request.manager,
				group = image_group,
				url = image['path'],
				width = image['width'],
				height = image['height']
			)
	ids_to_be_delete = existed_image_ids - image_ids
	Image.objects.filter(id__in=ids_to_be_delete).delete()

	response = create_response(200)
	return response.get_response()


@api(app='mall', resource='image_group', action='delete')
@login_required
def delete_image_group(request):
	"""
	删除图片分组

	Method: POST

	@param id 图片分组id
	"""
	id = request.POST['id']
	ImageGroup.objects.filter(id=id).delete()

	response = create_response(200)
	return response.get_response()


@api(app='mall', resource='image_group_images', action='get')
@login_required
def get_image_group_images(request):
	"""
	获取图片分组中的图片集合

	Method: GET

	@param id 图片分组id

	@return 如下格式的json
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
	[{
		"id": 1,
		"src": "http://upyun.com/a/1.jpg",
		"width": "100",
		"height": "100,
	}, {
		"id": 2,
		"src": "http://upyun.com/a/2.jpg",
		"width": "100",
		"height": "100,
	}, {
		......
	}]
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	group_id = request.GET['id']
	images = []
	for image in Image.objects.filter(group_id=group_id):
		images.append({
			"id": image.id,
			"src": image.url,
			"width": image.width,
			"height": image.height
		})

	response = create_response(200)
	response.data = images
	return response.get_response()


@api(app='mall', resource='image_groups', action='get')
@login_required
def get_image_groups(request):
	"""
	获取图片分组信息

	Method: GET

	@param id 图片分组id

	@return 如下格式的json
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
	[{
		"id": 1,
		"name": "图片分组1"
	}, {
		"id": 2,
		"name": "图片分组2"
	}, {
		......
	}]
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	image_groups = []
	for image_group in ImageGroup.objects.filter(owner=request.manager):
		image_groups.append({
			"id": image_group.id,
			"name": image_group.name
		})

	response = create_response(200)
	response.data = image_groups
	return response.get_response()
