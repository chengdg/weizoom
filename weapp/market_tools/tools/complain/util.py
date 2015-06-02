# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group, Permission
from django.db.models import F

import time

from market_tools.prize.models import Prize
from market_tools.tools.coupon import util as coupon_util

from watchdog.utils import watchdog_fatal, watchdog_error

from modules.member.models import Member, MemberGrade, BRING_NEW_CUSTOMER_VIA_QRCODE
from models import *

#############################################################################
#get_coupon_rules: 获取优惠券rule
#############################################################################
def get_coupon_rules(owner):
	return coupon_util.get_coupon_rules(owner)


#############################################################################
#get_all_grades_list: 获取会员等级
#############################################################################
def get_all_grades_list(request):
	webapp_id = request.user_profile.webapp_id
	return MemberGrade.get_all_grades_list(webapp_id)
