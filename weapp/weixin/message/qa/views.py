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

from models import *
from weixin.message.material.models import News

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from core import emotion

from utils.json_util import string_json

import weixin

FIRSTT_NAV_NAME = weixin.NAV_NAME
WEIXIN_SECOND_NAVS = weixin.get_weixin_second_navs()

COUNT_PER_PAGE = 20

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
	

########################################################################
# edit_follow_rule: 编辑关注自动回复
########################################################################
@login_required
def edit_follow_rule(request):
	rule = None
	newses_object = []
	try:
		rule = Rule.objects.get(owner=request.user, type=FOLLOW_TYPE)
	except:
		rule = None

	if rule:
		rule.answer = emotion.change_emotion_to_img(rule.answer)
		newses = list(News.objects.filter(material_id=rule.material_id))
		newses_object = __get_newses(newses)


	c = RequestContext(request, {
		'first_nav_name' : FIRSTT_NAV_NAME,
		'second_navs' : WEIXIN_SECOND_NAVS,
		'second_nav_name' : weixin.WEIXIN_QA_FOLLOW_QA_NAV_NAME,
		'rule': rule,
		'newses': json.dumps(newses_object)
	})
	return render_to_response('qa/edit_follow_rule.html', c)


########################################################################
# edit_unmatch_rule: 编辑不匹配时的自动回复
########################################################################
@login_required
def edit_unmatch_rule(request):
	rule = None
	newses_object = []
	try:
		rule = Rule.objects.get(owner=request.user, type=UNMATCH_TYPE)
	except:
		rule = None

	if rule:
		rule.answer = emotion.change_emotion_to_img(rule.answer)
		newses = list(News.objects.filter(material_id=rule.material_id))
		newses_object = __get_newses(newses)

	c = RequestContext(request, {
		'first_nav_name' : FIRSTT_NAV_NAME,
		'second_navs' : WEIXIN_SECOND_NAVS,
		'second_nav_name' : weixin.WEIXIN_QA_AUTO_QA_NAV_NAME,
		'rule': rule,
		'newses': json.dumps(newses_object)
	})
	return render_to_response('qa/edit_unmatch_rule.html', c)

########################################################################
# list_rules: 显示分类规则
########################################################################
@login_required
def list_rules(request):
	category = None
	webapp_template = request.user.get_profile().webapp_template
	
	rules = Rule.get_keyword_reply_rule(request.user)

	c = RequestContext(request, {
		'first_nav_name' : FIRSTT_NAV_NAME,
		'second_navs' : WEIXIN_SECOND_NAVS,
		'second_nav_name' : weixin.WEIXIN_QA_KEYWORD_QA_NAV_NAME,
		'rules': rules,
	    'webapp_template': webapp_template
	})
	return render_to_response('qa/list_rules.html', c)


########################################################################
# add_rule: 添加关键词
########################################################################
@login_required
def add_rule(request):
	c = RequestContext(request, {
		'first_nav_name' : FIRSTT_NAV_NAME,
		'second_navs' : WEIXIN_SECOND_NAVS,
		'second_nav_name' : weixin.WEIXIN_QA_KEYWORD_QA_NAV_NAME
	})
	return render_to_response('qa/edit_rule.html', c)


########################################################################
# update_rule: 修改关键词
########################################################################
@login_required
def update_rule(request, rule_id):
	rule = None
	try:
		rule = Rule.objects.get(owner=request.user, id=rule_id)
	except:
		raise Http404('Rule Not Found')

	if rule.type == NEWS_TYPE:
		newses = list(News.objects.filter(material_id=rule.material_id))
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

		c = RequestContext(request, {
			'first_nav_name' : FIRSTT_NAV_NAME,
			'second_navs' : WEIXIN_SECOND_NAVS,
			'second_nav_name' : weixin.WEIXIN_QA_KEYWORD_QA_NAV_NAME,
			'rule': rule,
			'newses': json.dumps(newses_object)
		})
		return render_to_response('qa/edit_rule.html', c)

	elif rule.type == TEXT_TYPE:
		if rule:
			rule.answer = emotion.change_emotion_to_img(rule.answer)

		c = RequestContext(request, {
			'first_nav_name' : FIRSTT_NAV_NAME,
			'second_navs' : WEIXIN_SECOND_NAVS,
			'second_nav_name' : weixin.WEIXIN_QA_KEYWORD_QA_NAV_NAME,
			'rule': rule
		})
		return render_to_response('qa/edit_rule.html', c)


########################################################################
# delete_rule: 删除规则
########################################################################
@login_required
def delete_rule(request, rule_id):
	Rule.objects.filter(owner=request.user, id=rule_id).delete()
	return HttpResponseRedirect('/weixin/message/qa/')
	