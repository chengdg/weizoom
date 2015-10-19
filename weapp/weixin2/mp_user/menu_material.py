# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F

from account import models as account_models
from weixin2 import export
import weixin2.models as weixin2_models
from core import resource
from core import paginator
from core.jsonresponse import create_response
from core import emotion

import weixin.user.models as weixin_models
from watchdog.utils import watchdog_fatal, watchdog_error
from weixin.mp_decorators import mp_required
from weixin.message.qa.models import Rule, TEXT_TYPE, NEWS_TYPE
from weixin.manage.customerized_menu.models import CustomerMenuItem
from weixin.message.material.models import *

from webapp.models import *

COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class MenuMaterial(resource.Resource):
	app = 'new_weixin'
	resource = 'menu_material'
	
	@login_required
	def api_get(request):
		material = Material.objects.get(id=request.GET['id'])
		response = create_response(200)
		newses = []
		for news in News.objects.filter(material=material):
			data = dict()
			data['id'] = news.id
			data['title'] = news.title
			data['summary'] = news.summary
			data['text'] = news.text
			data['pic_url'] = news.pic_url
			data['date'] = news.created_at.strftime('%m月%d日').strip('0')
			data['url'] = news.url
			data['link_target'] = news.link_target
			data['is_show_cover_pic'] = news.is_show_cover_pic
			newses.append(data)
	
		response.data.items = newses
		return response.get_response()