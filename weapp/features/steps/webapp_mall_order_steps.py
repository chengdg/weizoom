# -*- coding: utf-8 -*-

from behave import *
from test import bdd_util
from modules.member.models import WebAppUser
from mall.models import *
from features.testenv.model_factory import *
from tools.regional.models import *
from mall.promotion.models import *
import steps_db_util
from mall import module_api as mall_api

# 手机端订单支付相关step_impl在features/steps/mall_pay_interface_webapp_steps.py

ORDER_PAY_ACTION = {
	'name': u'支付',
	'action': 'pay',
	'button_class': 'btn-success'
}
ORDER_SHIP_ACTION = {
	'name': u'发货',
	'action': 'ship',
	'button_class': 'btn-success'
}
ORDER_FINISH_ACTION = {
	'name': u'完成',
	'action': 'finish',
	'button_class': 'btn-success'
}
ORDER_CANCEL_ACTION = {
	'name': u'取消订单',
	'action': 'cancel',
	'button_class': 'btn-danger'
}

# 临时，未保证全部数据准确
def get_order_actions_for_mobile_bdd(order):
        if isinstance(order, dict):
            pay_interface_type = order['pay_interface_type']
            status = order['status']
        else:
            pay_interface_type = order.pay_interface_type
            status = order.status
        if pay_interface_type == PAY_INTERFACE_COD and status == ORDER_STATUS_PAYED_NOT_SHIP:
        	return [ORDER_SHIP_ACTION, ORDER_CANCEL_ACTION]
        if status == ORDER_STATUS_NOT:
        	return [ORDER_CANCEL_ACTION, ORDER_PAY_ACTION]
        elif status == ORDER_STATUS_PAYED_NOT_SHIP:
        	return [ORDER_SHIP_ACTION, ORDER_CANCEL_ACTION]
        elif status == ORDER_STATUS_PAYED_SHIPED:
        	return [ORDER_FINISH_ACTION, ORDER_CANCEL_ACTION]
        elif status == ORDER_STATUS_SUCCESSED:
        	return [ORDER_CANCEL_ACTION]
        elif status == ORDER_STATUS_CANCEL:
        	return []


def get_prodcut_ids_info(order):
    product_ids = []
    product_counts = []
    product_model_names = []
    promotion_ids = []

    for product_group in order.product_groups:
        for product in product_group['products']:
            product_ids.append(str(product.id))
            product_counts.append(str(product.purchase_count))
            product_model_names.append(str(product.model_name))
            if product_group['can_use_promotion']:
                promotion_ids.append(str(product_group['promotion']['id']))
            else:
                promotion_ids.append('0')
    return {'product_ids': '_'.join(product_ids),
            'product_counts': '_'.join(product_counts),
            'product_model_names': '$'.join(product_model_names),
            'promotion_ids': '_'.join(promotion_ids)
            }


@when(u"{webapp_user_name}取消订单'{order_id}'")
def step_impl(context, webapp_user_name, order_id):
    id = steps_db_util.get_order_by_order_id(order_id).id
    post_data = dict()
    post_data["woid"] = context.webapp_owner_id
    post_data["module"] = 'mall'
    post_data["target_api"] = 'order_status/update'
    post_data["order_id"] = id
    post_data["action"] = u'cancel-custom'

    url = '/webapp/api/project_api/call/'
    response = context.client.post(url, post_data)
    response_json = json.loads(response.content)

    if response_json['code'] == 200:
        context.created_order_id = id
    else:
        context.created_order_id = -1


