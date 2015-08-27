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
	#pagestore = pagestore_manager.get_pagestore_by_type('mongo')
	project_id = request.GET['project_id']
	project = Project.objects.get(id=project_id)
	workspace = Workspace.objects.get(id=project.workspace_id)

	response = create_response(200)

	pages = [{
		'text': u'微站首页',
		'value': './?workspace_id=home_page&webapp_owner_id=%d&project_id=0' % request.workspace.owner_id
	}]
	response.data = [
		{
			'name': u'页面',
			'data': pages
		}
	]
	return response.get_response()
