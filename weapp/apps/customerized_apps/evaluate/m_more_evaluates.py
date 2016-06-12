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
from modules.member.module_api import get_member_by_id_list

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
		product_id = request.GET['product_id']
		webapp_owner_id = request.webapp_owner_id

		reviews = app_models.ProductEvaluates.objects(owner_id = webapp_owner_id, product_id = product_id)

		member_ids = [review.member_id for review in reviews]
		members = get_member_by_id_list(member_ids)
		member_id2member = dict([(m.id, m) for m in members])

		items = []
		for review in reviews:
			member_detail = member_id2member[review.member_id]
			items.append({
				'created_at': review.created_at,
				'review_detail': review.detail,
				'member_name': member_detail.username_for_html,
				'member_icon': member_detail.user_icon,
				'reviewed_product_pictures': review.pics,
			})

		c = RequestContext(request, {
			'page_title': "更多评价",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'reviews': items
		})


		return render_to_response('evaluate/templates/webapp/m_more_evaluates.html', c)

