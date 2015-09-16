# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from behave import given, then, when
from features.testenv.model_factory import ProductFactory, ProductCategoryFactory

from test import bdd_util
from mall import models as mall_models
from utils import mall_api

@given(u"{user}已添加商品分类")
def step_add_category(context, user):
    client = context.client
    uid = client.user.id
    context.product_categories = json.loads(context.text)
    for product_category in context.product_categories:
        mall_api.add_product_category(uid, product_category['name'])
        #url = '/mall2/api/category/?_method=put'
        #client.post(url, data)


@when(u"{user}添加商品分类")
def step_impl(context, user):
    client = context.client
    uid = client.user.id
    context.product_categories = json.loads(context.text)
    for product_category in context.product_categories:
        mall_api.add_product_category(uid, product_category['name'])
        #data = product_category
        #url = '/mall2/api/category/?_method=put'
        #client.post(url, data)


@then(u"{user}能获取商品分类列表")
def step_get_category(context, user):
    if hasattr(context, 'client'):
        context.client.logout()
    context.client = bdd_util.login(user)
    client = context.client

    response = client.get('/mall2/category_list/')
    actual = response.context['product_categories']
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@when(u"{user}更新商品分类'{category_name}'为")
def step_update_category(context, user, category_name):
    client = context.client
    existed_product_category = ProductCategoryFactory(name=category_name)
    new_product_category = json.loads(context.text)
    data = {
        'id': existed_product_category.id,
        'name': new_product_category['name']
    }
    url = '/mall2/api/category/'
    response = client.post(url, data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}删除商品分类'{category_name}'")
def step_delete_category(context, user, category_name):
    existed_product_category = ProductCategoryFactory(name=category_name)
    data = {
        'category_id': existed_product_category.id
    }
    url = '/mall2/api/category/?_method=delete'
    response = context.client.post(url, data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}从商品分类'{category_name}'中删除商品'{product_name}'")
def step_delete_p_in_categroy(context, user, category_name, product_name):
    existed_product_category = ProductCategoryFactory(name=category_name)
    existed_product = mall_models.Product.objects.get(name=product_name)
    data = {
        'category_id': existed_product_category.id,
        'product_id': existed_product.id
    }
    url = '/mall2/api/category/?_method=delete'
    response = context.client.post(url, data)
    bdd_util.assert_api_call_success(response)


@then(u"{user}能获得商品分类'{category_name}'的可选商品集合为")
def step_get_p_from_category(context, user, category_name):
    existed_product_category = ProductCategoryFactory(name=category_name)
    url = '/mall2/api/category_list/?id={}'.format(existed_product_category.id)
    response = context.client.get(url)

    actual = json.loads(response.content)['data']['items']
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@when(u"{user}向商品分类'{category_name}'中添加商品")
def step_add_p_to_category(context, user, category_name):
    existed_product_category = ProductCategoryFactory(name=category_name)

    product_names = json.loads(context.text)
    products = mall_models.Product.objects.filter(name__in=product_names)
    product_ids = [product.id for product in products]

    data = {
        "id": existed_product_category.id,
        "name": existed_product_category.name,
        "product_ids[]": product_ids
    }

    url = '/mall2/api/category/'
    context.client.post(url, data)

@when(u"{user}更新分类'{category_name}'中商品'{product_name}'商品排序{position}")
def step_impl(context, user, category_name, product_name, position):
    product = ProductFactory(name=product_name)
    category = ProductCategoryFactory(name=category_name)
    url = '/mall2/api/category_list/'
    data = {
        "category_id": category.id,
        "product_id": product.id,
        "position": position
    }
    context.client.post(url, data)


