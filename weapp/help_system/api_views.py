# -*- coding: utf-8 -*-
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

from models import *
import module_api as help_system_api
from account.models import UserProfile
from core.jsonresponse import create_response
from core import apiview_util

##############################################################
# get_document_targets: 获得文档链接集合
##############################################################
def get_document_targets(request):
	page_id = request.GET.get('page_id', None)
	page_help = PageHelp()
	page_help.document_id = None
	if page_id:
		try:
			page_help = PageHelp.objects.get(page_id=page_id)
		except:
			pass		

	links = [{'id':0, 'title':u'无帮助文档'}]
	for document in Document.objects.all():
		links.append({
			'id': document.id,
			'title': document.title
		})

	response = create_response(200)
	response.data = {
		'links': links,
		'page_help_document_id': page_help.document_id
	}

	return response.get_response()


########################################################################
# update_page_help: 更新页面的帮助信息
########################################################################
def update_page_help(request):
	page_id = request.POST['page_id']
	document_id = int(request.POST['document_id'])

	if document_id == 0:
		PageHelp.objects.filter(page_id=page_id).delete()
	else:
		if PageHelp.objects.filter(page_id=page_id).count() > 0:
			#更新PageHelp
			PageHelp.objects.filter(page_id=page_id).update(document=document_id)
		else:
			#创建PageHelp
			PageHelp.objects.create(
				page_id = page_id,
				document_id = document_id
			)

	return create_response(200).get_response()


########################################################################
# get_document: 获得帮助文档
########################################################################
def get_document(request):
	page_id = request.GET.get('page_id', None)
	if page_id:
		try:
			document = Document.objects.get(page_id=page_id)
			response = create_response(200)
			response.data = {
				'content': document.content
			}

			return response.get_response()
		except:
			pass
	else:
		pass

	response = create_response(200)
	response.data = {
		'content': '<div class="tc mt10">本页面无帮助文档</div>'
	}
	return response.get_response()


########################################################################
# get_feature_content: 获得feature内容
########################################################################
def get_feature_content(request):
	feature_id = request.GET.get('id', '0')
	if feature_id == '0':
		return create_response(404).get_response()

	response = create_response(200)
	response.data = help_system_api.get_feature_content(feature_id)
	return response.get_response()


########################################################################
# get_all_features: 获得所有feature内容
########################################################################
def get_all_features(request):
	response = create_response(200)
	response.data = help_system_api.get_all_features()
	return response.get_response()


def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)