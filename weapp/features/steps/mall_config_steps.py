#-*- coding:utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import MallConfig

@when(u"{user}'修改'通用设置")
def step_impl(context, user):
    data = json.loads(context.text)
    for key, value in data.items():
        if value == u'开启':
            data[key] = '1'
        elif value == u'关闭':
            data[key] = '0'

    url = '/mall2/config_product_list/'
    response = context.client.post(url, data)
    context.mall_config = response.context['mall_config']

@then(u"{user}获得通用设置")
def step_impl(context, user):
    if hasattr(context, 'mall_config'):
        mall_config = context.mall_config
        delattr(context, 'mall_config')
    else:
        assert False

    expected = json.loads(context.text)

    actual = dict(
            product_sales=u'开启' if mall_config.show_product_sales else u'关闭',
            product_sort=u'开启' if mall_config.show_product_sort else u'关闭',
            product_search=u'开启' if mall_config.show_product_search else u'关闭',
            shopping_cart=u'开启' if mall_config.show_shopping_cart else u'关闭'
        )

    bdd_util.assert_dict(expected, actual)