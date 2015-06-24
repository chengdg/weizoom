# -*- coding: utf-8 -*-
# __author__: zwidny 整理
import random
from datetime import datetime
from django.db.models import F

from . import models as promotion_models


def get_coupon_rules(owner):
    """
    获取优惠券列表
    多个营销工具使用
    """
    rules = list(promotion_models.CouponRule.objects.filter(
                                    owner=owner,
                                    is_active=True,
                                    end_date__gt=datetime.now()
                                    ).order_by('-id'))
    return rules


def consume_coupon(owner_id, rule_id, member_id, coupon_record_id=0):
    """
    领用优惠券
    """
    rules = promotion_models.CouponRule.objects.filter(
                                                       id=rule_id,
                                                       owner_id=owner_id)
    if len(rules) != 1:
        return None, u'该优惠券使用期已过，不能领取！'
    coupon_count = promotion_models.Coupon.objects.filter(
                                            coupon_rule_id=rule_id,
                                            member_id=member_id).count()

    if coupon_count >= rules[0].limit_counts and rules[0].limit_counts > 0:
        return None, u'该优惠券每人限领%s张，你已经领取过了！' % rules[0].limit_counts

    coupons = promotion_models.Coupon.objects.filter(
                        coupon_rule_id=rule_id,
                        member_id=0,
                        status=promotion_models.COUPON_STATUS_UNGOT)[:1]

    if len(coupons) == 1:

        promotion_models.Coupon.objects.filter(id=coupons[0].id).update(
                status=promotion_models.COUPON_STATUS_UNUSED,
                member_id=member_id,
                provided_time=datetime.today(),
                coupon_record_id=coupon_record_id
            )
        if coupon_count:
            rules.update(remained_count=F('remained_count')-1,
                         get_count=F('get_count')+1)
        else:
            rules.update(remained_count=F('remained_count')-1,
                         get_person_count=F('get_person_count')+1,
                         get_count=F('get_count')+1)
        return coupons[0], ''
    else:
        return None, u'该优惠券使用期已过，不能领取！'


def award_coupon_for_member(coupon_rule_info, member):
    """
    给会员发奖
    """
    rule = promotion_models.CouponRule.objects.get(id=coupon_rule_info.id)
    consume_coupon(rule.owner, rule.id, member.id)


def coupon_id_maker(a, b):
    random_args_value = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    return '%03d%04d%s' % (a, b, ''.join(random.sample(random_args_value, 6)))
