# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator

from models import *
from module_api import get_system_help_categories


########################################################################
# update_article_display_index: 修改排列顺序
########################################################################
@login_required
def update_article_display_index(request):
	src_id = request.POST.get('src_id', None)
	dst_id = request.POST.get('dst_id', None)

	if not src_id or not dst_id:
		response = create_response(500)
		response.errMsg = u'invalid arguments: src_id(%s), dst_id(%s)' % (src_id, dst_id)
		return response.get_response()		

	src_id = int(src_id)
	dst_id = int(dst_id)
	if dst_id == 0:
		#dst_id = 0, 将src的display_index设置得比第一个数据的display_index大即可
		first_article = Article.objects.filter(owner=request.user).order_by('-display_index')[0]
		if first_article.id != src_id:
			Article.objects.filter(id=src_id).update(display_index=first_article.display_index+1)
	else:
		#dst_id不为0，交换src, dst的display_index
		id2article = dict([(p.id, p) for p in Article.objects.filter(id__in=[src_id, dst_id])])
		Article.objects.filter(id=src_id).update(display_index=id2article[dst_id].display_index)
		Article.objects.filter(id=dst_id).update(display_index=id2article[src_id].display_index)

	response = create_response(200)
	return response.get_response()


########################################################################
# get_articles: 获取article列表
########################################################################
@login_required
def get_articles(request):
	query = request.GET.get('query', None)
		
	#处理排序
	sort_attr = request.GET.get('sort_attr', None);
	if not sort_attr:
		sort_attr = '-display_index'
	articles = Article.objects.filter(owner=request.user).order_by(sort_attr)

	#处理过滤
	filter_category_id = request.GET.get('filter_value', None)
	if filter_category_id and int(filter_category_id) > 0:
		article_ids = [r.article_id for r in CategoryHasArticle.objects.filter(category_id=filter_category_id)]
		articles = articles.filter(id__in=article_ids)

	#处理搜索
	if query:
		articles = articles.filter(title__icontains=query)

	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, articles = paginator.paginate(articles, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

	#article关联的category集合
	id2article = dict()
	article_ids = []
	for article in articles:
		article.categories = []
		id2article[article.id] = article
		article_ids.append(article.id)

	category_ids = []
	category2articles = {}
	for relation in CategoryHasArticle.objects.filter(article_id__in=article_ids):
		category_id = relation.category_id
		article_id = relation.article_id
		category_ids.append(category_id)
		category2articles.setdefault(category_id, []).append(article_id)

	for category in Category.objects.filter(id__in=category_ids):
		for article_id in category2articles[category.id]:
			id2article[article_id].categories.append({
				'id': category.id,
				'name': category.name
			})

	#获得文章分类集合
	all_categories = []
	for category in Category.objects.filter(owner=request.user):
		all_categories.append({
			'id': category.id,
			'name': category.name
		})

	# 构造返回数据
	items = []
	for article in articles:
		items.append({
			'id': article.id,
			'title': article.title,
			'categories': article.categories,
			'created_at': datetime.strftime(article.created_at, '%Y-%m-%d %H:%M')
		})
	
	response = create_response(200)
	response.data = {
		'items': items,
		'pageinfo': paginator.to_dict(pageinfo),
		'categories': all_categories,
		'sortAttr': sort_attr
	}
	return response.get_response()


########################################################################
# get_article: 获取article内容
########################################################################
def get_article(request):
	article_id = request.GET.get('id', None)
	if not article_id:
		response = create_response(404)
		return response.get_response()

	article = Article.objects.get(id=article_id)

	response = create_response(200)
	response.data = {
		'id': article.id,
		'title': article.title,
		'content': article.content,
		'created_at': datetime.strftime(article.created_at, '%Y-%m-%d %H:%M')
	}

	return response.get_jsonp_response(request)


########################################################################
# get_help_center_categories: 获得系统帮助的左侧信息
########################################################################
def get_help_center_categories(request):
	try:
		categories = get_system_help_categories()
	except:
		categories = list()

	items = []
	for category in  categories:
		items.append({
			'id': category['id'],
			'name': category['name'],
			'articles': category['articles']
		})

	response = create_response(200)
	response.data = {
		'items': items
	}
	return response.get_jsonp_response(request)


