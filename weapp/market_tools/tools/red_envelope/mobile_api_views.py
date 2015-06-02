# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
import time

from django.conf import settings
from core.jsonresponse import create_response, JsonResponse

from core.exceptionutil import unicode_full_stack

from modules.member import util as member_util
from modules.member.models import *
from modules.member.util import get_member
from market_tools.prize.models import *
from market_tools.tools.coupon.util import consume_coupon
from models import *
from watchdog.utils import watchdog_notice

# ########################################################################
# # record_prize: 记录抽奖历史
# ########################################################################
# def record_prize(request):
# 	webapp_user = request.webapp_user
# 	lottery_id = int(request.GET['lottery_id'])
# 	prize_id = int(request.GET['prize_id'])
# 	prize_position = int(request.GET.get('prize_position', 0))
# 	member = get_member(request)
	
# 	if not member:
# 		raise Http404(u"会员信息不存在")
	
# 	lottery = Lottery.objects.get(id=lottery_id)
# 	if prize_id:
# 		prize = Prize.objects.get(id=prize_id)
# 	else:
# 		prize = None
		
# 	response = create_response(200)
	
# 	__record_prize(webapp_user, lottery, member, prize, prize_position)
	
# 	return response.get_response()


########################################################################
# get_prize: 大转盘记录抽奖历史，并返回奖项
########################################################################
def get_prize(request):
	webapp_user = request.webapp_user
	red_envelope_id = int(request.GET['red_envelope_id'])
	if request.member:
		member = request.member
	else:
		member = None
	
	try:
		red_envelope = RedEnvelope.objects.get(id=red_envelope_id)
	except:
		raise Http404(u"该活动信息不存在")
	
	response = create_response(200)
	
	if webapp_user and RedEnvelopeRecord.objects.filter(owner=red_envelope.owner, webapp_user_id=webapp_user.id, red_envelope=red_envelope).count() > 0:
		red_envelope_record = RedEnvelopeRecord.objects.filter(owner=red_envelope.owner, webapp_user_id=webapp_user.id, red_envelope=red_envelope)[0]
		cur_prize = JsonResponse()
		cur_prize.name = red_envelope_record.prize_name
		cur_prize.detail = red_envelope_record.prize_detail
		cur_prize.prize_level = red_envelope_record.prize_level
		response.data.record_prize = cur_prize
	else:
		relations = RedEnvelopeHasPrize.objects.filter(red_envelope=red_envelope)
		prize_ids = [r.prize_id for r in relations]
		prizes = Prize.objects.filter(id__in=prize_ids)
		prizes_count = 0
		for prize in prizes:
			prizes_count = prize.count + prizes_count
			
		webapp_id = red_envelope.owner.get_profile().webapp_id
		sample_space_size = prizes_count
		# prize = draw_lottery(prizes, webapp_id, sample_space_size=sample_space_size)
		prize = draw_lottery_new(prizes, webapp_id)
		
		red_envelope_record = __record_prize(webapp_user, red_envelope, prize, member)

		cur_prize = JsonResponse()
		cur_prize.name = red_envelope_record.prize_name
		cur_prize.detail = red_envelope_record.prize_detail
		cur_prize.prize_level = red_envelope_record.prize_level
		response.data.record_prize = cur_prize
	# cur_member = JsonResponse()
	# cur_member.integral = webapp_user.integral_info['count']
	# response.data.member = cur_member

	return response.get_response()


########################################################################
# __record_prize: 记录抽奖历史内部操作
########################################################################
def __record_prize(webapp_user, red_envelope, prize, member, prize_position=0):
	prize_money = 0
	webapp_user_id = -1
	if webapp_user:
		webapp_user_id = webapp_user.id
	if not prize:
		return RedEnvelopeRecord.objects.create(owner=red_envelope.owner, red_envelope=red_envelope, red_envelope_name=red_envelope.name, prize_type=-1, prize_level=0,
			prize_name=u'红包领光了，您来晚了！', prize_number=time.time(), prize_detail='', prize_money=prize_money, webapp_user_id=webapp_user_id)
	
	relation = RedEnvelopeHasPrize.objects.get(red_envelope=red_envelope, prize=prize)
	
	if member is None and relation.prize_type != 1:
		return RedEnvelopeRecord.objects.create(owner=red_envelope.owner, red_envelope=red_envelope, red_envelope_name=red_envelope.name, prize_type=-1, prize_level=0,
			prize_name=u'谢谢参与', prize_number=time.time(), prize_detail='', prize_money=prize_money, webapp_user_id=webapp_user_id)

	#实物
	if relation.prize_type == 0:
		is_awarded = False
		prize_detail = relation.prize_source
	#优惠券
	elif relation.prize_type == 1:
		is_awarded = True
		rule_id = relation.prize_source
		# coupons = create_coupons(red_envelope.owner, rule_id, 1, member.id)
		# prize_detail = coupons[0].coupon_id
		# prize_money = coupons[0].money
		coupon, msg = consume_coupon(red_envelope.owner.id, rule_id, member.id)
		if coupon:
			prize_detail = coupon.coupon_id
			prize_money = coupon.money
		else:
			watchdog_notice('红包领取失败，错误原因:%s,owner.id:%s:rule.id:%s,member.id:%s' 
				% (msg, red_envelope.owner.id, rule_id, member.id), type="mall")
			return RedEnvelopeRecord.objects.create(owner=red_envelope.owner, red_envelope=red_envelope, red_envelope_name=red_envelope.name, prize_type=-1, prize_level=0,
			prize_name=u'谢谢参与', prize_number=time.time(), prize_detail='', prize_money=prize_money, webapp_user_id=webapp_user_id)
	#兑换码
	elif relation.prize_type == 2:
		is_awarded = True
		prize_detail = relation.prize_source
	#积分
	elif relation.prize_type == 3:
		is_awarded = True
		prize_detail = relation.prize_source
		#增加积分
		webapp_user.consume_integral(-int(prize_detail), u'红包积分')
	
	from hashlib import md5
	cur_time = str(time.time())
	prize_number = md5(cur_time).hexdigest()[10:-10] #生成一个12位字符串
		
	red_envelope_record = RedEnvelopeRecord.objects.create(owner=red_envelope.owner, webapp_user_id=webapp_user_id, red_envelope=red_envelope, red_envelope_name=red_envelope.name, prize_type=relation.prize_type, prize_level=prize.level,
			prize_name=prize.name, prize_number=prize_number, prize_detail=prize_detail, prize_money=prize_money, prize_position=prize_position, is_awarded=is_awarded)
	
	#更改奖品个数
	Prize.decrease_count(prize, 1)
	
	return red_envelope_record