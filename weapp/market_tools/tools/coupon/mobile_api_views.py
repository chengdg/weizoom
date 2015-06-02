# -*- coding: utf-8 -*-

__author__ = 'jiangzhe'

from core.jsonresponse import create_response
from mall.promotion import models
from util import consume_coupon as util_consume_coupon

def consume_coupon(request):
	"""
	领取优惠券
	参数：request.POST['rule_id']
	"""
	rule_id = request.POST.get('rule_id', '0')
	# if not rule_id.isdigit():
	# 	rule_id = 0
	coupon = None
	if not request.member:
		msg = u'请关注后再领取优惠券'
	else:
		coupon, msg = util_consume_coupon(request.webapp_owner_id, rule_id, request.member.id)
	if coupon:
		return create_response(200).get_response()
	return create_response(200, msg)

def get_couponRule(request):
	"""
	获取优惠券规则信息
	参数：request.GET['rule_id']
	"""
	rule_id = request.GET.get('rule_id', '0')
	rule = models.CouponRule.objects.filter(id=rule_id, owner_id=request.webapp_owner_id)

	if len(rule) == 1:
		response = create_response(200)
		response.data = rule[0]
		return response.get_response()
	return create_response(200, u'没有对应的优惠券规则')

