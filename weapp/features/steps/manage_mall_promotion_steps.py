# -*- coding: utf-8 -*-
import json
from behave import when

from mall.promotion import models
from modules.member.models import MemberGrade
from features.testenv.model_factory import ProductFactory
from test import bdd_util


@when(u"{user}'{action}'促销活动'{promotion_name}'")
def step_terminate_promotion(context, user, action, promotion_name):
    db_promotion = models.Promotion.objects.get(
        owner_id=context.webapp_owner_id,
        name=promotion_name
    )
    data = {
        'type': models.PROMOTION2TYPE[db_promotion.type]['name'],
        'ids[]': [db_promotion.id]
    }
    if action == u'开始':
        data['start'] = 'true'
    elif action == u'结束':
        data['start'] = 'false'
    elif action == u'删除':
        data['_method'] = 'delete'
    url = '/mall2/api/promotion/'

    response = context.client.post(url, data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}批量'{action}'促销活动")
def step_terminate_promotion(context, user, action):
    data = {
        'ids[]': []
    }
    promotions = json.loads(context.text)
    for promotion in promotions:
        db_promotion = models.Promotion.objects.get(
            owner_id=context.webapp_owner_id,
            name=promotion['name']
        )
        data['ids[]'].append(db_promotion.id)
    data['type'] = models.PROMOTION2TYPE[db_promotion.type]['name'],
    if action == u'开始':
        data['start'] = 'true'
    elif action == u'结束':
        data['start'] = 'false'
    elif action == u'删除':
        data['_method'] = 'delete'
    url = '/mall2/api/promotion/'

    response = context.client.post(url, data)
    bdd_util.assert_api_call_success(response)

@when(u"{user}创建积分应用活动")
def step_impl(context, user):
    #webapp_id = context.client.user.profile.webapp_id
    if context.table:
        # 处理tables
        promotions = context.table
    else:
        promotions = json.loads(context.text)
    if type(promotions) == dict:
        # 处理单个积分应用活动创建
        promotions = [promotions]

    for promotion in promotions:
        db_product = ProductFactory(name=promotion['product_name'])
        product_ids = [{
            'id': db_product.id
        }]
        if 'rules' in promotion:
            rules = promotion['rules']
            for rule in rules:
                if rule.has_key('member_grade'):
                    rule['member_grade_id'] = __get_member_grade(rule, context.webapp_id)
        else:
            rules = [{
                "member_grade_id": -1,
                "discount": promotion.get('discount', 100),
                "discount_money": promotion.get('discount_money', 0.0)
            }]
        data = {
            'name': promotion['name'],
            'promotion_title': promotion.get('promotion_title', ''),
            'member_grade': __get_member_grade(promotion, context.webapp_id),
            'products': json.dumps(product_ids),
            'rules': json.dumps(rules),
            'discount': promotion.get('discount', 100),
            'discount_money': promotion.get('discount_money', 0.0),
            'integral_price': promotion.get('integral_price', 0.0),
            'is_permanant_active': str(promotion.get('is_permanant_active', False)).lower(),
        }
        if data['is_permanant_active'] != 'true':
            data['start_date'] = bdd_util.get_datetime_no_second_str(promotion['start_date']),
            data['end_date'] = bdd_util.get_datetime_no_second_str(promotion['end_date']),
        url = '/mall2/api/integral_sale/?_method=put'
        response = context.client.post(url, data)
        if promotion.get('created_at'):
            models.Promotion.objects.filter(
            owner_id=context.webapp_owner_id,
            name=data['name']).update(created_at=bdd_util.get_datetime_str(promotion['created_at']))
        bdd_util.assert_api_call_success(response)


@when(u"{user}创建满减活动")
def step_impl(context, user):
    promotions = json.loads(context.text)
    if type(promotions) == dict:
        promotions = [promotions]

    for promotion in promotions:
        product_ids = []
        for product in promotion['products']:
            db_product = ProductFactory(name=product)
            product_ids.append({
                'id': db_product.id
            })

        data = {
            'name': promotion['name'],
            'promotion_title': promotion.get('promotion_title', ''),
            'member_grade': __get_member_grade(promotion, context.webapp_id),
            'start_date': bdd_util.get_datetime_no_second_str(promotion['start_date']),
            'end_date': bdd_util.get_datetime_no_second_str(promotion['end_date']),
            'products': json.dumps(product_ids),

            'price_threshold': promotion['price_threshold'],
            'cut_money': promotion['cut_money'],
            'is_enable_cycle_mode': "true" if promotion.get('is_enable_cycle_mode', False) else "false",
        }

        url = '/mall2/api/price_cut/?_method=put'
        response = context.client.post(url, data)
        bdd_util.assert_api_call_success(response)


