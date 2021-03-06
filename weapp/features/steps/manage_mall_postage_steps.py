# -*- coding: utf-8 -*-
import json
import time

from behave import when, given, then

from test import bdd_util

from django.test.client import Client
from tools.regional.models import Province

from steps_db_util import get_postage_config
from mall.models import PostageConfig, Supplier, Product

@when(u"{user}添加邮费配置")
def create_postage(context, user):
    client = context.client
    context.postages = json.loads(context.text)
    spcial_area_index = -1
    for postage in context.postages:
        data = __get_post_data_postage(postage)
        response = client.post('/mall2/api/postage/?_method=put', data)
        bdd_util.assert_api_call_success(response)


@given(u"{user}已添加运费配置")
def step_impl(context, user):
    create_postage(context, user)


@then(u"{user}能获取添加的邮费配置")
def step_impl(context, user):
    if hasattr(context, 'client'):
        context.client.logout()
    context.client = bdd_util.login(user)
    client = context.client
    response = context.client.get('/mall2/postage_list/')
    actual =response.context['postage_configs']
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@when(u"{user}修改'{postage_name}'运费配置")
def step_impl(context, user, postage_name):
    postage = json.loads(context.text)
    data = __get_post_data_postage(postage)
    config = get_postage_config(context.client.user.id, data['name'])
    data['id'] = config.id
    response = context.client.post('/mall2/api/postage/?_method=post', data)


@then(u"{user}能获取'{postage_name}'运费配置")
def step_impl(context, user, postage_name):
    config = get_postage_config(context.client.user.id, postage_name)
    response = context.client.get('/mall2/postage/?id=%d' % config.id)
    postage_config = response.context['postage_config'].to_dict()
    special_configs = response.context['jsons'][0]['content']
    actual = postage_config
    for config in special_configs:
        config['to_the'] = config['destination_str']
    actual['special_area'] = special_configs

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)


@when(u"{user}选择'{postage_name}'运费配置")
def step_impl(context, user, postage_name):
    config = get_postage_config(context.client.user.id, postage_name)
    data = {'id': config.id, 'is_used': 1 }
    response = context.client.post('/mall2/api/postage/?_method=post', data)


def __get_province_ids(province_names):
    ids = []
    province_names = province_names.split(',')
    for province_name in province_names:
        province = Province.objects.get(name=province_name)
        ids.append(str(province.id))
    return ids


def __get_post_data_postage(postage):
    postage['firstWeight'] = postage['first_weight']
    postage['firstWeightPrice'] = postage['first_weight_price']
    postage['addedWeight'] = postage.get('added_weight', '0')
    postage['addedWeightPrice'] = postage.get('added_weight_price', '0')
    
    if 'special_area' in postage:
        postage['isEnableSpecialConfig'] = 'true'
        special_configs = []
        for data in postage.get('special_area'):
            special_config = {
                "id": -1,
                "firstWeight": data.get('first_weight', "1.0"),
                "firstWeightPrice": data.get('first_weight_price', "1.0"),
                "addedWeight": data.get('added_weight', "1.0"),
                "addedWeightPrice": data.get('added_weight_price', "1.0")
            }
            special_config['destination'] = __get_province_ids(data.get('to_the', ''))
            special_configs.append(special_config)
        postage['specialConfigs'] = json.dumps(special_configs)
    else:
        postage['isEnableSpecialConfig'] = 'false'
        postage['specialConfigs'] = "[]"

    if 'free_postages' in postage:
        postage['isEnableFreeConfig'] = 'true'
        free_postages = []
        for data in postage.get('free_postages'):
            free_postage = {
                "id": -1,
                "condition": data['condition'],
                "value": data['value']
            }
            free_postage['destination'] = __get_province_ids(data.get('to_the', ''))
            free_postages.append(free_postage)
        postage['freeConfigs'] = json.dumps(free_postages)
    else:
        postage['isEnableFreeConfig'] = 'false'
        postage['freeConfigs'] = "[]"

    return postage


def __get_special_area_for_config(postage_config):
    special_areas = json.loads(postage_config.values_json_str)
    if special_areas:
        postage_config.special_area = []
        for special_area in special_areas:
            province = ','.join([p['name'] for p in special_area['province']])
            postage_config.special_area.append({
                'to_the': province,
                'first_weight_price': special_area['first_weight_price'],
                'added_weight_price': special_area['added_weight_price']
            })
    else:
        postage_config.special_area = []

@when(u"给供货商'{supplier_name}'添加运费配置")
def step_impl(context, supplier_name):
    """
    临时使用直接写库的方式实现添加数据，panda的代码写好之后再修改
    """
    postage_data = json.loads(context.text)
    supplier = Supplier.objects.get(name=supplier_name)
    for postage in postage_data:
        data = __get_post_data_postage(postage)
        response = context.client.post('/mall2/api/postage/?_method=put', data)
        bdd_util.assert_api_call_success(response)
        postage_config = list(PostageConfig.objects.all())[-1]
        PostageConfig.objects.filter(owner_id=postage_config.owner_id).update(is_used=True)
        postage_config.owner_id = supplier.owner_id
        postage_config.supplier_id = supplier.id
        postage_config.is_used = False
        postage_config.save()

@when(u"给供货商选择运费配置")
def set_impl(context):
    """
    临时使用直接写库的方式实现添加数据，panda的代码写好之后再修改
    """
    data = json.loads(context.text)
    supplier_name = data['supplier_name']
    postage_name = data['postage_name']
    supplier_id = Supplier.objects.get(name=supplier_name).id
    PostageConfig.objects.filter(supplier_id=supplier_id).update(is_used=False)
    PostageConfig.objects.filter(name=postage_name, supplier_id=supplier_id).update(is_used=True)
    Product.objects.filter(supplier=supplier_id, unified_postage_money=0).update(postage_id=0, postage_type='custom_postage_type')