# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random

from django.template import Context, RequestContext
from django.conf import settings

from core.jsonresponse import create_response, JsonResponse


######################################################################
# get_link_targets: 获得系统中的链接目标
######################################################################
def get_link_targets(request):
	response = create_response(200)

	pages = [{
		'text': u'微站首页',
		'value': './?workspace_id=home_page&webapp_owner_id=%d' % request.workspace.owner_id
	}]
	response.data = [
		{
			'name': u'页面',
			'data': pages
		}
	]
	return response.get_response()
