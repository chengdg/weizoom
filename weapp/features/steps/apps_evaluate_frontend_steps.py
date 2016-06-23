#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

__author__ = 'aix'

import json
import copy
import random
from behave import *
from test import bdd_util

import apps_step_utils


@when(u"{webapp_user}完成订单'{order_code}'中'{product_name}'的评价")
def step_impl(context, webapp_user, order_code, product_name):
    order_has_product = bdd_util.get_order_has_product(order_code, product_name)
    context_dict = json.loads(context.text)
    # 输入
    data = {
        'webapp_owner_id': context.webapp_owner_id,
        'product_score': context_dict['product_score'],
        'picture_list': ','.join(context_dict['picture_list']) if context_dict.get('picture_list', None) else '',
        'product_id': order_has_product.product_id,
        'order_has_product_id': order_has_product.id,
        'order_id': order_code
    }
    if context_dict.get('review_detail', None):
        data['review_detail'] = context_dict['review_detail']
        data['template_type'] = 'ordinary'
        data['serve_score'] = context_dict.get('serve_score', 5)
        data['deliver_score'] = context_dict.get('deliver_score', 5)
        data['process_score'] = context_dict.get('process_score', 5)
    else:
        data['template_type'] = 'custom'
        tem_dict = dict()

        for k, v in context_dict.items():
            for one in v:
                if 'answer' == k:
                    tem_dict['qa::'+_get_random_number()] = one['title'] + '::' + one['value']
                elif 'choose' == k:
                    tem_dict['selection::'+_get_random_number()] = one['title'] + '::' + one['value'] + '::' + _get_random_number()
                elif 'participate_info' == k:
                    tem_dict['textlist::'+_get_random_number()] = one
        data['review_detail'] = json.dumps(tem_dict)

    apps_step_utils.get_response(context, {
        "app": "m/apps/evaluate",
        "resource": "evaluate_participance",
        "method": "put",
        "type": "api",
        "args": data
    })
    context.product_name = product_name
    context.product_id = order_has_product.product_id
    context.order_has_product_id = order_has_product.id
    context.order_id = order_code

@when(u"{webapp_user}完成订单'{order_code}'中'{product_name}'的追加晒图")
def step_impl(context, webapp_user, order_code, product_name):
    context_dict = json.loads(context.text)
    # 输入
    data = {
        'webapp_owner_id': context.webapp_owner_id,
        'picture_list': ','.join(context_dict['picture_list']) if context_dict.get('picture_list', None) else '',
        'product_id': context.product_id,
        'order_has_product_id': context.order_has_product_id,
        'order_id': context.order_id,
        'template_type': 'custom'
    }
    apps_step_utils.get_response(context, {
        "app": "m/apps/evaluate",
        "resource": "evaluate_participance",
        "method": "post",
        "type": "api",
        "args": data
    })

def _get_random_number():
    return str(random.choice([1,2,3,4,5,6,7,8,9]))