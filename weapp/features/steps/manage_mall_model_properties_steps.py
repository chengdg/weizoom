# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
import logging
logger = logging.getLogger('console')

from behave import given, when, then

from test import bdd_util
from .steps_db_util import get_model_property_from_web_page
from mall import models as mall_models


@given(u"{user}已添加商品规格")
def step_add_model_property(context, user):
    product_model_properties = json.loads(context.text)
    for _property in product_model_properties:
        __add_product_model_property(context, _property)


@when(u"{user}添加商品规格")
def step_w_add_model_property(context, user):
    product_model_properties = json.loads(context.text)
    for property in product_model_properties:
        __add_product_model_property(context, property)


@then(u"{user}能获取商品规格'{product_model_property_name}'")
def step_get_model_property(context, user, product_model_property_name):
    expected = json.loads(context.text)
    actual = get_model_property_from_web_page(
        context,
        product_model_property_name)

    bdd_util.assert_dict(expected, actual)


@then(u"{user}能获取商品规格列表")
def step_get_model_property_list(context, user):
    response = context.client.get('/mall2/model_property_list/')

    expected = json.loads(context.text)

    actual = []
    model_properties = response.context['model_properties']
    for model_property in model_properties:
        data = {
            "name": model_property.name,
            "type": u'图片' if model_property.type == mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE else u'文字'
        }
        data['values'] = []
        property_values = mall_models.ProductModelPropertyValue.objects.filter(
            property_id=model_property.id,
            is_deleted=False)
        for property_value in property_values:
            data['values'].append({
                "name": property_value.name,
                "image": property_value.pic_url
            })
        actual.append(data)

    bdd_util.assert_list(expected, actual)


@when(u"{user}更新商品规格'{product_model_property_name}'为")
def step_update_model_property(context, user, product_model_property_name):
    user_id = bdd_util.get_user_id_for(user)
    db_model_property = mall_models.ProductModelProperty.objects.get(
        owner_id=user_id,
        name=product_model_property_name,
        is_deleted=False)
    property_id = db_model_property.id

    model_property = json.loads(context.text)

    # 更新name
    data = {
        "id": property_id,
        "field": 'name',
        "name": model_property['name']
    }
    update_url = '/mall2/api/model_property/'
    response = context.client.post(update_url, data)
    bdd_util.assert_api_call_success(response)

    #更新type
    data = {
        "id": property_id,
        "field": 'type',
        "type": 'text'
    }
    type = model_property.get('type', None)
    if type == u'图片':
        data['type'] = 'image'
    response = context.client.post(update_url, data)
    bdd_util.assert_api_call_success(response)

    #处理add_values
    create_url = '/mall2/api/model_property_value/?_method=put'
    for value in model_property.get('add_values', []):
        if 'image' in value:
            value['pic_url'] = value['image']
        else:
            value['pic_url'] = ''
        value['id'] = property_id
        logger.debug("add values: name->%(value)s",
                     {'value': value.get('name')})
        response = context.client.post(create_url, value)
        bdd_util.assert_api_call_success(response)

    #处理delete_values
    delete_url = '/mall2/api/model_property_value/?_method=delete'
    for value in model_property.get('delete_values', []):
        db_model_prop_val = mall_models.ProductModelPropertyValue.objects.get(
            property=db_model_property,
            name=value['name'],
            is_deleted=False)
        response = context.client.post(
            delete_url,
            {'id': db_model_prop_val.id})
        bdd_util.assert_api_call_success(response)


@when(u"{user}删除商品规格'{product_model_property_name}'的值'{property_value}'")
def step_impl(context, user, product_model_property_name, property_value):
    user_id = bdd_util.get_user_id_for(user)
    db_model_property = mall_models.ProductModelProperty.objects.get(
        owner_id=user_id,
        name=product_model_property_name,
        is_deleted=False)
    db_model_prop_val = mall_models.ProductModelPropertyValue.objects.get(
        property=db_model_property,
        name=property_value,
        is_deleted=False)

    url = '/mall2/api/model_property_value/?_method=delete'
    response = context.client.post(url, {'id': db_model_prop_val.id})
    bdd_util.assert_api_call_success(response)


@when(u"{user}删除商品规格'{product_model_property_name}'")
def step_delete_model_property(context, user, product_model_property_name):
    user_id = bdd_util.get_user_id_for(user)
    db_model_property = mall_models.ProductModelProperty.objects.get(
        owner_id=user_id,
        name=product_model_property_name,
        is_deleted=False)

    url = '/mall2/api/model_property/?_method=delete'
    response = context.client.post(url, {'id': db_model_property.id})
    bdd_util.assert_api_call_success(response)


def __add_product_model_property(context, model_property):
    data = model_property

    # 创建一个空的product model property
    url1 = '/mall2/api/model_property/?_method=put'
    response = context.client.post(url1, data)
    bdd_util.assert_api_call_success(response)
    property_id = json.loads(response.content)['data']

    # 更新name
    post_data = {
        "id": property_id,
        "field": 'name',
        "name": data['name']
    }
    url2 = '/mall2/api/model_property/'
    response = context.client.post(url2, post_data)
    bdd_util.assert_api_call_success(response)

    # 更新type
    post_data = {
        "id": property_id,
        "field": 'type',
        "type": 'text'
    }
    _type = data.get('type', None)
    if _type == u'图片':
        post_data['type'] = 'image'
    url = '/mall2/api/model_property/'
    response = context.client.post(url, post_data)
    bdd_util.assert_api_call_success(response)

    # 处理value
    url = '/mall2/api/model_property_value/?_method=put'
    for value in data['values']:
        if 'image' in value:
            value['pic_url'] = value['image']
        else:
            value['pic_url'] = ''
        value['id'] = property_id
        response = context.client.post(url, value)
        bdd_util.assert_api_call_success(response)
