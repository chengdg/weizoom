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

from tools.regional import views as regional_util
from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import unicode_full_stack
from core import dateutil

from modules.member.models import Member
from models import *

from watchdog.utils import watchdog_fatal


########################################################################
# get_system_help_categories: 获得系统帮助的分类信息
########################################################################
def get_system_help_categories():
	user = User.objects.get(username='product_support')
	categories = list()
	id2category = dict()
	category_ids = set()
	for category in Category.objects.filter(owner=user):
		category_data = {
			'id': category.id,
			'name': category.name,
			'articles': list()
		}

		categories.append(category_data)
		id2category[category.id] = category_data
		category_ids.add(category.id)

	category_article_relations = list(CategoryHasArticle.objects.filter(category_id__in=category_ids))
	article2category = dict([(r.article_id, r.category_id) for r in category_article_relations])
	article_ids = [r.article_id for r in category_article_relations]
	for id, title in  Article.objects.filter(id__in=article_ids).values_list('id', 'title'):
		category_id = article2category[id]
		id2category[category_id]['articles'].append({
			'id': id,
			'title': title
		})

	return categories


