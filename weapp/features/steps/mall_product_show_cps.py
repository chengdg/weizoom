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
from weixin.user.models import *
from eaglet.utils.resource_client import Resource

import logging



@When(u'{user}虚拟添加商品')
def step_impl(context, user):
    products = json.loads(context.text)
    current_user = User.objects.get(username=user)
    for product in products:
        Product.objects.create(owner=current_user,name=product.keys()[0],shelve_type=product.values()[0])
    assert 1

@When(u'{user}虚拟添加商品池')
def step_impl(context, user):
    current_user = User.objects.get(username=user)
    woid = current_user.id
    product_id = Product.objects.get(name='__虚拟商品1').id
    ProductPool.objects.create(woid=woid,product_id=product_id)
    product_id = Product.objects.get(name='__虚拟商品2').id
    ProductPool.objects.create(woid=woid,product_id=product_id)
    product_id = Product.objects.get(name='__虚拟商品5').id
    ProductPool.objects.create(woid=woid,product_id=product_id)
    assert 1

@When(u'{user}虚拟添加cps商品信息')
def step_impl(context, user):
    promote_time_from = datetime.strptime('2014-02-14 21:32:12', "%Y-%m-%d %H:%M:%S")
    promote_time_to = datetime.strptime('2017-02-14 21:32:12', "%Y-%m-%d %H:%M:%S")
    product_id = Product.objects.get(name='__虚拟商品1').id
    PromoteDetail.objects.create(product_id=product_id,promote_status=1,promote_money=10,promote_stock=11,promote_time_from=promote_time_from,promote_time_to=promote_time_to)
    product_id = Product.objects.get(name='__虚拟商品3').id
    PromoteDetail.objects.create(product_id=product_id,promote_status=1,promote_money=100,promote_stock=12,promote_time_from=promote_time_from,promote_time_to=promote_time_to)
    product_id = Product.objects.get(name='__虚拟商品5').id
    PromoteDetail.objects.create(product_id=product_id,promote_status=1,promote_money=1000,promote_stock=13,promote_time_from=promote_time_from,promote_time_to=promote_time_to)
    product_id = Product.objects.get(name='__虚拟商品6').id
    PromoteDetail.objects.create(product_id=product_id,promote_status=2,promote_money=100000,promote_stock=14,promote_time_from=promote_time_from,promote_time_to=promote_time_to)
    assert 1


@Then(u'{user}点击商品池所有商品标签栏')
def step_impl(context, user):
    expected = json.loads(context.text)
    url = '/mall2/api/product_pool/'
    data = {}
    if hasattr(context, 'pool_args'):
        data = context.pool_args
    if hasattr(context, 'page_num'):
        data['page'] = context.page_num
    if hasattr(context, 'count_per_page'):
        data['count_per_page'] = context.count_per_page
    response = context.client.get(url, data)
    products = json.loads(response.content)['data']['items']
    actual = []
    for product in products:
        if 'is_cps' in product:
            #assert ('promote_time_to' in product and 'promote_money' in product and 'promote_stock' in product and 'promote_time_from' in product)
            actual.append({
                'name': product['name'],
                'is_cps': product['is_cps'],
                'promote_money': product['promote_money'],
                'promote_stock': product['promote_stock'],
                'promote_time_from': product['promote_time_from'],
                'promote_time_to': product['promote_time_to']
                })
        else:
            actual.append({
                'name': product['name']
                })
    bdd_util.assert_list(expected, actual)

@Then(u'{user}点击商品池cps推广商品标签')
def step_impl(context, user):
    expected = json.loads(context.text)
    url = '/mall2/api/product_pool/'
    data = {'is_cps':1}
    if hasattr(context, 'pool_args'):
        data = context.pool_args
    if hasattr(context, 'page_num'):
        data['page'] = context.page_num
    if hasattr(context, 'count_per_page'):
        data['count_per_page'] = context.count_per_page
    response = context.client.get(url, data)
    assert 'is_request_cps' in json.loads(response.content)['data']
    products = json.loads(response.content)['data']['items']
    actual = []
    for product in products:
        assert ('promote_time_to' in product and 'promote_money' in product and 'promote_stock' in product and 'promote_time_from' in product and 'is_cps' in product)
        actual.append({
            'name': product['name'],
            'is_cps': product['is_cps'],
            'promote_money': product['promote_money'],
            'promote_stock': product['promote_stock'],
            'promote_time_from': product['promote_time_from'],
            'promote_time_to': product['promote_time_to']
            })
    bdd_util.assert_list(expected, actual)

