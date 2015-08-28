# -*- coding: utf-8 -*-

from behave import when, then, given

from test import bdd_util
from mall.models import (ORDER_TYPE2TEXT, STATUS2TEXT, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED, express_util,
                         ORDERSTATUS2TEXT)
from features.testenv.model_factory import timedelta, json, ORDER_STATUS_NOT
from mall.promotion.models import datetime
import steps_db_util

###############################
# when steps
###############################

@when(u"{user}'{action}'最新订单")
def step_impl(context, user, action):
    if hasattr(context, 'latest_order_id'):
        latest_order_id = context.latest_order_id
    else:
        latest_order_id = steps_db_util.get_latest_order().id
    data = {
        "order_id": latest_order_id
    }
    url = '/mall2/api/order/'
    if action == u"支付":
        data["action"] = "pay"
    elif action == u"完成":
        data["action"] = "finish"
    elif action == u"退款":
        data["action"] = "return_pay"
    elif action == u"完成退款":
        data["action"] = "return_success"
    elif action == u"取消":
        data["action"] = "cancel"
        try:
            if hasattr(context, 'caller_step_cancel_reason'):
                tmp_data = context.caller_step_cancel_reason
            else:
                tmp_data = json.loads(context.text)
            data['reason'] = tmp_data['reason']
        except:
            pass
    response = context.client.post(url, data)


@when(u"{user}修改订单'{order_code}'的价格")
def step_impl(context, user, order_code):
    url = '/mall2/api/order/'
    post_data = json.loads(context.text)
    order_real_id = bdd_util.get_order_by_order_no(order_code).id
    post_data['order_id'] = order_real_id
    context.client.post(url, post_data)


@when(u"{user}'支付'订单'{order_code}'")
def step_impl(context, user, order_code):
    context.latest_order_id = bdd_util.get_order_by_order_no(order_code).id
    context.execute_steps(u"when %s'支付'最新订单" % user)

# @when(u'{user}对最新订单进行退款')
# def step_impl(context, user):
#     context.execute_steps(u'when %s"退款"最新订单' % user)


# @when(u'{user}完成最新订单退款')
# def step_impl(context, user):
#     context.execute_steps(u'when %s"完成退款"最新订单' % user)
######

# 缺失对应feature
# @when(u"{user}设置未付款订单过期时间")
# def step_impl(context, user):
# config = json.loads(context.text)
# no_payment_order_expire_day = config['no_payment_order_expire_day'][:-1]
# from mall.models import MallConfig
#
# MallConfig.objects.filter(owner=context.client.user).update(order_expired_day=no_payment_order_expire_day)


@when(u"{user}通过后台管理系统对'{order_id}'的物流信息进行修改")
def step_impl(context, user, order_id):
    order = json.loads(context.text)
    express_value = express_util.get_value_by_name(order['logistics'])
    data_order_id = steps_db_util.get_order_by_order_id(order['order_no']).id
    url = '/mall2/api/delivery/'
    data = {
        'order_id': data_order_id,
        'express_company_name': express_value,
        'express_number': order['number'],
        'leader_name': 'aa',
        'is_update_express': 'true'
    }
    response = context.client.post(url, data)


###############################
# when steps
###############################

###############################
# then steps
###############################

@then(u"{user}后端订单状态改变为")
def step_impl(context, user):
    # if hasattr(context, 'client'):
    #     context.client.logout()

    # context.client = bdd_util.login(user)
    profile = context.client.user.profile
    webapp_id = context.client.user.profile.webapp_id

    expected = json.loads(context.text)

    order_id = steps_db_util.get_order_by_order_id(expected['order_no']).id
    response = context.client.get('/mall2/order/?order_id=%d' % order_id)

    order = response.context['order']
    actual_order = dict()
    actual_order['order_no'] = order.order_id
    actual_order['status'] = ORDERSTATUS2TEXT[order.status]

    bdd_util.assert_dict(expected, actual_order)


# @then(u"{user}通过后台管理系统可以看到配送套餐订单列表")
# def step_impl(context, user):
#     if hasattr(context, 'client'):
#         context.client.logout()
#     context.client = bdd_util.login(user)
#     client = context.client
#     response = context.client.get('/mall2/api/order_list/get/?version=1&sort_attr=-created_at&count_per_page=15&page=1')
#     items = json.loads(response.content)['data']['items']