@when(u"{webapp_user_name}在购物车订单编辑中点击提交订单")
def step_click_check_out(context, webapp_user_name):
    """
    {
        "pay_type":  "货到付款",
    }
    """
    from mall.models import PAYNAME2TYPE

    argument = json.loads(context.text)
    pay_type = argument.get(argument['pay_type'])

    order = context.response.context['order']
    argument_request = get_prodcut_ids_info(order)
    url = '/webapp/api/project_api/call/'
    data = {
        'module': 'mall',
        'target_api': 'order/save',
        'is_order_from_shopping_cart': 'true',
        'woid': context.webapp_owner_id,
        'xa-choseInterfaces': PAYNAME2TYPE.get(pay_type, -1),
        'bill': order.ship_name,
        'group2integralinfo': {},

        "ship_name": argument.get('ship_name', "未知姓名"),
        "area": steps_db_util.get_area_ids(argument.get('ship_area')),
        "ship_address": argument.get('ship_address', "长安大街"),
        "ship_tel": argument.get('ship_tel', "11111111111"),
    }

    data.update(argument_request)
    coupon_id = context.product_infos.get('coupon_id', None)
    if coupon_id:
        data['is_use_coupon'] = 'true'
        data['coupon_id'] = coupon_id
    if argument.get('integral', None):
        data['orderIntegralInfo'] = json.dumps({
            'integral': argument['integral'],
            'money': argument['integral_money']
        })
    response = context.client.post(url, data)
    response_json = json.loads(response.content)
    msg = response_json["data"].get("msg", None)
    if msg:
        context.server_error_msg = msg
        context.response_json = response_json
    else:
        context.created_order_id = response_json['data']['order_id']
        context.response = response
        if argument.get('order_no', None):
            db_order = Order.objects.get(order_id=context.created_order_id)
            db_order.order_id=argument['order_no']
            db_order.save()

            db_order_operation_log = OrderOperationLog.objects.get(order_id=context.created_order_id)
            db_order_operation_log.order_id=argument['order_no']
            db_order_operation_log.save()

            if db_order.origin_order_id <0:
                for order in Order.objects.filter(origin_order_id=db_order.id):
                    order.order_id = '%s^%s' % (argument['order_no'], order.supplier)
                    order.save()
            context.created_order_id = argument['order_no']


# 不在mall2
# @when(u"{webapp_user_name}'{order_type}'{webapp_owner_name}的'{product_name}'")
# def step_impl(context, webapp_user_name, order_type, webapp_owner_name, product_name):
# url = '/webapp/api/project_api/call/'
# args = {
#         "products": [{
#                          "name": product_name,
#                          "count": 1
#                      }],
#         "customer_message": "bill的订单备注1"
#     }
#
#     is_order_from_shopping_cart = "false"
#     webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
#     product_ids = []
#     product_counts = []
#     product_model_names = []
#     products = args['products']
#     for product in products:
#         product_counts.append(str(product['count']))
#         product_name = product['name']
#         product_obj = Product.objects.get(owner_id=webapp_owner_id, name=product_name)
#         product_ids.append(str(product_obj.id))
#
#         product_model_names.append("standard")
#
#     # 处理中文地区转化为id，如果数据库不存在的地区则自动添加该地区
#     ship_area = args.get('ship_area')
#     if ship_area:
#         areas = ship_area.split(' ')
#     else:
#         areas = '北京市 北京市 海淀区'.split(' ')
#
#     if len(areas) > 0:
#         pros = Province.objects.filter(
#             name=areas[0]
#         )
#         pro_count = pros.count()
#         if pro_count == 0:
#             province = Province.objects.create(
#                 name=areas[0]
#             )
#             pro_id = province.id
#         else:
#             pro_id = pros[0].id
#         ship_area = str(pro_id)
#     if len(areas) > 1:
#         cities = City.objects.filter(
#             name=areas[1]
#         )
#         city_count = cities.count()
#         if city_count == 0:
#             city = City.objects.create(
#                 name=areas[1],
#                 zip_code='',
#                 province_id=pro_id
#             )
#             city_id = city.id
#         else:
#             city_id = cities[0].id
#         ship_area = ship_area + '_' + str(city_id)
#     if len(areas) > 2:
#         dis = District.objects.filter(
#             name=areas[2]
#         )
#         dis_count = dis.count()
#         if dis_count == 0:
#             district = District.objects.create(
#                 name=areas[2],
#                 city_id=city_id
#             )
#             ship_area = ship_area + '_' + str(district.id)
#         else:
#             ship_area = ship_area + '_' + str(dis[0].id)
#
#     data = {
#         "woid": webapp_owner_id,
#         "module": 'mall',
#         "is_order_from_shopping_cart": is_order_from_shopping_cart,
#         "target_api": "order/save",
#         "product_ids": '_'.join(product_ids),
#         "product_counts": '_'.join(product_counts),
#         "product_model_names": '$'.join(product_model_names),
#         "ship_name": args.get('ship_name', "未知姓名"),
#         "area": ship_area,
#         "ship_id": 0,
#         "ship_address": args.get('ship_address', "长安大街"),
#         "ship_tel": args.get('ship_tel', "11111111111"),
#         "integral": "",
#         "is_use_coupon": "false",
#         "coupon_id": 0,
#         "coupon_coupon_id": "",
#         "message": args.get('customer_message', '')
#     }
#
#     if order_type == u'测试购买':
#         data['order_type'] = PRODUCT_TEST_TYPE
#
#     # 填充优惠券信息
#     coupon_id = args.get('coupon', None)
#     if coupon_id:
#         data['is_use_coupon'] = 'true'
#         if args['coupon_type'] == u'选择':
#             coupon = Coupon.objects.get(coupon_id=coupon_id)
#             data['coupon_id'] = coupon.id
#         elif args['coupon_type'] == u'输入':
#             data['coupon_coupon_id'] = coupon_id
#
#     # 填充积分信息
#     integral = args.get('integral', None)
#     if integral:
#         data['is_use_integral'] = 'true'
#         data['integral'] = integral
#
#     response = context.client.post(url, data)
#     context.response = response
#     # response结果为: {"errMsg": "", "code": 200, "data": {"msg": null, "order_id": "20140620180559"}}
#     response_json = json.loads(context.response.content)
#     if response_json['code'] == 200:
#         context.created_order_id = response_json['data']['order_id']
#     else:
#         context.created_order_id = -1
#
#     context.webapp_owner_name = webapp_owner_name

