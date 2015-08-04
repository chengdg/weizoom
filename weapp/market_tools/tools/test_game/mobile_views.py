# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from models import *
from modules.member import util as member_util
from core.jsonresponse import JsonResponse, create_response, decode_json_str


########################################################################
# get_test_game: 获取测试详情
########################################################################
def get_test_game(request):
	webapp_user = request.webapp_user
	member = request.member
	game_id = request.GET['game_id']
	
	request.should_hide_footer = True
	is_participated = False #是否已经参加
	
	#重新玩一次
	is_again = int(request.GET.get('is_again', 0))
	
	try:
		game = TestGame.objects.get(id=game_id)
	except:
		c = RequestContext(request, {
			'is_deleted_data': True
		})
		return render_to_response('test_game/webapp/game.html', c)
	
	hide_non_member_cover = False
	if game.is_non_member:
		hide_non_member_cover = True
	
	#判断是否参与过
	records = TestGameRecord.objects.filter(webapp_user_id=webapp_user.id, test_game=game_id).order_by('-created_at')
	if records:
		record = records[0]
		is_participated = True
	
	#参与后直接返回结果页面
	if is_participated and (not is_again):
		score = record.score
		prize_info = decode_json_str(game.award_prize_info)
		if prize_info['name'] == '_score-prize_':
			cur_prize = '[%s]%d' % (prize_info['type'], prize_info['id'])
		elif prize_info['name'] == 'non-prize':
#			 cur_prize = prize_info['type']
			cur_prize = None
		else:
			cur_prize = '[%s]%s' % (prize_info['type'], prize_info['name'])
		
		results = TestGameResult.objects.filter(test_game=game_id)
		cur_result_id = 0
		min_difference = None
		for result in results:
			start, end = result.section.split('-')
			start_difference = abs(int(start) - score)
			end_difference = abs(int(end) - score)
			if min_difference == None:
				min_difference = start_difference
				cur_result_id = result.id
			if start_difference < min_difference:
				min_difference = start_difference
				cur_result_id = result.id
			if end_difference < min_difference:
				min_difference = end_difference
				cur_result_id = result.id
		
		other_results = []
		for result in results:
			if result.id == cur_result_id:
			   cur_result = result
			else:
				other_results.append(result)
		
		is_show_prize = True
		if len(records) > 1:
			is_show_prize = False
	   
		
		c = RequestContext(request, {
			'page_title': game.name,
			'game': game,
			'record': record,
			'cur_result': cur_result,
			'other_results': other_results,
			'hide_non_member_cover' : hide_non_member_cover,
			'member': member,
			'cur_prize': cur_prize,
			'is_show_prize': is_show_prize
		})
		return render_to_response('test_game/webapp/result.html', c)
	
	questions = TestGameQuestion.objects.filter(test_game=game_id)
	for q in questions:
		q.answers = []
	id2question = dict([(q.id, q) for q in questions])
	question_ids = [q.id for q in questions]
	answers = TestGameQuestionAnswer.objects.filter(test_game_question__in=question_ids)
	for answer in answers:
		question = id2question[answer.test_game_question_id]
		question.answers.append(answer)
	
	c = RequestContext(request, {
		'page_title': game.name,
		'game': game,
		'questions': questions,
		'hide_non_member_cover' : hide_non_member_cover,
		'member': member
	})
	return render_to_response('test_game/webapp/game.html', c)