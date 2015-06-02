# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Sum
from django.db.models import Q

from market_tools import export
from excel_response import ExcelResponse

from webapp.modules.mall import models as mall_model
from modules.member import models as member_model
from core.jsonresponse import JsonResponse, create_response, decode_json_str
from core import paginator
from core import emotion
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from core.wxapi.weixin_api import *
from core.wxapi import get_weixin_api
from core.wxapi.weixin_api import WeixinApi
from core.wxapi.api_create_qrcode_ticket import QrcodeTicket
from watchdog.utils import watchdog_warning, watchdog_error

from models import *

COUNT_PER_PAGE = 20
MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'channel_qrcode'

########################################################################
# list_channel_qrcode_settings: 显示渠道扫码配置列表
########################################################################
@login_required
def list_channel_qrcode_settings(request):
	mpuser = get_system_user_binded_mpuser(request.user)

	if (mpuser is None) or (not mpuser.is_certified) or (not mpuser.is_service):
		should_show_authorize_cover = True
	else:
		should_show_authorize_cover = False
	
	settings = ChannelQrcodeSettings.objects.filter(owner=request.user)
	setting_ids = [s.id for s in settings]
	relations = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id__in=setting_ids)
	setting_id2count = {}
	member_id2setting_id = {} 
	member_ids = []
	for r in relations:
		member_ids.append(r.member_id)
		member_id2setting_id[r.member_id] = r.channel_qrcode_id
		if r.channel_qrcode_id in setting_id2count:
			setting_id2count[r.channel_qrcode_id] += 1
		else:
			setting_id2count[r.channel_qrcode_id] = 1
	
	webapp_users = member_model.WebAppUser.objects.filter(member_id__in=member_ids)
	webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
	webapp_user_ids = set(webapp_user_id2member_id.keys())
	orders = mall_model.Order.objects.filter(webapp_user_id__in=webapp_user_ids, status=mall_model.ORDER_STATUS_SUCCESSED)
	member_id2total_final_price = {}
	for order in orders:
		member_id = webapp_user_id2member_id[order.webapp_user_id]
		if member_id in member_id2total_final_price:
			member_id2total_final_price[member_id] += order.final_price
		else:
			member_id2total_final_price[member_id] = order.final_price
	
	setting_id2total_final_price = {}
	for member_id in member_id2total_final_price.keys():
		final_price = member_id2total_final_price[member_id]
		setting_id = member_id2setting_id[member_id]
		if setting_id in setting_id2total_final_price:
			setting_id2total_final_price[setting_id] += final_price
		else:
			setting_id2total_final_price[setting_id] = final_price
	
	
	mp_user = get_binding_weixin_mpuser(request.user)
	mpuser_access_token = get_mpuser_accesstoken(mp_user)
	for setting in settings:
		prize_info = decode_json_str(setting.award_prize_info)
		if prize_info['name'] == '_score-prize_':
			setting.cur_prize = '[%s]%d' % (prize_info['type'], prize_info['id'])
		elif prize_info['name'] == 'non-prize':
			setting.cur_prize = prize_info['type']
		else:
			setting.cur_prize = '[%s]%s' % (prize_info['type'], prize_info['name'])
		
		if setting.id in setting_id2count:
			setting.count = setting_id2count[setting.id]
		else:
			setting.count = 0
		if setting.id in setting_id2total_final_price:
			setting.total_final_price = setting_id2total_final_price[setting.id]
		else:
			setting.total_final_price = 0
		
		#如果没有ticket信息则获取ticket信息
		if not setting.ticket:
			try:
				if mp_user.is_certified and mp_user.is_service and mpuser_access_token.is_active:
					weixin_api = get_weixin_api(mpuser_access_token)
					qrcode_ticket = weixin_api.create_qrcode_ticket(int(setting.id), QrcodeTicket.PERMANENT)
			
					try:
						ticket = qrcode_ticket.ticket
					except:
						ticket = ''
					setting.ticket = ticket
					setting.save()
			except:
				pass
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'settings': settings,
		'should_show_authorize_cover': should_show_authorize_cover,
		'is_hide_weixin_option_menu': True
	})
	return render_to_response('channel_qrcode/editor/channel_qrcode_settings.html', c)


