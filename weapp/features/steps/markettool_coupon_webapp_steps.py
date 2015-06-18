# -*- coding: utf-8 -*-
import json
from behave import then
from test import bdd_util


@then(u"{webapp_user_name}能获得webapp优惠券列表")
def step_impl(context, webapp_user_name):
    url = '/workbench/jqm/preview/?module=market_tool:coupon&model=usage&action=get&workspace_id=market_tool:coupon&webapp_owner_id=%d&project_id=0&fmt=%s' % (context.webapp_owner_id, context.member.token)
    response = context.client.get(bdd_util.nginx(url))
    coupons = response.context['coupons']
    actual = []
    for coupon in coupons:
        if coupon.status == 0:
            coupon.status = u'未使用'
            actual.append(coupon)
        else:
            coupon.status = u'unknown'

        coupon.money = coupon.money

    expected = json.loads(context.text)
    # print("*"*40, "get_webapp_coupon", "*"*40)
    # from pprint import pprint
    # pprint(expected)
    # pprint(coupons)
    # print("*"*100)
    bdd_util.assert_list(expected, actual)