#     actual_orders = []
#     for order_item in items:
#         actural_order = {}
#         actural_order['status'] = order_item['status']
#         actural_order['price'] = order_item['total_price']
#         actural_order['buyer'] = order_item['buyer_name']

#         order_id = order_item['id']
#         buy_product_response = context.client.get(
#             '/mall2/api/order_product/?version=1&order_id=%d&timestamp=1406172500320' % (order_id))
#         buy_products = json.loads(buy_product_response.content)['data']['products']
#         buy_product_results = []
#         for buy_product in buy_products:
#             buy_product_result = {}
#             buy_product_result['product_name'] = buy_product['name']
#             buy_product_result['count'] = buy_product['count']
#             buy_product_result['total_price'] = buy_product['total_price']
#             buy_product_results.append(buy_product_result)

#         actural_order['products'] = buy_product_results
#         actual_orders.append(actural_order)

#         # 配置当前日期
#     now = datetime.now()
#     context.current_date = now.strftime('%Y-%m-%d')

#     expected = json.loads(context.text)

#     bdd_util.assert_list(expected, actual_orders)


# @then(u"{user}获取对应的订单")
# def step_impl(context, user):
#     # url = '/mall2/api/order_list/?sort_attr=-created_at&count_per_page=15&page=1'
#     # response = context.client.get(bdd_util.nginx(url))
#     response = context.response
#     content = json.loads(response.content)
#     items = content['data']['items']
#     # query_params = content['data']['pageinfo'].get('query_string')
#     # context.query_params = query_params

#     actual_orders = __get_actual_orders(items, context)
#     expected_order = json.loads(context.text)
#     bdd_util.assert_list(expected_order, actual_orders)


@then(u"{user}可以看到订单列表")
def step_impl(context, user):
    if user != context.client.user.username:
        context.client.logout()
        context.client = bdd_util.login(user)
    # client = context.client
    query_params = dict()
    if hasattr(context, 'query_params'):
        query_params = context.query_params
    response = context.client.get('/mall2/api/order_list/', query_params)
    items = json.loads(response.content)['data']['items']

    actual_orders = []
    source = {'mine_mall': u'本店', 'weizoom_mall': u'商城'}
    for order_item in items:
        actural_order = {}
        actural_order['order_no'] = order_item['order_id']
        actural_order['order_time'] = order_item['created_at']
        actural_order['ship_name'] = order_item['ship_name']
        actural_order['ship_tel'] = order_item['ship_tel']
        actural_order["sources"] = source[order_item['come']]
        actural_order["member"] = order_item['buyer_name']
        actural_order["methods_of_payment"] = order_item['pay_interface_name']
        actural_order["logistics"] = express_util.get_name_by_value(order_item['express_company_name'])
        actural_order["number"] = order_item['express_number']
        actural_order["shipper"] = order_item['leader_name']

        actural_order['status'] = order_item['status']
        actural_order['price'] = order_item['pay_money']
        actural_order['customer_message'] = order_item['customer_message']
        actural_order['buyer'] = order_item['buyer_name']

        order_id = order_item['id']
        buy_product_response = context.client.get(
            '/mall2/api/order_product/?version=1&order_id=%d&timestamp=1406172500320' % (order_id))

        buy_products = json.loads(buy_product_response.content)['data']['products']
        actural_order['products_count'] = len(buy_products)
        buy_product_results = []
        for buy_product in buy_products:
            buy_product_result = {}
            buy_product_result['product_name'] = buy_product['name']
            buy_product_result['count'] = buy_product['count']
            buy_product_result['total_price'] = buy_product['total_price']
            buy_product_result['img_url'] = buy_product['thumbnails_url']
            buy_product_results.append(buy_product_result)

        actural_order['products'] = buy_product_results
        actual_orders.append(actural_order)

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual_orders)


