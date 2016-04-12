# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from core.jsonresponse import JsonResponse, create_response

from django.shortcuts import render_to_response
from django.template import RequestContext

import random
from core import resource
from weapp.models import *
import json
import nav
import util

class Shops(resource.Resource):
	app = 'card'
	resource = 'shops'

	@login_required
	def api_get(request):
		"""
		获取专属商家
		"""
		user_id2store_name = [{
			"user_id": userprofile.user_id,
			"store_name": userprofile.store_name
		} for userprofile in UserProfile.objects.using('weapp').exclude(store_name="")]
		response = create_response(200)
		response.data.shops = user_id2store_name
		return response.get_response()