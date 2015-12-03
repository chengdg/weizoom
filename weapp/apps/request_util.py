# -*- coding: utf-8 -*-
from mall.promotion.models import CouponRule
from market_tools.tools.coupon.util import consume_coupon

__author__ = 'robert'

from datetime import datetime
import json

from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.contrib import auth

from account.views import save_base64_img_file_local_for_webapp
from customerized_apps import mysql_models as mongo_models

#===============================================================================
# __get_fields_to_be_save : 获得待存储的数据
#===============================================================================
def get_fields_to_be_save(request):
	fields = request.POST.dict()
	fields['created_at'] = datetime.today()
	fields['owner_id'] = request.manager.id
	
	webapp_user = getattr(request, 'webapp_user', None)
	if webapp_user:
		fields['webapp_user_id'] = request.webapp_user.id

	member = getattr(request, 'member', None)
	if member:
		fields['member_id'] = request.member.id

	if 'prize' in request.POST:
		fields['prize'] = json.loads(fields['prize'])

	if 'termite_data' in fields:
		fields['termite_data'] = json.loads(fields['termite_data'])
		for item in fields['termite_data']:
			att_url = []
			if fields['termite_data'][item]['type']=='appkit.uploadimg':
				fields['uploadImg'] = json.loads(fields['termite_data'][item]['value'])
				for picture in fields['uploadImg']:
					att_url.append(picture)
				fields['termite_data'][item]['value'] = att_url
	return fields

def get_consume_coupon(owner_id, app_name, app_id, rule_id, member_id, has_coupon_count=0):
	'''

	@param owner_id:
	@param app_name:
	@param app_id:
	@param rule_id:
	@param member_id:
	@param has_coupon_count: 表示在抽奖活动里某个会员获得优惠券的数量
	@return:
	'''
	coupon = None
	rules = CouponRule.objects.filter(id=rule_id, owner_id=owner_id)
	if rules and rules[0].end_date <= datetime.today():
		coupon_message = u'该优惠券使用期已过，不能领取！'
	elif rules and rules[0].limit_counts != -1 and has_coupon_count >= rules[0].limit_counts:
		coupon_message = u'该优惠券每人限领%s张，你已经领取过了！' % rules[0].limit_counts
	else:
		coupon,coupon_message =consume_coupon(owner_id, rule_id, member_id)
	data = {
		'user_id': owner_id,
		'app_name': app_name,
		'app_id': app_id,
		'member_id': member_id,
		'coupon_id': coupon.id if coupon else 0,
		'coupon_msg': coupon_message,
		'created_at': datetime.today()
	}
	consume_coupon_log = mongo_models.ConsumeCouponLog(**data)
	consume_coupon_log.save()
	return coupon,coupon_message


