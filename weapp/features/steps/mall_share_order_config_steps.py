# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from django.contrib.auth.models import User

from mall.models import *
from weixin2.models import News

@when(u"{user}设置订单提交成功后提示分享赚积分信息")
def step_impl(context, user):
    url = '/mall2/order_config/'

    user = User.objects.get(username=user)
    data = json.loads(context.text)
    news_title = data['text_picture']
    material_id = News.objects.get(title=news_title).material_id

    args = {
        'isShowPage': True,
        'backgroundImage': data['logo_pic'],
        'materialId': material_id,
        'shareImage': data['share_pic'],
        'shareInfo': data['share_description']
    }

    response = context.client.post(url, args)
    context.share_order_config = response.context['share_page_config']

@then(u"{user}获得订单提交成功后提示分享赚积分信息")
def step_impl(context, user):
    expected = json.loads(context.text)

    if hasattr(context, 'share_order_config'):
        share_order_config = context.share_order_config
        delattr(context, 'share_order_config')
    else:
        pass

    actual = {}
    actual['logo_pic'] = share_order_config.background_image
    actual['share_pic'] = share_order_config.share_image
    actual['share_description'] = share_order_config.share_describe
    actual['text_picture'] = News.objects.get(material_id=share_order_config.material_id).title

    bdd_util.assert_dict(expected, actual)

@then(u"{user}设置订单提交成功后提示分享赚积分信息时能获得图文管理列表")
def step_impl(context, user):
    url = "/new_weixin/api/materials/?from=share_page_config"
    response = context.client.get(url)

    expected = json.loads(context.text)
    actual = []
    for item in json.loads(response.content)['data']['items']:
        actual.append({'title': item['newses'][0]['title']})

    bdd_util.assert_list(expected, actual)