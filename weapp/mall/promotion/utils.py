# -*- coding: utf-8 -*-
# __author__: zwidny 整理
import random
from datetime import datetime
from django.db.models import F

from . import models as promotion_models
from core import search_util


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



def create_coupons(couponRule, count, promotion=None):
    """
    创建未使用的优惠券
    """
    i = 0
    if not promotion:
        promotion = promotion_models.Promotion.objects.filter(type=promotion_models.PROMOTION_TYPE_COUPON, detail_id=couponRule.id)[0]

    a = couponRule.owner.id
    b = couponRule.id

    # 创建未使用的优惠券
    current_coupon_ids = [coupon.coupon_id for coupon in promotion_models.Coupon.objects.filter(coupon_rule_id=b)]
    new_coupons = []
    while i < count:
        # 生成优惠券ID
        coupon_id = coupon_id_maker(a, b)
        while coupon_id in current_coupon_ids:
            coupon_id = coupon_id_maker(a, b)
        current_coupon_ids.append(coupon_id)
        new_coupons.append(promotion_models.Coupon(
                owner=couponRule.owner,
                coupon_id=coupon_id,
                provided_time=promotion.start_date,
                start_time=promotion.start_date,
                expired_time=promotion.end_date,
                money=couponRule.money,
                coupon_rule_id=couponRule.id,
                is_manual_generated=False,
                status=promotion_models.COUPON_STATUS_UNGOT
        ))
        i += 1
    promotion_models.Coupon.objects.bulk_create(new_coupons)


PROMOTION_FILTERS = {
    'promotion': [
        {
            'comparator': lambda promotion, filter_value: (filter_value == 'all') or (promotion_models.PROMOTION2TYPE[promotion.type]['name'] == filter_value),
            'query_string_field': 'promotionType'
        }, {
            'comparator': lambda promotion, filter_value: (int(filter_value) == -1) or (int(filter_value) == promotion.status),
            'query_string_field': 'promotionStatus'
        }, {
            'comparator': lambda promotion, filter_value: filter_value <= promotion.start_date.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'startDate'
        }, {
            'comparator': lambda promotion, filter_value: filter_value >= promotion.end_date.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'endDate'
        }
    ],
    'coupon': [{
            'comparator': lambda promotion, filter_value: filter_value in promotion.name,
            'query_string_field': 'name'
        }, {
            'comparator': lambda promotion, filter_value: filter_value in promotion.name,
            'query_string_field': 'coupon_type'
        }, {
            'comparator': lambda promotion, filter_value: (int(filter_value) == -1) or (int(filter_value) == promotion.status),
            'query_string_field': 'promotionStatus'
        }, {
            'comparator': lambda promotion, filter_value: filter_value <= promotion.start_date.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'startDate'
        }, {
            'comparator': lambda promotion, filter_value: filter_value >= promotion.end_date.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'endDate'
        }
    ],
    'product': [{
            'comparator': lambda product, filter_value: filter_value in product.name,
            'query_string_field': 'name'
        }, {
            'comparator': lambda product, filter_value: filter_value == product.bar_code,
            'query_string_field': 'barCode',
        }
    ],
}


def filter_promotions(request, promotions):
    has_filter = search_util.init_filters(request, PROMOTION_FILTERS)
    if not has_filter:
        # 没有filter，直接返回
        return promotions

    filtered_promotions = []
    if request.GET.get('type', 'all') == 'coupon':
        promotions = search_util.filter_objects(
            promotions, PROMOTION_FILTERS['coupon']
        )
        coupon_type = request.GET.get('couponPromotionType', None)
        if coupon_type != '-1':
            coupon_type = coupon_type == '2'
            promotion_models.Promotion.fill_details(
                request.manager,
                promotions,
                {'with_concrete_promotion': True})
            promotions = [promotion for promotion in promotions if promotion.detail['limit_product'] == coupon_type]
        return promotions
        #过滤promotion集合
    promotions = search_util.filter_objects(
        promotions, PROMOTION_FILTERS['promotion']
    )
    promotion_models.Promotion.fill_details(
        request.manager,
        promotions,
        {'with_product': True})

    if not promotions:
        return filtered_promotions

    for promotion in promotions:
        products = search_util.filter_objects(
            promotion.products, PROMOTION_FILTERS['product']
        )
        if products:
            filtered_promotions.append(promotion)
    return filtered_promotions