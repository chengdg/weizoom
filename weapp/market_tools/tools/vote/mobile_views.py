# -*- coding: utf-8 -*-
from __future__ import division
__author__ = 'chuter'

import os

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response

from core.exceptionutil import unicode_full_stack

from models import *

from modules.member.util import get_member

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
def get_vote(request):
	vote_id = int(request.GET['vote_id'])

	try:
		vote = Vote.objects.get(id=vote_id)
	except:
		c = RequestContext(request, {
			'is_deleted_data': True,
			'is_hide_weixin_option_menu':False
		})
		return render_to_response('%s/vote/webapp/my_vote_list.html' % TEMPLATE_DIR, c)
	
	hide_non_member_cover = False
	if vote.is_non_member:
		hide_non_member_cover = True
	
	vote_options = VoteOption.objects.filter(vote=vote)
	
	#如果选择柱状图
	if vote.show_style:
		webapp_user = request.webapp_user
		vote.webapp_user_vote_info = Vote.webapp_user_vote(vote_id, webapp_user)
		vote_options = _add_vote_option_bar_with(vote_options)
	
	# #是否展现搜索功能，总量大于一页的时候进行展现
	# is_show_search = True if vote_options.count() > COUNT_PER_PAGE else False

	# search = request.GET.get('search', '').strip()
	# if len(search) > 0:
	# 	vote_options = vote_options.filter(name__contains=search)

	# vote_options.order_by('-vote_count')

	c = RequestContext(request, {
		'page_title': vote.name,
		'vote_options': vote_options,
	    # 'search': search,
	    'vote': vote,
	    'hide_non_member_cover' : hide_non_member_cover,
	    'is_hide_weixin_option_menu':False
	    # 'COUNT_PER_PAGE': COUNT_PER_PAGE,
	    # 'is_show_search': is_show_search
	})
	if vote.show_style:
		return render_to_response('%s/vote/webapp/vote_bar.html' % TEMPLATE_DIR, c)
	else:	
		return render_to_response('%s/vote/webapp/my_vote.html' % TEMPLATE_DIR, c)
		

def _add_vote_option_bar_with(vote_options):
	hight_vote_count = 0
	for vote_option in vote_options:
		if vote_option.vote_count > hight_vote_count:
			hight_vote_count = vote_option.vote_count
			
	#根据最大票数计算条形宽度，最大占页面宽度80%
	for vote_option in vote_options:
		if hight_vote_count:
			vote_option.width = int(vote_option.vote_count * 80 / hight_vote_count)
		else:
			vote_option.width = 0
		
	return vote_options


def _build_vote_link(request, vote):
	if vote is None:
		return ''
	workspace_template_info = 'workspace_id=market_tool:vote&webapp_owner_id=%d&project_id=0' % request.project.owner_id

	return './?module=market_tool:vote&model=vote&action=get&vote_id=%d&%s' % (vote.id, workspace_template_info)

def get_usage(request):
	webapp_user = request.webapp_user
	webapp_user_voted_votes = Vote.get_webapp_user_voted_votes(webapp_user)
	for vote in webapp_user_voted_votes:
		vote.url = _build_vote_link(request, vote)
		
	c = RequestContext(request, {
		'page_title': u'我的投票',
	    'votes': webapp_user_voted_votes,
	    'is_hide_weixin_option_menu':False
	})

	return render_to_response('%s/vote/webapp/my_vote_list.html' % TEMPLATE_DIR, c)
