# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
from utils.string_util import byte_to_hex
import urllib, urllib2
import os
import json
import random
import shutil

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import apiview_util
from core import paginator

from modules.member.module_api import get_member_by_id_list
from modules.member.module_api import *
from mall.models import *

from models import *
from modules.member.models import *

#定向发放优惠券
#根据会员发放优惠券
SEND_COUPON_OF_MEMBER = 1 
#根据分组发放优惠券
SEND_COUPON_OF_TAG = 2
#根据等级发放优惠券
SEND_COUPON_OF_GRADE = 3



########################################################################
# 作废优惠券: discard_coupons
########################################################################
@login_required
def discard_coupons_bak(request):
	pool2coupons = json.loads(request.POST.get('pool2coupons', '{}'))
	coupon_ids = []
	for pool_id, coupons in pool2coupons.items():
		#更新coupon pool的remained count
		coupon_count = len(coupons)
		CouponPool.objects.filter(id=int(pool_id)).update(remained_count=F('remained_count')-coupon_count)
		for coupon_id in coupons:
			coupon_ids.append(int(coupon_id))

	#更新coupon的status
	Coupon.objects.filter(id__in=coupon_ids).update(status=COUPON_STATUS_DISCARD)
	
	response = create_response(200)
	return response.get_response()


########################################################################
# 作废优惠券: discard_coupons
########################################################################
@login_required
def discard_coupons(request):
	#更新coupon的status
	coupon_ids = request.POST['coupon_ids'].split(',')
	Coupon.objects.filter(id__in=coupon_ids).update(status=COUPON_STATUS_DISCARD)
	
	response = create_response(200)
	return response.get_response()


########################################################################
# create_manual_coupons: 创建manual类型的coupon集合
########################################################################
@login_required
def create_manual_coupons(request):
	coupons = _create_coupons(request, True)

	items = []
	for coupon in coupons:
		items.append({
			'coupon_id': coupon.coupon_id,
			'money': float(coupon.money),
			'expired_time': coupon.expired_time.strftime("%Y-%m-%d")
		})

	response = create_response(200)
	response.data = {
		'items': items
	}
	return response.get_response()


########################################################################
# _create_coupons: 创建优惠券
########################################################################
def _create_coupons(request, is_manual_generated=False):
	owner = request.user
	count = int(request.POST.get('count', 0))
	coupon_rule_id = request.POST['rule_id']
	coupon_rule = CouponRule.objects.get(id=coupon_rule_id)

	today = datetime.today()
	expired_time = today + timedelta(coupon_rule.valid_days)

	#创建coupon
	coupons = []
	i = 1
	if count > 0:
		random_args_value = ['1','2','3','4','5','6','7','8','9','0']
		while True:
			coupon_id = '%03d%04d%s' % (owner.id, coupon_rule.id, ''.join(random.sample(random_args_value, 6)))
			try:
				new_coupon = Coupon.objects.create(
					owner = owner,
					coupon_id = coupon_id,
					provided_time = today,
					expired_time = expired_time,
					money = coupon_rule.money,
					coupon_rule_id = coupon_rule.id,
					is_manual_generated = is_manual_generated
				)
				coupons.append(new_coupon)
				if i >= count:
					break
				i += 1
			except:
				continue
	return coupons

########################################################################
# _create_random_coupon_ids: 生成count个随机的优惠券id
########################################################################
def _create_random_coupon_ids(owner_id, coupon_pool_id, count):
	random_args_value = ['1','2','3','4','5','6','7','8','9','0']
	ids = set()

	while True:
		id = '%03d%04d%s' % (owner_id, coupon_pool_id, ''.join(random.sample(random_args_value, 6)))
		ids.add(id)
		if len(ids) >= count:
			return ids


########################################################################
# get_coupon_config: 获取优惠券设置
########################################################################
@login_required
def get_coupon_config(request):
	try:
		coupon_config = CouponConfig.objects.get(owner=request.user)
	except:
		#创建每个用户默认的coupon config
		coupon_config = CouponConfig.objects.create(
			owner = request.user
		)

	response = create_response(200)
	response.data = {
		'useType': 'nolimit' if coupon_config.use_type == COUPON_USE_TYPE_NOLIMIT else 'depend_to_price',
		'overflowType': 'drop' if coupon_config.overflow_type == COUPON_OVERFLOW_TYPE_DROP else 'change_to_score',
		'activatePrice': coupon_config.activate_price
	}
	return response.get_response()