@when(u"{user}创建买赠活动")
def step_create_premium_sale(context, user):
    promotions = json.loads(context.text)
    if type(promotions) == dict:
        promotions = [promotions]

    for promotion in promotions:
        product_ids = []
        db_product = ProductFactory(name=promotion['product_name'])
        product_ids =[{
            'id': db_product.id
        }]

        premium_products = []
        for premium_product in promotion['premium_products']:
            product_name = premium_product['name']
            db_product = ProductFactory(name=product_name)
            premium_products.append({
                'id': db_product.id,
                'count': premium_product['count'],
                'unit': premium_product['unit'] if premium_product.has_key('unit') else ''
            })

        data = {
            'name': promotion['name'],
            'promotion_title': promotion.get('promotion_title', ''),
            'member_grade': __get_member_grade(promotion, context.webapp_id),
            'start_date': bdd_util.get_datetime_no_second_str(promotion['start_date']),
            'end_date': bdd_util.get_datetime_no_second_str(promotion['end_date']),
            'products': json.dumps(product_ids),

            'count': promotion['count'],
            'is_enable_cycle_mode': "true" if promotion.get('is_enable_cycle_mode', False) else "false",
            'premium_products': json.dumps(premium_products)
        }

        url = '/mall2/api/premium_sale/?_method=put'
        response = context.client.post(url, data)
        bdd_util.assert_api_call_success(response)


@when(u"{user}创建限时抢购活动")
def step_create_flash_sales(context, user):
    promotions = json.loads(context.text)
    if type(promotions) == dict:
        promotions = [promotions]

    for promotion in promotions:
        db_product = ProductFactory(name=promotion['product_name'])
        product_ids =[{
            'id': db_product.id
        }]

        data = {
            'name': promotion['name'],
            'promotion_title': promotion.get('promotion_title', ''),
            'member_grade': __get_member_grade(promotion, context.webapp_id),
            'start_date': bdd_util.get_datetime_no_second_str(promotion['start_date']),
            'end_date': bdd_util.get_datetime_no_second_str(promotion['end_date']),
            'products': json.dumps(product_ids),

            'limit_period': promotion.get('limit_period', 0),
            'promotion_price': promotion['promotion_price'],
            'count_per_purchase': promotion.get('count_per_purchase', 9999999),
        }

        url = '/mall2/api/flash_sale/?_method=put'
        response = context.client.post(url, data)
        bdd_util.assert_api_call_success(response)


@when(u"{user}设置查询条件")
def step_impl(context, user):
    context.query_param = json.loads(context.text)


@then(u"{user}获取{type}活动列表")
def step_impl(context, user, type):
    if type == u"限时抢购":
        type = "flash_sale"
    elif type == u"买赠":
        type = "premium_sale"
    elif type == u"积分应用":
        type = "integral_sale"
    # elif type == u"优惠券":
    #     type = "coupon"
    url = '/mall2/api/promotion_list/?design_mode=0&version=1&type=%s' % type
    if hasattr(context, 'query_param'):
        if context.query_param.get('product_name'):
            url += '&name=' + context.query_param['product_name']
        if context.query_param.get('bar_code'):
            url += '&barCode='+ context.query_param['bar_code']
        if context.query_param.get('start_date'):
            url += '&startDate='+ bdd_util.get_datetime_str(context.query_param['start_date'])[:16]
        if context.query_param.get('end_date'):
            url += '&endDate='+ bdd_util.get_datetime_str(context.query_param['end_date'])[:16]
        if context.query_param.get('status', u'全部') != u'全部':
            if context.query_param['status'] == u'未开始':
                status = 1
            elif context.query_param['status'] == u'进行中':
                status = 2
            elif context.query_param['status'] == u'已结束':
                status = 3
            url += '&promotionStatus=%s' % status
    response = context.client.get(url)
    actual = json.loads(response.content)['data']['items']

    for promotion in actual:
        if type == 'integral_sale':
            promotion['product_name'] = promotion['product']['name']
            promotion['product_price'] = promotion['product']['display_price']
            promotion['bar_code'] = promotion['product']['bar_code']
            promotion['is_permanant_active'] = str(promotion['detail']['is_permanant_active']).lower()
            detail = promotion['detail']
            rules = detail['rules']
            if len(rules) == 1 and rules[0]['member_grade_id'] < 1:
                rule = rules[0]
                rule['member_grade'] = u'全部会员'
                promotion['discount'] = str(rule['discount']) + '%'
                promotion['discount_money'] = rule['discount_money']
            else:
                promotion['discount'] = detail['discount'].replace(' ', '')
                promotion['discount_money'] = detail['discount_money'].replace(' ', '')
            promotion['rules'] = rules
    expected = []
    if context.table:
        for promotion in context.table:
            promotion = promotion.as_dict()
            expected.append(promotion)
    else:
        expected = json.loads(context.text)

    for promotion in expected:
        promotion['is_permanant_active'] = str(promotion.get('is_permanant_active', False)).lower()
        if promotion.get('start_date') and promotion.get('end_date'):
            if promotion['is_permanant_active'] != 'true':
                promotion['start_date'] = bdd_util.get_datetime_str(promotion['start_date'])
                promotion['end_date'] = bdd_util.get_datetime_str(promotion['end_date'])
            else:
                promotion.pop('start_date')
                promotion.pop('end_date')
        if promotion.get('created_at'):
            promotion['created_at'] = bdd_util.get_datetime_str(promotion['created_at'])
    bdd_util.assert_list(expected, actual)


def __get_member_grade(promotion, webapp_id):
    member_grade = promotion.get('member_grade', 0)
    if member_grade == u'全部' or member_grade == u'全部会员':
        member_grade = 0
    elif member_grade:
        member_grade = MemberGrade.objects.get(name=member_grade, webapp_id=webapp_id).id
    return member_grade