@then(u"{user}可以获得最新订单详情")
def step_impl(context, user):
    order = steps_db_util.get_latest_order()
    context.latest_order_id = order.id
    # client = context.client
    response = context.client.get('/mall2/order/?order_id=%d' % context.latest_order_id)

    order = response.context['order']
    order.order_type = ORDER_TYPE2TEXT[order.type]
    order.total_price = float(order.final_price)
    order.ship_area = order.area + ' ' + order.ship_address
    from mall.templatetags import mall_filter

    actions = mall_filter.get_order_actions(order)
    order.actions = dict([(action['name'], 1) for action in actions])
    if order.status == ORDER_STATUS_PAYED_SHIPED or order.status == ORDER_STATUS_SUCCESSED:
        order.actions[u'修改物流'] = 1
    if order.status == ORDER_STATUS_NOT:
        order.actions[u'修改价格'] = 1
    for product in order.products:
        product['total_price'] = float(product['total_price'])
    order.status = STATUS2TEXT[order.status]
    for product in order.products:
        if 'custom_model_properties' in product and product['custom_model_properties']:
            product['model'] = ' '.join([property['property_value'] for property in product['custom_model_properties']])
    actual = order
    actual.reason = order.reason

    expected = json.loads(context.text)
    actions = expected['actions']
    expected['actions'] = dict([(action, 1) for action in actions])
    bdd_util.assert_dict(expected, actual)


@then(u"{webapp_owner_name}能获取订单")
def step_impl(context, webapp_owner_name):
    db_order = steps_db_util.get_latest_order()
    response = context.client.get('/mall2/order/?order_id=%d' % db_order.id, follow=True)

    order = response.context['order']

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, order)


###############################
# then steps
###############################

###############################
# given steps
###############################

@given(u"{user}已有的订单")
def step_impl(context, user):
    """TODO 弃用 改用 @when(u"{webapp_user_name}购买{webapp_owner_name}的商品")
    """
    if not hasattr(context.client.user, 'profile'):
        context.client.logout()
        context.client = bdd_util.login(user)
    profile = context.client.user.profile
    # webapp_id = context.client.user.profile.webapp_id

    context.orders = json.loads(context.text)
    for order in context.orders:
        steps_db_util.set_order_dict(order, profile)


PAYNAME2ID = {
    u'全部': -1,
    u'微信支付': 2,
    u'货到付款': 9,
    u'支付宝': 0,
    u'优惠抵扣': 10
}

ORDER_SOURCE2ID = {
    u'全部': -1,
    u'本店': 0,
    u'商城': 1
}

ORDER_STATUS2ID = {
    u'全部': -1,
    u'待支付': 0,
    u'已取消': 1,
    u'待发货': 3,
    u'已发货': 4,
    u'已完成': 5,
    u'退款中': 6,
    u'退款成功': 7
}


@when(u'{user}根据给定条件查询订单')
def step_look_for_order(context, user):
    """根据给定条件查询订单

    context: {
        "order_no":          # 订单编号            e.g.:
        "ship_name":         # 收货人姓名          e.g.:
        "ship_tel":          # 收货人电话          e.g.:
        "product_name":      # 商品名称            e.g.:
        "date_interval":     # 下单时间            e.g.:
        "pay_type":          # 支付方式            e.g.:
        "express_number":    # 物流单号            e.g.:
        "order_source":      # 订单来源            e.g.:
        "order_status":      # 订单状态            e.g.:
        "isUseWeizoomCard":  # 仅显示微众卡抵扣订单  e.g.:
    }
    """
    query_params = {
        'pay_type': u'全部',
        'order_source': u'全部',
        'order_status': u'全部',
        'belong': 'all'
    }

    query_params_c = json.loads(context.text)
    query_params.update(query_params_c)
    if query_params.get('order_no'):
        query_params['query'] = query_params['order_no']
        query_params.pop('order_no')

    query_params['pay_type'] = PAYNAME2ID[query_params['pay_type']]
    if query_params['pay_type'] == -1:
        query_params.pop('pay_type')

    query_params['order_source'] = ORDER_SOURCE2ID[query_params['order_source']]
    if query_params['order_source'] == -1:
        query_params.pop('order_source')

    query_params['order_status'] = ORDER_STATUS2ID[query_params['order_status']]
    if query_params['order_status'] == -1:
        query_params.pop('order_status')

    context.query_params = query_params
    # url = '/mall2/api/order_list/'
    # response = context.client.get(url, query_params)
    # context.response = response