@When(u"{webapp_user_name}点击支付")
def step_impl(context, webapp_user_name):
    url = '/workbench/jqm/preview/%s' % context.pay_result_url[2:]
    response = context.client.get(bdd_util.nginx(url), follow=True)

    actual_order = response.context['order']
    context.create_order_id = actual_order.id

###############################
# when steps
###############################

###############################
# then steps
###############################

@then(u"{webapp_user_name}手机端获取订单'{order_id}'状态")
def step_impl(context, webapp_user_name, order_id):
    url = '/workbench/jqm/preview/?woid=%s&module=mall&model=order&action=pay&order_id=%s' % (
        context.webapp_owner_id, order_id)
    response = context.client.get(bdd_util.nginx(url), follow=True)

    actual_order = response.context['order']
    actual_order.order_no = actual_order.order_id
    actual_order.status = ORDERSTATUS2TEXT[actual_order.status]

    expected = json.loads(context.text)

    bdd_util.assert_dict(expected, actual_order)


@then(u'{webapp_usr_name}手机端获取订单"{order_id}"')
def step_impl(context, webapp_usr_name, order_id):
    # 为获取完可顺利支付
    context.created_order_id = order_id

    url = '/workbench/jqm/preview/?woid=%s&module=mall&model=order&action=pay&order_id=%s' % (
        context.webapp_owner_id, order_id)
    response = context.client.get(bdd_util.nginx(url), follow=True)
    has_sub_order = response.context['has_sub_order']
    actual = response.context['order']
    actual.order_no = actual.order_id
    actual.order_time = (str(actual.created_at))
    actual.methods_of_payment = response.context['pay_interface']
    actual.member = actual.buyer_name
    actual.status = ORDERSTATUS2MOBILETEXT[actual.status]
    actual.ship_area = actual.area

    if has_sub_order:
        products = []
        orders = response.context['orders']
        for i, order in enumerate(orders):
            product_dict = {
                u"包裹" + str(i + 1): order.products,
                'status': ORDERSTATUS2MOBILETEXT[order.status]
            }
            products.append(product_dict)

        actual.products = products

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)

