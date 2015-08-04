# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os

from django.conf import settings
from core.jsonresponse import create_response

from core.exceptionutil import unicode_full_stack

from modules.member import util as member_util
from models import *

def create_ballot(request):
	option_id = int(request.GET['option_id'])

	member = member_util.get_member(request)
	try:
		VoteOption.vote_by_member(option_id, member)
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
		options_jsonarray.append(option.to_json())
	return options_jsonarray

########################################################################
# get_vote_options: 获取投票的所有选项
########################################################################
def get_vote_options(request):
	try:
		vote_id = int(request.POST['id'])
		count = int(request.POST['count'])
		next_display_index = int(request.POST['item_index'])
		search = request.POST.get('search', '').strip()

		poll_options = VoteOption.objects.filter(vote_id=vote_id)

		if len(search) > 0:
			poll_options = poll_options.filter(name__contains=search)

		poll_options = poll_options.order_by('-vote_count')

		end_index = next_display_index + count
		response = create_response(200)
		if poll_options.count() > end_index:
			response.data.is_has_more = True
			select_options = poll_options[next_display_index:end_index]
			response.data.items = __serialize_options_to_jsonarray(select_options)
			response.data.item_index = end_index
		else:
			response.data.is_has_more = False
			if poll_options.count() == 0:
				response.data.item_index = 0
				response.data.items = __serialize_options_to_jsonarray(poll_options)
			else:
				select_options = poll_options[next_display_index:end_index]
				response.data.item_index = end_index
				response.data.items = __serialize_options_to_jsonarray(select_options)

		member = member_util.get_member(request)
		response.data.is_member_vote = Vote.has_voted_by_member(vote_id, member)
		return response.get_response()
	except:
		response = create_response(500)
		response.errMsg = u'获取失败'
		response.innerErrMsg = unicode_full_stack()
		print response.innerErrMsg
		return response.get_response()