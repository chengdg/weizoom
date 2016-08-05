# -*- coding: utf-8 -*-

from django.conf import settings
from datetime import datetime

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error

import models as app_models


class Mexlottery(resource.Resource):
	app = 'apps/scanlottery'
	resource = 'm_scanlottery_page'

	def get(request):
		"""
		响应GET
		"""
		id = request.GET.get('id', '')
		share_page_desc = ''
		try:
			scanlottery = app_models.Scanlottery.objects.get(id=id)
			share_page_desc = scanlottery.name
		except:
			pass

		member = request.member
		is_pc = False if member else True
		thumbnails_url = '/static_v2/img/thumbnails_lottery.png'

		c = RequestContext(request, {
			'record_id': id,
			'page_title': u'扫码抽奖',
			'app_name': "scanlottery",
			'resource': "scanlottery",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': is_pc,
			'share_img_url': thumbnails_url,
			'share_page_desc': share_page_desc,
		})
		response = render_to_string('scanlottery/templates/webapp/m_scanlottery_page.html', c)

		return HttpResponse(response)