########################################################################
# get_coupon_rule: 优惠券规则
########################################################################
@login_required
def get_coupon_rule(request):
	sort_attr = request.GET.get('sort_attr', '-created_at')
	# 当排序条件无效时，使用创建时间倒序排列
	sort_attr_tmp = sort_attr.replace('-', '')
	if (sort_attr_tmp != 'valid_days') and (sort_attr_tmp != 'money') and (sort_attr_tmp != 'created_at'):
		sort_attr = '-created_at'

	filter_attr = request.GET.get('filter_attr')
	if filter_attr == 'valid':
		coupon_rules = list(CouponRule.objects.filter(owner=request.user, is_active=True, valid_restrictions=request.GET.get('filter_value')).order_by(sort_attr))
	else:
		coupon_rules = list(CouponRule.objects.filter(owner=request.user, is_active=True).order_by(sort_attr))
	
	#进行分页
	count_per_page = 10#int(request.GET.get('count_per_page', 10))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, rules = paginator.paginate(coupon_rules, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	
	response = create_response(200)
	
	response.data.items = []
	for rule in rules:
		cur_rule = JsonResponse()
		cur_rule.id = rule.id
		cur_rule.name = rule.name
		cur_rule.valid_days = rule.valid_days
		cur_rule.money = str(rule.money)
		cur_rule.valid_restrictions = rule.valid_restrictions
		response.data.items.append(cur_rule)
	
	from django.db.models import Count
	valids = CouponRule.objects.filter(owner=request.user, is_active=True).values('valid_restrictions').annotate(Count('id')).order_by('-valid_restrictions')
	response.data.valids = []
	for valid in valids:
		cur_valid = JsonResponse()
		cur_valid.name = str(valid.values()[0])
		response.data.valids.append(cur_valid)
		
	response.data.sortAttr = request.GET.get('sort_attr', sort_attr)
	response.data.pageinfo = paginator.to_dict(pageinfo)
	
	return response.get_response()


########################################################################
# update_coupon_config: 更新优惠券设置
########################################################################
@login_required
def update_coupon_config(request):
	params = {
		'use_type': COUPON_USE_TYPE_NOLIMIT if request.POST['use_type'] == 'nolimit' else COUPON_USE_TYPE_DEPEND_ON_PRICE,
		'overflow_type': COUPON_OVERFLOW_TYPE_DROP if request.POST['overflow_type'] == 'drop' else COUPON_OVERFLOW_TYPE_CHANGE_TO_SCORE
	}
	if params['use_type'] == COUPON_USE_TYPE_DEPEND_ON_PRICE:
		params['activate_price'] = request.POST['activate_price']
	CouponConfig.objects.filter(owner_id=request.user.id).update(**params)

	return create_response(200).get_response()


########################################################################
# get_records: 获取优惠券
########################################################################
# @login_required
# def get_records(request):
# 	"""
# 	TODO delete
# 	"""
# 	today = datetime.today()
# 	#更新过期优惠券状态
# 	Coupon.objects.filter(owner=request.user, expired_time__lt=today, status=COUPON_STATUS_UNUSED).update(status=COUPON_STATUS_EXPIRED)
# 	coupons = Coupon.objects.filter(owner=request.user).order_by('-id')
# 	#处理过滤
# 	sort_attr = request.GET.get('sort_attr', '-id')
# 	if sort_attr.replace('-', '') != 'provided_time' and sort_attr.replace('-', '') != 'expired_time' and sort_attr.replace('-', '') != 'money':
# 		sort_attr = '-id'
	
