# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core.dateutil import get_today
from core.exceptionutil import full_stack, unicode_full_stack

from watchdog.utils import watchdog_info

from webapp.modules.cms.models import *

from core.send_order_email_code import *
import util as cms_util


########################################################################
# get_article_list: 显示“文章列表”页面
########################################################################
def get_article_list(request):
	category_id = request.GET.get('rid', '0')
	if category_id == '0':
		category = Category()
		articles = list(Article.objects.filter(owner_id=request.webapp_owner_id).order_by('-display_index'))
		category_name = u'全部'
	else:
		article_ids = [r.article_id for r in CategoryHasArticle.objects.filter(category_id=category_id)]
		articles = list(Article.objects.filter(id__in=article_ids).order_by('-display_index'))
		try:
			category = Category.objects.get(id=category_id)
			category_name = category.name
		except:
			category = Category()
			category.is_deleted = True
			category_name = u'已删除分类'

	articles_categories = Category.objects.filter(owner_id=request.webapp_owner_id)
	has_category = False
	if articles_categories.count() > 0:
		has_category = True
	c = RequestContext(request, {
		'page_title': u'文章列表(%s)' % category_name,
		'articles': articles,
		'is_deleted_data': category.is_deleted if (category is not None and hasattr(category, 'is_deleted')) else False,
		'articles_categories': articles_categories,
		'has_category': has_category
	})
	return render_to_response('%s/articles.html' % request.template_dir, c)


########################################################################
# get_article: 显示“文章内容”页面
########################################################################
def get_article(request):
	try:
		article = Article.objects.get(id=request.GET['article_id'])
	except:
		article = Article()
		article.is_deleted = True

	c = RequestContext(request, {
		'page_title': article.title,
		'is_deleted_data': article.is_deleted if hasattr(article, 'is_deleted') else False,
		'article': article
	})
	return render_to_response('%s/article_detail.html' % request.template_dir, c)


########################################################################
# get_demo_home_page: 显示“文章内容”页面
########################################################################
def get_demo_home_page(request):
	swipe_images = [{
		'url': '/standard_static/test_resource_img/hangzhou1.jpg'
	}, {
		'url': '/standard_static/test_resource_img/hangzhou2.jpg'
	}, {
		'url': '/standard_static/test_resource_img/hangzhou3.jpg'
	}]
	request.should_hide_footer = True
	c = RequestContext(request, {
		'swipe_images_json': json.dumps(swipe_images)
	})
	return render_to_response('%s/demo_home_page.html' % request.template_dir, c)
