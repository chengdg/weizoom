# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from behave import given, then, when
from features.testenv.model_factory import ProductFactory, ProductCategoryFactory
from operator import attrgetter
from test import bdd_util
from mall import models as mall_models


@given(u"{user}已添加商品分类")
def step_add_category(context, user):
    client = context.client
    context.product_categories = json.loads(context.text)
    for product_category in context.product_categories:
        data = product_category
        url = '/mall2/api/category/?_method=put'
        client.post(url, data)


@when(u"{user}添加商品分类")
def step_impl(context, user):
    client = context.client
    context.product_categories = json.loads(context.text)
    for product_category in context.product_categories:
        data = product_category
        url = '/mall2/api/category/?_method=put'
        client.post(url, data)


@then(u"{user}能获取商品分类列表")
def step_get_category(context, user):
    if hasattr(context, 'client'):
        context.client.logout()
    context.client = bdd_util.login(user)
    client = context.client

    response = client.get('/mall2/category_list/')
    actual = response.context['product_categories']
    actual_list = []
    for a in actual:
        chp_list = mall_models.CategoryHasProduct.objects.filter(
        category_id=a['id'])
        product_id2chp = dict(map(lambda chp: (chp.product_id, chp), chp_list))
        product_ids = [chp.product_id for chp in chp_list]
        cache_products = mall_models.Product.objects.filter(id__in=product_ids,is_deleted=False)
        mall_models.Product.fill_display_price(cache_products)
        for product in cache_products:
            product.display_index = product_id2chp[product.id].display_index
            product.join_category_time = product_id2chp[product.id].created_at
        # 1.shelve_type, 2.display_index, 3.id
        products_is_0 = filter(lambda p: p.display_index == 0,
                                             cache_products)
        products_not_0 = filter(lambda p: p.display_index != 0,
                                              cache_products)
        products_is_0 = sorted(products_is_0, key=attrgetter('join_category_time','id'), reverse=True)
        products_not_0 = sorted(products_not_0, key=attrgetter('display_index'))
        cache_products = products_not_0 + products_is_0
        product_dict = {}
        product_dict['products'] = []
        product_dict['name'] = a['name']
        print('=============================')
        print(cache_products)
        for c_product in cache_products:
            dict_one = {
            "name": c_product.name,
            "status": "在售" if c_product.shelve_type==1 else "待售",
            "display_price": c_product.display_price,
            "display_index": c_product.display_index
            }
            product_dict['products'].append(dict_one)
        actual_list.append(product_dict)
    # print("111"+int(2))
    expected = json.loads(context.text)
    print('###################################')
    print(expected)
    print(actual_list)
    print('###################################')
    bdd_util.assert_list(expected, actual_list)


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


