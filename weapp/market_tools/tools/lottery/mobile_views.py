# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
import time
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response

from core.exceptionutil import unicode_full_stack

from market_tools.prize.models import *
from market_tools.tools.coupon.util import consume_coupon
from mall.promotion.models import CouponRule
from modules.member.util import get_member
from models import *

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
def get_lottery(request):
	lottery_id = int(request.GET['lottery_id'])
	try:
		member = request.member
	except:
		member = None

	try:
		lottery = Lottery.objects.get(id=lottery_id)
		lottery.check_time()
	except:
		c = RequestContext(request, {
			'is_deleted_data': True,
			'is_hide_weixin_option_menu':False
		})
		return render_to_response('%s/lottery/webapp/%s' % (TEMPLATE_DIR, 'roulette.html'), c)

	relations = LotteryHasPrize.objects.filter(lottery=lottery)
	prize_ids = [r.prize_id for r in relations]
	prizes = Prize.objects.filter(id__in=prize_ids)
	id2prize = dict([(p.id, p) for p in prizes])
	lottery.prizes = []
	for r in relations:
		#added by chuter
		if not id2prize.has_key(r.prize_id):
			continue

		prize = id2prize[r.prize_id]

		prize.prize_type = r.prize_type
		prize.prize_source = r.prize_source
		#如果是优惠券，则显示优惠券的配置名称
		if prize.prize_type == 1:
			coupon_rule = CouponRule.objects.get(id=r.prize_source)
			prize.prize_source = coupon_rule.name
		lottery.prizes.append(prize)
	lottery.prizes = sorted(lottery.prizes, reverse=False, key=lambda p : p.level) #排序奖项

	if lottery.type == SCRATCH_CARD:
		html_name = 'scratch_card.html'
	elif lottery.type == GOLDEN_EGG:
		html_name = 'egg.html'
	elif lottery.type == ROULETTE:
		html_name = 'roulette.html'

	#判断可玩次数
	if lottery.can_repeat:
		today_date_str = time.strftime("%Y-%m-%d")
		records = LotteryRecord.objects.filter(member=member, lottery=lottery, created_at__startswith=today_date_str)
		all_play_count = lottery.daily_play_count
	else:
		records = LotteryRecord.objects.filter(member=member, lottery=lottery)
		all_play_count = 1

	play_count = len(records)

	can_play_count = all_play_count - play_count

	if can_play_count < 0:
		can_play_count = 0

	#判断积分
	if not member or member.integral < lottery.expend_integral:
		can_play_count = 0

	#获取上次中奖
	records = LotteryRecord.objects.filter(member=member, lottery=lottery, prize_level__gt=0)
	if records:
		last_record = records[0]
	else:
		last_record = None

	#定义奖项：
	# if lottery.can_repeat:
	# 	play_times = lottery.daily_play_count
	# else:
	# 	play_times = 1

	#根据发奖规则发奖
	# cur_prize = _get_prize(lottery, member, prizes)

	c = RequestContext(request, {
		'page_title': lottery.name,
		'lottery': lottery,
		# 'cur_prize': cur_prize,
		'member': member,
		'can_play_count': can_play_count,
		'records': records,
		'last_record': last_record,
		'type': lottery.status,
		'is_hide_weixin_option_menu':False
	})

	return render_to_response('%s/lottery/webapp/%s' % (TEMPLATE_DIR, html_name), c)

def _get_prize(lottery, member, prizes):
	prize = None
	webapp_id = lottery.owner.get_profile().webapp_id
	sample_space_size = lottery.expected_participation_count
	# if lottery.award_type == ONCE_A_LOTTERY:
	# 	prize_records = LotteryRecord.objects.filter(member=member, lottery=lottery, prize_level__gt=0)
	# 	if prize_records:
	# 		prize = None
	# 	else:
	# 		prize = draw_lottery(prizes, webapp_id, sample_space_size=sample_space_size)
	# elif lottery.award_type == ONCE_A_DAY:
	# 	today = time.strftime('%Y-%m-%d')
	# 	prize_records = LotteryRecord.objects.filter(member=member, lottery=lottery, prize_level__gt=0, created_at__gt=today)
	# 	if prize_records:
	# 		prize = None
	# 	else:
	# 		prize = draw_lottery(prizes, webapp_id, sample_space_size=sample_space_size)
	# elif lottery.award_type == HOURLY:
	# 	now = datetime.today()
	# 	earlier = now - timedelta(hours=int(lottery.award_hour))
	# 	today = earlier.strftime('%Y-%m-%d %H:%M:%S')
	# 	prize_records = LotteryRecord.objects.filter(member=member, lottery=lottery, prize_level__gt=0, created_at__gt=today)
	# 	if prize_records:
	# 		prize = None
	# 	else:
	# 		prize = draw_lottery(prizes, webapp_id, sample_space_size=sample_space_size)
	# elif lottery.award_type == EVERY_TIME:
	# 	prize = draw_lottery(prizes, webapp_id, sample_space_size=sample_space_size)

	#prize = draw_lottery(prizes, webapp_id, sample_space_size=sample_space_size)

	prize = draw_lottery_new(prizes, webapp_id)
	return prize



