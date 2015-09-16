# -*- coding: utf-8 -*-
import json
import time

from behave import when, given, then

from test import bdd_util

from django.test.client import Client
from tools.regional.models import Province
from datetime import datetime
from steps_db_util import get_postage_config


@given(u"{user}添加供货商")
def step_impl(context,user):
    add_supplier(context, user)

@when(u"{user}添加供货商")
def add_supplier(context,user):
    client = context.client
    context.suppliers = json.loads(context.text)
    for supplier in context.suppliers:
		response = client.post('/mall2/api/supplier_info/?_method=put', supplier)
		bdd_util.assert_api_call_success(response)

@then(u"{user}能获取供货商'{name}'")
def step_impl(context, user, name):
    if hasattr(context, 'client'):
        context.client.logout()
    context.client = bdd_util.login(user)
    client = context.client
    response = context.client.get('/mall2/api/supplier_list/',data={"name":name})
    expected = json.loads(context.text)
    actual = json.loads(response.content)['data']['items']
    if len(actual) == 0:
        actual = {}
    else:
        actual = actual[0]
    bdd_util.assert_dict(expected, actual)

@then(u"{user}能获取供货商列表")
def step_impl(context, user):
    if hasattr(context, 'client'):
        context.client.logout()
    context.client = bdd_util.login(user)
    client = context.client
    filter_value = {}
    if hasattr(context, 'supplier_name'):
        filter_value = context.supplier_name
    response = context.client.get('/mall2/api/supplier_list/',data=filter_value)

    actual = json.loads(response.content)['data']['items']
    expected = json.loads(context.text)

    for ex in expected:
        if "create_at" in ex:
            ex["create_at"] = bdd_util.get_date(ex["create_at"])
            ex["create_at"] = datetime.strftime(ex["create_at"],"%Y-%m-%d")
    for ac in actual:
        if "create_at" in ac:
            ac["create_at"] = datetime.strptime(ac["create_at"],"%Y-%m-%d %H:%M")
            ac["create_at"] = datetime.strftime(ac["create_at"],"%Y-%m-%d")
    bdd_util.assert_list(expected,actual)

@when(u"{user}删除供货商'{name}'")
def step_impl(context,user,name):
    if hasattr(context, 'client'):
        context.client.logout()
    context.client = bdd_util.login(user)
    client = context.client
    response = context.client.get('/mall2/api/supplier_list/',data={"name":name})
    supplier = json.loads(response.content)['data']['items'][0]
    response = context.client.post('/mall2/api/supplier_info/?_method=delete',{"id":supplier["id"]})
    context.del_supplier_res = response

@then(u"{user}提示错误信息'{err_tip}'")
def step_impl(context,user,err_tip):
    response = context.del_supplier_res
    response = json.loads(response.content)
    if response['data']['msg'] == err_tip:
        assert True
    else:
        assert False

@when(u"{user}修改供货商'{name}'")
def step_impl(context,user,name):
    if hasattr(context, 'client'):
        context.client.logout()
    context.client = bdd_util.login(user)
    client = context.client
    expected = json.loads(context.text)
    response = context.client.get('/mall2/api/supplier_list/',data={"name":name})
    supplier = json.loads(response.content)['data']['items'][0]
    response = context.client.post('/mall2/api/supplier_info/',
                                   {"id":supplier["id"],
                                    "name":expected['name'],
                                    "responsible_person":expected['responsible_person'],
                                    "supplier_tel":expected['supplier_tel'],
                                    "supplier_address":expected['supplier_address'],
                                    "remark":expected['remark']
                                    })
    bdd_util.assert_api_call_success(response)

@when(u"{user}导出'供货商'")
def step_impl(context,user):
    filter_value = {}
    if hasattr(context, 'supplier_name'):
        filter_value = context.supplier_name
    from cStringIO import StringIO
    import csv

    url = '/mall2/supplier_export/'
    response = context.client.get(url, data=filter_value)
    reader = csv.reader(StringIO(response.content))
    header = reader.next()
    supplier_actual = []
    for line in reader:
        print line
        supplier_actual.append(line)
    context.supplier_actual = supplier_actual

@then(u"{user}能获取导出供货商信息")
def step_impl(context,user):
    expect_list = []
    for row in context.table:
        expect_list.append([row[0],row[1],row[2],row[3],row[4]])
    bdd_util.assert_list(expect_list,context.supplier_actual)

@when(u"{user}查询供货商")
def step_impl(context,user):
    supplier_name_json = json.loads(context.text)
    context.supplier_name = supplier_name_json




