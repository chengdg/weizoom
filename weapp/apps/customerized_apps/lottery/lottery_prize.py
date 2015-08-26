# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
from weixin2 import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

class lottery_prize(resource.Resource):
	app = 'apps/lottery'
	resource = 'lottery_prize'

	def api_put(request):
		"""
		响应PUT
		"""
		post = request.POST
		record_id = post['id']
		response = create_response(200)
		# result = 0
		# if record_id:
		# 	lottery = app_models.lottery.objects.get(id=record_id)
		# 	chance = lottery.chance / 100.0 #中奖率
		# 	participants_count = lottery.participant_count #所有参与的人数
		# 	winner_count = lottery.winner_count #中奖人数
		# 	#判定是否中奖
		# 	if participants_count == 0 or winner_count / float(participants_count) >= chance:
		# 		result = 0
		# 	else:
		# 		#中奖，构造奖项池
		# 		prize_tank = []
		# 		pagestore = pagestore_manager.get_pagestore('mongo')
		# 		page = pagestore.get_page(lottery.related_page_id, 1)
		# 		page_components = page['component']['components']
		# 		for sub_components in page_components:
		# 			if sub_components.type == 'appkit.lotterydescription':
		# 				sub_components = sub_components['components']
		# 				for c in sub_components['components']:
		# 					pass
		response.data = {'index': 0}
		return response.get_response()