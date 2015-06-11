# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from tools.regional.models import Province

@given(u"{user}已有的运费配置名称")
def step_impl(context, user):
	client = context.client
	context.postages = json.loads(context.text)
	for postage in context.postages:
		data = postage
		if data.get('is_enable_added_weight') == None and data.get('added_weight'):
			data['is_enable_added_weight'] = 1
		response = client.post('/mall/editor/postage_config/create/', data)
		time.sleep(1)


def _get_post_data_postage(postage):
	if postage.get('is_enable_added_weight') == None and postage.get('added_weight'):
		postage['is_enable_added_weight'] = 1

	if postage.get('TESHU_S'):
		i = 0
		for data in postage.get('TESHU_S'):
			postage['special^{}^province'.format(i)] =_get_province_ids(data.get('to_the'))
			postage['special^{}^first_weight_price'.format(i)] = data.get('first_weight_price',0)
			postage['special^{}^added_weight_price'.format(i)] = data.get('added_weight_price',0)
			i = i + 1

	return postage

def _get_province_ids(province_names):
	ids = []
	province_names = province_names.split(',')
	for province_name in province_names:
		print province_name
		province = Province.objects.get(name=province_name)
		ids.append(str(province.id))
	return ','.join(ids)

# @then(u"{user}能获取添加的邮费配置")
# def step_impl(context, user):
# 	if hasattr(context, 'client'):
# 		context.client.logout()
# 	context.client = bdd_util.login(user)
# 	client = context.client
	
# 	response = context.client.get('/mall/editor/mall_settings/')

# 	actual =response.context['postage_configs']
# 	for config in actual:
# 		if config.added_weight:
# 			config.added_weight = float(config.added_weight)
# 		if config.added_weight_price:
# 			config.added_weight_price = float(config.added_weight_price)
# 	expected = json.loads(context.text)
# 	bdd_util.assert_list(expected, actual)

