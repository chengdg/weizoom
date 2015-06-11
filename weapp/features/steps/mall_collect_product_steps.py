#-*- coding:utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from modules.member.models import WebAppUser, ShipInfo
from mall.models import Product

def _update_wishlist_product(context, status):
    product_info = json.loads(context.text)
    webapp_owner_id = context.webapp_owner_id
    product_name = product_info['name']
    product = Product.objects.get(owner_id=webapp_owner_id, name=product_name)

    data = {
        "product_id": product.id,
        "is_collect": status,
        "module": 'mall',
        'woid': webapp_owner_id,
        "target_api": "wishlist_product/update",
        "timestamp": '1404469450205'
    }

    response = context.client.post('/webapp/api/project_api/call/', data)
    return response

@when(u"{webapp_user_name}收藏{webapp_owner_name}的商品到我的收藏")
def step_impl(context, webapp_user_name, webapp_owner_name):
    time.sleep(1)
    response = _update_wishlist_product(context, "false")
    bdd_util.assert_api_call_success(response)

@then(u"{webapp_user_name}能获得我的收藏")
def step_impl(context, webapp_user_name):
    expected = json.loads(context.text)
    member = bdd_util.get_member_for(webapp_user_name, context.webapp_id)

    url = '/workbench/jqm/preview/?woid=%d&module=user_center&model=wishlist&action=get&member_id=%s' % (context.webapp_owner_id, member.id)
    response = context.client.get(bdd_util.nginx(url), follow=True)
    products = response.context['products']
    actual = []

    for product in products:
        product_info = {}
        product_info['name'] = product.name
        product_info['price'] = product.price_info['min_price'] if product.price_info['min_price'] else product.price
        actual.append(product_info)
    bdd_util.assert_list(expected, actual)

@when(u"{webapp_user_name}取消收藏已收藏的商品")
def step_impl(context, webapp_user_name):
    response = _update_wishlist_product(context, "true")
    bdd_util.assert_api_call_success(response)
