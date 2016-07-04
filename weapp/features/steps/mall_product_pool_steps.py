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

@given(u"添加{user}店铺名称为'{store_name}'")
def step_impl(context, user, store_name):
    user_id = User.objects.get(username=user).id
    UserProfile.objects.filter(user_id=user_id).update(store_name=store_name)

@given(u"添加{user}公众号名称为'{nick_name}'")
def step_impl(context, user, nick_name):
    user_id = User.objects.get(username=user).id
    auth_appid = ComponentAuthedAppid.objects.get(user_id=user_id).id
    ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid).update(nick_name=nick_name)

@given(u"设置{user}为自营平台账号")
def step_impl(context, user):
    user_id = User.objects.get(username=user).id
    UserProfile.objects.filter(user_id=user_id).update(webapp_type=1)

@given(u"{user}输出日志")
def step_impl(context, user):
    print(u"我是一一一一一一一条日志")

@then(u"{user}获得商品池商品列表")
def step_impl(context, user):
    expected = json.loads(context.text)
    url = '/mall2/api/product_pool/'
    data = {}
    if hasattr(context, 'pool_args'):
        data = context.pool_args
    if hasattr(context, 'page_num'):
        data['page'] = context.page_num
    if hasattr(context, 'count_per_page'):
        data['count_per_page'] = context.count_per_page
    response = context.client.get(url, data)
    products = json.loads(response.content)['data']['items']
    actual = []
    for product in products:
        actual.append({
                "name": product['name'],
                "price": product['price'],
                "user_code": product['user_code'],
                "supplier": product['store_name'],
                "stocks": product['stocks'],
                "status": STATUS2TEXT[product['status']],
                "sync_time": product['sync_time'],
                "actions": STATUS2ACTION[product['status']],
            })

    # for i in range(0,len(expected)):
    #     print expected[i]['name'], "+++", actual[i]['name']
    #     print expected[i]['status'], "+++", actual[i]['status']
    bdd_util.assert_list(expected, actual)

@when(u"{user}将商品'{product_name}'放入待售于'{sync_time}'")
def step_impl(context, user, product_name, sync_time):
    _put_product_will_sale(context, user, [product_name], sync_time)

@when(u"{user}将商品池商品批量放入待售于'{sync_time}'")
def step_impl(context, user, sync_time):
    _put_product_will_sale(context, user, json.loads(context.text), sync_time)

@when(u'{user}批量将商品放入待售')
def step_impl(context, user):
    _put_product_will_sale(context, user, json.loads(context.text))

def _put_product_will_sale(context, user, product_names, sync_time=None):
    user_id = User.objects.get(username=user).id
    product_name2product_id = dict([(product.name, product.id) for product in Product.objects.filter(name__in=product_names, supplier_user_id=0, is_deleted=False)])

    url = '/mall2/api/product_pool/?method=put'
    args = {
        'product_ids': json.dumps(product_name2product_id.values()),
        '_method': 'put'
    }
    response = context.client.post(url, args)
    bdd_util.assert_api_call_success(response)
    if sync_time:
        for product_name, product_id in product_name2product_id.items():
            sync_product = Product.objects.get(name=product_name, owner_id=user_id, is_deleted=False)
            sync_product_id = sync_product.id
            sync_product.created_at = sync_time
            sync_product.save()

            WeizoomHasMallProductRelation.objects.filter(
                mall_product_id=product_id,
                weizoom_product_id=sync_product_id).update(sync_time=sync_time)

@when(u"{user}更新商品池商品'{product_name}'于'{sync_time}'")
def step_impl(context, user, product_name, sync_time):
    url = '/mall2/api/product_pool/'
    product_id = Product.objects.get(name=product_name, supplier_user_id=0, is_deleted=False).id
    args = {
        'product_id': product_id,
        '_method': 'post'
    }
    response = context.client.post(url, args)
    try:
        bdd_util.assert_api_call_success(response)
    except:
        context.product_info = u"'该商品正在进行团购活动'"
        return
    user_id = User.objects.get(username=user).id
    sync_product = Product.objects.get(name=product_name, owner_id=user_id)
    sync_product_id = sync_product.id
    WeizoomHasMallProductRelation.objects.filter(
        mall_product_id=product_id,
        weizoom_product_id=sync_product_id).update(sync_time=sync_time)

@then(u"{user}获得失效商品列表")
def step_impl(context, user):
    time.sleep(1)
    expected = json.loads(context.text)
    for item in expected:
        item['delete_time'] = bdd_util.get_date(item['delete_time']).strftime('%Y-%m-%d')
    url = '/mall2/api/deleted_product_list/'
    data = {}
    if hasattr(context, 'time_args'):
        data['startDate'] = context.time_args['start_date']
        data['endDate'] = context.time_args['end_date']
        delattr(context, 'time_args')
    if hasattr(context, 'page_num'):
        data['page'] = context.page_num
    if hasattr(context, 'count_per_page'):
        data['count_per_page'] = context.count_per_page
    response = context.client.get(url, data)
    actual = json.loads(response.content)['data']['items']
    for item in actual:
        item['delete_time'] = item['delete_time'].split(" ")[0]
    bdd_util.assert_list(expected, actual)

@when(u"{user}设置失效商品列表查询条件")
def step_impl(context, user):
    time_args = json.loads(context.text)
    if time_args['start_date'] == time_args['end_date']:
        time_args['start_date'] = bdd_util.get_date(time_args['start_date']).strftime('%Y-%m-%d') + " 00:00:00"
        time_args['end_date'] = bdd_util.get_date(time_args['end_date']).strftime('%Y-%m-%d') + " 23:59:59"
    else:
        time_args['start_date'] = bdd_util.get_date(time_args['start_date'])
        time_args['end_date'] = bdd_util.get_date(time_args['end_date'])
    context.time_args = time_args

@when(u"{user}浏览失效商品列表第'{page_num}'页")
def step_impl(context, user, page_num):
    context.page_num = page_num

@when(u"{user}浏览失效商品列表下一页")
def step_impl(context, user):
    if not hasattr(context, 'page_num'):
        context.page_num = 1
    context.page_num = str(int(context.page_num) + 1)

@when(u"{user}浏览失效商品列表上一页")
def step_impl(context, user):
    context.page_num = str(int(context.page_num) - 1)

@when(u"{user}设置商品池列表查询条件")
def step_impl(context, user):
    args = json.loads(context.text)
    if args.has_key('status'):
        if args['status'] == u'全部':
            args.pop('status')
        elif args['status'] == u'待更新':
            args['status'] = '1'
        elif args['status'] == u'未选择':
            args['status'] = '2'
        elif args['status'] == u'已选择':
            args['status'] = '3'
    context.pool_args = args

@when(u"{user}浏览商品池列表下一页")
def step_impl(context, user):
    if not hasattr(context, 'page_num'):
        context.page_num = 1
    context.page_num = str(int(context.page_num) + 1)

@when(u"{user}浏览商品池列表上一页")
def step_impl(context, user):
    context.page_num = str(int(context.page_num) - 1)

@when(u"{user}浏览商品池列表第'{page_num}'页")
def step_impl(context, user, page_num):
    context.page_num = page_num

