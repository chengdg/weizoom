# -*- coding: utf-8 -*-

__author__ = 'aix'

import json
import datetime
from core.jsonresponse import create_response
from market_tools.tools.distribution import models
from django.db.models import F

def change_state(request):
	"""
	修改订单状态
	"""
	member_id = request.POST.get('member_id','')
	qrocde = models.ChannelDistributionQrcodeSettings.objects.filter(bing_member_id=member_id)
	if qrcode[0].commission_return_standard  < qrcode[0].will_return_reward \
		and  not qrcode[0].extraction_money :
		qrcode.update (
			state = 1,
			commit_time = datetime.datetime.now(),
			extraction_money = F('will_return_reward')
		)

		response = create_response(200)
		return response.get_response()