@then(u"{webapp_user_name}查看个人中心全部订单")
def step_visit_personal_orders(context, webapp_user_name):
    """
    [{
        "status": "待支付",
        "created_at": "今天",
        "products": [{
            "name": "商品1"
        }, {
            "name": "商品2"
        }, {
            "name": "商品3"
        }],
        "counts": 5,
        "final_price": 38.7,
        "actions": ["取消订单", "支付"]
    }, {
        "status": "待支付",
        "created_at": "今天",
        "products": [{
            "name": "商品1"
        }],
        "counts": 2,
        "final_price": 19.8,
        "actions": ["取消订单", "支付"]
    }, {
        "status": "待支付",
        "created_at": "今天",
        "products": [{
            "name": "商品1"
        }],
        "counts": 1,
        "final_price": 9.9,
        "actions": ["取消订单", "支付"]
    }]
    """
    expected = json.loads(context.text)
    actual = []

    from mall.models import STATUS2TEXT

    url = '/workbench/jqm/preview/?woid=%d&module=mall&model=order_list&action=get&member_id=%d&workspace_id=mall&type=-1' % (
        context.webapp_owner_id, context.member.id)
    response = context.client.get(bdd_util.nginx(url), follow=True)
    orders = response.context['orders']
    import datetime
    for actual_order in orders:
        order = {}
        order['final_price'] = actual_order['final_price']
        order['products'] = []
        order['counts'] = actual_order['product_count']
        order['status'] = ORDERSTATUS2MOBILETEXT[actual_order['status']]
        order['created_at'] = actual_order['created_at']
        order['actions'] = [action['name'] for action in get_order_actions_for_mobile_bdd(actual_order)]
        # BBD中购买的时间再未指定购买时间的情况下只能为今天
        if actual_order['created_at'].date() == datetime.date.today():
            order['created_at'] = u'今天'

        for i, product in enumerate(actual_order['products']):
            # 列表页面最多显示3个商品
            if i > 2:
                break
            a_product = {}
            a_product['name'] = product['name']
            # a_product['price'] = product.total_price
            order['products'].append(a_product)
        actual.append(order)
    bdd_util.assert_list(expected, actual)


@then(u"{webapp_user_name}在webapp查看'{order_id}'的物流信息")
def step_impl(context, webapp_user_name, order_id):
    expected_order = json.loads(context.text)

    url = '/workbench/jqm/preview/?woid=%s&module=mall&model=order&action=pay&order_id=%s' % (
        context.webapp_owner_id, order_id)
    response = context.client.get(bdd_util.nginx(url), follow=True)
    actual_order = response.context['order']
    actual_order = {
        'order_no': actual_order.order_id,
        'logistics': express_util.get_name_by_value(actual_order.express_company_name),
        'number': actual_order.express_number,
        'status': ORDERSTATUS2TEXT[actual_order.status]
    }

    bdd_util.assert_dict(expected_order, actual_order)


@then(u"{webapp_user_name}支付订单成功")
def step_impl(context, webapp_user_name):
    order, order_has_products = steps_db_util.get_order_has_products(context)
    actual_order = order
    actual_order.ship_area = actual_order.area
    actual_order.status = ORDERSTATUS2TEXT[actual_order.status]
    actual_order.methods_of_payment = PAYTYPE2NAME[actual_order.pay_interface_type] #兼容feature
    actual_order.pay_interface_type = PAYTYPE2NAME[actual_order.pay_interface_type]

    actual_order.order_no = order.order_id
    actual_order.order_time = str(order.created_at)

    # 获取order的products
    actual_order.products = []
    for relation in order_has_products:
        product = relation.product
        product.price = relation.price
        product.count = relation.number
        product.model = relation.product_model_name
        # product.fill_specific_model('standard')
        actual_order.products.append(product)

    expected = json.loads(context.text)
    if 'products' in expected:
        for product in expected['products']:
            if 'model' in product:
                product['model'] = steps_db_util.get_product_model_keys(product['model'])
    bdd_util.assert_dict(expected, actual_order)


