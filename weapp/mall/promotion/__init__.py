# -*- coding: utf-8 -*-
from __future__ import absolute_import

from market_tools.prize.module_api import PrizeType, register_prize_type
from .utils import get_coupon_rules, award_coupon_for_member

from . import promotion
from . import integral_sales
from . import price_cut
from . import flash_sales
from . import premium_sale
from . import forbidden_coupon_product

from . import coupon
from . import coupon_rule
from . import red_envelpoe
from . import issuing_coupon
from . import card_exchange
from . import virtual_products

SCORE_PRIZE_TYPE = PrizeType(
                             u'优惠券',
                             get_coupon_rules,
                             award_coupon_for_member
                            )

register_prize_type(SCORE_PRIZE_TYPE)
