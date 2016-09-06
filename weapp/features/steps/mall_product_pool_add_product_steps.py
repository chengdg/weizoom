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


@given(u"给{zy1}, {zy2}两个自营平台同步商品，供货商是-{supplier_name}")
def step_impl(context, zy1, zy2, supplier_name):

    context = json.loads(context.text)
    # print 'context %s' % context
    # print 'zy2 %s' % zy2
    # print 'zy1 %s' % zy1

    EAGLET_CLIENT_ZEUS_HOST = 'api.zeus.com'
    ZEUS_SERVICE_NAME = 'zeus'
    supplier = Supplier.objects.filter(name=supplier_name).first()
    if not supplier:
        assert False
    img = context.get('image')
    images = [{'url': img}]
    params = {
        'supplier': supplier.id,
        'name': context.get('name'),
        'promotion_title': context.get('promotion_title'),
        'purchase_price': context.get('purchase_price'),
        'price': context.get('price'),
        'weight': context.get('weight'),
        'stock_type': 'limit',
        'images': json.dumps(images),
        'model_type': 'single',
        'stocks': context.get('stocks'),
        'detail': context.get('detail')
    }

    resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put(
        {
            'resource': 'mall.sync_product',
		    'data': params
        }
    )
    if resp and resp.get('code') == 200:
        auth_users = User.objects.filter(username__in=[zy1, zy2])
        user_ids = [user.id for user in auth_users]
        weapp_product_id = resp.get('data').get('product').get('id')
        # pool_params = {}
        account_params = {
            'product_id': weapp_product_id,
            'accounts': json.dumps(user_ids)
        }
        account_resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
            'resource': 'mall.product_pool',
            'data': account_params
        })
        if account_resp and account_resp.get('code') == 200:
            assert True
        else:
            assert False
        assert True
    else:
        assert False


@given(u'创建一个特殊的供货商叫-{supplier_name}')
def step_impl(context, supplier_name):
    pool_account = UserProfile.objects.filter(webapp_type=2).first()
    if pool_account:
        Supplier.objects.create(owner_id=pool_account.user_id,
                                 name=supplier_name,
                                 supplier_tel=u'',
                                 supplier_address=u'',
                                 remark=u'商品池测试供货商')
        assert True
    else:
        assert False


@then(u"可以查到一个叫-{supplier_name}-的供货商")
def step_impl(context, supplier_name):
    suppliers = Supplier.objects.filter(name=supplier_name, is_delete=False)
    assert suppliers.count() > 0


@then(u'{zy1},{zy2}可以查看到商品里有一个商品叫-{product_name}')
def step_impl(context, zy1, zy2, product_name):
    
    user = User.objects.get(username=zy1)
    products = Product.objects.filter(name=product_name)
    product_ids = [p.id for p in products]

    pool = ProductPool.objects.filter(product_id__in=product_ids,
                                      woid=user.id)
    assert pool.count() > 0


@When(u'{zy1}上架商品池商品“{product_name}”')
def step_impl(context, zy1, product_name):
    url = '/mall2/api/product_pool/?_method=put'
    product = Product.objects.get(name=product_name)
    data = {
        'product_ids': "[%s]" % product.id
    }
    response = context.client.post(url, data)
    bdd_util.assert_api_call_success(response)


@then(u'给供货商"{supplier_name}"添加运费配置')
def step_impl(context, supplier_name):
    context = json.loads(context.text)
    postage = context.get('postage')
    condition_money = context.get('condition_money')
    supplier = Supplier.objects.filter(name=supplier_name).first()
    if not supplier:
        assert False
    params = {
        'supplier_id': supplier.id,
        'condition_type': 'money',
        'postage': postage,
        'condition_money': condition_money
    }

    resp = Resource.use('zeus', 'api.zeus.com').put(
        {
            'resource': 'mall.supplier_postage_config',
            'data': params
        }
    )
    if resp and resp.get('code') == 200:
        assert True
