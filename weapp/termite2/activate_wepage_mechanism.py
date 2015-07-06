# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from account import models as account_models
from core import resource
from core.jsonresponse import create_response
from webapp import models as webapp_models


class ActivateWepageMechanism(resource.Resource):
	app = 'termite2'
	resource = 'activate_wepage_mechanism'

	@login_required
	def api_put(request):
		"""
		激活wepage机制
		"""
		account_models.UserProfile.objects.filter(user_id=request.user.id).update(is_use_wepage=True)

		response = create_response(200)
		return response.get_response()
