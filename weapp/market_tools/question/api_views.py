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
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response, decode_json_str
from core import dateutil

from models import *
from qa.models import has_duplicate_pattern


########################################################################
# create_question: 创建一条问答数据
########################################################################
def create_question(request):
	response = create_response(200)
	start_patterns = request.POST.get('start_patterns','').strip()
	end_patterns = request.POST.get('end_patterns','').strip()
	finished_message = request.POST.get('finished_message','')
	problems = request.POST.get('problems')
	prizes = request.POST.get('prizes')

	question = QuestionInfo.objects.create(
		owner=request.user,
		start_patterns=start_patterns,
		end_patterns=end_patterns,
		finished_message=finished_message
	)
	json_problems = decode_json_str(problems)
	json_prizes = decode_json_str(prizes)

	display_index = 0
	for problem in json_problems:
		display_index = display_index + 1

		Problem.objects.create(
			question_answer=question,
			title=problem['title'],
			right_answer=problem['right_answer'],
			right_feedback=problem['right_feedback'],
			error_feedback=problem['error_feedback'],
			display_index=display_index
		)


	for prize in json_prizes:
		Prize.objects.create(
			question_answer=question,
			right_count_min=prize['right_count_min'],
			right_count_max=prize['right_count_max'],
			content=prize['content'],
			count=prize['count']
		)
	return response.get_response()



########################################################################
# get_problems: 获得所有问答题目
########################################################################
@login_required
def get_problems(request, question_id):
	response = create_response(200)
	response.data = []

	question_id = int(question_id)
	if question_id > 0:
		problems = Problem.objects.filter(question_answer_id=question_id)

		for problem in problems:
			data = dict()
			data['id'] = problem.id
			data['display_index'] = problem.display_index
			data['title'] = problem.title
			data['right_answer'] = problem.right_answer
			data['right_feedback'] = problem.right_feedback
			data['error_feedback'] = problem.error_feedback
			response.data.append(data)

	return response.get_response()


########################################################################
# get_prizes: 获得所有奖品
########################################################################
@login_required
def get_prizes(request, question_id):
	response = create_response(200)
	response.data = []

	question_id = int(question_id)
	if question_id > 0:
		prizes = Prize.objects.filter(question_answer_id=question_id)

		for prize in prizes:
			data = dict()
			data['id'] = prize.id
			data['right_count_min'] = prize.right_count_min
			data['right_count_max'] = prize.right_count_max
			data['content'] = prize.content
			data['count'] = prize.count
			response.data.append(data)

	return response.get_response()


########################################################################
# check_duplicate_start_patterns: 检查start_patterns是否有重复
########################################################################
@login_required
def check_duplicate_start_patterns(request):
	patterns = request.POST['patterns']
	ignore_rule_id = request.POST.get('rule', None)
	ignore_question_id = request.POST.get('question', None)
	has_duplicate, duplicate_patterns = has_duplicate_pattern(request.user, patterns, ignore_rule_id)

	ignore_group_id = request.POST.get('group', None)

	questions = QuestionInfo.objects.filter(owner=request.user, start_patterns=patterns, is_deleted=False)
	if ignore_question_id:
		questions = questions.filter( ~Q(id=int(ignore_group_id)) )

	if has_duplicate:
		response = create_response(601)
		response.errMsg = u'本系统已经有一个该关键词的规则，请重新设置一个'
		return response.get_response()
	elif questions.count() > 0:
		response = create_response(601)
		response.errMsg = u'本系统已经有一个该关键词的规则，请重新设置一个'
		return response.get_response()
	else:
		return create_response(200).get_response()