# 	params = {'owner':request.user}
# 	#微优惠券规则、试用状态2选一
#  	filter_value = int(request.GET.get('filter_value', -1))
# 	filter_attr = request.GET.get('filter_attr', None)
# 	if (filter_attr == None) or (filter_value == -1):
# 		pass
# 	else:
# 		params[filter_attr] = filter_value
# 	#处理搜索
# 	query_attr = request.GET.get('query_attr', None)
# 	query = request.GET.get('query', None)
# 	if query_attr == 'target':
# 		if query==u"手工":
# 			params['is_manual_generated'] = True
# 		else:
# 			query = byte_to_hex(query)
# 			members = Member.objects.filter(webapp_id=request.user_profile.webapp_id, is_for_test=False, username_hexstr__contains=query)
# 			member_ids = [m.id for m in members]
# 			params['member_id__in'] = member_ids
# 	else:
# 		if query:
# 			params['coupon_id__contains'] = query

# 	#获取数据
# 	coupons = coupons.filter(**params).order_by(sort_attr)
	
# 	#获取coupon所属的rule的name
# 	id2rule = dict([(rule.id, rule) for rule in CouponRule.objects.filter(owner=request.user)])
	
# 	#进行分页
# 	count_per_page = int(request.GET.get('count_per_page', 15))
# 	cur_page = int(request.GET.get('page', '1'))
# 	pageinfo, coupons = paginator.paginate(coupons, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
# 	#避免便利整个优惠券列表
# 	member_ids = [c.member_id for c in coupons]
# 	members = get_member_by_id_list(member_ids)
# 	member_id2member = dict([(m.id, m) for m in members])
	
# 	#获取被使用的优惠券使用者信息
# 	coupon_ids = [c.id for c in coupons if c.status==COUPON_STATUS_USED]
# 	orders = Order.get_orders_by_coupon_ids(coupon_ids)
# 	if orders:
# 		coupon_id2webapp_user_id = dict([(o.coupon_id, o.webapp_user_id) for o in orders])
# 	else:
# 		coupon_id2webapp_user_id = {}
	
# 	response = create_response(200)
# 	response.data.items = []
# 	#统计是否有active的coupon
# 	has_active_coupon = False
# 	for coupon in coupons:
# 		cur_coupon = JsonResponse()
# 		cur_coupon.id = coupon.id
# 		cur_coupon.status = coupon.status
# 		cur_coupon.coupon_id = coupon.coupon_id
# 		cur_coupon.provided_time = coupon.provided_time.strftime('%m月%d日')
# 		cur_coupon.expired_time = coupon.expired_time.strftime('%m月%d日')
# 		cur_coupon.money = str(coupon.money)
# 		cur_coupon.is_manual_generated = coupon.is_manual_generated
# 		cur_member = JsonResponse()
# 		member_id = int(coupon.member_id)
# 		if coupon.status == COUPON_STATUS_UNUSED:
# 			has_active_coupon = True
# 		if member_id in member_id2member:
# 			member = member_id2member[member_id]
# 			cur_member.username_for_html = member.username_for_html
# 		else:
# 			member = ''
# 			cur_member.username_for_html = ''
# 		cur_member.id = member_id
		
# 		consumer = JsonResponse()
# 		consumer.username_for_html = ''
# 		if coupon.status == COUPON_STATUS_USED:
# 			if coupon.id in coupon_id2webapp_user_id:
# 				webapp_user_id = coupon_id2webapp_user_id[coupon.id]
# 				member = WebAppUser.get_member_by_webapp_user_id(webapp_user_id)
# 				if member:
# 					consumer.username_for_html = member.username_for_html
# 				else:
# 					consumer.username_for_html = '未知'
# 			else:
# 				consumer.username_for_html = '未知'
		
# 		cur_coupon.member = cur_member
# 		cur_coupon.consumer = consumer
# 		cur_coupon.rule_name = id2rule[coupon.coupon_rule_id].name
# 		response.data.items.append(cur_coupon)
	
# 	#获取所有优惠券规则
# 	coupon_rules = list(CouponRule.objects.filter(owner=request.user, is_active=True).order_by('-id'))
# 	response.data.roles = []
# 	for role in coupon_rules:
# 		cur_role = JsonResponse()
# 		cur_role.id = role.id
# 		cur_role.name = role.name
# 		response.data.roles.append(cur_role)
		
