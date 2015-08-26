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
		print 11111111111111111111
		response = create_response(200)
		response.data = {'index': 4}
		return response.get_response()