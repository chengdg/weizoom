# -*- coding: utf-8 -*-
__author__ = 'guoliyan'
import json
import time
from test import bdd_util
from market_tools.tools.red_envelope.models import *
from mall.promotion.models import CouponRule

#######################################################################
# __supplement_red_envelope: 补足一个红包的数据
#######################################################################
def __supplement_red_envelope(red_envelop):
    red_envelop_prototype = {
        "name": u"微信红包",
        "total_award_value": u"522",
        "desc": u"红包",
        "expected_participation_count": u"85",
        "is_non_member": u"非会员可参与",
        "prize_odds|1": u"100",
        "prize_count|1": u"3",
        "prize_type|1": u"3",
        "prize_name|1": u"一等奖",
        "prize_source|1": u"3",
        "logo_url": u"/static/upload/6_20140710/1404981209095_5.jpg",
    }

    red_envelop_prototype.update(red_envelop)
    return red_envelop_prototype


#######################################################################
# __add_red_envelope: 添加一个红包
#######################################################################
def __add_red_envelope(context, red_envelope):
    red_envelope = __supplement_red_envelope(red_envelope)
    __process_red_envelope_data(red_envelope)
    context.client.post("/market_tools/red_envelope/api/red_envelope/edit/", red_envelope)


#######################################################################
# __process_red_envelope_data: 转换一个微信红包的数据
#######################################################################
def __process_red_envelope_data(red_envelope):
    if red_envelope['is_non_member'] == u'非会员可参与':
        red_envelope['is_non_member'] = 1
    else:
         red_envelope['is_non_member'] = 0
    if red_envelope['prize_type|1'] == u'1':
        prize_source = red_envelope['prize_source|1']
        prize_source = CouponRule.objects.get(name=prize_source)
        red_envelope['prize_source|1'] = prize_source.id


@when(u"{user}添加微信红包")
def step_impl(context, user):

    client = context.client
    context.red_envelopes = json.loads(context.text)
    for red_envelope in context.red_envelopes:
        __add_red_envelope(context, red_envelope)


@then(u"{user}能获取红包列表")
def step_impl(context, user):
    context.client = bdd_util.login(user)
    client = context.client
    response = client.get('/market_tools/red_envelope/')
    actual_red_envelopes = response.context['red_envelopes']
    actual_data = []
    for red_envelope in actual_red_envelopes:
        actual_data.append({
            "name": red_envelope.name
        })

    expected = json.loads(context.text)

    bdd_util.assert_list(expected, actual_data)


@given(u"{user}已添加微信红包")
def step_impl(context, user):
    if hasattr(context, 'client'):
        context.client.logout()
    context.client = bdd_util.login(user)

    context.red_envelopes = json.loads(context.text)
    for red_envelope in context.red_envelopes:
        __add_red_envelope(context, red_envelope)


@when(u"{user}删除微信红包'{red_envelope_name}'")
def step_impl(context, user, red_envelope_name):
    red_envelope = RedEnvelope.objects.get(name=red_envelope_name)
    url = '/market_tools/red_envelope/api/red_envelope/delete/'
    context.client.post(url, {'id': red_envelope.id}, HTTP_REFERER='/market_tools/red_envelope/')


@when(u"{member}参加微信红包'{red_envelope_name}'")
def step_impl(context, member, red_envelope_name):
    client = context.client
    red_envelope = RedEnvelope.objects.get(name=red_envelope_name)
    url = '/workbench/jqm/preview/?woid=%s&module=market_tool:red_envelope&model=red_envelope&action=get&red_envelope_id=%s&fmt=%s' % (context.webapp_owner_id, red_envelope.id, context.member.token)
    context.client.get(url)