# 	response.data.has_active_coupon = has_active_coupon
# 	response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
# 	response.data.pageinfo = paginator.to_dict(pageinfo)
# 	return response.get_response()


########################################################################
# get_member_list: 获取会员列表
########################################################################
@login_required
def get_member_list(request):
	response = create_response(200)
	response.data.items = []
	
	#获取所有会员 等级
	webapp_id = request.user_profile.webapp_id
	members = Member.get_members(webapp_id)
	member_id2grade_name = dict([(m.id, m.grade.name)for m in members])
	for m in members:
		cur_member = JsonResponse()
		cur_member.id = m.id
		if m.user_icon:
			cur_member.user_icon = m.user_icon
		else:
			#当图片不存在时页面会自动加载默认图片
			cur_member.user_icon = u'/static/img/user-1.jpg' 
		cur_member.name = m.username_for_html
		cur_member.grade = member_id2grade_name[m.id]
		response.data.items.append(cur_member)
		
	return response.get_response()

########################################################################
# get_member_grade_list: 获取会员等级列表
########################################################################
@login_required
def get_member_grade_list(request):
	response = create_response(200)
	response.data.items = []
	
	#获取所有会员 等级
	webapp_id = request.user_profile.webapp_id
	member_grades = MemberGrade.get_all_grades_list(webapp_id)
	for m in member_grades:
		cur_member_grade = JsonResponse()
		cur_member_grade.id = m.id
		cur_member_grade.name = m.name
		cur_member_grade.member_count = len(Member.get_member_list_by_grade_id(m.id))
		if cur_member_grade.member_count==0:
			cur_member_grade.member_count = u'-'
		response.data.items.append(cur_member_grade)
	
	return response.get_response()

########################################################################
# get_member_tag_list: 获取会员分组列表
########################################################################
@login_required
def get_member_tag_list(request):
	response = create_response(200)
	response.data.items = []
	
	#获取所有会员 等级
	webapp_id = request.user_profile.webapp_id
	member_tags = MemberTag.get_member_tags(webapp_id)
	for m in member_tags:
		cur_member_tag = JsonResponse()
		cur_member_tag.id = m.id
		cur_member_tag.name = m.name
		cur_member_tag.member_count = len(MemberHasTag.get_member_list_by_tag_id(m.id))
		if cur_member_tag.member_count==0:
			cur_member_tag.member_count = u'-'
		response.data.items.append(cur_member_tag)
	
	return response.get_response()

########################################################################
# send_coupons: 发放优惠券
########################################################################
@login_required
def send_coupons(request):
	type = int(request.POST['type'])
	id_str = request.POST.get('ids')
	count = int(request.POST.get('count'))
	rule_id = request.POST['rule_id']
	members = []
	if type == SEND_COUPON_OF_MEMBER:
		if id_str:
			member_ids = id_str.split('_')
			members = get_member_by_id_list(member_ids)
	if type == SEND_COUPON_OF_TAG:
		if id_str:
			tag_ids = id_str.split('_')
			for id in tag_ids:
				members += MemberHasTag.get_member_list_by_tag_id(id)
	if type == SEND_COUPON_OF_GRADE:
		if id_str:
			grade_ids = id_str.split('_')
			for id in grade_ids:
				members += Member.get_member_list_by_grade_id(id)
		
	id2member = dict([(m.id, m)for m in members])
	from util import create_coupons
	for id in id2member:
		member = id2member[id]
		create_coupons(request.user, rule_id, count, member.id)
	response = create_response(200)
	return response.get_response()


########################################################################
# update_coupon_saller_data: 更新优惠券排行榜时间
########################################################################
@login_required
def update_coupon_saller_data(request):
	start_date = request.POST['start_date']
	end_date = request.POST['end_date']
	coupon_saller_data = CouponSallerDate.objects.filter(owner=request.user)
	if coupon_saller_data:
		coupon_saller_data.update(start_date=start_date, end_date=end_date)
	else:
		coupon_saller_data = CouponSallerDate()
		coupon_saller_data.owner = request.user
		coupon_saller_data.start_date = start_date
		coupon_saller_data.end_date = end_date
		coupon_saller_data.save()
		
	response = create_response(200)
	return response.get_response()
	
def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)