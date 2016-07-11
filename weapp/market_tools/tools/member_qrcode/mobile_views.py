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
from utils import url_helper

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
# def get_settings(request):
# 	settings_id = int(request.GET['settings_id'])
#
# 	try:
# 		member = request.member
# 	except:
# 		member = None
#
# 	default_img = SpecialArticle.objects.filter(owner=request.project.owner_id, name='not_from_weixin')[0].content if SpecialArticle.objects.filter(owner=request.project.owner_id, name='not_from_weixin').count()>0 else None
#
# 	try:
# 		member_qrcode_settings = MemberQrcodeSettings.objects.get(id=settings_id)
# 		limit_chance_used = 0
# 		limit_chance_left = member_qrcode_settings.limit_chance
# 		if member and member.is_subscribed:
# 			#检查奖励限制
# 			limit_log = MemberQrcodeLimitLog.objects.filter(belong_settings_id=member_qrcode_settings.id, owner_member_id=member.id, created_at=datetime.now().date())
# 			if limit_log.count() > 0:
# 				limit_log = limit_log.first()
# 				limit_chance_used = limit_log.count
# 				limit_chance_left = limit_chance_left - limit_chance_used
# 				limit_chance_left = limit_chance_left if limit_chance_left >= 0 else 0
# 			try:
# 				ticket, expired_second = get_member_qrcode(request.project.owner_id, member.id)
# 				if ticket:
# 					qrcode_url = get_qcrod_url(ticket)
# 				else:
# 					qrcode_url = None
# 			except:
# 				ticket, expired_second, qrcode_url = None, None, None
# 				notify_msg = u"获取微信会员二维码mobile view失败 cause:\n{}".format(unicode_full_stack())
# 				watchdog_fatal(notify_msg)
# 		else:
# 			ticket, expired_second, qrcode_url = None, None, None
# 	except:
# 		c = RequestContext(request, {
# 			'is_deleted_data': True
# 		})
# 		return render_to_response('%s/member_qrcode/webapp/member_qrcode.html' % TEMPLATE_DIR, c)
#
# 	c = RequestContext(request, {
# 		'page_title': u'会员二维码',
# 		'member': member,
# 		'member_qrcode_settings': member_qrcode_settings,
# 		'default_img': default_img,
# 		'expired_second': expired_second,
# 		'qrcode_url': qrcode_url,
# 		'is_hide_weixin_option_menu': True,
# 		'limit_chance_used': limit_chance_used,
# 		'limit_chance_left': limit_chance_left
# 	})
#
# 	return render_to_response('%s/member_qrcode/webapp/member_qrcode.html' % TEMPLATE_DIR, c)

def get_settings(request):
	"""
	分享推广扫码页面后，用户点击进入不再显示自己的二维码，而是显示最初分享者的二维码
	@param request:
	@return:
	"""
	settings_id = int(request.GET['settings_id'])
	fid = request.GET.get('fid', None)
	member = request.member
	if not member:
		return return_deleted_page(request)

	is_member = member.is_subscribed
	member_id = member.id
	if is_member:
		if not fid:
			new_url = url_helper.add_query_part_to_request_url(request.get_full_path(), 'fid', member_id)
			response = HttpResponseRedirect(new_url)
			response.set_cookie('fid', member_id, max_age=60 * 60 * 24 * 365)
			return response
	else:
		if not fid:
			return return_deleted_page(request)
	#检查奖励限制
	member_qrcode_settings = MemberQrcodeSettings.objects.filter(id=settings_id)
	if member_qrcode_settings.count() <= 0:
		return return_deleted_page(request)

	owner_member = member
	member_qrcode_settings = member_qrcode_settings.first()
	limit_chance_used = 0
	limit_chance_left = member_qrcode_settings.limit_chance
	limit_log = MemberQrcodeLimitLog.objects.filter(belong_settings_id=member_qrcode_settings.id, owner_member_id=fid, created_at=datetime.now().date())
	if limit_log.count() > 0:
		limit_log = limit_log.first()
		limit_chance_used = limit_log.count
		limit_chance_left = limit_chance_left - limit_chance_used
		limit_chance_left = limit_chance_left if limit_chance_left >= 0 else 0
	try:
		ticket, expired_second = get_member_qrcode(request.project.owner_id, fid)
		owner_member = Member.objects.get(id=fid)
		if ticket:
			qrcode_url = get_qcrod_url(ticket)
		else:
			qrcode_url = None
	except:
		ticket, expired_second, qrcode_url = None, None, None
		notify_msg = u"获取微信会员二维码mobile view失败 cause:\n{}".format(unicode_full_stack())
		watchdog_fatal(notify_msg)

	default_img = SpecialArticle.objects.filter(owner=request.project.owner_id, name='not_from_weixin')[0].content if SpecialArticle.objects.filter(owner=request.project.owner_id, name='not_from_weixin').count()>0 else None
	c = RequestContext(request, {
		'page_title': u'会员二维码',
		'member': owner_member,
		'member_qrcode_settings': member_qrcode_settings,
		'default_img': default_img,
		'expired_second': expired_second,
		'qrcode_url': qrcode_url,
		'is_hide_weixin_option_menu': False,
		'limit_chance_used': limit_chance_used,
		'limit_chance_left': limit_chance_left,
		'is_shared_page': str(fid) != str(member_id)
	})

	return render_to_response('%s/member_qrcode/webapp/member_qrcode.html' % TEMPLATE_DIR, c)

weixin_qcrod_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s'
def get_qcrod_url(ticket):
	return 	weixin_qcrod_url % ticket

def return_deleted_page(request):
	c = RequestContext(request, {
		'is_deleted_data': True
	})
	return render_to_response('%s/member_qrcode/webapp/member_qrcode.html' % TEMPLATE_DIR, c)