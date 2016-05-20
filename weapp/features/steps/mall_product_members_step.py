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

STATUS2TEXT = {
    0: u'已取消',
    1: u'已关注',
}
SOURCE2TEXT = {
    -1:u'未关注',
    0: u'直接关注',
    1: u'推广扫码',
    2: u'会员分享',
}
@then(u"{user}获得商品'{product_name}'的会员列表")
def step_impl(context, user, product_name):
    expected = []
    if context.table:
        for row in context.table:
            cur_p = row.as_dict()
            cur_p['attention_time'] = bdd_util.get_date(cur_p['attention_time']).strftime('%Y-%m-%d')
            expected.append(cur_p)


    product_id = Product.objects.get(name=product_name, supplier_user_id=0, is_deleted=False).id
    url = "/mall2/api/product_members/"
    data = {'id':product_id}
    response = context.client.get(url, data)
    actual = json.loads(response.content)['data']['items']
    for item in actual:
        item['member'] = item['username']
        item['member_rank'] = item['grade_name']
        item['attention_time'] = item['created_at'].split(" ")[0]
        item['source']  = SOURCE2TEXT[item['source']]
        item['tags'] = item['tags'][0]['name']
        item['status']  = STATUS2TEXT[item['is_subscribed']]
    bdd_util.assert_list(expected, actual)
