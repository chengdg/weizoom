# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core import dateutil

from models import *


###############################################
#get_problem_title_list: 
###############################################
@login_required
def get_problem_title_list(request):
	response = create_response(200)
	items = []

	try:
		titles = CommonProblemTitle.objects.all().order_by('display_index','created_at')
	except:
		titles = ''
    
    #封装siteMenu数据
	for title in titles:
		data = dict()
		data['id'] = title.id
		data['title'] = title.problem_title
		data['display_index'] = title.display_index
		items.append(data)
	
	response.data.items = items
	return response.get_response()


#==============================================
#更新标题排序
#==============================================
def update_problem_title_display_index(request):
	menu_ids = request.GET['sorted_menu_ids'].split('_')
	for index, menu_id in enumerate(menu_ids):
		CommonProblemTitle.objects.filter(id=menu_id).update(display_index=index+1)
	response = create_response(200)
	return response.get_response()


#===============================================
#list_problems:获得问题列表
#===============================================
def list_problems(request, title_id):
	response = create_response(200)
	items = []
	try:
		title = CommonProblemTitle.objects.get(id=title_id)
		problems = CommonProblem.objects.filter(problem_title=title).order_by('display_index')
	except:
		titles = ''
		problems = ''
    
    #封装siteMenu数据
	for problem in problems:
		data = dict()
		data['id'] = problem.id
		data['problem'] = problem.problem
		data['answer'] = problem.answer
		data['display_index'] = problem.display_index
		items.append(data)
	
	response.data.items = items
	return response.get_response()


#
#增加常见问题
#
def add_problem(request):
	if request.POST:
		response = create_response(200)
		id = request.POST['id']
		titleName = request.POST['titleName']
		problem = request.POST['problem'].replace('<p>','').replace('</p>','').replace('<br/>','')
		answer = request.POST['answer'].replace('<p>','').replace('</p>','').replace('<br/>','')

		problem_title = CommonProblemTitle.objects.get(id=id)#.update(problem_title=titleName)
		problem_title.problem_title = titleName
		problem_title.save()
		
		problems = CommonProblem.objects.filter(problem_title=problem_title).order_by('display_index')
		if problems.count()>0:
			display_index = problems[problems.count()-1].display_index+1
		else:
			display_index = 1
		CommonProblem.objects.create(problem_title=problem_title,problem=problem,answer=answer,display_index=display_index)

		return response.get_response()
	else:
		response = create_response(500)
	return response.get_response()


#
#add_problem_title 增加标题
#
def add_problem_title(request):
	if request.POST:
		response = create_response(200)
		id = int(request.POST['id'])
		titleName = request.POST['titleName']
		print (id==0)
		if id == 0:
			problem_titles = CommonProblemTitle.objects.all().order_by('display_index')
			
			if problem_titles.count() > 0:
				display_index = problem_titles[problem_titles.count()-1].display_index+1
			else:
				display_index = 1
			problem_title = CommonProblemTitle.objects.create(problem_title=titleName,display_index=display_index)
			id = problem_title.id
		else:
			problem_title = CommonProblemTitle.objects.get(id=id)
			problem_title.problem_title=titleName
			problem_title.save()
			
		response.data.id = id
	else:
		response = create_response(500)
	return response.get_response()


#
#更新问题顺序
#
def update_problems_display_index(request):
	menu_ids = request.GET['sorted_menu_ids'].split('_')
	for index, menu_id in enumerate(menu_ids):
		CommonProblem.objects.filter(id=menu_id).update(display_index=index+1)
	response = create_response(200)
	return response.get_response()


#
#add_feedback
#
def add_feedback(request):
	if request.POST:
		detail = request.POST['detail']
		user_profile = request.user.get_profile()
		Feedback.objects.create(user=request.user,webapp_temp=user_profile.webapp_template,content=detail)
		response = create_response(200)
		return response.get_response()
	else:
		return render_to_response('operation/editor/add_feedback.html')