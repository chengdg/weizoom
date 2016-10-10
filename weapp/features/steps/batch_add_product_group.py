# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from behave import given, then, when
from features.testenv.model_factory import ProductFactory, ProductCategoryFactory
from operator import attrgetter
from test import bdd_util
from mall import models as mall_models
import sys


@then(u"{user}能够获得'在售'商品列表")
def step_get_products(context,user):
    response = context.client.get('/mall2/api/product_list?design_mode=0&version=1&highStocks=-1&count_per_page=30&page=1&enable_paginate=1&timestamp=1476006299009&_=1476006298475')
    actual = json.loads(response.content)['data']['items']
    actual_list = []
    for a in actual:
        product_dict = {}
        product_dict['name'] = a['name']
        product_dict['categories'] = []
        for c in a['categories']:
            product_dict['categories'].append(c['name'])
        actual_list.append(product_dict)
        #actual_list = actual_list[::-1]
    actual_list = actual_list[::-1]
    expected = json.loads(context.text)

    bdd_util.assert_list(expected, actual_list)





@when(u"{user}批量添加商品分组")
def step_impl(context, user):
    if hasattr(context, 'product_ids'):
        product_ids = context.product_ids
        category_names = json.loads(context.text)
        category_ids = []
        for category_name in category_names:
            existed_product_category = ProductCategoryFactory(name=category_name)
            category_ids.append(str(existed_product_category.id))
        category_ids = ','.join(category_ids)
        data =  {'product_ids': product_ids, 'category_ids':category_ids}

        url = '/mall2/api/batch_update_product_category/'
        response = context.client.post(url, data)
        bdd_util.assert_api_call_success(response)

    else:
        raise False