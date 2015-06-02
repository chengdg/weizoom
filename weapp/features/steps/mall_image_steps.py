# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *


@when(u"{user}添加图片分组")
def step_impl(context, user):
	image_groups = json.loads(context.text)
	if not type(image_groups) == list:
		image_groups = [image_groups]
	
	for image_group in image_groups:
		for image in image_group['images']:
			image['id'] = -1
			image['width'] = '640'
			image['height'] = '640'
		image_group['images'] = json.dumps(image_group['images'])
	
		response = context.client.post('/mall/api/image_group/create/', image_group)
		bdd_util.assert_api_call_success(response)


@then(u"{user}能获取图片分组列表")
def step_impl(context, user):
	response = context.client.get('/mall/image_groups/get/')
	actual =response.context['image_groups']
	for image_group in actual:
		for image in image_group.images:
			image.path = image.url
	
	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


@then(u"{user}能获取图片分组'{image_group_name}'")
def step_impl(context, user, image_group_name):
	db_image_group = ImageGroup.objects.get(owner_id=context.webapp_owner_id, name=image_group_name)

	response = context.client.get('/mall/api/image_group_images/get/?id=%d' % db_image_group.id)
	images =json.loads(response.content)['data']
	for image in images:
		image['path'] = image['src']
	actual = {
		"images": images
	}
	
	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)


@when(u"{user}更新图片分组'{image_group_name}'")
def step_impl(context, user, image_group_name):
	db_image_group = ImageGroup.objects.get(owner_id=context.webapp_owner_id, name=image_group_name)

	image_group = json.loads(context.text)
	for image in image_group['images']:
		image['id'] = -1
		image['width'] = '640'
		image['height'] = '640'
	image_group['images'] = json.dumps(image_group['images'])
	image_group['id'] = db_image_group.id

	response = context.client.post('/mall/api/image_group/update/', image_group)
	bdd_util.assert_api_call_success(response)


@when(u"{user}删除图片分组'{image_group_name}'")
def step_impl(context, user, image_group_name):
	db_image_group = ImageGroup.objects.get(owner_id=context.webapp_owner_id, name=image_group_name)

	data = {
		"id": db_image_group.id
	}
	response = context.client.post('/mall/api/image_group/delete/', data)
	bdd_util.assert_api_call_success(response)