########################################################################
# edit_channel_qrcode_setting: 编辑配置
########################################################################
@login_required
def edit_channel_qrcode_setting(request):
	if request.POST:
		setting_id = int(request.POST["setting_id"])
		name = request.POST["name"]
		award_prize_info = request.POST['prize_info'].strip()
		reply_type = int(request.POST.get("reply_type", 0))
		reply_detail = request.POST.get("reply_detail", '')
		reply_material_id = request.POST.get("reply_material_id", 0)
		remark = request.POST.get("remark", '')
		grade_id = int(request.POST.get("grade_id", -1))
		re_old_member = int(request.POST.get("re_old_member", 0))
		
		if reply_type == 0:
			reply_material_id = 0
			reply_detail = ''
		elif reply_type == 1:
			reply_material_id = 0
		elif reply_type == 2:
			reply_detail = ''
		
		if setting_id:
			ChannelQrcodeSettings.objects.filter(owner=request.user, id=setting_id).update(
	 				name=name, 
	 				award_prize_info=award_prize_info,
	 				reply_type=reply_type,
	 				reply_detail=reply_detail,
	 				reply_material_id=reply_material_id,
	 				remark=remark,
	 				grade_id=grade_id,
	 				re_old_member=re_old_member
	 			)
		else:
	 		cur_setting = ChannelQrcodeSettings.objects.create(
	 				owner=request.user, 
	 				name=name, 
	 				award_prize_info=award_prize_info,
	 				reply_type=reply_type,
	 				reply_detail=reply_detail,
	 				reply_material_id=reply_material_id,
	 				remark=remark,
	 				grade_id=grade_id,
	 				re_old_member=re_old_member
	 			)
	 		
			mp_user = get_binding_weixin_mpuser(request.user)
			mpuser_access_token = get_mpuser_accesstoken(mp_user)
			weixin_api = get_weixin_api(mpuser_access_token)
			
			try:
				qrcode_ticket = weixin_api.create_qrcode_ticket(int(cur_setting.id), QrcodeTicket.PERMANENT)
				ticket = qrcode_ticket.ticket
			except:
				ticket = ''
			cur_setting.ticket = ticket
			cur_setting.save()
		
   		return HttpResponseRedirect('/market_tools/channel_qrcode/')
	else:
		member_grades = MemberGrade.get_all_grades_list(request.user_profile.webapp_id)
		c = RequestContext(request, {
			'first_nav_name': MARKET_TOOLS_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
			'member_grades': member_grades
		})
		return render_to_response('channel_qrcode/editor/edit_channel_qrcode_setting.html', c)


########################################################################
# view_channel_qrcode_setting: 更新/查看配置
########################################################################
@login_required
def view_channel_qrcode_setting(request, setting_id):
	setting = ChannelQrcodeSettings.objects.get(id=setting_id)
	member_grades = MemberGrade.get_all_grades_list(request.user_profile.webapp_id)

	if setting.grade_id == -1 and member_grades.count() > 0:
		setting.grade_id = member_grades[0].id
		setting.save()

	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'setting': setting,
		'member_grades': member_grades
	})
	return render_to_response('channel_qrcode/editor/edit_channel_qrcode_setting.html', c)


########################################################################
# delete_research: 删除调研
########################################################################
@login_required
def delete_research(request, research_id):
	Research.objects.filter(id=research_id).delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#######################################################################
# view_research_info: 展示调研参与结果
########################################################################
@login_required
def view_research_info(request):
	research_id = request.GET['research_id']
	research = Research.objects.get(id=research_id)
	
	research_items = ResearchItem.objects.filter(research=research)
	research_item_id2research_item = dict([i.id, i] for i in research_items)
	for research_item in research_items:
		research_item.count = 0
		if research_item.type == RESEARCHITEM_TYPE_SELECT:
			research_item.info = {}
			for key in research_item.initial_data.split('|'):
				key = key.strip()
				if key:
					research_item.info[key] = 0
		if research_item.type == RESEARCHITEM_TYPE_CHECKBOX:
			research_item.info = {}
			for key in research_item.initial_data.split('|'):
				key = key.strip()
				if key:
					research_item.info[key] = 0
	research_item_values = ResearchItemValue.objects.filter(research=research).exclude(value='')
	
	for research_item_value in research_item_values:
		research_item = research_item_id2research_item[research_item_value.item_id]
		research_item.count += 1
		if research_item.type == RESEARCHITEM_TYPE_SELECT:
			key = key.strip()
			key = research_item_value.value
			research_item.info[key] += 1
		if research_item.type == RESEARCHITEM_TYPE_CHECKBOX:
			for key in research_item_value.value.split(','):
				key = key.strip()
				if key:
					research_item.info[key] += 1

	c = RequestContext(request, {
			'first_nav_name': MARKET_TOOLS_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
			'research': research,
			'research_items': research_items
		})
	return render_to_response('research/editor/research_info.html', c)


