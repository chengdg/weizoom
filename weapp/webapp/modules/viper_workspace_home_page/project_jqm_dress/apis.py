# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
try:
    import Image
except:
    from PIL import Image

from django.template import Context, RequestContext
from django.conf import settings

from models import *
from core.jsonresponse import create_response, JsonResponse
import pagestore as pagestore_manager


article_page_id = '3'
category_page_id = '1'


######################################################################
# get_article_list: 获取文章列表
######################################################################
def get_article_list(request):
	pagestore = pagestore_manager.get_pagestore(request)
	project_id = request.display_info['project_id']
	project = request.display_info['project']
	datasource_project_id = request.display_info['datasource_project_id']

	#获得category
	category_record = request.display_info['datasource_record']
	category_name = category_record['model']['name']

	#获得article
	article_records = pagestore.get_records(datasource_project_id, article_page_id)
	articles = []
	for article_record in article_records:
		article_model = article_record['model']
		print article_model['category'], ' ', category_name
		if article_model['category'] == category_name:
			articles.append({
				'title': article_model['title'],
				'summary': article_model['content'][:20],
				'link': './?type=viper&rid=%s&project_id=%d' % (article_record['id'], request.project.id)
			})

	data = {
		'article_list': {
			'articles': articles
		}
	}
	return data


######################################################################
# get_article: 获得文章详情
######################################################################
def get_article(request):
	article_record = request.display_info['datasource_record']
	article_model = article_record['model']

	data = {
		'article': {
			'title': article_model['title'],
			'publish_time': article_model['publish_time'],
			'content': article_model['content']
		}
	}
	return data
