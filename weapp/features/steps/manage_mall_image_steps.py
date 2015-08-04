# -*- coding: utf-8 -*-
import json
from behave import when, then

from test import bdd_util
from mall import models as mall_models


@when(u"{user}添加图片分组")
def step_add_image_group(context, user):
    image_groups = json.loads(context.text)
    if not type(image_groups) == list:
        image_groups = [image_groups]

    for image_group in image_groups:
        for image in image_group['images']:
            image['id'] = -1
            image['width'] = '640'
            image['height'] = '640'
        image_group['images'] = json.dumps(image_group['images'])

        url = '/mall2/api/image_group/?_method=put'
        response = context.client.post(url, image_group)
        bdd_util.assert_api_call_success(response)


@then(u"{user}能获取图片分组列表")
def step_get_image_group_list(context, user):
    url = '/mall2/image_group_list/'
    response = context.client.get(url)
    actual = response.context['image_groups']
    for image_group in actual:
        for image in image_group.images:
            image.path = image.url

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@then(u"{user}能获取图片分组'{image_group_name}'")
def step_get_image_group(context, user, image_group_name):
    db_image_group = mall_models.ImageGroup.objects.get(
        owner_id=context.webapp_owner_id,
        name=image_group_name)

    url = '/mall2/api/image_group/?id=%d' % (db_image_group.id, )
    response = context.client.get(url)
    images = json.loads(response.content)['data']
    for image in images:
        image['path'] = image['src']
    actual = {
        "images": images
    }

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)


@when(u"{user}更新图片分组'{image_group_name}'")
def step_update_image_group(context, user, image_group_name):
    db_image_group = mall_models.ImageGroup.objects.get(
        owner_id=context.webapp_owner_id,
        name=image_group_name
    )

    image_group = json.loads(context.text)
    for image in image_group['images']:
        image['id'] = -1
        image['width'] = '640'
        image['height'] = '640'
    image_group['images'] = json.dumps(image_group['images'])
    image_group['id'] = db_image_group.id

    url = '/mall2/api/image_group/'
    response = context.client.post(url, image_group)
    bdd_util.assert_api_call_success(response)


@when(u"{user}删除图片分组'{image_group_name}'")
def step_delete_image_group(context, user, image_group_name):
    db_image_group = mall_models.ImageGroup.objects.get(
        owner_id=context.webapp_owner_id,
        name=image_group_name)

    data = {
        "id": db_image_group.id
    }
    url = '/mall2/api/image_group/?_method=delete'
    response = context.client.post(url, data)
    bdd_util.assert_api_call_success(response)