#######################################################################
# list_research_item_value: 展示调研参项的结果
########################################################################
@login_required
def list_research_item_value(request):
	item_id = request.GET['item_id']
	
	research_item = ResearchItem.objects.get(id=item_id)
	research_item_values = ResearchItemValue.objects.filter(item_id=item_id).exclude(value='')
	
	c = RequestContext(request, {
			'first_nav_name': MARKET_TOOLS_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
			'research_item': research_item,
			'research_item_values': research_item_values
		})
	return render_to_response('research/editor/research_item_value_list.html', c)


########################################################################
# list_research_members: 展示参与调研列表
########################################################################
@login_required
def list_research_members(request):
	research_id = request.GET['research_id']
	research = Research.objects.get(id=research_id)
	
	webapp_users = research.joined_users
	webapp_user_ids = [webapp_user.id for webapp_user in webapp_users]
	member_ids = [webapp_user.member_id for webapp_user in webapp_users]
	
	members = Member.objects.filter(id__in=member_ids)
	id2member = dict([(m.id, m) for m in members])
	
	webapp_user2values = {}
	for item_value in ResearchItemValue.objects.filter(research=research, webapp_user_id__in=webapp_user_ids):
		webapp_user2values.setdefault(item_value.webapp_user_id, {})[item_value.item_id] = item_value
		
	items = list(ResearchItem.objects.filter(research=research))

	for webapp_user in webapp_users:
		item_values = []
		for item in items:
			id2value = webapp_user2values[webapp_user.id]
			if not item.id in id2value:
				#存在非必填项
				continue

			value = id2value[item.id]
			user_input_value = value.value

			is_image = False
			if item.type == RESEARCHITEM_TYPE_IMAGE:
				is_image = True

			item_values.append({
				'title': item.title,
				'created_at': item.created_at,
				'is_image': is_image,
				'user_input_value': user_input_value
			})
			
		webapp_user.item_values = item_values
		
		if webapp_user.member_id in id2member:
			webapp_user.member = id2member[webapp_user.member_id]
		else:
			webapp_user.member = None

	c = RequestContext(request, {
			'first_nav_name': MARKET_TOOLS_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
			'research': research,
			'webapp_users': webapp_users
		})
	return render_to_response('research/editor/research_members.html', c)


########################################################################
# get_channel_qrcode_pay_orders: 获取渠道二维码成交订单列表
########################################################################
def get_channel_qrcode_pay_orders(request, setting_id):
	# relations = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=setting_id)
	# setting_id2count = {}
	# member_id2setting_id = {} 
	# member_ids = []
	# for r in relations:
	# 	member_ids.append(r.member_id)
	# 	member_id2setting_id[r.member_id] = r.channel_qrcode_id
	# 	if r.channel_qrcode_id in setting_id2count:
	# 		setting_id2count[r.channel_qrcode_id] += 1
	# 	else:
	# 		setting_id2count[r.channel_qrcode_id] = 1
	
	# webapp_users = member_model.WebAppUser.objects.filter(member_id__in=member_ids)
	# webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
	# webapp_user_ids = set(webapp_user_id2member_id.keys())
	# orders = mall_model.Order.objects.filter(webapp_user_id__in=webapp_user_ids, status=mall_model.ORDER_STATUS_SUCCESSED).order_by('-created_at')

	c = RequestContext(request, {
			'first_nav_name': MARKET_TOOLS_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
			'setting_id':setting_id
		})
	return render_to_response('channel_qrcode/editor/channel_qrcode_orders.html', c)

