# -*- coding: utf-8 -*-
from __future__ import absolute_import
from mall.promotion import models as promotion_models


def get_vip_discount(request):
    """得到会员折扣

    Return:
      discount(float): 如果请求用户是会员返回对应折扣， 否则返回1.00

    # Todo
      请求支持, cache
    """
    grade_id = request.member.grade_id
    member_grade = filter(lambda x: x.id == grade_id,
                          request.webapp_owner_info.member_grades)
    return (member_grade[0].shop_discount / 100.00)


def get_user_member_grade_id(request):
    """得到用户会员等级
    Return:
      int - 如果用户是会员， 将返回对应的会员级别ID，
      None - 如果用户不是会员
    """
    member_grade_id = None
    if hasattr(request, 'member') and request.member:
        member_grade_id = request.member.grade_id
    return member_grade_id


def get_processed_products(request, products):
    """按需求处理商品

    Return:
      products

    """
    # 得到商品的会员价
    discount = get_vip_discount(request)
    member_grade_id = get_user_member_grade_id(request)
    new_products = []
    for p in products:
        new_products.append(get_display_price(discount, member_grade_id, p))
    return new_products


def get_processed_product(request, product):
    """按需求处理商品

    Return:
      product
    """
    # 得到商品的会员价
    discount = get_vip_discount(request)
    product.price_info['vip_price'] = product.price_info['display_price'] * discount
    return product


def has_promotion(user_member_grade_id=None, promotion_member_grade_id=0):
    """判断促销是否对用户开放.

    Args:
      user_member_grade_id(int): 用户会员等价
      promotion_member_grade_id(int): 促销制定的会员等级

    Return:
      True - if 促销对用户开放
      False - if 促销不对用户开放
    """
    if promotion_member_grade_id == 0:
        return True
    elif promotion_member_grade_id == user_member_grade_id:
        return True
    else:
        return False


def get_display_price(discount, member_grade_id, product):
    """商品促销类型，更新商品价格

    Return:
      product
    """
    # 如果用户不是会员
    if member_grade_id is None:
        return product
    # 如果用户是会员
    else:
        # 商品参加促销
        if hasattr(product, 'promotion') and product.promotion:
            promotion_type = int(product.promotion.get('type'))
            # 限时抢购
            if promotion_type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
                # user是否满足限时抢购条件
                if has_promotion(member_grade_id, int(product.promotion['member_grade_id'])):
                    product.display_price = product.promotion['detail']['promotion_price']
                    return product
            # 买赠
            elif promotion_type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
                if has_promotion(member_grade_id, int(product.promotion['member_grade_id'])):
                    return product
            # 满减
            elif promotion_type == promotion_models.PROMOTION_TYPE_PRICE_CUT:
                pass
            # 优惠券
            elif promotion_type == promotion_models.PROMOTION_TYPE_COUPON:
                pass
            # 积分抵扣
            elif promotion_type == promotion_models.PROMOTION_TYPE_INTEGRAL_SALE:
                if has_promotion(member_grade_id, int(product.integral_sale['member_grade_id'])):
                    return product
        # 商品是否参加会员折扣
        if product.is_member_product:
            product.display_price = product.display_price * discount
            return product
        else:
            return product
