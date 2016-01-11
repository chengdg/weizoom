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

from core.jsonresponse import JsonResponse, create_response
from core import emotion

#from models import *
from weixin2.models import *
from weixin.message.material.models import News
from market_tools.question.models import QuestionInfo

from utils.json_util import string_json

#TODO 和佩瑜重构自定义菜单使用的api
'''
@login_required
def get_newses(request):
	rule = Rule.objects.get(id=request.POST['id'])
	newses = list(News.objects.filter(material_id=rule.material_id))
	newses_object = __get_newses(newses)
	response = create_response(200)
	one_rule = {}
	one_rule['id'] = rule.id
	one_rule['type'] = rule.type
	one_rule['patterns'] = rule.patterns
	one_rule['material_id'] = rule.material_id
	one_rule['answer'] = rule.answer
	response.data.rule = one_rule
	response.data.newses = newses_object
	return response.get_response()


def __get_newses(newses):
	newses_object = []
	news_count = len(newses)
	for news in newses:
		one_news = {}
		one_news['id'] = news.id
		one_news['title'] = string_json(news.title)
		one_news['display_index'] = news.display_index
		one_news['type'] = 'news'
		if news_count > 0:
			one_news['text'] = string_json(news.text.encode("utf-8"))
		one_news['date'] = news.created_at.strftime('%m月%d日').strip('0')
		one_news['url'] = news.url
		one_news['pic_url'] = news.pic_url
		one_news['summary'] = string_json(news.summary)
		if news.display_index == 1:
			one_news['metadata'] = {'autoSelect':'true'};
		else:
			one_news['metadata'] = {};
		newses_object.append(one_news)
	return newses_object


@login_required
def get_keywords(request):
	rules = Rule.objects.filter(owner=request.user, type__in=[TEXT_TYPE, NEWS_TYPE])
	data = []
	for rule in rules:
		one_rule = dict()
		one_rule['id'] = rule.id
		one_rule['patterns'] = rule.patterns
		data.append(one_rule)

	response = create_response(200)
	response.data.rules = data
	return response.get_response()
'''

########################################################################
# check_duplicate_patterns: 检查pattern是否有重复
########################################################################
@login_required
def check_duplicate_patterns(request):
	patterns = request.POST['patterns']
	ignore_rule_id = request.POST.get('rule', None)
	has_duplicate, duplicate_patterns = has_duplicate_pattern(request.user, patterns, ignore_rule_id)

	questions = QuestionInfo.objects.filter(owner=request.user, start_patterns=patterns, is_deleted=False)
	if has_duplicate:
		response = create_response(601)
		response.errMsg = u'下列关键词已经存在: %s' % duplicate_patterns[0]
		return response.get_response()
	elif questions.count() > 0:
		response = create_response(601)
		response.errMsg = u'下列关键词已经存在: %s' % questions[0].start_patterns
		return response.get_response()
	else:
		return create_response(200).get_response()


########################################################################
# __package_rule: 封装rule为json response
########################################################################
def __package_rule(rule, should_change_emotion=False):
	response = create_response(200)
	response.data = dict()
	response.data['id'] = rule.id
	response.data['patterns'] = rule.patterns
	if should_change_emotion:
		response.data['answer'] = emotion.change_emotion_to_img(rule.answer)
	else:
		response.data['answer'] = rule.answer

	return response.get_response()


########################################################################
# add_rule: 添加关键词内容
########################################################################
@login_required
def add_rule(request):
	patterns = request.POST['patterns'].strip()
	answer = request.POST['answer']
	material_id = int(request.POST.get('material_id', 0))

	if material_id == 0:
		type = TEXT_TYPE
	else:
		type = NEWS_TYPE
	rule = Rule.objects.create(
		owner = request.user,
		type = type,
		patterns = patterns,
		answer = answer,
		material_id = material_id
	)

	return __package_rule(rule)


########################################################################
# update_rule: 更新关键词内容
########################################################################
@login_required
def update_rule(request):
	rule_id = int(request.POST.get('rule_id', -1))
	patterns = request.POST['patterns'].strip()
	answer = request.POST['answer']
	material_id = int(request.POST.get('material_id', 0))

	if material_id == 0:
		type = TEXT_TYPE
	else:
		type = NEWS_TYPE

	Rule.objects.filter(id=rule_id).update(
		patterns = patterns,
		answer = answer,
		material_id = material_id,
		type = type
	)

	return __package_rule(Rule.objects.get(id=rule_id))

