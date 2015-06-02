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
from django.db.models import Sum
from django.db.models import Q

from market_tools import export

from core.jsonresponse import JsonResponse, create_response
from core import paginator

from models import *
from modules.member import module_api as member_module_api

COUNT_PER_PAGE = 20
MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'test_game'

########################################################################
# list_test_games: 显示趣味测试列表
########################################################################
@login_required
def list_test_games(request):
	test_games = TestGame.objects.filter(owner=request.user)
	
	#分页
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, activities = paginator.paginate(test_games, cur_page, COUNT_PER_PAGE, query_string=request.META['QUERY_STRING'])
	
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'test_games': test_games,
		'pageinfo': json.dumps(paginator.to_dict(pageinfo)),
	})
	return render_to_response('test_game/editor/test_game_list.html', c)


########################################################################
# create_create_game: 创建趣味测试
########################################################################
@login_required
def create_create_game(request):
	user = request.user
	if request.POST:
		name = request.POST['name']
		is_non_member = request.POST.get('is_non_member', 0)
		award_prize_info = request.POST.get('award_prize_info')
		background_pic_url = request.POST.get('background_pic_url')
		testgame = TestGame.objects.create(owner=user, name=name, is_non_member=is_non_member, background_pic_url=background_pic_url, award_prize_info=award_prize_info)
		for key, value in request.POST.items():
			if key.startswith('test_game_question_'):
				name = request.POST[key]
				display_index = int(key.split('_')[3])
				test_game_question = TestGameQuestion()
				test_game_question.test_game = testgame
				test_game_question.name = name
				test_game_question.display_index = display_index
				test_game_question.save()
				for key, value in request.POST.items():
					if key.startswith('test_game_answer_score_%s_' % display_index):
						score = request.POST[key]
						answer_title = key.split('_')[5]
						name = request.POST['test_game_answer_%s_%s' % (display_index, answer_title)]
						test_game_question_answer = TestGameQuestionAnswer()
						test_game_question_answer.test_game_question = test_game_question
						test_game_question_answer.name = name
						test_game_question_answer.score = score
						test_game_question_answer.display_index = answer_title
						test_game_question_answer.save()
		for key, value in request.POST.items():
			if key.startswith('result_name_'):
				result_name = request.POST[key]
				result_index = key.split('_')[2]
				max_score = request.POST['max_score_%s' % result_index]
				min_score = request.POST['min_score_%s' % result_index] 
				result_range = '%s-%s' % (min_score, max_score)
				detail = request.POST['result_detail_%s' % result_index] 
				test_game_result = TestGameResult()
				test_game_result.test_game = testgame
				test_game_result.section = result_range
				test_game_result.content = detail
				test_game_result.title = result_name
				test_game_result.display_index = result_index
				test_game_result.save();
		
		return HttpResponseRedirect('/market_tools/test_game/')
	else:
		c = RequestContext(request, {
			'first_nav_name': MARKET_TOOLS_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
		})
		return render_to_response('test_game/editor/edit_test_game.html', c)
	
########################################################################
# update_test_game: 编辑趣味测试
########################################################################
@login_required
def update_test_game(request, test_game_id):
	if request.POST:
		name = request.POST['name']
		is_non_member = request.POST.get('is_non_member', 0)
		award_prize_info = request.POST.get('award_prize_info')
		background_pic_url = request.POST.get('background_pic_url')
		testgame = TestGame.objects.get(id=test_game_id)
		testgame.name = name
		testgame.is_non_member = is_non_member
		testgame.award_prize_info = award_prize_info
		testgame.background_pic_url = background_pic_url
		testgame.save()
		test_game_questions = TestGameQuestion.objects.filter(test_game=testgame)
		TestGameQuestionAnswer.objects.filter(test_game_question__in=test_game_questions).delete()
		test_game_questions.delete()
		TestGameResult.objects.filter(test_game=testgame).delete()
		for key, value in request.POST.items():
			if key.startswith('test_game_question_'):
				name = request.POST[key]
				display_index = int(key.split('_')[3])
				test_game_question = TestGameQuestion()
				test_game_question.test_game = testgame
				test_game_question.name = name
				test_game_question.display_index = display_index
				test_game_question.save()
				for key, value in request.POST.items():
					if key.startswith('test_game_answer_score_%s_' % display_index):
						score = request.POST[key]
						answer_title = key.split('_')[5]
						name = request.POST['test_game_answer_%s_%s' % (display_index, answer_title)]
						test_game_question_answer = TestGameQuestionAnswer()
						test_game_question_answer.test_game_question = test_game_question
						test_game_question_answer.name = name
						test_game_question_answer.score = score
						test_game_question_answer.display_index = answer_title
						test_game_question_answer.save()
		for key, value in request.POST.items():
			if key.startswith('result_name_'):
				result_name = request.POST[key]
				result_index = key.split('_')[2]
				max_score = request.POST['max_score_%s' % result_index]
				min_score = request.POST['min_score_%s' % result_index] 
				result_range = '%s-%s' % (min_score, max_score)
				detail = request.POST['result_detail_%s' % result_index] 
				test_game_result = TestGameResult()
				test_game_result.test_game = testgame
				test_game_result.section = result_range
				test_game_result.display_index = result_index
				test_game_result.content = detail
				test_game_result.title = result_name
				test_game_result.save();
		return HttpResponseRedirect('/market_tools/test_game/')
	else:
		test_game = TestGame.objects.get(id=test_game_id)
		questions = TestGameQuestion.objects.filter(test_game=test_game).order_by('display_index')
		answers = TestGameQuestionAnswer.objects.filter(test_game_question__in=questions).order_by('display_index')
		question_id2answers= dict([(answer.test_game_question_id, []) for answer in answers])
		for answer in answers:
			question_id2answers[answer.test_game_question_id].append(answer)
		for question in questions:
			question.answers = question_id2answers[question.id]
		test_game.questions = questions
		test_game_results = TestGameResult.objects.filter(test_game=test_game).order_by('display_index')
		for result in test_game_results:
			score = result.section
			score = score.split('-')
			result.min_score = score[0]
			result.max_score = score[1]
		test_game.results = test_game_results
		c = RequestContext(request, {
			'first_nav_name': MARKET_TOOLS_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
			'test_game': test_game
		})
		return render_to_response('test_game/editor/edit_test_game.html', c)
	

########################################################################
# join_user: 参加人员列表
########################################################################
@login_required
def join_user(request, test_game_id):
	test_game = TestGame.objects.get(id=test_game_id).joined_users
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
	})
	return render_to_response('test_game/editor/join_user_list.html', c)

########################################################################
# delete_test_game: 删除趣味测试
########################################################################
@login_required
def delete_test_game(request, test_game_id):
	TestGame.objects.get(id=test_game_id).delete();
	return HttpResponseRedirect(request.META['HTTP_REFERER'])
	
	