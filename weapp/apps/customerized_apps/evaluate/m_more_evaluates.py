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
import export
from apps import request_util
from termite2 import pagecreater
import weixin.user.models as weixin_models

class MyEvaluates(resource.Resource):
	app = 'apps/evaluate'
	resource = 'm_more_evaluates'
	
	def get(request):
		"""
		响应GET
		"""
		c = RequestContext(request, {
			'page_title': "更多评价",
			'hide_non_member_cover': True, #非会员也可使用该页面
		})


		return render_to_response('evaluate/templates/webapp/m_more_evaluates.html', c)

