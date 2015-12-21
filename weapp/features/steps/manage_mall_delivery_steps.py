#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behave import *

from test import bdd_util
from features.testenv.model_factory import *
import steps_db_util
from mall import module_api as mall_api
from mall.models import Order, OrderOperationLog, Supplier
from tools.express.models import ExpressHasOrderPushStatus


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
    if hasattr(context, 'latest_order_id'):
        latest_order_no = Order.objects.get(id=context.latest_order_id).id
    else:
        latest_order_no = steps_db_util.get_latest_order().id
    print "last----------------------------",latest_order_no
    url = '/mall2/api/delivery/'
    data = {
        'order_id': latest_order_no,
        'express_company_name': 'shentong',
        'express_number': '123456789',
        'leader_name': user,
        'is_update_express': 'false'
    }
    response = context.client.post(url, data)

@when(u'{user}对订单进行发货')
def step_impl(context, user):

    delivery_data = json.loads(context.text)
    order_no = delivery_data['order_no']
    if '-' in order_no:
        order_no_info = order_no.split('-')
        order_no = '%s^%s' % (order_no_info[0], Supplier.objects.get(name = order_no_info[1]).id)
    order_id = Order.objects.get(order_id=order_no).id

    logistics = delivery_data.get('logistics', 'off')
    if logistics == u'其他':
        logistics = delivery_data.get('name')
    leader_name = delivery_data.get('shipper', '')
    express_company_name = ''
    express_number = ''
    is_update_express = ''
    if logistics != 'off':
        express_company_name = logistics
        express_number = delivery_data['number']
        is_update_express = 'false'
    url = '/mall2/api/delivery/'
    data = {
        'order_id': order_id,
        'express_company_name': express_company_name,
        'express_number': express_number,
        'leader_name': leader_name,
        'is_update_express': is_update_express
    }
    if logistics == u'其他':
        data['is_100'] = 'false'
    response = context.client.post(url, data)
    if 'date' in delivery_data:
        OrderOperationLog.objects.filter(order_id=delivery_data['order_no'], action="订单发货").update(
            created_at=bdd_util.get_datetime_str(delivery_data['date']))

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


@when(u"快递100发送物流单号'{express_number}'完成的信息")
def step_impl(context, express_number):
    """
    参考test_analog_push_data（tools/express/views.py）
    """
    express_id = ExpressHasOrderPushStatus.objects.get(express_number=express_number).id

    # domain = 'red.weapp.weizzz.com'

    url = "/tools/api/express/kuaidi/callback/?callbackid=%s&version=2.0" % express_id
    # 快递信息
    param_json = {
        "status": "shutdown",
        "lastResult": {
            "state": "0",
            "ischeck": "0",
            "com": "yuantong",
            "nu": "V030344422",
            "data": [{
                "context": "张三香派送（之前吃了鸭翅膀）",
                "time": "2012-08-30 09:09:36",
                "ftime": "2012-08-30 09:09:36"
            }, {
                "context": "北京烤鸭（五仁味的）到北京",
                "time": "2012-08-29 10:23:04",
                "ftime": "2012-08-29 10:23:04"
            }, {
                "context": "王丽/装件入车扫描（扫掉了鸭锁骨） ",
                "time": "2012-08-28 16:33:19",
                "ftime": "2012-08-28 16:33:19"
            }, {
                "context": "师帅/下车扫描（偷吃了左边的鸭腿）",
                "time": "2012-08-27 23:22:42",
                "ftime": "2012-08-27 23:22:42",
            }, {
                "context": "王新蕊收件北京烤鸭并吃掉了右边的鸭腿",
                "time": "2012-08-27 18:22:42",
                "ftime": "2012-08-27 18:22:42",
            }]
        }
    }
    param_json['lastResult']['state'] = "3"
    param_json['lastResult']['data'].insert(0, {"context": "冯雪静已签收了鸭骨架", "time": "2012-08-30 16:52:02",
                                                "ftime": "2012-08-30 16:52:02"})

    # 将PARAMETERS的json转换为字符串
    param_str = json.dumps(param_json)
    json_data = {
        "param": param_str
    }
    context.client.post(url, json_data)