def get_usage(request):
	member = get_member(request)
	lottery_records =  Lottery.get_lottery_records(request, member)

	c = RequestContext(request, {
		'page_title': u'我的抽奖',
	    'lottery_records': lottery_records,
	    'is_hide_weixin_option_menu':False
	})

	return render_to_response('%s/lottery/webapp/lotteries.html' % TEMPLATE_DIR, c)

########################################################################
# record_prize: 记录抽奖历史
# ########################################################################
# def record_prize(webapp_user,lottery_id,prize_id,member):
# 	prize_position = 0

# 	if not member:
# 		raise Http404(u"会员信息不存在")

# 	lottery = Lottery.objects.get(id=lottery_id)
# 	if prize_id:
# 		prize = Prize.objects.get(id=prize_id)
# 	else:
# 		prize = None
# 	__record_prize(webapp_user, lottery, member, prize, prize_position)

# ########################################################################
# # __record_prize: 记录抽奖历史内部操作
# ########################################################################
# def __record_prize(webapp_user, lottery, member, prize, prize_position=0):
# 	prize_money = 0

# 	#减积分
# 	if lottery.expend_integral > 0:
# 		webapp_user.consume_integral(lottery.expend_integral, u'参与抽奖，花费积分')

# 	if not prize:
# 		LotteryRecord.objects.create(owner=lottery.owner, member=member, lottery=lottery, lottery_name=lottery.name, prize_type=0, prize_level=0,
# 			prize_name=u'谢谢参与', is_awarded=True, prize_number=time.time(), prize_detail='', prize_money=prize_money)

# 		return None

# 	relation = LotteryHasPrize.objects.get(lottery=lottery, prize=prize)

# 	#实物
# 	if relation.prize_type == 0:
# 		is_awarded = False
# 		prize_detail = relation.prize_source
# 	#优惠券
# 	elif relation.prize_type == 1:
# 		is_awarded = True
# 		rule_id = relation.prize_source
# 		# coupons = create_coupons(lottery.owner, rule_id, 1, member.id)
# 		# prize_detail = coupons[0].coupon_id
# 		# prize_money = coupons[0].money
# 		coupon, msg = consume_coupon(lottery.owner.id, rule_id, member.id)
# 		if coupon:
# 			prize_detail = coupon.coupon_id
# 			prize_money = coupon.money
# 		else:
# 			watchdog_notice('微信抽奖失败，错误原因:%s,owner.id:%s:rule.id:%s,member.id' 
# 				% (msg, lottery.owner.id, rule_id, member.id))
# 			LotteryRecord.objects.create(owner=lottery.owner, member=member, lottery=lottery, lottery_name=lottery.name, prize_type=0, prize_level=0,
# 			prize_name=u'谢谢参与', is_awarded=True, prize_number=time.time(), prize_detail='', prize_money=prize_money)
# 			return None
# 	#兑换码
# 	elif relation.prize_type == 2:
# 		is_awarded = True
# 		prize_detail = relation.prize_source
# 	#积分
# 	elif relation.prize_type == 3:
# 		is_awarded = True
# 		prize_detail = relation.prize_source
# 		#增加积分
# 		webapp_user.consume_integral(-int(prize_detail), u'参与抽奖，赢得积分')

# 	from hashlib import md5
# 	cur_time = str(time.time())
# 	prize_number = md5(cur_time).hexdigest()[10:-10] #生成一个12位字符串

# 	LotteryRecord.objects.create(owner=lottery.owner, member=member, lottery=lottery, lottery_name=lottery.name, prize_type=relation.prize_type, prize_level=prize.level,
# 			prize_name=prize.name, is_awarded=is_awarded, prize_number=prize_number, prize_detail=prize_detail, prize_money=prize_money, prize_position=prize_position)

# 	#更改奖品个数
# 	Prize.decrease_count(prize, 1)

# 	return None