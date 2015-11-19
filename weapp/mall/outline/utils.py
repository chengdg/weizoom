# -*- coding: utf-8 -*-
from django.db.models import Q

from mall import models as mall_models
from core.charts_apis import create_line_chart_response
from datetime import timedelta, datetime
from core import dateutil


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


def get_purchase_trend(webapp_id, low_date, high_date):
    """
    购买趋势折线图
    从outline.py中迁移而来，为了便于供wapi中调用
    duhao 20151026
    """
    date_fmt = "%Y-%m-%d"
    today = dateutil.get_today()
    if (not low_date) or (not high_date):
        high_date = datetime.strptime(today, date_fmt).date()
        low_date = datetime.strptime(dateutil.get_previous_date('today', 6), date_fmt).date()

    if type(low_date) == unicode:
        low_date = datetime.strptime(low_date, date_fmt).date()
    if type(high_date) == unicode:
        high_date = datetime.strptime(high_date, date_fmt).date()

    date_list = [date.strftime(date_fmt) for date in dateutil.get_date_range_list(low_date, high_date)]
    #当最后一天是今天时，折线图中不显示最后一天的数据 duhao 2015-09-17
    #当起止日期都是今天时，数据正常显示
    
    if len(date_list) > 1 and date_list[-1] == today:
        del date_list[-1]

    date2count = dict()
    date2price = dict()

    # 11.20从查询mall_purchase_daily_statistics变更为直接统计订单表，解决mall_purchase_daily_statistics遗漏统计订单与统计时间不一样导致的统计结果不同的问题。
    orders = mall_models.Order.objects.belong_to(webapp_id).filter(
        created_at__range=(low_date, (high_date) + timedelta(days=1)))
    statuses = set([mall_models.ORDER_STATUS_PAYED_SUCCESSED, mall_models.ORDER_STATUS_PAYED_NOT_SHIP,
                    mall_models.ORDER_STATUS_PAYED_SHIPED, mall_models.ORDER_STATUS_SUCCESSED])
    # orders = [order for order in orders if (order.type != 'test') and (order.status in statuses)]
    for order in orders:
        if (order.type != 'test') and (order.status in statuses):
            # date = dateutil.normalize_date(order.created_at)
            date = order.created_at.strftime(date_fmt)
            if order.webapp_id != webapp_id:
                order_price = mall_models.Order.get_order_has_price_number(order) + order.postage
            else:
                order_price = order.final_price + order.weizoom_card_money

            if date in date2count:
                old_count = date2count[date]
                date2count[date] = old_count + 1
            else:
                date2count[date] = 1

            if date in date2price:
                old_price = date2price[date]
                date2price[date] = old_price + order_price
            else:
                date2price[date] = order_price

    count_trend_values = []
    price_trend_values = []
    for date in date_list:
        count_trend_values.append(date2count.get(date, 0))
        price_trend_values.append(round(date2price.get(date, 0.0), 2))
    result = create_line_chart_response(
        '',
        '',
        date_list,
        [{
            "name": "销售额",
            "values": price_trend_values
        }, {
            "name": "订单数",
            "values": count_trend_values
        }],
        use_double_y_lable = True,
        get_json = True
    )
    result['yAxis'][0]['name'] = '销售额'
    result['yAxis'][1]['name'] = '订单数'
    result['yAxis'][1]['splitLine'] = {'show':False}

    return result