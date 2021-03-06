# -*- coding: utf-8 -*-
import urllib
import urllib2

from behave import when, then, given
from django.contrib.auth.models import User
from test import bdd_util
from mall.models import (ORDER_TYPE2TEXT, STATUS2TEXT, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED, express_util,
                         ORDERSTATUS2TEXT, Order, Supplier)
from mall.models import Supplier
from account.models import UserProfile
from features.testenv.model_factory import timedelta, json, ORDER_STATUS_NOT
from mall.promotion.models import datetime
import steps_db_util


###############################
# when steps
###############################
from tools.express.models import ExpressHasOrderPushStatus


def get_order_action_set(actions):
    return set([action['name'] for action in actions])


ORDER_ACTION_NAME2ACTION = {
    u'支付': 'pay',
    u'完成': 'finish',
    u'退款': 'return_pay',
    u'申请退款': 'return_pay',
    u'完成退款': 'return_success',
    u'取消': 'cancel',
    u'退款成功': 'return_success'
}


@when(u"{user}'{action}'最新订单")
def step_impl(context, user, action):
    if hasattr(context, 'latest_order_id'):
        try:
            latest_order_no = Order.objects.get(id=context.latest_order_id).order_id
        except:
            latest_order_no = Order.objects.get(order_id=context.latest_order_id).order_id
    else:
        latest_order_no = steps_db_util.get_latest_order().order_id

    context.execute_steps(u"when %s'%s'订单'%s'" % (user, action, latest_order_no))


@when(u"{user}修改订单'{order_code}'的价格")
def step_impl(context, user, order_code):
    url = '/mall2/api/order/'
    post_data = json.loads(context.text)
    order_real_id = bdd_util.get_order_by_order_no(order_code).id
    post_data['order_id'] = order_real_id
    response = context.client.post(url, post_data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}'{action}'订单'{order_code}'")
def step_impl(context, action, user, order_code):
    url = '/mall2/api/order/'
    order_id = bdd_util.get_order_by_order_no(order_code).id

    data = {
        'order_id': order_id,
        'action': ORDER_ACTION_NAME2ACTION[action]
    }
    response = context.client.post(url, data)
    bdd_util.assert_api_call_success(response)

    if hasattr(context, 'order_payment_time'):
        Order.objects.filter(order_id=order_code).update(payment_time=context.order_payment_time)
        delattr(context, 'order_payment_time')

@when(u"{user}'{action}'订单'{order_code}'于{payment_time}")
def step_impl(context, action, user, order_code, payment_time):
    context.order_payment_time = payment_time
    context.execute_steps(u"When %s'%s'订单'%s'" % (user, action, order_code))


# @when(u"{user}设置订单过期时间{order_expired_day}天")
@when(u"{user}设置未付款订单过期时间{order_expired_hour}小时")
def step_impl(context, user, order_expired_hour):
    url = '/mall2/order_config/'
    data = {
        "order_expired_day": order_expired_hour
    }
    context.client.post(url, data)