@then(u"{user}导出订单获取订单信息")
def step_get_specify_order(context, user):
    """
    """

    filter_value = context.query_params
    from cStringIO import StringIO
    import csv

    if filter_value:
        url = '/mall2/order_export/'
        response = context.client.get(url, filter_value)
        reader = csv.reader(StringIO(response.content))
        # 去掉表头信息
        header = reader.next()
        header = [
            'order_no',
            'order_time',
            'pay_time',
            'product_name',
            'model',
            'product_unit_price',
            'product_count',
            'weigth',
            'methods_of_payment',
            'money_total',
            'money',
            'money_wcard',
            'postage',
            'integral',
            'coupon_money',
            'coupon_name',
            'status',
            'member',
            'ship_name',
            'ship_tel',
            'ship_province',
            'ship_address',
            'shipper',
            'shipper_note',
            'sources',
            'logistics',
            'number',
            'delivery_time'
        ]
        actual = []
        for row in reader:
            item = dict(map(None, header, [str(r).decode('utf8') for r in row]))
            item['ship_address'] = '' if not item.get('ship_address') else item.get('ship_address').replace(' ', ',')
            actual.append(item)
        # remove statistical information
        actual.pop()

        expected_order = json.loads(context.text)
        bdd_util.assert_list(expected_order, actual)
    del StringIO
    del csv


@then(u'{user}能获得订单"{order_id}"')
def step_impl(context, user, order_id):
    order = __get_order(context, order_id)

    response = context.client.get('/mall2/order/?order_id=%d' % order['id'])
    order_obj = response.context['order']

    from mall.templatetags import mall_filter
    actions = mall_filter.get_order_actions(order_obj)
    source = {'mine_mall': u'本店', 'weizoom_mall': u'商城'}
    actual = {
        "order_no": order['order_id'],
        "member": order['buyer_name'],
        "status": order['status'],
        "actions": [action['name'] for action in actions],
        "shipper": order['leader_name'],
        "order_time": order['created_at'],
        "methods_of_payment": order['pay_interface_name'],
        "ship_name": order['ship_name'],
        "ship_tel": order['ship_tel'],
        "sources": source[order['come']]
    }

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)


@when(u'{user}完成订单"{order_id}"')
def step_impl(context, user, order_id):
    order = __get_order(context, order_id)
    data = {
        'order_id': order['id'],
        'action': 'finish'
    }
    response = context.client.post('/mall2/api/order/', data)


def __get_order(context, order_id):
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

    return order


def __get_actual_orders(json_items, context):
    actual_orders = []
    source = {'mine_mall': u'本店', 'weizoom_mall': u'商城'}
    for item in json_items:
        url = '/mall2/order/?order_id={}'.format(item.get('id'))
        response = context.client.get(bdd_util.nginx(url))
        order = response.context['order']
        actual_order = dict()
        actual_order['order_no'] = order.order_id
        actual_order['status'] = ORDERSTATUS2TEXT[order.status]
        if actual_order['status'] == '已发货' or actual_order['status'] == '已完成':
            actual_orders.append({
                'order_no': order.order_id,
                'member': item.get('buyer_name'),
                'status': ORDERSTATUS2TEXT[int(order.status)],
                'order_time': item.get('created_at'),
                'methods_of_payment': item.get('pay_interface_name'),
                'sources': source[item.get('come')],
                'ship_name': item.get('ship_name'),
                'ship_tel': order.ship_tel,
                "logistics": express_util.get_name_by_value(order.express_company_name),
                "number": order.express_number,
                "shipper": ""
            })
        else:
            actual_orders.append({
                'order_no': order.order_id,
                'member': item.get('buyer_name'),
                'status': ORDERSTATUS2TEXT[int(order.status)],
                'order_time': item.get('created_at'),
                'methods_of_payment': item.get('pay_interface_name'),
                'sources': source[item.get('come')],
                'ship_name': item.get('ship_name'),
                'ship_tel': order.ship_tel
            })

    return actual_orders

# jz 2015-08-26
# def _pay_weizoom_card(context, data, order):
#     url = '/webapp/api/project_api/call/'
#     card = json.loads(context.text)

#     # 1.根据卡号密码获取id
#     data['target_api'] = 'weizoom_card/check'
#     data['name'] = card['id']
#     data['password'] = card['password']
#     response = context.client.post(url, data)
#     response_json = json.loads(response.content)
#     if response_json['code'] == 200:
#         card_id = response_json['data']['id']
#     else:
#         return False

#     # 2.确认支付
#     data['target_api'] = 'weizoom_card/pay'
#     data['card_id'] = card_id
#     data['order_id'] = order.order_id
#     del data['name']
#     del data['password']
#     response = context.client.post(url, data)
#     response_json = json.loads(response.content)

