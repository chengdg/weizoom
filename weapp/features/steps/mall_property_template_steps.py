# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *


@when(u"{user}添加属性模板")
def step_impl(context, user):
	property_templates = json.loads(context.text)
	if not type(property_templates) == list:
		property_templates = [property_templates]
	
	for property_template in property_templates:
		property_template['title'] = property_template['name']
		for property in property_template['properties']:
			property['id'] = -1
			property['value'] = property['description']
		property_template['newProperties'] = json.dumps(property_template['properties'])
	
		response = context.client.post('/mall/api/property_template/create/', property_template)
		bdd_util.assert_api_call_success(response)


@then(u"{user}能获取属性模板列表")
def step_impl(context, user):
	response = context.client.get('/mall/property_templates/get/')
	actual =response.context['templates']
	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


@then(u"{user}能获取属性模板'{property_template_name}'")
def step_impl(context, user, property_template_name):
	db_property_template = ProductPropertyTemplate.objects.get(owner_id=context.webapp_owner_id, name=property_template_name)

	response = context.client.get('/mall/api/template_properties/get/?id=%d' % db_property_template.id)
	properties =json.loads(response.content)['data']
	for property in properties:
		property['description'] = property['value']
	actual = {
		"properties": properties
	}
	
	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)


@when(u"{user}更新属性模板'{property_template_name}'")
def step_impl(context, user, property_template_name):
	db_property_template = ProductPropertyTemplate.objects.get(owner_id=context.webapp_owner_id, name=property_template_name)

	property_template = json.loads(context.text)
	property_template['id'] = db_property_template.id
	property_template['title'] = property_template['name']
	#处理添加的property
	for property in property_template['add_properties']:
		property['id'] = -1
		property['value'] = property['description']
	property_template['newProperties'] = json.dumps(property_template['add_properties'])
	#处理更新的property
	for property in property_template['update_properties']:
		db_property = TemplateProperty.objects.get(owner_id=context.webapp_owner_id, name=property['original_name'])
		property['id'] = db_property.id
		property['value'] = property['description']
		del property['original_name']
	property_template['updateProperties'] = json.dumps(property_template['update_properties'])
	#处理删除的property
	deletedIds = []
	for property in property_template['delete_properties']:
		db_property = TemplateProperty.objects.get(owner_id=context.webapp_owner_id, name=property['name'])
		deletedIds.append(db_property.id)
	property_template['deletedIds'] = json.dumps(deletedIds)

	response = context.client.post('/mall/api/property_template/update/', property_template)
	bdd_util.assert_api_call_success(response)


@when(u"{user}删除属性模板'{property_template_name}'")
def step_impl(context, user, property_template_name):
	db_property_template = ProductPropertyTemplate.objects.get(owner_id=context.webapp_owner_id, name=property_template_name)

	data = {
		"id": db_property_template.id
	}
	response = context.client.post('/mall/api/property_template/delete/', data)
	bdd_util.assert_api_call_success(response)