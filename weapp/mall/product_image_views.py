# -*- coding: utf-8 -*-

"""@package mall.product_image_views
图片管理模块的页面的实现文件

一个图片分组中可以包含多张图片，这些图片可以供系统在需要使用图片的不同地方选择
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


########################################################################
# get_image_groups: 显示图片分组列表
########################################################################
@view(app='mall', resource='image_groups', action='get')
@login_required
def get_image_groups(request):
	"""
	图片分组列表页面

	@note 每个图片分组最多显示8张图片
	"""
	#获取image group
	image_groups = list(ImageGroup.objects.filter(owner=request.manager))
	group_ids = []
	id2group = {}
	for image_group in image_groups:
		image_group.images = []
		group_ids.append(image_group.id)
		id2group[image_group.id] = image_group

	#向group中填充image
	for image in Image.objects.filter(group_id__in=group_ids):
		id2group[image.group_id].images.append(image)
	for image_group in image_groups:
		if len(image_group.images) > 8:
			image_group.images = image_group.images[:8]

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_product_second_navs(request),
		'second_nav_name': export.PRODUCT_MANAGE_IMAGE_NAV,
		'image_groups': image_groups
	})
	return render_to_response('mall/editor/image_groups.html', c)
