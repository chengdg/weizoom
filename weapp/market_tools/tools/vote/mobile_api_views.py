# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os

from django.conf import settings
from core.jsonresponse import create_response

from core.exceptionutil import unicode_full_stack

from modules.member import util as member_util
from market_tools.prize.module_api import *
from models import *

def create_ballot(request):
	option_id = int(request.GET['option_id'])

	member = request.member
	webapp_user = request.webapp_user
	try:
		option = VoteOption.objects.get(id=option_id)
		vote = option.vote
		VoteOption.vote_by_webapp_user(option_id, webapp_user)
		if member:
			prize_info = PrizeInfo.from_json(vote.award_prize_info)
			award(prize_info, member, u'投票获得积分')
			
		response = create_response(200)
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()

	return response.get_response()

def __serialize_options_to_jsonarray(vote_options):
	if vote_options is None or len(vote_options) == 0:
		return []

	options_jsonarray = []
	for option in vote_options:
		option_json = option.to_json()
		option_json['has_voted'] = option.has_voted if hasattr(option, 'has_voted') else False
		options_jsonarray.append(option_json)
	return options_jsonarray

########################################################################
# get_vote_options: 获取投票的所有选项
########################################################################
def get_vote_options(request):
	member = request.member
	webapp_user = request.webapp_user

	try:
		vote_id = int(request.POST['id'])
		count = int(request.POST['count'])
		next_display_index = int(request.POST['item_index'])
		search = request.POST.get('search', '').strip()

		vote_options = VoteOption.objects.filter(vote_id=vote_id)

		if len(search) > 0:
			vote_options = vote_options.filter(name__contains=search)

		vote_options = vote_options.order_by('-vote_count')

		end_index = next_display_index + count
		response = create_response(200)
		if vote_options.count() > end_index:
			response.data.is_has_more = True
			select_options = vote_options[0:end_index]
			response.data.item_index = end_index
		else:
			response.data.is_has_more = False
			if vote_options.count() == 0:
				response.data.item_index = 0
				select_options = []
			else:
				select_options = vote_options[0:end_index]
				response.data.item_index = end_index

		#标识当前会员已经投过票的投票选项
		webapp_user_voted_options_for_vote = VoteOptionHasWebappUser.voted_options_by_webapp_user_for_vote(webapp_user, vote_id)
		for vote_option in select_options:
			for voted_option_for_vote in webapp_user_voted_options_for_vote:
				if vote_option.id == voted_option_for_vote.id:
					vote_option.has_voted = True
					break

		response.data.items = __serialize_options_to_jsonarray(select_options)
		response.data.is_webapp_user_vote = Vote.has_voted_by_webapp_user(vote_id, webapp_user)
		return response.get_response()
	except:
		response = create_response(500)
		response.errMsg = u'获取失败'
		response.innerErrMsg = unicode_full_stack()
		print response.innerErrMsg
		return response.get_response()