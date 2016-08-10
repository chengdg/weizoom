# -*- coding: utf-8 -*-

__author__ = 'aix'

import json
from core.jsonresponse import create_response
from market_tools.tools.distribution import models

def change_state(request):
	"""
	修改订单状态
	"""
	member_id = request.POST.get('member_id','')
	models.ChannelDistributionQrcodeSettings.objects.get(bing_member_id=member_id).update (
		state = 1
	)

	return response.get_response()
