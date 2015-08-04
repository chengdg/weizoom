# -*- coding: utf-8 -*-

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

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from core.dateutil import get_today

from excel_response import ExcelResponse

from account.models import *
from models import *
from modules.member.models import IntegralStrategySttings

import export


COUNT_PER_PAGE = 20


FIRST_NAV_NAME = 'webapp'
ARTICLE_NAV = 'cms-article'


########################################################################
# list_articles: 显示文章列表
########################################################################
@login_required
def list_articles(request):
	articles = Article.objects.filter(owner=request.user).order_by('display_index')

	c = RequestContext(request, {
		'articles': articles,
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': ARTICLE_NAV
	})

	return render_to_response('cms/editor/articles.html', c)

########################################################################
# add_article: 添加文章
########################################################################
@login_required
def add_article(request):
	if request.POST:
		article = Article.objects.create(
			owner = request.user,
			title = request.POST.get('title', '').strip(),
			summary = request.POST.get('summary', '').strip(),
			content = request.POST.get('content', '').strip(),
		)
		first_article = Article.objects.filter(owner=request.user).order_by('-display_index')[0]
		article.display_index = first_article.display_index+1
		article.save()

		category_id = int(request.POST.get('category', -1))
		if category_id != -1:
			CategoryHasArticle.objects.create(category_id=category_id, article=article)

		return HttpResponseRedirect('/cms/editor/articles/')
	else:
		categories = Category.objects.filter(owner=request.user)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': ARTICLE_NAV,
			'categories': categories
		})
		return render_to_response('cms/editor/edit_article.html', c)


########################################################################
# update_article: 更新文章
########################################################################
@login_required
def update_article(request, article_id):
	if request.POST:
		#更新article
		Article.objects.filter(owner=request.user, id=article_id).update(
			title = request.POST.get('title', '').strip(),
			summary = request.POST.get('summary', '').strip(),
			content = request.POST.get('content', '').strip()
		)

		CategoryHasArticle.objects.filter(article_id=article_id).delete()
		category_id = int(request.POST.get('category', -1))
		if category_id != -1:
			CategoryHasArticle.objects.create(category_id=category_id, article_id=article_id)

		return HttpResponseRedirect('/cms/editor/articles/')
	else:
		article = Article.objects.get(owner=request.user, id=article_id)

		target_category = None
		article_related_categories = CategoryHasArticle.objects.filter(article=article)
		if article_related_categories.count() > 0:
			target_category = article_related_categories[0].category

		categories = Category.objects.filter(owner=request.user)
		if target_category:
			for category in categories:
				if category.id == target_category.id:
					category.is_selected = True

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': ARTICLE_NAV,
			'article': article,
			'categories': categories
		})
		return render_to_response('cms/editor/edit_article.html', c)

########################################################################
# delete_article: 删除文章
########################################################################
@login_required
def delete_article(request, article_id):
	CategoryHasArticle.objects.filter(article_id=article_id).delete()
	Article.objects.filter(id=article_id).delete()

	return  HttpResponseRedirect('/cms/editor/articles/')