@when(u"{user}触发订单超时取消任务")
def step_impl(context, user):
    from services.cancel_not_pay_order_service.tasks import cancel_not_pay_order_timeout
    cancel_not_pay_order_timeout('', '')


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
    data_order_id = __get_order(context, order['order_no']).id
    if 'name' in order:
        express_value = order['name']
    url = '/mall2/api/delivery/'
    data = {
        'order_id': data_order_id,
        'express_company_name': express_value,
        'express_number': order['number'],
        'leader_name': 'aa' if 'shipper' not in order else order['shipper'],
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

def __get_customer_message_str(customer_message_data):
    customer_message = {}
    for supplier_name, message in customer_message_data.items():
        if UserProfile.objects.filter(store_name=supplier_name).count() > 0:
            key = "%du" % UserProfile.objects.get(store_name=supplier_name).user_id
            customer_message[key] = {'supplier_name': 'supplier_name', 'customer_message': message}

        if Supplier.objects.filter(name=supplier_name).count() > 0:
            key = "%ds" % Supplier.objects.get(name=supplier_name).id
            customer_message[key] = {'supplier_name': 'supplier_name', 'customer_message': message}
    return customer_message

@then(u"{user}可以看到订单列表")
def step_impl(context, user):
    user_id = User.objects.get(username=user).id
    mall_type = UserProfile.objects.get(user_id=user_id).webapp_type
    if user != context.client.user.username:
        context.client.logout()
        context.client = bdd_util.login(user)
    # client = context.client
    query_params = dict()
    if hasattr(context, 'query_params'):
        query_params = context.query_params
        delattr(context, 'query_params')
    response = context.client.get('/mall2/api/order_list/', query_params)
    items = json.loads(response.content)['data']['items']

    actual_orders = []
    source = {'mine_mall': u'本店', 'weizoom_mall': u'商城'}

    for order_item in items:
        sync_order = False
        if 'u' in order_item['order_id']:
            sync_order = True
            user_id = order_item['order_id'].split('^')[1][:-1]
            store_name = UserProfile.objects.get(user_id=user_id).store_name
            order_item['order_id'] = '%s-%s' % (order_item['order_id'].split('^')[0], store_name)
        actual_order = {}
        actual_order['order_no'] = order_item['order_id']
        actual_order['order_time'] = order_item['created_at']
        actual_order['ship_name'] = order_item['ship_name']
        actual_order['ship_tel'] = order_item['ship_tel']
        actual_order["sources"] = u'商城' if sync_order else u'本店'
        actual_order["member"] = order_item['buyer_name'] if order_item['member_is_subscribed'] else '非会员'
        actual_order["methods_of_payment"] = order_item['pay_interface_name']
        actual_order["logistics"] = express_util.get_name_by_value(order_item['express_company_name'])
        actual_order["number"] = order_item['express_number']
        actual_order["shipper"] = order_item['leader_name']
        actual_order["integral"] = order_item['integral']
        actual_order['status'] = order_item['status']
        actual_order['price'] = order_item['pay_money']
        actual_order['payment_time'] = order_item['payment_time']
        actual_order['final_price'] = order_item['pay_money']
        actual_order['customer_message'] = order_item['customer_message']
        actual_order['buyer'] = order_item['buyer_name']
        actual_order['postage'] = order_item['postage']
        actual_order['save_money'] = '' if sync_order or not order_item['save_money'] else order_item['save_money']
        actual_order['is_first_order'] = 'true' if order_item['is_first_order'] else 'false'
        actual_order['is_group_buying'] = 'true' if order_item['is_group_buying'] else 'false'

        if 'edit_money' in order_item and order_item['edit_money']:
            actual_order["order_no"] = actual_order["order_no"] + "-" + str(order_item['edit_money']).replace('.',
                                                                                                              '').replace(
                '-', '')

        children_order_action = True
        if order_item['parent_action']:
            actual_order['actions'] = get_order_action_set(order_item['parent_action'])
        else:
            actual_order['actions'] = get_order_action_set(order_item['groups'][0]['fackorder']['actions'])

        if len(order_item['groups']) <= 1 or order_item['status'] == 0:
            children_order_action = False

        # order_list的接口数据返回格式已经更新，上面的代码可以改为如下代码：
        buy_product_results = []
        for group in order_item['groups']:
            for buy_product in group['products']:
                total_price = buy_product.get('total_price',
                                              round(float(buy_product.get('price')) * buy_product.get('count'), 2))
                buy_product_result = {}
                buy_product_result['product_name'] = buy_product['name']
                buy_product_result['name'] = buy_product['name']
                buy_product_result['count'] = buy_product['count']
                buy_product_result['total_price'] = total_price
                buy_product_result['price'] = '' if sync_order else buy_product.get('price')
                buy_product_result['img_url'] = buy_product['thumbnails_url']
                buy_product_result['promotion'] = buy_product['promotion']
                if 'supplier_store_name' in buy_product:
                    if buy_product['supplier_store_name']:
                        buy_product_result['supplier'] = buy_product['supplier_store_name']
                if 'supplier_name' in buy_product:
                    if buy_product['supplier_name']:
                        buy_product_result['supplier'] = buy_product['supplier_name']
                buy_product_result['status'] = group['fackorder']['status']
                if children_order_action:
                    buy_product_result['actions'] = get_order_action_set(group['fackorder']['actions'])
                buy_product_results.append(buy_product_result)
        actual_order['products'] = buy_product_results
        actual_order['products_count'] = len(buy_product_results)
        actual_orders.append(actual_order)

    expected = json.loads(context.text)
    for order in expected:
        if 'actions' in order:
            order['actions'] = set(order['actions'])  # 暂时不验证顺序
        for pro in order.get('products', []):
            if 'supplier' in pro and order.get('status', None) == u'待支付':
                del pro['supplier']
            if 'actions' in pro:
                pro['actions'] = set(pro['actions'])
            if 'is_sync_supplier' in pro:
                del pro['is_sync_supplier']
        if mall_type and order.get('customer_message'):
            order['customer_message'] = json.dumps(__get_customer_message_str(order['customer_message']))
            actual_order['products'] = sorted(actual_order['products'], key=lambda p: p['name'])
    # for i in range(len(expected)):
    #     # print expected[i]['order_no'], '++++', actual_orders[i]['order_no']
    #     # for j in range(len(expected[i]['products'])):
    #     #     print expected[i]['products'][j].get('actions',""), '****', actual_orders[i]['products'][j].get('actions',"")
    #     #     print expected[i]['products'][j].get('actions',"") == actual_orders[i]['products'][j].get('actions',"")
    #     print expected[i]['order_no'], '++++', actual_orders[i]['order_no']
    #     print expected[i]['price'], actual_orders[i]['price']
    # for i in range(len(expected[0]['products'])):
    #     print expected[0]['products'][i]['name'], "+++++++" ,actual_orders[0]['products'][i]['name']
    #     print expected[0]['products'][i]['price'], "+++++++" ,actual_orders[0]['products'][i]['price']
    bdd_util.assert_list(expected, actual_orders)


@then(u"{user}可以获得最新订单详情")
def step_impl(context, user):
    order = steps_db_util.get_latest_order()
    context.latest_order_id = order.id
    # client = context.client
    response = context.client.get('/mall2/order/?order_id=%d' % context.latest_order_id)

    order = response.context['order']
    order.order_no = order.order_id
    # order.order_type = ORDER_TYPE2TEXT[order.type]
    order.order_type = ''
    order.total_price = float(order.final_price)
    order.ship_area = order.area  # + ' ' + order.ship_address

    order.actions = get_order_action_set(order.actions)
    for product in order.products:
        product['price'] = float(product['price'])
    order.status = STATUS2TEXT[order.status]
    for product in order.products:
        if 'custom_model_properties' in product and product['custom_model_properties']:
            product['model'] = ' '.join([property['property_value'] for property in product['custom_model_properties']])
        product['supplier'] = product.get('supplier_name', '')
        product['status'] = product.get('order_status', '')
    actual = order
    actual.reason = order.reason

    expected = json.loads(context.text)
    expected['order_type'] = ''
    if 'actions' in expected:
        expected['actions'] = set(expected['actions'])
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

ORDER_TYPE = {
    u'全部': -1,
    u'首单': 1,
    u'非首单': 0,
    u'团购订单': 2
}


@when(u'{user}根据给定条件查询订单')
def step_look_for_order(context, user):
    """根据给定条件查询订单

    context: {
        "order_no":          # 订单编号            e.g.:
        "ship_name":         # 收货人姓名          e.g.:
        "ship_tel":          # 收货人电话          e.g.:
        "product_name":      # 商品名称            e.g.:
        "date_interval":     # 查询时间段          e.g.: 今天 3天前  or  "2014-10-07|2014-10-08",
        "date_interval_type":# 时间类型            e.g.: 1 下单时间 2 付款时间 3 发货时间
        "pay_type":          # 支付方式            e.g.:
        "express_number":    # 物流单号            e.g.:
        "order_source":      # 订单来源            e.g.:
        "order_status":      # 订单状态            e.g.:
        "isUseWeizoomCard":  # 仅显示微众卡抵扣订单  e.g.:
        "is_first_order":        # 订单是不是首单
    }
    """
    query_params = {
        'pay_type': u'全部',
        'order_source': u'全部',
        'order_status': u'全部',
        'order_type': u'全部',
        'is_first_order': u'全部',
        'belong': 'all',
        "date_interval": "",
        "date_interval_type": 1,
        "product_name": "",
    }

    query_params_c = json.loads(context.text)
    query_params.update(query_params_c)
    if query_params.get('order_no'):
        query_params['query'] = query_params['order_no']
        query_params.pop('order_no')

    if query_params.get('date_interval'):
        query_params['date_interval']

    query_params['pay_type'] = PAYNAME2ID[query_params['pay_type']]
    if query_params['pay_type'] == -1:
        query_params.pop('pay_type')

    query_params['order_source'] = ORDER_SOURCE2ID[query_params['order_source']]
    if query_params['order_source'] == -1:
        query_params.pop('order_source')

    query_params['order_type'] = ORDER_TYPE[query_params['order_type']]
    if query_params['order_type'] == -1:
        query_params.pop('order_type')

    query_params['order_status'] = ORDER_STATUS2ID[query_params['order_status']]
    if query_params['order_status'] == -1:
        query_params.pop('order_status')

    #惠惠卡处理首单非首单
    # if query_params.get('is_first_order'):
    #     query_params['is_first_order'] = IS_FIRST_ORDER[query_params['is_first_order']]
    #     if query_params['is_first_order'] == -1:
    #         query_params.pop('is_first_order')
    is_first_order =  True if (query_params.get('is_first_order') in ('true', 'yes', 'True', 'Yes', True)) else False
    is_not_first_order =  True if (query_params.get('is_not_first_order') in ('true', 'yes', 'True', 'Yes', True)) else False
    if query_params.get('is_not_first_order'):
        query_params.pop('is_not_first_order')
    if (is_first_order and is_not_first_order) or (not is_first_order and  not is_not_first_order):
        query_params.pop('is_first_order')
    if is_first_order and not is_not_first_order:
        query_params['is_first_order'] = '1'
    if not is_first_order and is_not_first_order:
        query_params['is_first_order'] = '0'
    #惠惠卡处理首单非首单
    if query_params.get('date'):
        query_params['date_interval_type'] = 1
        query_params['date_interval'] = bdd_util.get_date_to_time_interval(query_params.get('date'))
    if query_params.get('payment_time'):
        query_params['date_interval_type'] = 2
        query_params['date_interval'] = bdd_util.get_date_to_time_interval(query_params.get('payment_time'))
    if query_params.get('delivery_time'):
        query_params['date_interval_type'] = 3
        query_params['date_interval'] = bdd_util.get_date_to_time_interval(query_params.get('delivery_time'))

    if query_params.get('isUseWeizoomCard'):
        query_params['isUseWeizoomCard'] = 1 if query_params['isUseWeizoomCard'] == 'true' else 0

    if query_params.get('supplier_type'):
        if query_params.get('supplier_type') == u'全部':
            del query_params['supplier_type']
            query_params['orderSupplierType'] = -1
        elif query_params.get('supplier_type') == u'同步供货商':
            del query_params['supplier_type']
            query_params['orderSupplierType'] = 0
        elif query_params.get('supplier_type') == u'自建供货商':
            del query_params['supplier_type']
            query_params['orderSupplierType'] = 1

    context.query_params = query_params
    context.export_query_params = query_params



@then(u"{user}导出订单获取订单统计信息")
def step_get_all_info_of_order(context, user):
    filter_value = dict()
    if hasattr(context, 'export_query_params'):
        filter_value = context.export_query_params
        filter_value["bdd"]=1
        #print "filter_value---------------",filter_value
        delattr(context, 'export_query_params')
    from cStringIO import StringIO
    import csv

    url = '/mall2/order_export/?bdd=1'
    response = context.client.get(url, filter_value)
    reader = csv.reader(StringIO(response.content))
    # 去掉表头信息
    csv_items = [row for row in reader]
    context.last_csv_order_info = csv_items[-1]
    all_info = context.last_csv_order_info
    expect_info = json.loads(context.text)
    actual = dict([(info.split(':')[0].encode('utf-8'),info.split(':')[1]) for info in all_info[1:]])
    actual_encode = {}
    for x,y in actual.items():
        x = x.encode('utf-8')
        actual_encode[unicode(x)] = y

    bdd_util.assert_list(expect_info,[actual_encode])


@then(u"{user}导出订单获取订单信息")
def step_get_specify_order(context, user):
    """
    """

    filter_value = dict()
    if hasattr(context, 'query_params'):
        filter_value = context.query_params
        filter_value["bdd"]=1
    from cStringIO import StringIO
    import csv

    url = '/mall2/order_export/?bdd=1'
    response = context.client.get(url, filter_value)
    reader = csv.reader(StringIO(response.content))
    csv_items = [row for row in reader]
    csv_items[0] = [
        'order_no',
        'order_time',
        'pay_time',
        'product_name',
        'model',
        'product_unit_price',
        'count',
        'sales_money',
        'weight',
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
        'leader_remark',
        'sources',
        'logistics',
        'number',
        'delivery_time',
        'remark',
        'customer_message',
        'customer_source',
        'customer_recommender',
        'is_older_mermber',
        'purchase_price',
        'purchase_costs'

    ]
    actual = []
    for row in csv_items[1:]:
        # if reader.line_num :
        item = dict(map(None, csv_items[0], [str(r).decode('utf8') for r in row]))
        item['ship_address'] = '' if not item.get('ship_address') else item.get('ship_address').replace(' ', ',')
        if '' != item.get('pay_time') and '已完成' not in item.get('pay_time').encode('utf-8'):
            data = datetime.strptime(item['pay_time'], '%Y-%m-%d %H:%M')
            item['pay_time'] = '%s 00:00' % data.strftime('%Y-%m-%d')
        if None != item.get('delivery_time') and '' != item.get('delivery_time'):
            data = datetime.strptime(item['delivery_time'], '%Y-%m-%d %H:%M')
            item['delivery_time'] = '%s 00:00' % data.strftime('%Y-%m-%d')
        actual.append(item)
    context.last_csv_order_info = csv_items[-1]
    # remove statistical information
    actual.pop()
    expected_order = []
    if context.table:
        for row in context.table:
            order = row.as_dict()
            if 'order_time' in order:
                if order['order_time'] != '':
                    order['order_time'] = bdd_util.get_datetime_no_second_str(order['order_time'])
                else:
                    del order['order_time']

            if 'pay_time' in order:
                if order['pay_time'] != '':
                    order['pay_time'] = bdd_util.get_datetime_no_second_str(order['pay_time'])
                else:
                    del order['pay_time']

            if 'delivery_time' in order:
                if order['delivery_time'] != '':
                    order['delivery_time'] = bdd_util.get_datetime_no_second_str(order['delivery_time'])
                else:
                    del order['delivery_time']
            if '-' in order['order_no']:

                order_no_info = order['order_no'].split('-')
                if len(order_no_info) > 2:
                    order['order_no'] = '%s^%s-%s' % (
                    order_no_info[0], Supplier.objects.get(name=order_no_info[1]).id, order_no_info[2])
                else:
                    order_no_info = order['order_no'].split('-')
                    if u'' != order['edit_money']:
                        order['order_no'] = '%s-%s' % (order_no_info[0], order_no_info[1])
                    else:
                        order['order_no'] = '%s^%s' % (order_no_info[0], Supplier.objects.get(name=order_no_info[1]).id)

            expected_order.append(order)
        for row in expected_order:
            if 'edit_money' in row:
                del row['edit_money']  # 不校验该字段，无效字段，只用来判断order_no的格式
    else:

        expected_order = json.loads(context.text)

    bdd_util.assert_list(expected_order, actual)
    del StringIO
    del csv


@then(u"{user}能获得订单'{order_id}'")
def step_impl(context, user, order_id):
    user_id = User.objects.get(username=user).id
    mall_type = UserProfile.objects.get(user_id=user_id).webapp_type
    real_id = bdd_util.get_order_by_order_no(order_id).id
    response = context.client.get('/mall2/order/?order_id=%d' % real_id)
    actual_order = response.context['order']

    actual_order.actions = get_order_action_set(actual_order.actions)

    source_dict = {0: u'本店', 1: u'商城'}
    actual_order.order_no = actual_order.order_id
    # actual_order.member = actual_order.buyer_name
    leader_name_and_remark = actual_order.leader_name.split('|')
    actual_order.shipper = leader_name_and_remark[0]
    if len(leader_name_and_remark) > 1:
        actual_order.leader_remark = leader_name_and_remark[1]
    actual_order.order_time = str(actual_order.created_at)
    actual_order.methods_of_payment = actual_order.pay_interface_name
    actual_order.sources = source_dict[actual_order.order_source]
    actual_order.status = STATUS2TEXT[actual_order.status]
    if actual_order.edit_money:
        actual_order.order_no = actual_order.order_no + "-" +\
            str(actual_order.edit_money).replace('.', '').replace('-', '')

    for product in actual_order.products:
        if 'supplier_store_name' in product:
            if product['supplier_store_name']:
                product['supplier'] = product['supplier_store_name']
        if 'supplier_name' in product:
            if product['supplier_name']:
                product['supplier'] = product['supplier_name']

    if '^' in actual_order.order_no:
        user_id = actual_order.order_no.split('^')[1][:-1]
        store_name = UserProfile.objects.get(user_id=user_id).store_name
        actual_order.order_no = '%s-%s' % (actual_order.order_no.split('^')[0], store_name)
        actual_order.sources = u'商城'
        actual_order.final_price = actual_order.total_purchase_price
    else:
        actual_order.sources = u'本店'



    expected = []
    if context.table:
        for order in context.table:
            expected.append(order.as_dict())
    else:
        expected = json.loads(context.text)
    if "logistics" in expected:
        express_value = express_util.get_value_by_name(expected['logistics'])
        expected['logistics'] = express_value
    if "actions" in expected:
        expected["actions"] = set(expected["actions"])

    if 'products' in expected:
        for product in expected['products']:
            if 'is_sync_supplier' in product:
                del product['is_sync_supplier']
    if mall_type and 'customer_message' in expected:
        expected['customer_message'] = __get_customer_message_str(expected['customer_message']).values()
        actual_order.customer_message = actual_order.customer_message


    # 会员详情页无会员信息
    if "member" in expected:
        del expected["member"]
    if actual_order.express_company_name:
        actual_order.logistics = actual_order.express_company_name
    # 字段名称不匹配，order中有number属性
    actual_order.number = actual_order.express_number
    bdd_util.assert_dict(expected, actual_order)


@when(u"{user}完成订单'{order_id}'")
def step_impl(context, user, order_id):
    order = __get_order(context, order_id)
    data = {
        'order_id': order.id,
        'action': 'finish'
    }
    response = context.client.post('/mall2/api/order/', data)


def __get_order(context, order_id):
    if '-' in order_id:
        order_no_info = order_id.split('-')

        order_id = '%s^%ds' % (order_no_info[0], Supplier.objects.get(name=order_no_info[1]).id)

    return Order.objects.get(order_id=order_id)


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


@then(u"{user}能获得订单'{order_id}'操作日志")
def step_impl(context, user, order_id):
    order_id = steps_db_util.get_order_by_order_id(order_id).id
    response = context.client.get('/mall2/order/?order_id=%d' % order_id)

    order_operation_logs = response.context['order_operation_logs']
    actual = []
    for log in order_operation_logs:
        # if u'订单发货' in log.action:
        #     log.operator = '%s - %s' % (log.operator, log.leader_name)
        actual.append({
            log.action: log.operator.strip()
        })

    expected = []
    for item in context.table:
        expected.append({
            item['action']: item['operator']
        })

    bdd_util.assert_list(expected, actual)


@then(u"{user}获得订单列表筛选结果")
def step_impl(context, user):
    expected = json.loads(context.text)
    response = context.client.get('/mall2/api/order_list/')
    total_orders_count = json.loads(response.content)['data']['order_return_count']

    actual = {
        'total_orders_count': total_orders_count
    }

    bdd_util.assert_dict(expected, actual)

@then(u"{user}获得财务审核'团购退款'订单列表")
def step_impl(context, user):
    # query_params = {
    #     'order_status': 8,
    #     'belong': 'audit'
    # }
    # context.query_params = query_params
    # context.execute_steps(u"Then %s可以看到订单列表" % user)
    pass

@when(u"{user}通过财务审核'{action}'自营订单'{order_code}'")
def step_impl(context, action, user, order_code):
    url = '/mall2/api/refund_successful_sub_order/?_method=put'
    order_id = bdd_util.get_order_by_order_no(order_code).origin_order_id
    delivery_item_id = bdd_util.get_order_by_order_no(order_code).id
    
    data = {
        'order_id': order_id,
        'delivery_item_id': delivery_item_id
    }
    response = context.client.post(url, data)
    bdd_util.assert_api_call_success(response)

@when(u"{user}'申请退款'自营订单'{order_code}'")
def step_imple(context,user,order_code):
    url = '/mall2/api/refunding_order/?_method=put'
    order_id = bdd_util.get_order_by_order_no(order_code).origin_order_id
    delivery_item_id = bdd_util.get_order_by_order_no(order_code).id

    a = json.loads(context.text)
    data = {
        'order_id': order_id,
        'delivery_item_id': delivery_item_id,
        'cash': a.get('cash', 0),
        'weizoom_card_money': a.get('weizoom_card', 0),
        'integral': a.get('integral', 0),
        'coupon_money': a.get('coupon_money', 0)
    }

    response = context.client.post(url, data)
    bdd_util.assert_api_call_success(response)


@then(u"{user}获得自营订单'{order_code}'")
def step_impl(context, user, order_code):
    order_db_id = bdd_util.get_order_by_order_no(order_code).id
    response = context.client.get('/mall2/order/?order_id=%d' % order_db_id)
    
    expected = json.loads(context.text)
    #expected.pop('total_save')
    order = response.context['order']
    child_orders = response.context['child_orders']
    
    order.order_no = order.order_id
    order.invoice=order.bill
    order.business_message=order.remark
    order.methods_of_payment = order.pay_interface_name
    order.weizoom_card = order.weizoom_card_money
    order.actions = [ action.get('name', '') for action in order.actions ]

    sub_orders = []

    for sub_order in child_orders:
        supplier_name = Supplier.objects.get(id=sub_order.supplier).name
        sub_order.order_no = u'{}-{}'.format(order.order_id, supplier_name)
        sub_order.status = sub_order.get_status_text()
        sub_order.products = []

        sub_orders.append(sub_order)

    _products = []
    order.refund_details = {
        'cash':order.refund_info['total_cash'],
        'weizoom_card':order.refund_info['total_weizoom_card_money'],
        'coupon_money':order.refund_info['total_coupon_money'],
        'integral_money':order.refund_info['total_integral_money'],

    }

    order.original_cash=order.refund_info['origin_final_price']
    order.original_weizoom_card= order.refund_info['origin_weizoom_card_money']
    order.original_final_price= order.refund_info['origin_pay_money']
    order.refund_money = order.refund_info['refund_money']

    for p in order.products:
        p['supplier_id'] = p['supplier']
        p['supplier'] = p['supplier_name']
        # if p['promotion']:
        #     p['single_save'] = p['promotion']['promotion_saved_money']
        # else:
        #     p['single_save'] = 0

        _products.append(p)

    for p in _products:
        for o in sub_orders:
            if o.supplier == p['supplier_id']:
                o.products.append(p)

    print('-------------------------------------------',repr(_products))
    order.group = sub_orders
    final_price = order.final_price
    order.final_price = order.pay_money
    order.product_price =order.total_price
    order.cash = final_price
    order.products_count = order.number
    order.ship_area = order.area
    order.total_save = order.save_money
    order.status = order.get_status_text()


    bdd_util.assert_dict(expected, order)


def __get_order_items_for_self_order(items):
    actual_orders = []
    for order_item in items:
        actual_order = {}
        actual_order['order_no'] = order_item['order_id']
        actual_order["methods_of_payment"] = order_item['pay_interface_name']
        actual_order['order_time'] = order_item['created_at']
        actual_order['payment_time'] = order_item['payment_time']
        actual_order['save_money'] = order_item['save_money']
        actual_order['buyer'] = order_item['buyer_name']
        actual_order['ship_name'] = order_item['ship_name']
        actual_order['ship_tel'] = order_item['ship_tel']
        actual_order['ship_address'] = order_item['ship_address']
        actual_order['invoice'] = ""
        actual_order['final_price'] = order_item['pay_money']
        actual_order['postage'] = order_item['postage']
        actual_order['status'] = STATUS2TEXT[order_item['order_status']
]
        actual_order['group'] = []
        action_list = []
        if order_item['order_status'] != 0:
            buy_product_results = []
            group_dict = {}
            for group in order_item['groups']:
                group_dict['status'] = group['fackorder']['status']
                order_supplier = ''
                for buy_product in group['products']:
                    buy_product_result = {}
                    buy_product_result['name'] = buy_product['name']
                    buy_product_result['count'] = buy_product['count']
                    buy_product_result['price'] = buy_product['price']
                    order_supplier = buy_product['supplier_name'] or ''
                    buy_product_results.append(buy_product_result)
                
                group_dict['products'] = buy_product_results
                group_dict['supplier'] = order_supplier
                group_dict['order_no'] = order_item['order_id'] + '-' + order_supplier

                if group_dict['status'] in ['退款中', '退款成功']:
                    group_dict['refund_details'] = group['fackorder']['refund_info']
                    group_dict['refund_details']['weizoom_card'] = group_dict['refund_details']['weizoom_card_money']
                # 获取子订单状态对应的操作
                group_dict['actions'] = [action.get('name', '') for action in group['fackorder']['actions']]
                actual_order['group'].append(group_dict)
        else:
            buy_product_results = []

            for group in order_item['groups']:
                for buy_product in group['products']:
                    buy_product_result = {}
                    buy_product_result['name'] = buy_product['name']
                    buy_product_result['count'] = buy_product['count']
                    buy_product_result['price'] = buy_product['price']
                    buy_product_results.append(buy_product_result)
                action_list = [action.get('name', '') for action in group['fackorder']['actions']]
            actual_order['products'] = buy_product_results
            actual_order['actions'] = action_list
        
        actual_orders.append(actual_order)
    return actual_orders


@then(u"{user}获得自营订单列表")
def step_impl(context, user):
    user_id = User.objects.get(username=user).id
    mall_type = UserProfile.objects.get(user_id=user_id).webapp_type
    if user != context.client.user.username:
        context.client.logout()
        context.client = bdd_util.login(user)

    url='/mall2/api/order_list/'

    query_params = dict()

    if hasattr(context, 'query_params'):
        query_params = context.query_params
        query_params['count_per_page'] = 99999
        delattr(context, 'query_params')
    response = context.client.get(url, query_params)


    items = json.loads(response.content)['data']['items']
    actual_orders = __get_order_items_for_self_order(items)

    expected = json.loads(context.text)
    for order in expected:
        # if order.get('payment_time',''):
        #     del order['payment_time'] 
        if 'actions' in order:
            order['actions'] = order['actions']  # 暂时不验证顺序
   
    bdd_util.assert_list(expected, actual_orders)


@then(u"{user}获得自营财务审核'{order_type}'订单列表")
def step_impl(context, user, order_type):
    user_id = User.objects.get(username=user).id
    mall_type = UserProfile.objects.get(user_id=user_id).webapp_type
    if user != context.client.user.username:
        context.client.logout()
        context.client = bdd_util.login(user)

    if order_type =='退款中':
        url = '/mall2/api/order_list/?design_mode=0&version=1&belong=audit&orderSupplierType=undefined&order_status=6&count_per_page=9999'

    elif order_type == '退款成功':
        url = '/mall2/api/order_list/?design_mode=0&version=1&belong=audit&orderSupplierType=undefined&order_status=7&date_interval_type=1&count_per_page=9999'
    elif order_type =='全部':
        url = '/mall2/api/order_list/?design_mode=0&version=1&belong=audit&orderSupplierType=undefined&order_status=-1&date_interval_type=1&count_per_page=9999'

    query_params = dict()
    if hasattr(context, 'query_params'):
        query_params = context.query_params
        delattr(context, 'query_params')
    response = context.client.get(url, query_params)

    items = json.loads(response.content)['data']['items']

    actual_orders = __get_order_items_for_self_order(items)

    expected = json.loads(context.text)
    for order in expected:
        if 'actions' in order:
            order['actions'] = set(order['actions'])  # 暂时不验证顺序

    bdd_util.assert_list(expected, actual_orders)