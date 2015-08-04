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
from util import *

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
def get_settings(request):
	settings_id = int(request.GET['settings_id'])
	
	try:
		member = request.member
	except:
		member = None

	default_img = SpecialArticle.objects.filter(owner=request.project.owner_id, name='not_from_weixin')[0].content if SpecialArticle.objects.filter(owner=request.project.owner_id, name='not_from_weixin').count()>0 else None

	try:
		member_qrcode_settings = MemberQrcodeSettings.objects.get(id=settings_id)
		if member and member.is_subscribed:
			try:
				ticket, expired_second = get_member_qrcode(request.project.owner_id, member.id)
				if ticket:
					qrcode_url = get_qcrod_url(ticket)
				else:
					qrcode_url = None
			except:
				ticket, expired_second, qrcode_url = None, None, None
				notify_msg = u"获取微信会员二维码mobile view失败 cause:\n{}".format(unicode_full_stack())
				watchdog_fatal(notify_msg)
		else:
			ticket, expired_second, qrcode_url = None, None, None
	except:
		c = RequestContext(request, {
			'is_deleted_data': True
		})
		return render_to_response('%s/member_qrcode/webapp/member_qrcode.html' % TEMPLATE_DIR, c)

	c = RequestContext(request, {
		'page_title': u'会员二维码',
		'member': member,
		'member_qrcode_settings': member_qrcode_settings,
		'default_img': default_img,
		'expired_second': expired_second,
		'qrcode_url': qrcode_url,
		'is_hide_weixin_option_menu': True
	})

	return render_to_response('%s/member_qrcode/webapp/member_qrcode.html' % TEMPLATE_DIR, c)

weixin_qcrod_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s'
def get_qcrod_url(ticket):
	return 	weixin_qcrod_url % ticket