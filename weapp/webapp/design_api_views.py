# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil
import base64
import random

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group
from django.contrib import auth

from models import *
from account.models import UserProfile
from product.models import Product
from product.models import UserHasProduct
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from core import apiview_util
from termite import pagestore as pagestore_manager
from webapp.modules.cms.models import Article, CategoryHasArticle
from mall.models import Product, CategoryHasProduct, PRODUCT_SHELVE_TYPE_ON
from workbench.models import Workspace

#===============================================================================
# 用于支持workbench设计时获取数据
#===============================================================================

#===============================================================================
# get_articles_by_category_id : 根据category id获取article集合
#===============================================================================
def get_articles_by_category_id(request):
	category_id = request.GET['id']
	count = int(request.GET.get('count', 3))

	article_ids = [r.article_id for r in CategoryHasArticle.objects.filter(category_id=category_id)]
	articles = Article.objects.filter(id__in=article_ids).order_by('-display_index')[:count]

	data = []
	workspace_id = 0
	for article in articles:
		data.append({
			"id": article.id,
			"name": article.title,
			"url": '?module=cms&model=article&article_id=%d&webapp_owner_id=%d&workspace_id=cms' % (article.id, article.owner.id)
		})

	if getattr(request, 'response_ajax', True):
		response = create_response(200)
		response.data = data
		return response.get_response()
	else:
		return data

#===============================================================================
# get_products_by_category_id : 根据category id获取product集合
#===============================================================================
def get_products_by_category_id(request):
	category_id = request.GET['id']
	count = int(request.GET.get('count', 5))

	product_ids = [r.product_id for r in CategoryHasProduct.objects.filter(category_id=category_id)]
	products = Product.objects.filter(id__in=product_ids, is_deleted=False, shelve_type=PRODUCT_SHELVE_TYPE_ON).order_by('-display_index')[:count]
	Product.fill_display_price(products)
	data = []
	workspace_id = 0
	for product in products:
		data.append({
			"id": product.id,
			"name": product.name,
			'pic': product.thumbnails_url,
			'price': product.display_price,
			"url": '?module=mall&model=product&action=get&rid=%d&webapp_owner_id=%d&workspace_id=mall' % (product.id, product.owner.id)
		})
	if getattr(request, 'response_ajax', True):
		response = create_response(200)
		response.data = data
		return response.get_response()
	else:
		return data
