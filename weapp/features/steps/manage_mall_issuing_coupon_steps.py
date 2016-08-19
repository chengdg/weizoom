# -*- coding: utf-8 -*-


import json
from datetime import datetime, timedelta

from behave import given, then, when

from test import bdd_util
from mall.models import Product
from mall.promotion.models import Promotion, Coupon, CouponRule
from account.social_account.models import SocialAccount
from modules.member.models import Member, MemberHasSocialAccount


@when(u"{user_name}为会员发放优惠券")
def step_impl(context, user_name):
    __send_coupons(context, user_name)


@then(u"{user_name}能获得发放优惠券失败的信息")
def step_impl(context, user_name):
    expected = json.loads(context.text)
    error_data = json.loads(context.response.content)
    actual = dict(
        error_message=error_data['errMsg']
    )
    context.tc.assertTrue(200 != error_data['code'])
    bdd_util.assert_dict(expected, actual)


###################################################################################
# __get_member_by_openid: 根据openid获得member
###################################################################################
def __get_member_by_openid(webapp_id, openid):
    social_account = SocialAccount.objects.get(openid=openid)
    relation = MemberHasSocialAccount.objects.get(account_id=social_account.id, webapp_id=webapp_id)
    member = Member.objects.get(id=relation.member_id)

    return member


def __send_coupons(context, webapp_owner_name):
    webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
    coupon_info = json.loads(context.text)
    coupon_rule_name = coupon_info['name']


    count = coupon_info['count']
    member_names = coupon_info['members']

    coupon_rule = CouponRule.objects.get(owner_id=webapp_owner_id, name=coupon_rule_name, is_active=True)

    member_ids = []
    for member_name in member_names:
        openid = u'%s_%s' % (member_name, webapp_owner_name)
        member = __get_member_by_openid(context.webapp_id, openid)
        member_ids.append(str(member.id))

    url = '/mall2/api/issuing_coupons_record/?_method=put'
    data = {
    "member_id": json.dumps(member_ids),
    "coupon_rule_id": coupon_rule.id,
    "pre_person_count": count
    }

    response = context.client.post(url, data)
    context.response = response