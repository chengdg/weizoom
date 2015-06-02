# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth

from core.jsonresponse import JsonResponse
from core import paginator

from models import *

PROBLEM_NAV_NAME = 'operation-problem'
VERSION_NAV_NAME = 'operation-version'
FEEDBACK_NAV_NAME = 'operation-feedback'

COUNT_PER_PAGE = 3

########################################################################
# list_problems:问题列表
########################################################################
@login_required
def list_problem_titles(request):
	
	problems = CommonProblemTitle.objects.all().order_by('display_index')
	c = RequestContext(request, {
		'nav_name': PROBLEM_NAV_NAME,
		'embed_url': 'default',
		'problem_titles': problems
	})
	return render_to_response('operation/editor/list_problem_titles.html', c)


########################################################################
# delete_problem_title: 删除常见问题标题
########################################################################
@login_required
def delete_problem_title(request, title_id):
	CommonProblemTitle.objects.filter(id=title_id).delete()

	return HttpResponseRedirect(request.META['HTTP_REFERER'])

###################################################################
#获得常见问题标题
###################################################################
def get_problem_title(request, title_id):
	try:
		title = CommonProblemTitle.objects.get(id=title_id)
	except:
		title = ''
		
	c = RequestContext(request, {
		'nav_name': PROBLEM_NAV_NAME,
		'embed_url': 'default',
		'title': title
	})
	return render_to_response('operation/editor/list_problems.html', c)
#
#
#

def add_problem(request, title_id):
	if request.POST:
		pass
	else:
		c = RequestContext(request, {
			'nav_name': PROBLEM_NAV_NAME
		})
		return render_to_response('operation/editor/list_problems.html', c)


######
#版本升级列表
######
def list_versions(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	

	#获得product集合和分页信息
	
	versions = VersionUpdated.objects.all().order_by('-created_at')
	pageinfo, versions = paginator.paginate(versions, cur_page, COUNT_PER_PAGE, query_string=request.META['QUERY_STRING'])



	c = RequestContext(request, {
		'nav_name': VERSION_NAV_NAME,
	    'versions': versions,
	    'pageinfo': json.dumps(paginator.to_dict(pageinfo))
	})
	return render_to_response('operation/editor/list_versions.html', c)


#######
#修改版本升级信息
#######
def update_version(request, version_id):
	if request.POST:
		name = request.POST['name']
		detail = request.POST['detail']
		VersionUpdated.objects.filter(
			id=version_id
		).update(
			update_time=name,
			update_content=detail
		)
		return HttpResponseRedirect('/operation/editor/versions/')
	else:
		if version_id == 0:
			c = RequestContext(request, {
				'nav_name': VERSION_NAV_NAME,
			})
		else:
			version = VersionUpdated.objects.get(id=version_id)
			c = RequestContext(request, {
				'nav_name': VERSION_NAV_NAME,
				'version' : version
		})
		return render_to_response('operation/editor/edit_version.html', c)
		

#
#删除版本升级信息
#
def delete_version(request, version_id):
	VersionUpdated.objects.filter(id=version_id).delete()

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#
#增加版本升级信息
#
def add_version(request):
	if request.POST:
		name = request.POST['name']
		detail = request.POST['detail']
		VersionUpdated.objects.create(
			update_time=name,
			update_content=detail
		)
		return HttpResponseRedirect('/operation/editor/versions/')
	else:
		c = RequestContext(request, {
				'nav_name': VERSION_NAV_NAME,
		})
		return render_to_response('operation/editor/edit_version.html', c)


#
#list_feedbacks:反馈列表
#
def list_feedbacks(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	
	feedbacks = Feedback.objects.all().order_by('created_at')
	pageinfo, feedbacks = paginator.paginate(feedbacks, cur_page, COUNT_PER_PAGE, query_string=request.META['QUERY_STRING'])

	c = RequestContext(request, {
		'nav_name': FEEDBACK_NAV_NAME,
	    'feedbacks': feedbacks,
	    'pageinfo': json.dumps(paginator.to_dict(pageinfo))
	})
	return render_to_response('operation/editor/list_feedbacks.html', c)


#
#
#
def delete_problem(request,problem_id):
	CommonProblem.objects.filter(id=problem_id).delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#
#
#
# def use_help(request):
# 	CommonProblemTitle.objects.all().order_by('')