@then(u"{webapp_user_name}查看订单")
def step_impl(context, webapp_user_name):
    actual_order = {}

    if hasattr(context, 'pay_order_id'):
        order, order_has_products = steps_db_util.get_order_has_products(context)

        actual_order = order
        actual_order.ship_area = actual_order.area
        actual_order.status = ORDERSTATUS2TEXT[actual_order.status]
        actual_order.pay_interface_type = PAYTYPE2NAME[actual_order.pay_interface_type]

        # 获取order的products
        actual_order.products = []
        for relation in order_has_products:
            product = relation.product
            product.count = relation.number
            product.fill_specific_model('standard')
            actual_order.products.append(product)

    expected = json.loads(context.text)

    bdd_util.assert_dict(expected, actual_order)


@then(u"{webapp_user_name}获得待编辑订单")
def step_impl(context, webapp_user_name):
    """
        e.g.:
        [{'name': "asdfasdfa",
          'count': "111"
        },{...}]
    """
    context_text = json.loads(context.text)
    if context_text == []:
        actual = []
        expected_products = []
    else:
        actual = []
        expected_products = context_text['products']
        product_groups = context.response.context['product_groups']
        for i in product_groups:
            for product in i['products']:
                _a = {}
                _a['name'] = product.name
                _a['count'] = product.count
                actual.append(_a)

    bdd_util.assert_list(expected_products, actual)


@then(u"{webapp_user_name}获得创建订单失败的信息'{error_msg}'")
def step_impl(context, webapp_user_name, error_msg):
    error_data = json.loads(context.response.content)
    context.tc.assertTrue(200 != error_data['code'])
    response_msg = error_data['data']['msg']
    if response_msg == '':
        response_msg = error_data['data']['detail'][0]['msg']
    context.tc.assertEquals(error_msg, response_msg)


@then(u"{webapp_user_name}获得创建订单失败的信息")
def step_impl(context, webapp_user_name):
    error_data = json.loads(context.response.content)
    expected = json.loads(context.text)
    webapp_owner_id = bdd_util.get_user_id_for(context.webapp_owner_name)
    for detail in expected['detail']:
        product = steps_db_util.get_product_by_prouduct_id(owner_id=webapp_owner_id, name=detail['id'])
        detail['id'] = product.id

    actual = error_data['data']
    context.tc.assertTrue(200 != error_data['code'])
    bdd_util.assert_dict(expected, actual)


@then(u"{webapp_user_name}成功创建订单")
def step_impl(context, webapp_user_name):
    order_id = context.created_order_id
    if order_id == -1:
        print 'Server Error: ', json.dumps(json.loads(context.response.content), indent=True)
        assert False, "order_id must NOT be -1"
        return

    # order = Order.objects.get(order_id=order_id)

    url = '/workbench/jqm/preview/?woid=%s&module=mall&model=order&action=pay&order_id=%s' % (
        context.webapp_owner_id, order_id)
    response = context.client.get(bdd_util.nginx(url), follow=True)

    actual_order = response.context['order']
    actual_order.order_no = actual_order.order_id
    actual_order.ship_area = actual_order.area
    actual_order.status = ORDERSTATUS2TEXT[actual_order.status]
    # 获取coupon规则名
    if (actual_order.coupon_id != 0) and (actual_order.coupon_id != -1):
        # coupon = Coupon.objects.get(id=actual_order.coupon_id)
        coupon = steps_db_util.get_coupon_by_id(actual_order.coupon_id)
        actual_order.coupon_id = coupon.coupon_rule.name

    for product in actual_order.products:
        if 'custom_model_properties' in product and product['custom_model_properties']:
            product['model'] = ' '.join([property['property_value'] for property in product['custom_model_properties']])


    expected = json.loads(context.text)
    if expected.get('actions', None):
        # TODO 验证订单页面操作
        del expected['actions']
    bdd_util.assert_dict(expected, actual_order)