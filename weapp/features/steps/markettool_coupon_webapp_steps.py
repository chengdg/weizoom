# -*- coding: utf-8 -*-
import json
from behave import then
from test import bdd_util

def __sort(dict_array):
    if len(dict_array) > 0 and not type(dict_array[0]) == dict:
        dict_array = sorted(dict_array, key=lambda x:x.coupon_id)
    else:
        dict_array = sorted(dict_array, key=lambda x:x['coupon_id'])
    return dict_array


@then(u"{webapp_user_name}能获得webapp优惠券列表")
def step_impl(context, webapp_user_name):
    url = '/workbench/jqm/preview/?module=market_tool:coupon&model=usage&action=get&workspace_id=market_tool:coupon&webapp_owner_id=%d&project_id=0&fmt=%s' % (context.webapp_owner_id, context.member.token)
    url = bdd_util.nginx(url)
    response = context.client.get(url)
    if response.status_code == 302:
        print('[info] redirect by change fmt in shared_url')
        redirect_url = bdd_util.nginx(response['Location'])
        response = context.client.get(bdd_util.nginx(redirect_url))
        print('response!!!!!!!!!!!!!!!!!!!!!')
        print(response)
    else:
        print('[info] not redirect')
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
    actual = __sort(actual)
    expected = __sort(expected)

    bdd_util.assert_list(expected, actual)


