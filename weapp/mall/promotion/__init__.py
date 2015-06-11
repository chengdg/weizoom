# -*- coding: utf-8 -*-

from market_tools.prize.module_api import PrizeType, register_prize_type
from .utils import get_coupon_rules, award_coupon_for_member
from models import CouponRule

SCORE_PRIZE_TYPE = PrizeType(
                             u'优惠券',
                             get_coupon_rules,
                             award_coupon_for_member
                            )

register_prize_type(SCORE_PRIZE_TYPE)
