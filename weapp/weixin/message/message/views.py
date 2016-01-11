# -*- coding: utf-8 -*-

__author__ = 'chuter'


import json
import weixin

from django.conf import settings
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from account import models as account_models
from models import *
from weixin.user.models import get_system_user_binded_mpuser, is_subscribed

FIRSTT_NAV_NAME = weixin.NAV_NAME
WEIXIN_SECOND_NAVS = weixin.get_weixin_second_navs()


########################################################################
# list_timelines: 显示实时消息列表
########################################################################
@login_required
def list_timelines(request):
	mpuser = get_system_user_binded_mpuser(request.user)

	if (mpuser is None) or (not mpuser.is_certified) or (not mpuser.is_service):
		should_show_authorize_cover = True
	else:
		should_show_authorize_cover = False
	c = RequestContext(request, {
		'first_nav_name' : FIRSTT_NAV_NAME,
		'second_navs' : WEIXIN_SECOND_NAVS,
		'second_nav_name' : weixin.WEIXIN_MESSAGE_NAV_NAME,
		'should_show_authorize_cover': should_show_authorize_cover,
	    'IS_DEBUG': settings.DEBUG
	})

	account_models.reset_new_message_count(user=request.user)
	return render_to_response('message/list_sessions.html', c)


########################################################################
# show_history: 显示交互历史
########################################################################
@login_required
def show_history(request):
	mpuser = get_system_user_binded_mpuser(request.user)

	if mpuser is None:
		raise Http404('Binded MpUser Not Found')

	return_path = request.GET.get('return_path', 'message')
	nav_name = request.GET.get('nav_name', weixin.WEIXIN_MESSAGE_NAV_NAME)
	session_id = request.GET['session_id']
	
	session = None
	try:
		session = Session.objects.get(mpuser=mpuser, id=session_id)
	except:
		raise Http404('Session Not Found')

	#根据fake_id 得到对应用户信息weixin_user
	if not session.weixin_user:
		is_user_subscribed = 0
	else:
		is_user_subscribed = is_subscribed(session.weixin_user)

	session.unread_count = 0
	session.save()
	c = RequestContext(request, {
		'first_nav_name' : FIRSTT_NAV_NAME,
		'second_navs' : WEIXIN_SECOND_NAVS,
		'second_nav_name' : nav_name,

		'session': session,
	    'return_path': return_path,
	    'is_subscribed': is_user_subscribed
	})
	return render_to_response('message/list_histories.html', c)


def list_collect_message(request):
	nav_name = request.GET.get('nav_name', weixin.WEIXIN_MESSAGE_NAV_NAME)
	c = RequestContext(request, {
		'first_nav_name' : FIRSTT_NAV_NAME,
		'second_navs' : WEIXIN_SECOND_NAVS,
		'second_nav_name' : nav_name,
	})
	return render_to_response('message/list_collected_message.html', c)