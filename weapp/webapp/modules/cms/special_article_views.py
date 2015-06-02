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
ARTICLE_NAV = 'cms-special-article'

# 一个用户的默认special article在account.models中的signal handler中创建

########################################################################
# list_articles: 显示文章列表
########################################################################
@login_required
def list_articles(request):
	articles = SpecialArticle.objects.filter(owner=request.user)

	c = RequestContext(request, {
		'articles': articles,
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': ARTICLE_NAV
	})

	return render_to_response('cms/editor/special_articles.html', c)


########################################################################
# update_article: 更新文章
########################################################################
@login_required
def update_article(request, article_id):
	if request.POST:
		#更新article
		SpecialArticle.objects.filter(owner=request.user, id=article_id).update(
			content = request.POST.get('content', '').strip()
		)

		return HttpResponseRedirect('/cms/editor/special_articles/')
	else:
		article = SpecialArticle.objects.get(owner=request.user, id=article_id)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': ARTICLE_NAV,
			'article': article
		})

		if article.name == 'not_from_weixin':
			return render_to_response('cms/editor/special_not_from_mobile_article.html', c)
		else:
			return render_to_response('cms/editor/special_content_article.html', c)
