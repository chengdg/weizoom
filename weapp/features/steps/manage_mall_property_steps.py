# -*- coding: utf-8 -*-
import json
from behave import when, then

from test import bdd_util
from mall import models as mall_models


@when(u"{user}添加属性模板")
def step_add_property(context, user):
    property_templates = json.loads(context.text)
    if not type(property_templates) == list:
        property_templates = [property_templates]

    url = '/mall2/api/property/?_method=put'
    for property_template in property_templates:
        property_template['title'] = property_template['name']
        for property in property_template['properties']:
            property['id'] = -1
            property['value'] = property['description']
        property_template['newProperties'] = json.dumps(property_template['properties'])
        response = context.client.post(url, property_template)
        bdd_util.assert_api_call_success(response)


@then(u"{user}能获取属性模板列表")
def step_get_property_list(context, user):
    url = '/mall2/property_list/'
    response = context.client.get(url)
    actual = response.context['templates']
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@then(u"{user}能获取属性模板'{property_template_name}'")
def step_get_property(context, user, property_template_name):
    db_property_template = mall_models.ProductPropertyTemplate.objects.get(
        owner_id=context.webapp_owner_id,
        name=property_template_name)

    url = '/mall2/api/property_list/?id=%d' % db_property_template.id
    response = context.client.get(url)
    properties = json.loads(response.content)['data']
    for property in properties:
        property['description'] = property['value']
    actual = {
        "properties": properties
    }

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)


@when(u"{user}更新属性模板'{property_template_name}'")
def step_update_property(context, user, property_template_name):

    db_property_template = mall_models.ProductPropertyTemplate.objects.get(
        owner_id=context.webapp_owner_id,
        name=property_template_name
    )

    property_template = json.loads(context.text)
    property_template['id'] = db_property_template.id
    property_template['title'] = property_template['name']
    # 处理添加的property
    for property in property_template['add_properties']:
        property['id'] = -1
        property['value'] = property['description']
    property_template['newProperties'] = json.dumps(property_template['add_properties'])
    # 处理更新的property
    for property in property_template['update_properties']:
        db_property = mall_models.TemplateProperty.objects.get(
            owner_id=context.webapp_owner_id,
            name=property['original_name']
        )
        property['id'] = db_property.id
        property['value'] = property['description']
        del property['original_name']
    property_template['updateProperties'] = json.dumps(property_template['update_properties'])
    # 处理删除的property
    deletedIds = []
    for property in property_template['delete_properties']:
        db_property = mall_models.TemplateProperty.objects.get(
            owner_id=context.webapp_owner_id,
            name=property['name']
        )
        deletedIds.append(db_property.id)
    property_template['deletedIds'] = json.dumps(deletedIds)

    url = '/mall2/api/property/'
    response = context.client.post(url, property_template)
    bdd_util.assert_api_call_success(response)


@when(u"{user}删除属性模板'{property_template_name}'")
def step_delete_property(context, user, property_template_name):

    db_property_template = mall_models.ProductPropertyTemplate.objects.get(
        owner_id=context.webapp_owner_id,
        name=property_template_name)

    data = {
        "id": db_property_template.id
    }

    url = '/mall2/api/property/?_method=delete'
    response = context.client.post(url, data)
    bdd_util.assert_api_call_success(response)
