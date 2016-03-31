# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *
from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from django.contrib.auth.models import User

from account.models import UserProfile
from mall.models import *

STATUS2TEXT = {
    1: u'待更新',
    2: u'未选择',
    3: u'已选择'
}

STATUS2ACTION = {
    1: [u'更新'],
    2: [u'放入待售'],
    3: [u'无更新']
}

@given(u"添加{user}店铺名称为'{store_name}'")
def step_impl(context, user, store_name):
    user_id = User.objects.get(username=user).id
    UserProfile.objects.filter(user_id=user_id).update(store_name=store_name)

@given(u"设置{user}为自营平台账号")
def step_impl(context, user):
    user_id = User.objects.get(username=user).id
    UserProfile.objects.filter(user_id=user_id).update(webapp_type=1)


@then(u"{user}获得商品池商品列表")
def step_impl(context, user):
    expected = json.loads(context.text)
    url = '/mall2/api/product_pool/'
    response = context.client.get(url)
    products = json.loads(response.content)['data']['items']
    actual = []
    for product in products:
        actual.append({
                "name": product['name'],
                "user_code": product['user_code'],
                "supplier": product['store_name'],
                "stocks": product['stocks'],
                "status": STATUS2TEXT[product['status']],
                "sync_time": product['sync_time'],
                "actions": STATUS2ACTION[product['status']],
            })

    bdd_util.assert_list(expected, actual)

@when(u"{user}将商品'{product_name}'放入待售于'{sync_time}'")
def step_impl(context, user, product_name, sync_time):
    user_id = User.objects.get(username=user).id
    url = '/mall2/api/product_pool/?method=put'
    product_id = Product.objects.get(name=product_name, supplier_user_id=0).id
    args = {
        'product_ids': json.dumps([product_id]),
        '_method': 'put'
    }
    response = context.client.post(url, args)
    bdd_util.assert_api_call_success(response)
    sync_product = Product.objects.get(name=product_name, owner_id=user_id)
    sync_product_id = sync_product.id
    sync_product.created_at = sync_time
    sync_product.save()

    WeizoomHasMallProductRelation.objects.filter(
        mall_product_id=product_id,
        weizoom_product_id=sync_product_id).update(sync_time=sync_time)

@when(u"{user}更新商品池商品'{product_name}'于'{sync_time}'")
def step_impl(context, user, product_name, sync_time):
    url = '/mall2/api/product_pool/'
    product_id = Product.objects.get(name=product_name, supplier_user_id=0).id
    args = {
        'product_id': product_id,
        '_method': 'post'
    }
    response = context.client.post(url, args)
    bdd_util.assert_api_call_success(response)
    user_id = User.objects.get(username=user).id
    sync_product = Product.objects.get(name=product_name, owner_id=user_id)
    sync_product_id = sync_product.id
    WeizoomHasMallProductRelation.objects.filter(
        mall_product_id=product_id,
        weizoom_product_id=sync_product_id).update(sync_time=sync_time)
