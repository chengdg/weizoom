# -*- coding: utf-8 -*-

__author__ = 'chuter'


from django.contrib.auth.decorators import login_required
from django.conf import settings

import copy
from core.jsonresponse import create_response
from core import apiview_util
from core.exceptionutil import unicode_full_stack

from module_api import PRIZE_TYPES, PrizeInfo, get_request_prize_type, REAL_PRIZE_TYPE_NAME

@login_required
def get_prize_types(request):
	response = create_response(200)
	is_entity = request.GET.get('is_entity', '1')
	
	prize_type_names_json_array = [prize_type.name for prize_type in PRIZE_TYPES]
	if is_entity == '0':
		prize_type_names_json_array.remove(REAL_PRIZE_TYPE_NAME)
	response.data.items = prize_type_names_json_array

	return response.get_response()

@login_required
def get_prize_list(request):
	prize_type_name = request.GET.get('name', None)
	response = create_response(200)

	try:
		if prize_type_name is not None:
			request_prize_type = get_request_prize_type(prize_type_name)
			if request_prize_type is not None:
				prizes_list = request_prize_type.get_all_prizes(request.user)
				return_prize_infos_json_array = []
				for prize in prizes_list:
					info = PrizeInfo.build_from(prize, request_prize_type).to_json() 
					if hasattr(prize, 'remained_count'):
						info['count'] = prize.remained_count
					return_prize_infos_json_array.append(info)
				response.data.items = return_prize_infos_json_array
	except:
		response = create_response(500)
		response.errMsg = u'获取奖品列表失败'
		response.innerErrMsg = unicode_full_stack()

	return response.get_response()

def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())

	return api_function(request)
