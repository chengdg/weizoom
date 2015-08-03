# -*- coding: utf-8 -*-


def get_processed_products(request, products):
    """按需求处理商品

    Return:
      products

    """

    # 得到商品的会员价
    if hasattr(request, 'member'):
        member = request.member
        discount = member.discount
        for p in products:
            p.display_price = p.display_price * discount
        return products
    return products


def get_processed_product(request, product):
    """按需求处理商品

    Return:
      product
    """
    # 得到商品的会员价
    if hasattr(request, 'member'):
        member = request.member
        discount = member.discount
        product.price_info['vip_price'] = product.price_info['display_price'] * discount
        return product
    return product

