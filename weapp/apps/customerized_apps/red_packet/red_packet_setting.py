# -*- coding: utf-8 -*-

import json
import random
import os
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
from apps import request_util
from mall import export as mall_export
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api
import termite.pagestore as pagestore_manager
from weapp import settings

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class RedPacketSetting(resource.Resource):
	app = 'apps/red_packet'
	resource = 'red_packet_setting'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		cert_done = key_done = False
		cert_setting = app_models.RedPacketCertSettings.objects(owner_id=str(request.webapp_owner_id))
		if cert_setting.count() > 0:
			cert_setting = cert_setting.first()
			if '' != cert_setting.cert_path:
				cert_done = True
			if '' != cert_setting.key_path:
				key_done = True
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
            'third_nav_name': mall_export.MALL_APPS_REDPACKET_NAV,
			'cert_done': cert_done,
			'key_done': key_done
		})
		return render_to_response('red_packet/templates/editor/red_packet_cert_setting.html', c)