@Then(u'{user}点击在售商品所有商品标签')
def step_impl(context, user):
    expected = json.loads(context.text)
    url = '/mall2/api/product_list/'
    data = {}
    if hasattr(context, 'pool_args'):
        data = context.pool_args
    if hasattr(context, 'page_num'):
        data['page'] = context.page_num
    if hasattr(context, 'count_per_page'):
        data['count_per_page'] = context.count_per_page
    response = context.client.get(url, data)
    products = json.loads(response.content)['data']['items']
    actual = []
    for product in products:
        if 'is_cps' in product:
            #assert ('promote_time_to' in product and 'promote_money' in product and 'promote_stock' in product and 'promote_time_from' in product)
            actual.append({
                'name': product['name'],
                'is_cps': product['is_cps'],
                'promote_money': product['promote_money'],
                'promote_stock': product['promote_stock'],
                'promote_time_from': product['promote_time_from'],
                'promote_time_to': product['promote_time_to']
                })
        else:
            actual.append({
                'name': product['name']
                })
    bdd_util.assert_list(expected, actual)

@Then(u'{user}点击在售商品cps推广商品标签')
def step_impl(context, user):
    expected = json.loads(context.text)
    url = '/mall2/api/product_list/'
    data = {'is_cps':1}
    if hasattr(context, 'pool_args'):
        data = context.pool_args
    if hasattr(context, 'page_num'):
        data['page'] = context.page_num
    if hasattr(context, 'count_per_page'):
        data['count_per_page'] = context.count_per_page
    response = context.client.get(url, data)
    assert 'is_request_cps' in json.loads(response.content)['data']
    products = json.loads(response.content)['data']['items']
    actual = []
    for product in products:
        assert ('promote_time_to' in product and 'promote_money' in product and 'promote_stock' in product and 'promote_time_from' in product and 'is_cps' in product)
        actual.append({
            'name': product['name'],
            'is_cps': product['is_cps'],
            'promote_money': product['promote_money'],
            'promote_stock': product['promote_stock'],
            'promote_time_from': product['promote_time_from'],
            'promote_time_to': product['promote_time_to']
            })
    bdd_util.assert_list(expected, actual)

@Then(u'{user}点击待售商品所有商品标签')
def step_impl(context, user):
    expected = json.loads(context.text)
    url = '/mall2/api/product_list/'
    data = {'type':'offshelf'}
    if hasattr(context, 'pool_args'):
        data = context.pool_args
    if hasattr(context, 'page_num'):
        data['page'] = context.page_num
    if hasattr(context, 'count_per_page'):
        data['count_per_page'] = context.count_per_page
    response = context.client.get(url, data)
    products = json.loads(response.content)['data']['items']
    actual = []
    for product in products:
        if 'is_cps' in product:
            #assert ('promote_time_to' in product and 'promote_money' in product and 'promote_stock' in product and 'promote_time_from' in product)
            actual.append({
                'name': product['name'],
                'is_cps': product['is_cps'],
                'promote_money': product['promote_money'],
                'promote_stock': product['promote_stock'],
                'promote_time_from': product['promote_time_from'],
                'promote_time_to': product['promote_time_to']
                })
        else:
            actual.append({
                'name': product['name']
                })
    print (actual)
    bdd_util.assert_list(expected, actual)

@Then(u'{user}点击待售商品cps推广商品标签')
def step_impl(context, user):
    expected = json.loads(context.text)
    url = '/mall2/api/product_list/'
    data = {'is_cps':1,'type':'offshelf'}
    if hasattr(context, 'pool_args'):
        data = context.pool_args
    if hasattr(context, 'page_num'):
        data['page'] = context.page_num
    if hasattr(context, 'count_per_page'):
        data['count_per_page'] = context.count_per_page
    response = context.client.get(url, data)
    assert 'is_request_cps' in json.loads(response.content)['data']
    products = json.loads(response.content)['data']['items']
    actual = []
    for product in products:
        assert ('promote_time_to' in product and 'promote_money' in product and 'promote_stock' in product and 'promote_time_from' in product and 'is_cps' in product)
        actual.append({
            'name': product['name'],
            'is_cps': product['is_cps'],
            'promote_money': product['promote_money'],
            'promote_stock': product['promote_stock'],
            'promote_time_from': product['promote_time_from'],
            'promote_time_to': product['promote_time_to']
            })
    bdd_util.assert_list(expected, actual)