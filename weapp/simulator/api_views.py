# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil
import base64
import random

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group
from django.contrib import auth

from models import *
from account.models import UserProfile
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from core import apiview_util
from termite import pagestore as pagestore_manager
from account.social_account.models import SocialAccount
from modules.member import member_settings 


#################################################################################
# share_webapp_page: 分享页面
#################################################################################
def share_webapp_page(request):
	simulator_user = SimulatorUser.objects.get(name=request.POST['user'])
	message = request.POST.get('message', '')
	link_title = request.POST.get('link_title', u'[请阅读我...]')
	link_url = request.POST.get('link_url', u'javascript:alert("invalid url");')
	link_img = request.POST.get('link_img', '')
	SharedMessage.objects.create(
		owner = simulator_user,
		message = message,
		link_title = link_title,
		link_url = link_url,
		link_img = link_img
	)

	return create_response(200).get_response()



#################################################################################
# get_shared_messages: 获取朋友圈消息
#################################################################################
def get_shared_messages(request):
	simulator_user = SimulatorUser.objects.get(name=request.GET['user'])

	owner_ids = [simulator_user.id]
	owner_ids.extend([r.followed_id for r in SimulatorUserRelation.objects.filter(follower=simulator_user)])

	id2user = dict([(u.id, u) for u in SimulatorUser.objects.all()])

	messages = []
	for message in SharedMessage.objects.filter(owner_id__in=owner_ids).order_by('-id'):
		simulator_user = id2user[message.owner_id]
		messages.append({
			'userName': simulator_user.name,
			'displayUserName': simulator_user.display_name,
			'content': message.message,
			'linkUrl': message.link_url,
			'linkTitle': message.link_title,
			'linkImg': message.link_img
		})

	response = create_response(200)
	response.data = {
		'messages': messages
	}
	return response.get_response()


#################################################################################
# delete_sct_cookie: 删除sct cookie
#################################################################################
def delete_sct_cookie(request):
	response = create_response(200)
	response = response.get_response()
	response.delete_cookie('sct')

	return response


#################################################################################
# get_sct_cookie_url: 获得sct cookie
#################################################################################
def get_sct_cookie_url(request):
	openid = request.GET['openid']
	webapp_id = request.GET['webapp_id']
	webapp_owner_id = UserProfile.objects.get(webapp_id=webapp_id).user_id
	sct = SocialAccount.objects.get(openid=openid).token
	url = '/workbench/jqm/preview/?module=mall&model=products&action=list&category_id=0&workspace_id=mall&webapp_owner_id=%d&sct=%s' % (webapp_owner_id, sct)
	response = create_response(200)
	response.data = {
		"url": url
	}
	response = response.get_response()
	response.set_cookie(member_settings.OPENID_WEBAPP_ID_KEY, "%s____%s" % (openid, webapp_id), max_age=60*60*24*365)

	return response


def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)