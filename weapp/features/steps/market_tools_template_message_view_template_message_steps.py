# -*- coding: utf-8 -*-
__author__ = 'slzhu'
import json
import time

from test import bdd_util
from features.testenv.model_factory import *
from market_tools.tools.template_message.models import *


@given(u"{user}已有行业")
def step_impl(context, user):
    MarketToolsTemplateMessage.objects.all().delete()
    if hasattr(context, 'client') is False:
        context.client = bdd_util.login(user, password=None, context=context)
    context.industries = json.loads(context.text)
    for industry in context.industries:
        industry_type = INDUSTRY2TYPE.get(industry['name'])
        MarketToolsTemplateMessage.objects.create(
            industry = industry_type,
            title = u'订单支付成功'
        )
        MarketToolsTemplateMessage.objects.create(
            industry = industry_type,
            title = u'商品已发出通知'
        )

@when(u"{user}选择行业")
def step_impl(context, user):
    MarketToolsTemplateMessageDetail.objects.all().delete()
    select_industry = json.loads(context.text)
    major_type = INDUSTRY2TYPE.get(select_industry['host_industry'])
    deputy_type = INDUSTRY2TYPE.get(select_industry['deputy_industry'])
    params = {
        "major_type": major_type,
        "deputy_type": deputy_type
    }
    context.client.post('/market_tools/template_message/api/template/create/', params)


@then(u"{user}查看模板消息列表")
def step_impl(context, user):
    expected = json.loads(context.text)
    response = context.client.get('/market_tools/template_message/api/template/get')
    data = json.loads(response.content)['data']
    items = data['items']
    actual = []
    for item in items:
        actual_item = {}
        actual_item['template_id'] = item['template_id']
        actual_item['headline'] = item['title']
        actual_item['industry'] = item['industry_name']
        actual_item['status'] = item['status']
        actual_item['type'] = item['type']
        actual_item['operate'] = u'查看'
        actual.append(actual_item)
    bdd_util.assert_list(sorted(expected), sorted(actual))