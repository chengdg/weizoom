
# -*- coding: utf-8 -*-
import json
import time
from test import bdd_util
from market_tools.tools.store.models import *

def __add_store(context, store):
    context.client.post('/market_tools/store/add/', store)

@when(u"{user}添加门店")
def step_impl(context, user):
    client = context.client
    stores = json.loads(context.text)

    for store in stores:
        if 'swipe_images' in store:
            store['swipe_images'] = json.dumps(store['swipe_images'])
        __add_store(context, store)

@then(u"{user}能获取'{store_name}'的信息")
def step_impl(context, user, store_name):
    client = context.client
    expected = json.loads(context.text)
    store = Store.objects.get(name=store_name)

    response = context.client.get('/market_tools/store/update/%d/' % store.id)
    actual_data = response.context['store']

    actual = {}
    actual['name'] = actual_data.name
    actual['thumbnails_url'] = actual_data.thumbnails_url
    actual['store_intro'] = actual_data.store_intro
    actual['swipe_images'] = json.loads(actual_data.swipe_images_json)
    actual['city'] = actual_data.city
    actual['address'] = actual_data.address
    actual['location'] = actual_data.location
    actual['bus_line'] = actual_data.bus_line
    actual['zone'] = actual_data.tel.split("-")[0]
    actual['num'] = actual_data.tel.split("-")[1]
    actual['detail'] = actual_data.detail

    bdd_util.assert_dict(expected, actual)

@then(u"{user}能获取门店列表")
def step_impl(context, user):
    expected = json.loads(context.text)
    response = context.client.get('/market_tools/store/api/store/get/?count_per_page=10')
    actual_data = json.loads(response.content)['data']['items']
    actual_data = sorted(actual_data,key=lambda x:x['name'],reverse=False)
    actual = []
    for store in actual_data:
        actual.append({
            "name": store['name'],
            "city": store['city']
        })

    bdd_util.assert_list(expected, actual)

@given(u"{user}已经添加门店信息")
def step_impl(context, user):
    client = context.client
    stores = json.loads(context.text)

    for store in stores:
        if 'swipe_images' in store:
            store['swipe_images'] = json.dumps(store['swipe_images'])
        __add_store(context, store)

@when(u"{user}修改'{store_name}'信息")
def step_impl(context, user, store_name):
    client = context.client
    store_new = json.loads(context.text)[0]
    store = Store.objects.get(name=store_name)
    print(store_new,store_name)
    if 'swipe_images' in store_new:
        store_new['swipe_images'] = json.dumps(store_new['swipe_images'])

    context.client.post('/market_tools/store/update/%d/' % store.id, store_new)

@then(u"{user}不能取到'{store_name}'的信息")
def step_impl(context, user, store_name):
    client = context.client
    expected = json.loads(context.text)
    store = Store.objects.filter(name=store_name)
    actual = []
    if not store:
        bdd_util.assert_list(expected, actual)

@when(u"{webapp_user_name}浏览{webapp_owner_name}的webapp中'{city}'地区内的门店列表")
def step_impl(context, webapp_user_name, webapp_owner_name, city):
    bdd_util.use_webapp_template(webapp_owner_name, 'simple_fashion')
    url = '/workbench/jqm/preview/?woid=%s&module=market_tool:store&model=store_list&action=get&city=%s&fmt=%s' % (context.webapp_owner_id, city, context.member.token)
    response = context.client.get(bdd_util.nginx(url))

    context.stores = response.context['stores']

@then(u"{webapp_user_name}获得webapp中所在地为'{city}'的门店")
def step_impl(context, webapp_user_name,city):
    expected = json.loads(context.text)
    actual = context.stores
    bdd_util.assert_list(expected, actual)

@when(u"{user}删除'{store_name}'")
def step_impl(context, user, store_name):
    client = context.client
    store = Store.objects.get(name=store_name)

    response = context.client.post('/market_tools/store/api/store/delete/',{"store_id": store.id}, HTTP_REFERER='/market_tools/store/')
