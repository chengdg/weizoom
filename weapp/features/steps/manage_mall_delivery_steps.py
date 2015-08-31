#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behave import *

from test import bdd_util
from features.testenv.model_factory import *
import steps_db_util
from mall import module_api as mall_api
from mall.models import Order


def _handle_fahuo_data(orders):
    data = []
    for order in orders:
        item = dict()
        item['order_id'] = order['order_no']
        item['express_company_name'] = order['logistics']
        item['express_number'] = order['number']
        data.append(item)

    return data


@When(u"{user}对最新订单进行发货")
def step_impl(context, user):
    # TODO 废弃这个方法，改用 @when(u'{user}对订单进行发货')
    url = '/mall2/api/delivery/'
    data = {
        'order_id': context.latest_order_id,
        'express_company_name': 'shentong',
        'express_number': '123456789',
        'leader_name': user,
        'is_update_express': 'false'
    }
    response = context.client.post(url, data)

@when(u'{user}对订单进行发货')
def step_impl(context, user):
    delivery_data = json.loads(context.text)
    order_id = delivery_data['order_no']

    url = '/mall2/api/order_list/'
    query_params = {
        'query': order_id
    }
    response = context.client.get(url, query_params)
    content = json.loads(response.content)
    items = content['data']['items']
    order = {}
    if len(items) > 0:
        order = items[0]

    delivery_data = json.loads(context.text)
    order_id = delivery_data['order_no']
    logistics = delivery_data['logistics']
    leader_name = delivery_data['shipper']
    express_company_name = ''
    express_number = ''
    is_update_express = ''
    if logistics != 'off':
        express_company_name = logistics
        express_number = delivery_data['number']
        is_update_express = 'false'
    url = '/mall2/api/delivery/'
    data = {
        'order_id': order['id'],
        'express_company_name': express_company_name,
        'express_number': express_number,
        'leader_name': leader_name,
        'is_update_express': is_update_express
    }
    response = context.client.post(url, data)

# 批量发货
@When(u"{user}填写订单信息")
def step_impl(context, user):
    orders = json.loads(context.text)
    orders = _handle_fahuo_data(orders)
    context.result_dict = mall_api.batch_handle_order(orders, context.client.user)


@when(u"{webapp_owner_user}填写发货信息")
def step_fill_delivery(context, webapp_owner_user):
    """
    顺丰速递 must be provided
        {
            'order_no': '2134654646',
            'express_company_name': 'shunfeng',
            'express_number': '13654546684',
            'leader_name': 'bill'
        }
    """
    expected = json.loads(context.text)
    url = '/mall2/api/delivery/'
    order_id = expected[0].get('order_no')
    from mall.models import Order

    order_id = steps_db_util.get_order_by_order_id(order_id).id
    del Order
    the_kwargs = {}
    the_kwargs['order_id'] = order_id
    the_kwargs['express_company_name'] = 'shunfeng' if expected[0].get('顺丰速递') else '0'
    the_kwargs['express_number'] = expected[0].get('number', -1)
    the_kwargs['leader_name'] = expected[0].get('ship_name', -1)
    context.client.post(url, the_kwargs)


@then(u"{user}能获取商铺首页的代发货订单列表")
def step_impl(context, user):
    stock_infos = json.loads(context.text)

    url = '/mall2/outline/'
    response = context.client.get(url)
    actual = response.context['order_info']

    expected = json.loads(context.text)
    for orders in expected['orders_list']:
        orders['date'] = bdd_util.get_date(orders['date']).strftime('%Y-%m-%d')
        for order in orders['items']:
            order['final_price'] = order['order_money']
            del order['order_money']

    bdd_util.assert_dict(expected, actual)


@then(u"{user}获得批量发货提示错误信息")
def step_impl(context, user):
    expected = []
    for result in context.table:
        result = result.as_dict()
        expected.append(result)
    actual = context.result_dict[1]
    for info in actual:
        info['order_no'] = info['order_id']
        info['logistics'] = info['express_company_name']
        info['number'] = info['express_number']
        info['failure_reasons'] = info['error_info']

    bdd_util.assert_list(expected, actual)
