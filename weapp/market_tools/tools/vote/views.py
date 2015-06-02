# -*- coding: utf-8 -*-

__author__ = 'chuter'

import json

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.db.models import Sum

from models import *
from modules.member.models import Member

from market_tools import export
from excel_response import ExcelResponse

from watchdog.utils import watchdog_error
from core.jsonresponse import JsonResponse, create_response, decode_json_str
from core.exceptionutil import unicode_full_stack

COUNT_PER_PAGE = 20
MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'vote'

########################################################################
# list_votes: 显示投票列表
########################################################################
@login_required
def list_votes(request):
	votes = Vote.objects.filter(owner=request.user).order_by('-id')
	for vote in votes:
		vote_options = VoteOption.objects.filter(vote=vote).order_by("-vote_count")

		#选项数
		vote.option_count = vote_options.count()

		#最高选票项信息
		vote.max_vote_option_name = ""
		if vote_options.count() > 0:
			vote.max_vote_option_name = vote_options[0].name

		#总选票
		vote_counts = vote_options.aggregate(Sum("vote_count"))

		vote.vote_count = 0
		if vote_counts["vote_count__sum"] is not None:
			vote.vote_count = vote_counts["vote_count__sum"]

	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'votes': votes,
	})
	return render_to_response('vote/editor/vote_list.html', c)

########################################################################
# add_vote: 添加投票
########################################################################
@login_required
def add_vote(request):
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
	})
	return render_to_response('vote/editor/edit_vote.html', c)

########################################################################
# update_vote: 更新投票
########################################################################
@login_required
def update_vote(request, vote_id):
	vote = Vote.objects.get(owner=request.user, id=vote_id)
	vote_options = VoteOption.objects.filter(vote=vote)

	vote_options_jsonarray = []
	for vote_option in vote_options:
		vote_options_jsonarray.append(vote_option.to_json())

	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'vote': vote,
		'vote_options': json.dumps(vote_options_jsonarray)
	})
	return render_to_response('vote/editor/edit_vote.html', c)


########################################################################
# delete_vote: 删除投票
########################################################################
@login_required
def delete_vote(request, vote_id):
	Vote.objects.filter(owner=request.user, id=vote_id).delete()
	return HttpResponseRedirect('/market_tools/vote/')


########################################################################
# show_vote_statistics: 投票统计信息
########################################################################
@login_required
def show_vote_statistics(request, vote_id):
	vote = Vote.objects.get(id=vote_id, owner=request.user)
	vote_options = VoteOption.objects.filter(vote=vote).order_by('-vote_count')
	prize_info = decode_json_str(vote.award_prize_info)
	if prize_info['name'] == '_score-prize_':
		vote.cur_prize = '[%s]%d' % (prize_info['type'], prize_info['id'])
	elif prize_info['name'] == 'non-prize':
		vote.cur_prize = prize_info['type']
	else:
		vote.cur_prize = '[%s]%s' % (prize_info['type'], prize_info['name'])
	
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'vote': vote,
		'vote_options': vote_options
	})
	return render_to_response('vote/editor/vote_statistics.html', c)

########################################################################
# export_vote_list: 导出列表数据
########################################################################
@login_required
def export_vote_statistics(request, vote_id):
	vote = Vote.objects.get(id=vote_id)
	vote_options = VoteOption.objects.filter(vote=vote)

	votes =  [
		[vote.name],
		[u'名称', u'票数'],
	]
	
	for vote_option in vote_options:
		votes.append([
			vote_option.name,
			vote_option.vote_count,
		])

	return ExcelResponse(
			votes, 
			output_name=u'投票列表'.encode('utf-8'),
			force_csv=False
		)