# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F

import models as weixin_models
from core import resource
from core import paginator
from core.jsonresponse import create_response


class LandingPage(resource.Resource):
	app = 'new_weixin'
	resource = 'landing_page'

	@login_required
	def get(request):
		"""
		获取微信登陆页面列表
		1. 如果已经绑定，进入微信首页
		2. 如果没有绑定，进入一键绑定页面
		"""
		user_profile = request.manager.get_profile()
		if not user_profile.is_mp_registered:
			return HttpResponseRedirect('/new_weixin/unbind_account/')
		else:
			return HttpResponseRedirect('/new_weixin/outline/')