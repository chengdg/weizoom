# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
import shutil
try:
    import Image
except:
    from PIL import Image
import copy

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth

from models import *
from core.jsonresponse import create_response, JsonResponse
from termite import pagestore as pagestore_manager
import modules as raw_webapp_modules
from account.social_account.models import SocialAccount


########################################################################
# list_documents: 显示文档列表
########################################################################
@login_required
def list_documents(request):
	page_id = request.page_id
	
	c = RequestContext(request, {
		'first_nav_name': '',
		'documents': Document.objects.all()
	})
	return render_to_response('help/editor/documents.html', c)


########################################################################
# add_document: 添加文档
########################################################################
@login_required
def add_document(request):
	if request.POST:
		document = Document.objects.create(
			page_id = request.POST.get('page_id', '').strip(),
			title = '',
			content = request.POST.get('content', '').strip()
		)
		
		return HttpResponseRedirect(request.POST.get('redirect_url', '/'))
	else:
		c = RequestContext(request, {
			'page_id': request.GET['page_id'],
			'first_nav_name': '',
			'from_url': request.META['HTTP_REFERER']
		})
		return render_to_response('help/editor/edit_document.html', c)


########################################################################
# update_document: 更新文档
########################################################################
@login_required
def update_document(request):
	page_id = request.REQUEST.get('page_id', '')
	if request.POST:
		Document.objects.filter(page_id=page_id).update(
			content = request.POST.get('content', '').strip()
		)

		return HttpResponseRedirect(request.POST.get('redirect_url', '/'))
	else:
		document = Document.objects.get(page_id=page_id)
		c = RequestContext(request, {
			'page_id': request.GET['page_id'],
			'first_nav_name': '',
			'from_url': request.META['HTTP_REFERER'],
			'document': document
		})
		return render_to_response('help/editor/edit_document.html', c)
