# -*- coding: utf-8 -*-
__author__='justing'
from test import bdd_util
import copy
import json, time
import logging
from behave import when, then, given
from mall.models import ProductCategory, Product, ProductModel,SenderInfo
from webapp.models import WebApp
from django.contrib.auth.models import User
from django.db.models import Q

from mall import models as mall_models  # 注意不要覆盖此module
from test import bdd_util
from features.testenv.model_factory import (
    ProductCategoryFactory, ProductFactory
)
from .steps_db_util import (
    get_custom_model_id_from_name, get_custom_model_name_from_id,
    get_product_response_from_web_page, get_custom_model_id_from_user_code
)


@when(u'{user}添加发件人新地址')
def step_impl(context, user):
    url = '/mall2/sender_info/?_method=put'
    sender_infos = json.loads(context.text)

    for sender_info in sender_infos:
        #sender_info['tel'] = sender_info['sender_tel']
        test = sender_info['area']
        sender_info['area'] = bdd_util.get_ship_area_id_for(test)
        context.client.post(url, sender_info)

@then(u'{user}能获得发件人信息列表')
def step_impl(context, user):
    url = '/mall2/api/sender_info_list/'
    response = context.client.get(url)

   
    actual_infos = json.loads(response.content)['data']['items']
    expected_infos = json.loads(context.text)
    for expected_info in expected_infos:
        expected_info['is_selected'] = True if expected_info['is_selected'] in ('true', 'yes', 'True', 'Yes', True, '1') else False
        if expected_info.has_key("actions"):
            expected_info.pop("actions")
    
    bdd_util.assert_list(expected_infos,actual_infos)

@when(u"{user}编辑'{sender}'地址信息")
def step_impl(context, user, sender):
    sender_infos = SenderInfo.objects.filter(sender_name=sender)
    if sender_infos:
        id = sender_infos[0].id
        url = '/mall2/sender_info/?_method=post'
        sender_info = json.loads(context.text)
        test = sender_info['area']
        sender_info['area'] = bdd_util.get_ship_area_id_for(test)
        sender_info["id"] = id
        context.client.post(url, sender_info)
    else:
        raise 'Error'

@when(u"{user}设置'{sender}'为默认地址")
def step_impl(context, user, sender):
    sender_infos = SenderInfo.objects.filter(sender_name=sender)
    if sender_infos:
        id = sender_infos[0].id
        url = '/mall2/sender_info/?_method=post'
        param = {"is_selected":True}
        param["id"] = id
        context.client.post(url, param)

    else:
        raise 'Error'


@when(u"{user}删除'{sender}'地址信息")
def step_impl(context, user, sender):
    sender_infos = SenderInfo.objects.filter(sender_name=sender)
    if sender_infos:
        id = sender_infos[0].id
        url = '/mall2/api/sender_info/?_method=delete'
        param = {"id":id}
        context.client.post(url, param)
    else:
        raise 'Error'