# -*- coding: utf-8 -*-
from __future__ import absolute_import
from mall.promotion import models as promotion_model


def get_vip_discount(request):
    """得到会员折扣

    Return:
      discount(float): 如果请求用户是会员返回对应折扣， 否则返回1.00

    # Todo
      请求支持, cache
    """
    if hasattr(request, 'member'):
        return request.member.discount
    else:
        return 1.00


def get_processed_products(request, products):
    """按需求处理商品

    Return:
      products

    """

    # 得到商品的会员价
    discount = get_vip_discount(request)
    for p in products:
        p.display_price = p.display_price * discount
    return products


def get_processed_product(request, product):
    """按需求处理商品

    Return:
      product
    """
    # 得到商品的会员价
    discount = get_vip_discount(request)
    product.price_info['vip_price'] = product.price_info['display_price'] * discount
    return product


def get_price(discount, product):
    """商品促销类型，更新商品价格
    """
    # 商品参加促销
    if hasattr(product, 'promotion'):
        promotion_type = int(product.promotion.get('type'))
        # 限时抢购
        if promotion_type == promotion_model.PROMOTION_TYPE_FLASH_SALE:
            pass
        # 买赠
        elif promotion_type == promotion_model.PROMOTION_TYPE_PREMIUM_SALE:
            pass
        # 满减
        elif promotion_type == promotion_model.PROMOTION_TYPE_PRICE_CUT:
            pass
        # 优惠券
        elif promotion_type == promotion_model.PROMOTION_TYPE_COUPON:
            pass
        # 积分抵扣
        elif promotion_type == promotion_model.PROMOTION_TYPE_INTEGRAL_SALE:
            pass
    # 商品不参加促销
    else:
        product.price_info['vip_price'] = product.price_info['display_price'] * discount
