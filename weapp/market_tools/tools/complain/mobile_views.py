# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response

from core.exceptionutil import unicode_full_stack

from modules.member.util import get_member
from models import *
from webapp.modules.cms.models import SpecialArticle
from modules.member.models import *

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
def get_settings(request):
	settings_id = int(request.GET['settings_id'])
	
	try:
		member = request.member
	except:
		member = None

	#default_img = SpecialArticle.objects.filter(owner=request.project.owner_id, name='not_from_weixin')[0].content if SpecialArticle.objects.filter(owner=request.project.owner_id, name='not_from_weixin').count()>0 else None
	hide_non_member_cover = False
	try:
		member_complain_settings = MemberComplainSettings.objects.get(id=settings_id)
		if member_complain_settings.is_non_member:
			hide_non_member_cover = True	
	except:
		c = RequestContext(request, {
			'is_deleted_data': True
		})
		return render_to_response('%s/complain/webapp/member_complain.html' % TEMPLATE_DIR, c)
		
	request.should_hide_footer = True
	c = RequestContext(request, {
		'page_title': u'用户反馈',
		'member': member,
		'member_complain_settings': member_complain_settings,
		'hide_non_member_cover' : hide_non_member_cover
	})

	return render_to_response('%s/complain/webapp/member_complain.html' % TEMPLATE_DIR, c)
