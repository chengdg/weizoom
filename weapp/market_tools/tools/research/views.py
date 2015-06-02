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

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from market_tools.tools.coupon.util import get_coupon_rules 

from models import *

COUNT_PER_PAGE = 20
MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'research'

########################################################################
# list_researches: 显示调研列表
########################################################################
@login_required
def list_researches(request):
	researches = Research.objects.filter(owner=request.user, is_deleted=False)

	for research in researches:
		research.member_count = research.joined_user_count
		if request.user.username == 'oujia':
			 research.member_count += 563

	#分页
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, researches = paginator.paginate(researches, cur_page, COUNT_PER_PAGE, query_string=request.META['QUERY_STRING'])
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'researches': researches,
		'pageinfo': json.dumps(paginator.to_dict(pageinfo)),
	})
	return render_to_response('research/editor/researches.html', c)


########################################################################
# __extract_items: 抽取activity items
########################################################################
def __extract_items(request):
	id2info = {}
	for key, value in request.POST.items():
		if not key.startswith('item_'):
			continue

		_, type, name, id = key.split('_')
		if type == 'text':
			type = RESEARCHITEM_TYPE_TEXT
		elif type == 'select':
			type = RESEARCHITEM_TYPE_SELECT
		elif type == 'checkbox':
			type = RESEARCHITEM_TYPE_CHECKBOX
		elif type == 'image':
			type = RESEARCHITEM_TYPE_IMAGE
		else:
			type = -1

		if id in id2info:
			info = id2info[id]
		else:
			info = {'type': type, 'id': int(id)}
			id2info[id] = info

		info[name] = value

	items = id2info.values()
	items.sort(lambda x,y: cmp(x['id'], y['id']))

	return items


########################################################################
# __update_research_items: 更新research items
########################################################################
def __update_research_items(request, research_id):
	ResearchItem.objects.filter(research_id=research_id).delete()

	for item in __extract_items(request):
		ResearchItem.objects.create(
			owner = request.user, 
			research_id = research_id, 
			title = item['title'], 
			type = item['type'],
			initial_data = item.get('data', ''),
			is_mandatory = 'mandatory' in item
		)


########################################################################
# create_research: 添加调研
########################################################################
TYPE_TEXT_NAME = "text_%s"
TYPE_SELECT_NAME = "select_%s"
TYPE_IMAGE_NAME = "image_%s"
TYPE_SELECT_OPTION = "option_%s"
@login_required
def create_research(request):
	if request.POST:
		name = request.POST["name"]
		detail =request.POST.get("detail", '')
		prize_type = request.POST.get("prize_type", '-1')
		prize_source = request.POST.get("prize_source", '')
		is_non_member = request.POST.get("is_non_member", 0)
		
		research = Research.objects.create(
			owner=request.user, 
			name=name, 
			detail=detail,
			prize_type=prize_type,
			is_non_member=is_non_member,
			prize_source=prize_source
		)

		__update_research_items(request, research.id)
		
		return HttpResponseRedirect('/market_tools/research/')
	else:
		coupon_rules = get_coupon_rules(request.user)
		coupon_rule_items = []
		for coupon_rule in coupon_rules:
			coupon_rule_items.append(coupon_rule.to_dict())
		
		c = RequestContext(request, {
			'first_nav_name': MARKET_TOOLS_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
			'coupon_rule_items': json.dumps(coupon_rule_items)
		})
		return render_to_response('research/editor/edit_research.html', c)


########################################################################
# update_research: 更新/查看调研
########################################################################
@login_required
def update_research(request, research_id):
	research = Research.objects.get(id=research_id)

	research_items = []
	for research_item in ResearchItem.objects.filter(research=research):
		type = 'text'
		if research_item.type == RESEARCHITEM_TYPE_SELECT:
			type = 'select'
		elif research_item.type == RESEARCHITEM_TYPE_IMAGE:
			type = 'image'
		elif research_item.type == RESEARCHITEM_TYPE_CHECKBOX:
			type = 'checkbox'

		research_items.append({
			'id': research_item.id,
			'title': research_item.title,
			'initial_data': research_item.initial_data,
			'is_mandatory': research_item.is_mandatory,
			'type': type
		})
	
	coupon_rules = get_coupon_rules(request.user)
	coupon_rule_items = []
	for coupon_rule in coupon_rules:
		coupon_rule_items.append({
			'id': coupon_rule.id,
			'name': coupon_rule.name,
		})
	
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'research': research,
		'research_items': json.dumps(research_items),
		'coupon_rule_items': json.dumps(coupon_rule_items)
	})
	return render_to_response('research/editor/edit_research.html', c)


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
			# key = key.strip()
			key = research_item_value.value.strip()
			research_item.info[key] += 1
		if research_item.type == RESEARCHITEM_TYPE_CHECKBOX:
			for key in research_item_value.value.split(','):
				key = key.strip()
				if key and research_item.info.has_key(key):
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
	
	#分页
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, webapp_users = paginator.paginate(webapp_users, cur_page, COUNT_PER_PAGE, query_string=request.META['QUERY_STRING'])
	
	for webapp_user in webapp_users:
		item_values = []
		for item in items:
			id2value = webapp_user2values[webapp_user.id]
			if not item.id in id2value:
				#存在非必填项
				continue

			value = id2value[item.id]
			user_input_value = value.value
			webapp_user.join_at = value.created_at

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
			'webapp_users': webapp_users,
			'pageinfo': json.dumps(paginator.to_dict(pageinfo)),
		})
	return render_to_response('research/editor/research_members.html', c)
