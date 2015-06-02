# -*- coding: utf-8 -*-

import logging
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
from termite.core import stripper

from models import *
from account.models import UserProfile
from termite.core.jsonresponse import create_response
import pagerender
import pagestore as pagestore_manager


#######################################################################
# get_datasource_project_pages: 获得数据源project中的page集合
#######################################################################
@login_required
def get_datasource_project_pages(request):
	pagestore = pagestore_manager.get_pagestore(request)

	project_id = request.GET['project_id']
	project = Project.objects.get(id=project_id)
	workspace = Workspace.objects.get(id=project.workspace_id)

	pages = [{'name': u'选择页面...', 'value': '-1'}]
	if workspace.data_backend:
		type, name_or_id = workspace.data_backend.split(':')
		if type == 'viper':
			datasource_project_id = name_or_id
			for page in pagestore.get_pages(datasource_project_id):
				page_model = page['component']['model']
				one_page = {}
				one_page['name'] = page_model['title']
				one_page['value'] = page['page_id']

				pages.append(one_page)
		elif type == 'module':
			module_info = 'webapp.modules.%s.export' % name_or_id
			module = __import__(module_info, {}, {}, ['*',])
			pages = [{'name': u'选择页面...', 'value': '0'}]
			pages.extend(module.PAGES)

	response = create_response(200)
	response.data = pages
	return response.get_response()