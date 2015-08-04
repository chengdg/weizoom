# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from models import *
from modules.member import util as member_util

from mall.promotion.models import CouponRule


########################################################################
# get_research: 获取调研详情
########################################################################
def get_research(request):
	webapp_user = request.webapp_user
	member = request.member
	research_id = request.GET['research_id']

	is_participated = False #是否已经参加
	
	try:
		research = Research.objects.get(id=research_id)
	except:
		c = RequestContext(request, {
			'is_deleted_data': True
		})
		return render_to_response('research/webapp/research.html', c)
	
	hide_non_member_cover = False
	if research.is_non_member:
		hide_non_member_cover = True
	
	if research.prize_type == 1:
		research.prize_source = CouponRule.objects.get(id=research.prize_source).name

	items = ResearchItem.objects.filter(research=research)
	for item in items:
		item.input_name = '{}-{}'.format(item.id, item.type)
		if item.type == RESEARCHITEM_TYPE_SELECT:
			item.options = item.initial_data.split('|')
		if item.type == RESEARCHITEM_TYPE_CHECKBOX:
			item.options = item.initial_data.split('|')

		if item.title == u'姓名':
			item.value = member.member_info.name if (member is not None) else ''
		elif item.title == u'手机号':
			item.value = member.member_info.phone_number if (member is not None) else ''
		else:
			item.value = ''

		type = 'text'
		if item.type == RESEARCHITEM_TYPE_SELECT:
			type = 'select'
		elif item.type == RESEARCHITEM_TYPE_IMAGE:
			type = 'image'
		elif item.type == RESEARCHITEM_TYPE_CHECKBOX:
			type = 'checkbox'
		item.type = type

	#确定是否已经报名
	if webapp_user:
		is_participated = (ResearchItemValue.objects.filter(research=research, webapp_user=webapp_user).count() > 0)

	#获取报名人数
	joined_user_count = research.joined_user_count
	if research.owner.username == 'oujia':
		joined_user_count += 563

	#参与活动的好友信息
	joined_user_ids = set(ResearchItemValue.objects.filter(research=research).values_list("webapp_user_id", flat=True).distinct())
	friend_members = member.friends if member else []
	joined_friend_members = []
	for member in friend_members:
		if member.id in joined_friend_members:
			joined_friend_members.append(member)

	request.should_hide_footer = True
	c = RequestContext(request, {
		'page_title': research.name,
	    'research': research,
	    'is_participated': is_participated,
	    'items': items,
	    'member_count': joined_user_count,
	    'friend_members': joined_friend_members,
	    'hide_non_member_cover' : hide_non_member_cover,
	    'member': member
	})
	return render_to_response('research/webapp/research.html', c)

