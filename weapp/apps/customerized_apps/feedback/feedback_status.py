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

class feedbackStatus(resource.Resource):
	app = 'apps/feedback'
	resource = 'feedback_status'
	
	@login_required
	def api_post(request):
		"""
		响应POST
		"""
		target_status = request.POST['target']
		if target_status == 'stoped':
			target_status = app_models.STATUS_STOPED
			now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
			app_models.feedback.objects(id=request.POST['id']).update(set__end_time=now_time)
		elif target_status == 'running':
			target_status = app_models.STATUS_RUNNING
		elif target_status == 'not_start':
			target_status = app_models.STATUS_NOT_START
		app_models.feedback.objects(id=request.POST['id']).update(set__status=target_status)
		
		response = create_response(200)
		return response.get_response()
