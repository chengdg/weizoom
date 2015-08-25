# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
import time
from datetime import datetime, timedelta

from django.conf import settings
from core.jsonresponse import create_response, JsonResponse

from core.exceptionutil import unicode_full_stack

from modules.member import util as member_util
from modules.member.models import *
from modules.member.util import get_member
from market_tools.prize.models import *
from market_tools.tools.coupon.util import consume_coupon
from market_tools.tools.lottery.mobile_views import _get_prize
from models import *
from watchdog.utils import watchdog_notice


########################################################################
# record_prize: 记录抽奖历史
########################################################################
def record_prize(request):
	webapp_user = request.webapp_user
	lottery_id = int(request.GET['lottery_id'])
	prize_id = int(request.GET['prize_id'])
	prize_position = int(request.GET.get('prize_position', 0))
	member = get_member(request)
	
	if not member:
		raise Http404(u"会员信息不存在")
	
	lottery = Lottery.objects.get(id=lottery_id)
	if prize_id:
		prize = Prize.objects.get(id=prize_id)
	else:
		prize = None
		
	response = create_response(200)
	
	__record_prize(webapp_user, lottery, member, prize, prize_position)
	
	return response.get_response()


########################################################################
# get_prize: 大转盘记录抽奖历史，并返回奖项
########################################################################
def get_prize(request):
	webapp_user = request.webapp_user
	lottery_id = int(request.GET['lottery_id'])
	prize_position = int(request.GET.get('prize_position', 0))
	try:
		lottery = Lottery.objects.get(id=lottery_id)
	except:
		raise Http404(u"该活动信息不存在")
	
	member = request.member
	
	if not member:
		raise Http404(u"会员信息不存在")
	
	relations = LotteryHasPrize.objects.filter(lottery=lottery)
	prize_ids = [r.prize_id for r in relations]
	prizes = Prize.objects.filter(id__in=prize_ids)
	
	#定义奖项：
	if lottery.can_repeat:
		play_times = lottery.daily_play_count
	else:
		play_times = 1
	
	#根据发奖规则发奖
	prize = _get_prize(lottery, member, prizes)

	response = create_response(200)
	
	prize = __record_prize(webapp_user, lottery, member, prize,prize_position)
	
	if prize:
		cur_prize = JsonResponse()
		cur_prize.name = prize.name
		cur_prize.id = prize.id
		cur_prize.level = prize.level
		response.data.prize = cur_prize
	else:
		response.data.prize = None

	cur_member = JsonResponse()
	cur_member.integral = webapp_user.integral_info['count']
	response.data.member = cur_member

	return response.get_response()


########################################################################
# __record_prize: 记录抽奖历史内部操作
########################################################################
def __record_prize(webapp_user, lottery, member, prize, prize_position=0):
	prize_money = 0
	
	#减积分
	if lottery.expend_integral > 0:
		if webapp_user.integral_info['count'] > lottery.expend_integral:
			expend_integral = lottery.expend_integral
		else:
			expend_integral = webapp_user.integral_info['count']
		webapp_user.consume_integral(expend_integral, u'参与抽奖，花费积分')
	
	if not prize:
		LotteryRecord.objects.create(owner=lottery.owner, member=member, lottery=lottery, lottery_name=lottery.name, prize_type=0, prize_level=0,
			prize_name=u'谢谢参与', is_awarded=True, prize_number=time.time(), prize_detail='', prize_money=prize_money)
		
		return None
	
	relation = LotteryHasPrize.objects.get(lottery=lottery, prize=prize)
		
	#实物
	if relation.prize_type == 0:
		is_awarded = False
		prize_detail = relation.prize_source
	#优惠券
	elif relation.prize_type == 1:
		is_awarded = True
		rule_id = relation.prize_source
		# coupons = create_coupons(lottery.owner, rule_id, 1, member.id)
		# prize_detail = coupons.coupon_id
		# prize_money = coupons[0].money
		coupon, msg = consume_coupon(lottery.owner.id, rule_id, member.id)
		if coupon:
			prize_detail = coupon.coupon_id
			prize_money = coupon.money
		else:
			watchdog_notice('微信抽奖失败，错误原因:%s,owner.id:%s:rule.id:%s,member.id:%s' 
				% (msg, lottery.owner.id, rule_id, member.id), type="mall")
			LotteryRecord.objects.create(owner=lottery.owner, member=member, lottery=lottery, lottery_name=lottery.name, prize_type=0, prize_level=0,
			prize_name=u'谢谢参与', is_awarded=True, prize_number=time.time(), prize_detail='', prize_money=prize_money)
			return None
	#兑换码
	elif relation.prize_type == 2:
		is_awarded = True
		prize_detail = relation.prize_source
	#积分
	elif relation.prize_type == 3:
		is_awarded = True
		prize_detail = relation.prize_source
		#增加积分
		webapp_user.consume_integral(-int(prize_detail), u'参与抽奖，赢得积分')
	
	from hashlib import md5
	cur_time = str(time.time())
	prize_number = md5(cur_time).hexdigest()[10:-10] #生成一个12位字符串
		
	LotteryRecord.objects.create(owner=lottery.owner, member=member, lottery=lottery, lottery_name=lottery.name, prize_type=relation.prize_type, prize_level=prize.level,
			prize_name=prize.name, is_awarded=is_awarded, prize_number=prize_number, prize_detail=prize_detail, prize_money=prize_money, prize_position=prize_position)
	
	#更改奖品个数
	Prize.decrease_count(prize, 1)
	
	return prize