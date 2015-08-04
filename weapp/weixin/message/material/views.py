# -*- coding: utf-8 -*-

__author__ = 'chuter'

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
from utils.json_util import string_json

from models import *
from weixin.message.material.models import News
from weixin.user.models import set_share_img
from account.models import OperationSettings
from modules.member.util import get_member
from watchdog.utils import watchdog_alert
from core.exceptionutil import unicode_full_stack

import weixin

from weixin.user.module_api import get_mp_nick_name

FIRSTT_NAV_NAME = weixin.NAV_NAME
WEIXIN_SECOND_NAVS = weixin.get_weixin_second_navs()

########################################################################
# show_news_detail: 显示图文详情
########################################################################
def show_news_detail(request, newsid):
	try:
		news = News.objects.get(id=newsid)
		# 为了支持是否显示点击关注的区域
		settings = OperationSettings.get_settings_for_user(news.user.id)
		request.operation_settings = settings
		request.user_profile = news.user.get_profile()
		request.member = get_member(request)
		nick_name = get_mp_nick_name(news.user.id)

		#设置分享图片为默认头像
		set_share_img(request)
	except:
		alert_message = u"显示图文详情异常,素材id：{}, cause:\n{}".format(newsid, unicode_full_stack())
		watchdog_alert(alert_message)
		raise Http404(u'不存在该素材')

	c = RequestContext(request, {
		'page_title': news.title,
		'detail': news.text,
		'pic_url': news.pic_url,
		'is_show_cover_pic': news.is_show_cover_pic,
		'date': news.created_at.strftime('%Y-%m-%d'),
		'nick_name': nick_name if nick_name else '',
		'hide_non_member_cover':True,
		'share_page_desc':news.summary,
		'share_img_url':news.pic_url
	})
	return render_to_response('material/detail.html', c)

########################################################################
# list_news: 显示图文列表
########################################################################
@login_required
def list_news(request):
	materials = Material.objects.filter(owner=request.user, is_deleted=False)
	c = RequestContext(request, {
		'first_nav_name' : FIRSTT_NAV_NAME,
		'second_navs' : WEIXIN_SECOND_NAVS,
		'second_nav_name' : weixin.WEIXIN_QA_MATERAL_NEWS_NAV_NAME,
		'materials': materials,
	})
	return render_to_response('material/list_news.html', c)


########################################################################
# add_single_news: 添加单图文规则
########################################################################
@login_required
def add_single_news(request):
	c = RequestContext(request, {
		'first_nav_name' : FIRSTT_NAV_NAME,
		'second_navs' : WEIXIN_SECOND_NAVS,
		'second_nav_name' : weixin.WEIXIN_QA_MATERAL_NEWS_NAV_NAME,
		'newses': []
		#'return_url': request.META['HTTP_REFERER'],
	})
	return render_to_response('material/edit_single_news.html', c)


########################################################################
# add_multi_news: 添加多图文规则
########################################################################
@login_required
def add_multi_news(request):
	c = RequestContext(request, {
		'first_nav_name' : FIRSTT_NAV_NAME,
		'second_navs' : WEIXIN_SECOND_NAVS,
		'second_nav_name' : weixin.WEIXIN_QA_MATERAL_NEWS_NAV_NAME,
		'newses': []
		#'return_url': request.META['HTTP_REFERER'],
	})
	return render_to_response('material/edit_multi_news.html', c)


########################################################################
# update_news: 修改图文信息
########################################################################
@login_required
def update_news(request, material_id):
	newses = list(News.objects.filter(material_id=material_id))
	news_count, newses_object = __get_newses_object(newses)
	c = RequestContext(request, {
		'first_nav_name' : FIRSTT_NAV_NAME,
		'second_navs' : WEIXIN_SECOND_NAVS,
		'second_nav_name' : weixin.WEIXIN_QA_MATERAL_NEWS_NAV_NAME,
	    'material_id': material_id,
		'newses': json.dumps(newses_object)
	})
	if news_count > 1 :
		return render_to_response('material/edit_multi_news.html', c)
	else:
		return render_to_response('material/edit_single_news.html', c)


def __get_newses_object(newses):
	newses_object = []
	news_count = len(newses)
	for news in newses:
		one_news = {}
		one_news['id'] = news.id
		one_news['title'] = news.title
		one_news['display_index'] = news.display_index
		one_news['type'] = 'news'
		if news_count > 0:
			one_news['text'] = string_json(news.text.encode("utf-8"))
		one_news['date'] = news.created_at.strftime('%m月%d日').strip('0')
		one_news['url'] = news.url
		if len(news.link_target) > 0:
			one_news['link_target'] = json.loads(news.link_target)
		else:
			one_news['link_target'] = {}
		one_news['pic_url'] = news.pic_url
		one_news['summary'] = string_json(news.summary)
		if news.display_index == 1:
			one_news['metadata'] = {'autoSelect':'true'};
		else:
			one_news['metadata'] = {};
		one_news['is_show_cover_pic'] = news.is_show_cover_pic
		newses_object.append(one_news)
	return news_count, newses_object
