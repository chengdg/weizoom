# -*- coding: utf-8 -*-

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
# get_link_targets: 获得系统中的链接目标
######################################################################
def get_link_targets(request):
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')
	project_id = request.GET['project_id']

	response = create_response(200)

	#获得category集合
	categories = []
	category_records = pagestore.get_records(project_id, category_page_id)
	for category_record in category_records:
		categories.append({'text': category_record['model']['name'], 'value': './?type=viper&rid='+category_record['id']})

	#获得article
	article_records = pagestore.get_records(project_id, article_page_id)
	articles = []
	for article_record in article_records:
		articles.append({'text': article_record['model']['title'], 'value': './?type=viper&rid='+article_record['id']})

	response.data = [
		{
			'name': u'文章分类',
			'data': categories
		}, {
			'name': u'文章',
			'data': articles
		}
	]
	return response.get_response()