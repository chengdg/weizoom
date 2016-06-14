#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'aix'

import json
import copy
from behave import *
from test import bdd_util

import apps_step_utils


@when(u"{webapp_user}完成订单'{order_code}'中'{product_name}'的评价")
def step_finished_a_product_review(context, webapp_user, order_code, product_name):
    url = '/webapp/api/project_api/call/'
    order_has_product = bdd_util.get_order_has_product(order_code, product_name)
    # 输入
    data = {}
    context_dict = json.loads(context.text)
    data.update(context_dict)
    data['target_api'] = 'product_review/create'
    data['module'] = 'mall'
    data['woid'] = context.webapp_owner_id
    data['order_id'] = order_has_product.order_id
    data['product_id'] = order_has_product.product_id
    data['order_has_product_id'] = order_has_product.id
    has_picture = context_dict.get('picture_list', None)
    if has_picture:
        data['picture_list'] = str(has_picture)

    context.client.post(url, data)