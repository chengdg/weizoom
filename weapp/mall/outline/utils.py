# -*- coding: utf-8 -*-
from mall import models as mall_models
from django.db.models import Q


def get_to_be_shipped_order_infos(request):
    """获取待发货订单信息.

    Return json:

    {
        "count": 20,
        "orders_list": [{
            "date": "2015-02-01",
            "items": [order1, order2]
        }, {
            ......
        }]
    }
    """
    webapp_id = request.user_profile.webapp_id
    total_to_be_shipped_order_count = mall_models.Order.objects.belong_to(
        webapp_id
    ).filter(
        # Q(status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP) &
        # ~Q(type='test')
        status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP  #跟订单管理保持一致，不进行type字段的test判断 duhao 20150917
    ).count()
    orders = mall_models.Order.objects.belong_to(
        webapp_id
    ).filter(
        # Q(status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP) &
        # ~Q(type='test')
        status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP  #跟订单管理保持一致，不进行type字段的test判断 duhao 20150917
    ).order_by('-id')[:10]
    order_ids = []
    id2order = {}
    for order in orders:
        order_ids.append(order.id)
        id2order[order.id] = order
        order.product_count = 0

    _order_has_product = mall_models.OrderHasProduct.objects.filter(
        order_id__in=order_ids)
    for relation in _order_has_product:
        id2order[relation.order_id].product_count += relation.number

    date2orders = {}
    for order in orders:
        date = order.created_at.strftime("%Y-%m-%d")
        date2orders.setdefault(date, []).append(order)

    orders_list = []
    for date, orders in date2orders.items():
        orders_list.append({
            "date": date,
            "items": orders
        })
    orders_list.sort(lambda x, y: cmp(y['date'], x['date']))

    return {
        "count": total_to_be_shipped_order_count,
        "orders_list": orders_list
    }
