# -*- coding: utf-8 -*-

__author__ = 'bert'

import os
import random
import time
from datetime import datetime
from decimal import Decimal

from django.db import connection, transaction
from django.conf import settings
from core.jsonresponse import create_response, JsonResponse

from core.exceptionutil import unicode_full_stack

from modules.member import util as member_util
from modules.member.models import *
from modules.member.util import get_member
from models import *
from watchdog.utils import watchdog_fatal, watchdog_error
import tasks

def to_decimal(s, precision=8):
	'''
	to_decimal('1.2345', 2) => Decimal('1.23')
	to_decimal(1.2345, 2) => Decimal('1.23')
	to_decimal(Decimal('1.2345'), 2) => Decimal('1.23')
	'''
	r = pow(10, precision)
	v = s if type(s) is Decimal else Decimal(str(s))
	try:
		return Decimal(int(v * r)) / r
	except:
		return Decimal(s)

# ########################################################################
# # record_prize: 记录中奖历史
# ########################################################################
def record_prize(request):
	member_id = request.GET.get('member_id', None)
	request_member = request.member
	response = create_response(200)
	error_msg = ''
	send_price = 0
	play_count = 0
	#try:
	# if member_id is None:
	# 	opid = request.GET.get('oid', None)
	# 	member_id = MemberHasSocialAccount.objects.filter(account__openid=opid)[0].member.id
	member = Member.objects.get(id=request_member.id)
	# except:
	# 	member = None

	# if member and member.id != request_member.id:
	# 	member = None

	if member and member.is_subscribed:
		detail_id = int(request.GET.get('shake_detail_id', 0))
		if detail_id != 0:
			now = datetime.now()
			#try:
			member_play_count = ShakeRecord.objects.filter(member=member, shake_detail_id=detail_id).count()
			now_join_count = ShakeRecord.objects.filter(shake_detail_id=detail_id).count()
			max_price_member = False
			if now_join_count >= 30:
				max_price_member = (0 == now_join_count%30)
			with transaction.atomic():
				shake_detail = ShakeDetail.objects.select_for_update().get(id=detail_id)
				if shake_detail.shake.is_deleted == False and shake_detail.start_at <= now and shake_detail.end_at >= now:
					if shake_detail.residue_price > 10:
						if  member_play_count >= shake_detail.play_count:
							error_msg = u'您已经参加过本次摇一摇活动'
						else:
							if shake_detail.residue_price <= shake_detail.fixed_price or shake_detail.residue_price <= shake_detail.random_price_end:
								send_price = random.uniform(1, float(shake_detail.residue_price))
								
							elif max_price_member and shake_detail.fixed_price_residue_number > 0:# and shake_detail.residue_price > shake_detail.fixed_price:
								send_price = shake_detail.fixed_price
								max_price_member = False
							else:
								send_price = random.uniform(float(shake_detail.random_price_start), float(shake_detail.random_price_end))
								max_price_member = False
							if send_price > 0 and send_price < shake_detail.residue_price:
								send_price = to_decimal(send_price, 2)
								shake_detail.residue_price -= send_price
								if max_price_member:
									shake_detail.fixed_price_residue_number -= 1
									assert shake_detail.fixed_price_residue_number >= 0
									shake_detail.save(update_fields=['residue_price', 'fixed_price_residue_number'])
								else:
									shake_detail.save(update_fields=['residue_price'])

								record = ShakeRecord.objects.create(owner_id=request.webapp_owner_id, shake_detail=shake_detail, member=member, money=send_price)
								play_count = shake_detail.play_count - now_join_count - 1
				
								try:
									ip = request.META['REMOTE_ADDR']
								except:
									ip = None
								
								tasks.send_red_pack_task.delay(shake_detail.id, request.webapp_owner_id, member.id, record.id, ip)
							else:
								error_msg = shake_detail.shake.not_winning_desc
					else:
						error_msg = u'本次活动红包已经发送完毕'
				else:
					error_msg = u'活动已经结束'
			# except:
			# 	error_msg = u'活动不存在'
	else:
		error_msg = u"请先关注公众号"

	result = JsonResponse()
	result.error_msg =error_msg
	result.send_price = float(send_price)
	result.play_count = play_count
	response.data.result = result
	return response.get_response()
