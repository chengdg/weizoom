# -*- coding: utf-8 -*-
__author__ = 'slzhu'
import json
import time

from test import bdd_util
from features.testenv.model_factory import *
from market_tools.tools.template_message.models import *


@given(u"{user}已有模板消息")
def step_impl(context, user):
    MarketToolsTemplateMessage.objects.all().delete()
    MarketToolsTemplateMessageDetail.objects.all().delete()
    if hasattr(context, 'client') is False:
        context.client = bdd_util.login(user, password=None, context=context)
    context.template_message_details = json.loads(context.text)
    context.message_detail = {}
    for template_message_detail in context.template_message_details:
        industry_type = INDUSTRY2TYPE.get(template_message_detail['industry'])
        template_message = MarketToolsTemplateMessage.objects.create(
            industry = industry_type,
            title = template_message_detail['headline']
        )
        type = 1
        if template_message_detail['type'] == u'主营行业':
            type = 0
        status = 1
        if template_message_detail['status'] == u'未启用':
            status = 0
        message_detail = MarketToolsTemplateMessageDetail.objects.create(
            owner = context.client.user,
            template_message = template_message,
            industry = industry_type,
            template_id = template_message_detail['template_id'],
            first_text = '',
            remark_text = '',
            type = type,
            status = status
        )
        key = '%d-%s-%s' % (context.client.user.id, template_message_detail['industry'], template_message_detail['headline'])
        context.message_detail[key] = message_detail
    
    
@when(u"{user}给'{industry}'行业标题为'{title}'的模板消息添加内容")
def step_impl(context, user, industry, title):
    detail = json.loads(context.text)
    
    key = '%d-%s-%s' % (context.client.user.id, industry, title)
    params = {
        "id": context.message_detail[key].id,
        "template_id": detail['template_id'],
        "first_text": detail['first'],
        "remark_text": detail['remark'],
    }
    context.client.post('/market_tools/template_message/api/detail/update/', params)


@when(u"{user}修改'{industry}'行业标题为'{title}'的状态")
def step_impl(context, user, industry, title):
    detail = json.loads(context.text)
    
    key = '%d-%s-%s' % (context.client.user.id, industry, title)
    status = 1
    if detail['status'] == u'未启用':
        status = 0
    message_detail = context.message_detail[key]
    params = {
        "id": message_detail.id,
        "template_id": detail['template_id'],
        "first_text": 'first',
        "remark_text": 'remark',
        "status": status,
        "action": 'enable'
    }
    context.client.post('/market_tools/template_message/api/detail/update/', params)


@then(u"{user}查看'{industry}'行业标题为'{title}'的模板消息")
def step_impl(context, user, industry, title):
    expected = json.loads(context.text)
    
    key = '%d-%s-%s' % (context.client.user.id, industry, title)
    detail = MarketToolsTemplateMessageDetail.objects.get(id=context.message_detail[key].id)
    actual = {}
    actual['template_id'] = detail.template_id
    actual['first'] = detail.first_text
    actual['remark'] = detail.remark_text
    bdd_util.assert_list(sorted(expected), sorted(actual))