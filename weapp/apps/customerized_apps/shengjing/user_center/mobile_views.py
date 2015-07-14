# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
from webapp.modules.cms.models import SpecialArticle

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core.dateutil import get_today
from core.exceptionutil import full_stack, unicode_full_stack

from modules.member.member_decorators import member_required
from modules.member.util import get_member
from modules.member.models import *

from market_tools.tools.member_qrcode.models import *

from shengjing.models import *
import integral_util as integral_util

from util import *
from qrcode_util import *
#from watchdog.utils import watchdog_debug
from shengjing.study_plan import mobile_views as study_plan_views

from apps.register import mobile_view_func
from watchdog.utils import watchdog_info

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates/webapp' % template_path_items[-1]

def _get_template_name_and_response_data(request):
	member = request.member
	# 判断是否需要加 “binding_for_father”积分
	is_need_to_add_integral_for_father = request.GET.get('is_need_to_add_integral_for_father', False)

	binding_member,member_info = get_binding_info_by_member(member, is_need_to_add_integral_for_father)
	response_data = dict()

	if binding_member and member_info:
		response_data['member'] = member
		response_data['member_info'] = member_info
		template_name = 'webapp/user_center.html'
	elif binding_member:
		response_data['binding_member'] = binding_member		
		template_name = 'webapp/binding_info.html'
	else:
		template_name = 'webapp/binding_page.html'	
		
	response_data['is_hide_weixin_option_menu'] = True

	webapp_owner_id = request.GET.get('webapp_owner_id')
	response_data['webapp_owner_id'] = webapp_owner_id

	return response_data, template_name

def _handle_post(request):
	if request.method == "POST":
		watchdog_info(u'绑定盛景信息，保存手动输入公司名称，request：{}'.format(request.__dict__), 'SHENGJING')
		binding_member_id = request.POST.get('binding_member_id', -1)
		name  = request.POST.get('name', None)
		position  = request.POST.get('position', '')
		company = request.POST.get('company', '')
		#判断是否绑定过
		if name and binding_member_id != -1: #and ShengjingBindingMemberInfo.objects.filter(binding_id=binding_member_id, name=name).count == 0:
			if ShengjingBindingMemberInfo.objects.filter(binding_id=binding_member_id).count() == 0:
				ShengjingBindingMemberInfo.objects.create(name=name, position=position, binding_id=binding_member_id)
				#绑定成功 给父节点增加积分
				ShengjingIntegralStrategySttings.increase_integral_for_father_by_binding_id(binding_member_id, request.user_profile.webapp_id)
			
				ShengjingBindingMemberHasCompanys.objects.get_or_create(name=company, binding_id=binding_member_id)

@member_required
@mobile_view_func(resource='user_info', action='get')
def get_user_info(request):
	"""
	个人信息
	"""
	_handle_post(request)
	response_data, template_name = _get_template_name_and_response_data(request)
	response_data['page_title'] = u'个人信息'
	c = RequestContext(request, response_data)
	return render_to_response(template_name, c)


@member_required
def get_binding_page(request):
	"""
	绑定页面
	"""
	_handle_post(request)
	response_data, template_name = _get_template_name_and_response_data(request)
	response_data['page_title'] = u'绑定页面'
	c = RequestContext(request, response_data)
	return render_to_response(template_name, c)

########################################################################
# get_integral_log: 获取会员积分使用日志
########################################################################
@member_required
@mobile_view_func(resource='integral_log', action='get')
def get_integral_log(request):
	response_data, template_name = study_plan_views._get_template_name_and_response_data(request)
	
	if not template_name:
		organized_integral_log_list = integral_util.get_integral_log(request)
		member = request.member	
		_, member_info = get_binding_info_by_member(member)
		c = RequestContext(request, {
			'page_title': u'积分日志',
			'member_integral_logs': organized_integral_log_list,
			'member': member,
			'member_info': member_info,
			'is_hide_weixin_option_menu': True
		})
		return render_to_response('webapp/integral_log.html' , c)
	else:
		response_data['page_title'] = u'积分日志'
		c = RequestContext(request, response_data)
		return render_to_response(template_name, c)	
	

########################################################################
# get_binding_info: 获取绑定信息记录
########################################################################
@mobile_view_func(resource='binding_info', action='get')
def get_binding_info(request):
	_handle_post(request)
	response_data, template_name = _get_template_name_and_response_data(request)
	response_data['page_title'] = u'绑定纪录'
	c = RequestContext(request,response_data)
	return render_to_response(template_name, c)

@mobile_view_func(resource='member_qrcode', action='get')
def get_settings(request):
	owner_id = request.user_profile.user_id

	validate_template_name = 'webapp/user_center.html'

	response_data, template_name = _get_template_name_and_response_data(request)

	if validate_template_name != template_name:
		c = RequestContext(request,response_data)
		return render_to_response(template_name, c)

	if MemberQrcodeSettings.objects.filter(owner=owner_id).count() > 0:
		member_qrcode_settings = MemberQrcodeSettings.objects.filter(owner=owner_id)[0]
	else:
		member_qrcode_settings = MemberQrcodeSettings.objects.create(owner_id=owner_id)
	
	try:
		member = request.member
	except:
		member = None

	default_img = SpecialArticle.objects.filter(owner=owner_id, name='not_from_weixin')[0].content if SpecialArticle.objects.filter(owner=owner_id, name='not_from_weixin').count()>0 else None

	try:
		if member and member.is_subscribed:
			try:
				ticket, expired_second = get_member_qrcode(owner_id, member.id)
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
			'default_img': default_img,
			'is_deleted_data': True
		})
		return render_to_response('webapp/member_qrcode.html', c)

	c = RequestContext(request, {
		'page_title': u'会员二维码',
		'member': member,
		'member_qrcode_settings': member_qrcode_settings,
		'default_img': default_img,
		'expired_second': expired_second,
		'qrcode_url': qrcode_url,
		'is_hide_weixin_option_menu': True
	})
	return render_to_response('webapp/member_qrcode.html', c)

########################################################################
# test_index:
########################################################################
#@member_required
def show_test_index(request):
	c = RequestContext(request, {
	})
	return render_to_response('webapp/test_index.html' , c)

########################################################################
# get_friends: 我的朋友
########################################################################
#@member_required
@mobile_view_func(resource='my_friends', action='get')
def get_friends(request):
	member = request.member
	friend_binding_member_infos = None
	if member:
		friend_binding_member_infos = ShengjingBindingMember.get_binding_friends(member)
	c = RequestContext(request, {
		'page_title': u'我的朋友',
		'friend_binding_member_infos':friend_binding_member_infos,
		'is_hide_weixin_option_menu': True
	})
	return render_to_response('webapp/friend_page.html' , c)