########################################################################
# add_follow_rule: 添加关注自动回复消息
########################################################################
@login_required
def add_follow_rule(request):
	answer = request.POST['answer']
	material_id = request.POST['material_id']

	rule = Rule.objects.create(
		owner = request.user,
		type = FOLLOW_TYPE,
		answer = answer,
		material_id = material_id
	)

	return __package_rule(rule, True)


########################################################################
# update_follow_rule: 更新关注自动回复消息
########################################################################
@login_required
def update_follow_rule(request):
	rule_id = int(request.POST.get('rule_id', -1))
	answer = request.POST['answer']
	material_id = request.POST['material_id']

	rule = Rule.objects.filter(id=rule_id).update(
		answer = answer,
		material_id = material_id
	)

	return __package_rule(Rule.objects.get(id=rule_id), True)


########################################################################
# add_unmatch_rule: 添加关键词不匹配时的自动回复
########################################################################
@login_required
def add_unmatch_rule(request):
	answer = request.POST['answer']
	material_id = request.POST['material_id']

	active_type = int(request.POST.get('active_type', 1))
	start_hour = int(request.POST.get('start_hour', 0))
	end_hour = int(request.POST.get('end_hour', 1))

	rule = Rule.objects.create(
		owner = request.user,
		active_type = active_type,
		start_hour = start_hour,
		end_hour = end_hour,
		type = UNMATCH_TYPE,
		patterns = '',
		answer = answer,
		material_id = material_id
	)

	return __package_rule(rule, True)


########################################################################
# update_unmatch_rule: 更新关键词不匹配时的自动回复
########################################################################
@login_required
def update_unmatch_rule(request):
	rule_id = int(request.POST.get('rule_id', -1))
	answer = request.POST['answer']
	material_id = request.POST['material_id']
	active_type = request.POST['active_type']
	start_hour = request.POST['start_hour']
	end_hour = request.POST['end_hour']

	Rule.objects.filter(id=rule_id).update(
		answer = answer, 
		active_type = active_type,
		start_hour = start_hour,
		end_hour = end_hour,
		material_id = material_id
	)

	return __package_rule(Rule.objects.get(id=rule_id), True)


'''
########################################################################
# __package_news: 封装news为json response
########################################################################
def __package_news(news):
	response = create_response(200)
	response.id = news.id
	response.data.title = news.title
	response.data.pic_url = news.pic_url
	response.data.description = news.description
	response.data.url = news.url
	response.data.date = news.created_at.strftime('%m月%d日').strip('0')

	return response.get_response()


########################################################################
# __package_newses: 封装newses为json response
########################################################################
def __package_newses(newses):
	data = []
	for news in newses:
		one_news = dict()
		one_news['id'] = news.id
		one_news['title'] = news.title
		one_news['type'] = 'news'
		one_news['pic_url'] = news.pic_url
		one_news['text'] = news.text
		one_news['url'] = news.url
		one_news['date'] = news.created_at.strftime('%m月%d日').strip('0')
		one_news['summary'] = news.summary
		one_news['display_index'] = news.display_index
		if news.display_index == 1:
			one_news['metadata'] = {'autoSelect':'true'};
		else:
			one_news['metadata'] = {};

		data.append(one_news)

	return data


########################################################################
# api_add_news: 添加图文消息
########################################################################
@login_required
def add_news(request):
	rule_id = int(request.POST['rule_id'])
	category_id = int(request.POST.get('category_id', 0))
	patterns = request.POST.get('patterns', '').strip()
	material_id = int(request.POST.get('material_id', 0))

	rule = None
	if rule_id == -1:
		rule = Rule.objects.create(
			owner = request.user,
			category_id = category_id,
			type = NEWS_TYPE,
			patterns = patterns,
			answer = '',
			material_id = material_id
		)
	else:
		rule = Rule.objects.get(id=rule_id)
		if rule.patterns != patterns:
			rule.patterns = patterns
			rule.save()

	#返回当前所以news
	newses = News.objects.filter(material_id=rule.material_id)
	response = create_response(200)
	response.data.id = rule.id
	response.data.newses = __package_newses(newses)
	return response.get_response()
'''